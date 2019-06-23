// Copied from http://man7.org/linux/man-pages/man3/mbstowcs.3.html

#include <wctype.h>
#include <locale.h>
#include <wchar.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int
main(int argc, char *argv[])
{
    size_t mbslen;      /* Number of multibyte characters in source */
    wchar_t *wcs;       /* Pointer to converted wide character string */
    wchar_t *wp;

    if (argc < 3) {
        fprintf(stderr, "Usage: %s <locale> <string>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    /* Apply the specified locale */

    if (setlocale(LC_ALL, argv[1]) == NULL) {
        perror("setlocale");
        exit(EXIT_FAILURE);
    }

    /* Calculate the length required to hold argv[2] converted to
       a wide character string */

    mbslen = mbstowcs(NULL, argv[2], 0);
    if (mbslen == (size_t) -1) {
        perror("mbstowcs");
        exit(EXIT_FAILURE);
    }

    /* Describe the source string to the user */

    printf("Length of source string (excluding terminator):\n");
    printf("    %zu bytes\n", strlen(argv[2]));
    printf("    %zu multibyte characters\n\n", mbslen);

    /* Allocate wide character string of the desired size.  Add 1
       to allow for terminating null wide character (L'\0'). */

    wcs = calloc(mbslen + 1, sizeof(wchar_t));
    if (wcs == NULL) {
        perror("calloc");
        exit(EXIT_FAILURE);
    }

    /* Convert the multibyte character string in argv[2] to a
       wide character string */

    if (mbstowcs(wcs, argv[2], mbslen + 1) == (size_t) -1) {
        perror("mbstowcs");
        exit(EXIT_FAILURE);
    }

    printf("Wide character string is: %ls (%zu characters)\n",
            wcs, mbslen);

    /* Now do some inspection of the classes of the characters in
       the wide character string */

    for (wp = wcs; *wp != 0; wp++) {
        printf("    %lc ", (wint_t) *wp);

        if (!iswalpha(*wp))
            printf("!");
        printf("alpha ");

        if (iswalpha(*wp)) {
            if (iswupper(*wp))
                printf("upper ");

            if (iswlower(*wp))
                printf("lower ");
        }

        putchar('\n');
    }

    exit(EXIT_SUCCESS);
}
