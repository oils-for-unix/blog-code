

## Notes on Lib/asyncio implementation

Why does  StreamReader -> readuntil() -> `_wait_for_data()` handle PAUSING?

For flow control?

But I think backpressure can be handled by queues


Potential problem:
- readuntil(':') is not safe from an adversary
  - you want `readuntil(':', max_bytes=10)` or something

https://peps.python.org/pep-3156/

> set_write_buffer_limits(high=None, low=None). Set the high- and low-water
> limits for flow control.

> These two values control when to call the protocol’s pause_writing() and
> resume_writing() methods. If specified, the low-water limit must be less than
> or equal to the high-water limit. Neither value can be negative.

> The defaults are implementation-specific. If only the high-water limit is
> given, the low-water limit defaults to an implementation-specific value less
> than or equal to the high-water limit. Setting high to zero forces low to
> zero as well, and causes pause_writing() to be called whenever the buffer
> becomes non-empty. Setting low to zero causes resume_writing() to be called
> only once the buffer is empty. Use of zero for either limit is generally
> sub-optimal as it reduces opportunities for doing I/O and computation
> concurrently.

> pause_reading(). Suspend delivery of data to the protocol until a subsequent
> resume_reading() call. Between pause_reading() and resume_reading(), the
> protocol’s data_received() method will not be called.

> resume_reading().  Restart delivery of data to the protocol via
> data_received().  Note that “paused” is a binary state – pause_reading()
> should only be called when the transport is not paused, while
> resume_reading() should only be called when the transport is paused.


I'm not sure we should handle all this.  It makes sense for network servers perhaps

Or Streaming servers


I think I want fairly simple HTTP, with robust limits.  e.g. 1 MB max request
size and 1 MB response size.

- An exception is multi-part/mime post of large files
  - but those will be buffered to disk I think
  - definitely if they are big


### Subprocess

```
$ wc -l subprocess.py
229 subprocess.py


$ showpy subprocess.py  | cat
class SubprocessStreamProtocol(streams.FlowControlMixin,
    def __init__(self, limit, loop):
    def __repr__(self):
    def connection_made(self, transport):
    def pipe_data_received(self, fd, data):
    def pipe_connection_lost(self, fd, exc):
    def process_exited(self):
    def _maybe_close_transport(self):
    def _get_close_waiter(self, stream):
class Process:
    def __init__(self, transport, protocol, loop):
    def __repr__(self):
    def returncode(self):
    async def wait(self):
    def send_signal(self, signal):
    def terminate(self):
    def kill(self):
    async def _feed_stdin(self, input):
    async def _noop(self):
    async def _read_stream(self, fd):
    async def communicate(self, input=None):
async def create_subprocess_shell(cmd, stdin=None, stdout=None, stderr=None,
async def create_subprocess_exec(program, *args, stdin=None, stdout=None,
```

This is pretty interesting

```
   868 events.py
   897 proactor_events.py
   901 windows_events.py
   926 sslproto.py
  1065 tasks.py
  1321 selector_events.py
  1500 unix_events.py
  2012 base_events.py
 14299 total
andy@hoover:~/src/Python-3.12.4/Lib/asyncio$ wc -l *.py|sort -n
```

Damn Windows support must have been a lot of work

## Event Loops

> There is no actual class named EventLoop. There is an AbstractEventLoop class
> which defines all the methods without implementations, and serves primarily
> as documentation. The following concrete classes are defined:

> SelectorEventLoop is a concrete implementation of the full API based on the
> selectors module (new in Python 3.4). The constructor takes one optional
> argument, a selectors.Selector object. By default an instance of
> selectors.DefaultSelector is created and used.

> ProactorEventLoop is a concrete implementation of the API except for the I/O
> event handling and signal handling methods. It is only defined on Windows (or
> on other platforms which support a similar API for “overlapped I/O”). The
> constructor takes one optional argument, a Proactor object. By default an
> instance of IocpProactor is created and used. (The IocpProactor class is not
> specified by this PEP; it is just an implementation detail of the
> ProactorEventLoop class.)

Damn I thought we could do something portable ...

Well this one reason to constrain it to YSH.

## Claude AI on 2 different kinds of async I/O in Windows

Windows offers two different mechanisms for handling multiple I/O operations:
WaitForMultipleObjects() and I/O Completion Ports (IOCP). They serve similar
purposes but with significant architectural differences:

### WaitForMultipleObjects()

Operation Model: Notification-based - waits until one or more objects from a specified array enter a signaled state.

Scalability: Limited to a maximum of MAXIMUM_WAIT_OBJECTS (typically 64) handles at once.

Usage Pattern: Better for smaller applications with fewer concurrent operations.

Threading Model: Often requires creating multiple threads when you exceed the handle limit.

Behavior: Returns when any of the objects becomes signaled, requiring you to determine which one(s).

Performance: Less efficient for high-concurrency scenarios.

### I/O Completion Ports (IOCP)

Operation Model: Completion-based - returns when an asynchronous I/O operation has finished.

Scalability: Designed for thousands of concurrent operations.

Usage Pattern: Ideal for high-performance servers and applications with many connections.

Threading Model: Uses a thread pool with optimized thread scheduling - threads are only awakened when work is available.

Behavior: Queues completed I/O operations for processing by an available thread.

Performance: Offers the best performance for high-concurrency scenarios on Windows.

This is why asyncio on Windows uses the ProactorEventLoop (based on IOCP) by
default - it provides much better scalability for handling many concurrent
connections compared to what would be possible with WaitForMultipleObjects().
