Coprocesses
=========

- The async experiments reminded me of my experiments: Torn, fly, xmap

- General idea 
  - Turn CLI into coprocesses with FANOS protocol
  - then you can use fly to invoke them
    - or use YSH itself
    - it can have a pool of processes perhaps

- then you can use xmap to parallelize them locally

- then you can use the CGI 2/PGI server to multiplex them
- you just deploy the server exactly as is


- I also wonder if we do some kind of multi-language / multi-process caching thing, like litestream
  - I think that uses a lot of decorators
  - we could do that in shell

## Useful for YSH

- SSH to server
  - wrap arbitrary group of programs with YSH
  - set timeouts

- YSH listens on an HTTP port
  - and then you can server an HTML skeleton
  - and all the logs executing in parallel
  - as well as time and resource usage

- problem: are you authorized to do that
  - there is no protocol for making an arbitrary machine a web server
  - you could do it on some "guessed" port, though that's a bit dangerous
  - I guess this is what Tailscale is for
    - but I wouldn't want to install Tailscale on that server?

