/*
 * seccomp example with syscall reporting
 *
 * Copyright (c) 2012 The Chromium OS Authors <chromium-os-dev@chromium.org>
 * Authors:
 *  Kees Cook <keescook@chromium.org>
 *  Will Drewry <wad@chromium.org>
 *
 * Use of this source code is governed by a BSD-style license that can be
 * found in the LICENSE file.
 */
#define _GNU_SOURCE 1
#include <stdio.h>
#include <stddef.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char *argv[])
{
	char buf[1024];

	printf("Type stuff here: ");
	fflush(NULL);
	buf[0] = '\0';
	fgets(buf, sizeof(buf), stdin);
	printf("You typed: %s", buf);

	printf("And now we fork, which should do quite the opposite ...\n");
	fflush(NULL);
	sleep(1);

	fork();
	printf("You should not see this because I'm dead.\n");

	return 0;
}
