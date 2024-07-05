#!/usr/bin/env bash

build-1() {
  cc -o example-1 step-1/example.c
}

download-2() {
  mkdir step-2

  local url=https://outflux.net/teach-seccomp/step-2
  pushd step-2
  wget $url/{LICENSE,Makefile,config.h.in,configure.ac,example.c,seccomp-bpf.h}
  popd
}

build-2() {
  cc -o example-2 step-2/example.c
}

download-3() {
  mkdir step-3

  local url=https://outflux.net/teach-seccomp/step-3
  pushd step-3
  wget $url/{LICENSE,Makefile,config.h.in,configure.ac,example.c,seccomp-bpf.h,syscall-reporter.{c,h,mk}}
  popd
}

build-3() {
  cc -o example-3 step-3/{example.c,syscall-reporter.c}
}

"$@"
