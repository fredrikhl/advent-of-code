#include "log.h"
#include "room.h"

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


#define CHECKSUM_LEN 5


/**
 * Reimplementation of the POSIX getline
 *
 * Differences:
 *     - the function returns int64_t instead of ssize_t
 *     - does not accept NUL characters in the input file
 */
int get_line(char **restrict line, size_t *restrict len, FILE *restrict fp)
{
    // Check if either line, len or fp are NULL pointers
    if (line == NULL || len == NULL || fp == NULL) {
        log_warn("get_line(): unexpected null value")
        return -1;
    }

    // Use a chunk array of 128 bytes as parameter for fgets
    char chunk[128];

    // Allocate a block of memory for *line if it is NULL or smaller than the
    // chunk array
    if (*line == NULL || *len < sizeof(chunk)) {
        *len = sizeof(chunk);
        if ((*line = malloc(*len)) == NULL) {
            log_warn("get_line(): malloc(%d) failed", *len);
            return -1;
        }
    }

    // terminate string at start
    (*line)[0] = '\0';

    while (fgets(chunk, sizeof(chunk), fp) != NULL) {
        // Resize the line buffer if necessary
        size_t len_used = strlen(*line);
        size_t chunk_used = strlen(chunk);

        if (*len - len_used < chunk_used) {
            // Check for overflow
            if (*len > SIZE_MAX / 2) {
                log_warn("get_line(): overflow");
                return -1;
            } else {
                *len *= 2;
            }

            if ((*line = realloc(*line, *len)) == NULL) {
                log_warn("get_line(): realloc(%d) failed", *len);
                return -1;
            }
        }

        // Copy the chunk to the end of the line buffer
        memcpy(*line + len_used, chunk, chunk_used);
        len_used += chunk_used;
        (*line)[len_used] = '\0';

        // Check if *line contains '\n', if yes, return the *line length
        if ((*line)[len_used - 1] == '\n') {
            // strip newline
            (*line)[len_used - 1] = '\0';
            return len_used;
        }
    }
    return -1;
}


int solve_file(char *filename)
{
    // File pointers and line buffers
    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    int read;
    int lineno = 0;

    room_t room_data;
    room_t * room = &room_data;
    char * plain = NULL;

    // calculated checksum buffer and result
    char checksum[CHECKSUM_LEN + 1] = { '\0' };
    size_t checksum_res;

    // part 1 sum, and part 2 target_sid
    int sum = 0;
    int found_sid = -1;

    fp = fopen(filename, "r");
    if (fp == NULL) {
        log_error("solve_file(): unable to open file %s", filename);
        exit(EXIT_FAILURE);
    }

    while ((read = get_line(&line, &len, fp)) != -1) {
        log_debug("read line #%d, length %zu: %s", ++lineno, read, line);

        if (room_parse(line, room) != 0) {
            log_error("unable to parse lineno %d: %s", lineno, line);
            exit(EXIT_FAILURE);
        }

        checksum_res = room_calc_checksum(room->name, CHECKSUM_LEN, checksum);
        if (checksum_res != CHECKSUM_LEN) {
            log_error("unable to calc checksum: %s", room->name);
            room_clear(room);
            exit(EXIT_FAILURE);
        }

        if (strncmp(room->chk, checksum, 5) != 0) {
            log_warn("invalid checksum for %s: got: %s, expexted: %s",
                     room->name, room->chk, checksum);
            room_clear(room);
            continue;
        }

        sum += room->sid;

        if ((plain = room_decrypt(room->name, room->sid)) == NULL) {
            log_error("unable to decrypt room name %s", room->name);
            room_clear(room);
            exit(EXIT_FAILURE);
        }

        if (room_is_storage(plain) != 0) {
            log_debug("found north pole storage on line %d: %s",
                      lineno, plain);
            found_sid = room->sid;
        }
        free(plain);
        room_clear(room);
    }
    free(line);
    fclose(fp);

    printf("Part 1: %d\n", sum);
    printf("Part 2: %d\n", found_sid);
    exit(EXIT_SUCCESS);
}


/*
room_t test_code_call(char * mystr)
{
    room_t foo = { .name = NULL, .sid = 3, .chk = NULL };
    log_debug("size: %d", sizeof(foo));
    return foo;
}


void test_code() {
    char mystr[6]= { '\0' };
    room_t bar;
    bar = test_code_call(mystr);
    log_debug("size: %d", sizeof(bar));
}
*/


int main(int argc, char **argv)
{
    char usage[256];
    char *filename;

    // make a usage const-like
    sprintf(usage, "usage: %s <file>\n", argv[0]);

    for (int i = 0; i < argc; i++) {
        log_debug("arg %02d: '%s'", i, argv[i]);
    }

    switch (argc) {
        case 2:
            filename = argv[1];
            break;
        case 1:
            log_error("missing arguments (got: %d, expected: 1)", argc - 1);
            fprintf(stderr, usage);
            exit(EXIT_FAILURE);
        default:
            log_error("too many arguments (got: %d, expected: 1)", argc - 1);
            fprintf(stderr, usage);
            exit(EXIT_FAILURE);
    }


    solve_file(filename);
    //test_code();

    return EXIT_SUCCESS;
}
