#!/usr/bin/env python3
import asyncio
import sys
from enum import Enum
from typing import Dict, List, Optional, Tuple, Union

class EventType(Enum):
    NETSTRING = "netstring"
    PROCESS_EXIT = "process_exit"

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
    def __init__(self, worker_script: str, sleep_interval: float, args_list: List[List[str]]):
        self.worker_script = worker_script
        self.sleep_interval = sleep_interval
        self.args_list = args_list
        self.event_queue = asyncio.Queue()
        self.processes: Dict[int, asyncio.subprocess.Process] = {}
    
    async def start_workers(self):
        """Start all worker processes."""
        for args in self.args_list:
            cmd = [self.worker_script, str(self.sleep_interval)] + args
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            self.processes[process.pid] = process
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
                await self.event_queue.put(event)
                
            except asyncio.IncompleteReadError:
                # EOF reached
                break
            except Exception as e:
                print(f"Error processing output from PID {process.pid}: {e}", file=sys.stderr)
                break
    
    async def monitor_exit(self, process: asyncio.subprocess.Process):
        """Monitor the process exit and create an event when it exits."""
        exit_code = await process.wait()
        event = Event(
            pid=process.pid,
            event_type=EventType.PROCESS_EXIT,
            exit_code=exit_code
        )
        await self.event_queue.put(event)
    
    async def events(self):
        """Generator that yields events from all processes."""
        active_processes = len(self.processes)
        
        while active_processes > 0:
            event = await self.event_queue.get()
            yield event
            
            if event.event_type == EventType.PROCESS_EXIT:
                active_processes -= 1

async def main():
    # Define arguments for two worker processes
    args_list = [
        ["foo", "bar", "baz"],
        ["hello", "world", "asyncio"]
    ]
    
    # Create the multiplexer
    multiplexer = ProcessMultiplexer("./worker.sh", 0.5, args_list)
    
    # Start the worker processes
    await multiplexer.start_workers()
    
    # Process events from all workers as they arrive
    async for event in multiplexer.events():
        print(event)

if __name__ == "__main__":
    asyncio.run(main())
