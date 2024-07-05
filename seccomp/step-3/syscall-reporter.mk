#
# syscall reporting example for seccomp
#
# Copyright (c) 2012 The Chromium OS Authors <chromium-os-dev@chromium.org>
# Authors:
#  Kees Cook <keescook@chromium.org>
#
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

syscall-names.h: /usr/include/sys/syscall.h syscall-reporter.mk
	echo "static const char *syscall_names[] = {" > $@ ;\
	echo "#include <sys/syscall.h>" | cpp -dM | grep '^#define __NR_' | \
		LC_ALL=C sed -r -n -e 's/^\#define[ \t]+__NR_([a-z0-9_]+)[ \t]+([0-9]+)(.*)/ [\2] = "\1",/p' >> $@ ;\
	echo "};" >> $@

syscall-reporter.o: syscall-reporter.c syscall-names.h
