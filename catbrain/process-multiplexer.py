#!/usr/bin/env python3
import asyncio
import sys
from enum import Enum
from typing import Dict, List, Optional, Tuple, Union

"""
Original prompt:

now write a process multiplexer with python asyncio.  It should start 2
worker.sh processes in parallel.  it should parse a netstring, using
readuntil(":") and read(N).   it should create events for a new netstring, and
process exit.   the events will be tagged with PID.   it should merge these all
into a single awaitable stream
"""

def log(msg, *args):
    if args:
        msg = msg % args
    print(msg, file=sys.stderr)


class EventType(Enum):
    NETSTRING = "netstring"
    PROCESS_EXIT = "process_exit"

# Note: this could use a data class
# It has Optional data and Optional exit code, which is a bit weird

class Event:
    def __init__(self, pid: int, event_type: EventType, data: Optional[str] = None, exit_code: Optional[int] = None):
        self.pid = pid
        self.event_type = event_type
        self.data = data
        self.exit_code = exit_code
    
    def __str__(self) -> str:
        if self.event_type == EventType.NETSTRING:
            return f"Process {self.pid}: {self.data}"
        else:
            return f"Process {self.pid}: exited with code {self.exit_code}"

class ProcessMultiplexer:
    # ANDY: doesn't need to be a class
    # Should be more functional

    def __init__(self, argv_list: List[List[str]]):
        self.argv_list = argv_list
        self.event_queue: asyncio.Queue[Event] = asyncio.Queue()
        # these are the active processes
        self.processes: Dict[int, asyncio.subprocess.Process] = {}
    
    async def start_workers(self):
        """Start all worker processes."""
        for argv in self.argv_list:
            process = await asyncio.create_subprocess_exec(
                *argv,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            self.processes[process.pid] = process

            # monitor output and exit
            asyncio.create_task(self.monitor_output(process))
            asyncio.create_task(self.monitor_exit(process))
    
    async def monitor_output(self, process: asyncio.subprocess.Process):
        """Monitor and parse netstrings from the process stdout."""
        assert process.stdout is not None
        
        while True:
            try:
                # Read the length part until ':' delimiter
                length_bytes = await process.stdout.readuntil(b":")
                if not length_bytes:
                    break
                
                # Parse the length (remove the trailing ':')
                length = int(length_bytes[:-1].decode())
                
                # Read the content based on the length
                content = await process.stdout.readexactly(length)
                
                # Read the trailing comma
                comma = await process.stdout.readexactly(1)
                if comma != b',':
                    raise ValueError(f"Expected ',' after netstring content, got {comma!r}")
                
                # Create and queue the netstring event
                event = Event(
                    pid=process.pid,
                    event_type=EventType.NETSTRING,
                    data=content.decode()
                )

                # Put it in a queue, good
                await self.event_queue.put(event)
                
            except asyncio.IncompleteReadError:
                # EOF reached

                # ANDY: This is a PROTOCOL ERROR
                # TODO: test this case!  Test invalid netstrings
                break
            except Exception as e:
                # ANDY: Do you need this?
                print(f"Error processing output from PID {process.pid}: {e}", file=sys.stderr)
                break
    
    async def monitor_exit(self, process: asyncio.subprocess.Process):
        """Monitor the process exit and create an event when it exits."""

        # ANDY: OK we start a concurrent task for waiting?
        # Well why not just wait until you've reached EOF?

        #log('await process exit %r', process)
        exit_code = await process.wait()
        event = Event(
            pid=process.pid,
            event_type=EventType.PROCESS_EXIT,
            exit_code=exit_code
        )
        await self.event_queue.put(event)
    
    async def events(self):
        """Generator that yields events from all processes."""

        # Can't we just wait for 2 EOF events?
        # I think that's better
        active_processes = len(self.processes)
        
        while active_processes > 0:
            event = await self.event_queue.get()
            yield event
            
            if event.event_type == EventType.PROCESS_EXIT:
                active_processes -= 1

async def main():
    # Define arguments for two worker processes
    argv_list = [
        ["./worker.sh", "0.2"] + ['foo%d' % i for i in range(10)],
        ["./worker.sh", "0.5", "world", "asyncio"]
    ]
    if 1:
        new = []
        for argv in argv_list:
            # trickle output
            new.append(['sh', '-c', ' '.join(argv) + ' | ./trickle.py 2 100 0.3'])
        argv_list = new

    print(argv_list)
    
    # Create the multiplexer
    multiplexer = ProcessMultiplexer(argv_list)
    
    # Start the worker processes
    await multiplexer.start_workers()
    
    # Process events from all workers as they arrive
    async for event in multiplexer.events():
        print(event)

if __name__ == "__main__":
    asyncio.run(main())
