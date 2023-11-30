#include "room.h"

/**
 * The room pattern.
 */
const char * const ROOM_PATTERN = "^([-a-z]+)-(\\d+)\\[([a-z]+)\\]$";
const int ROOM_GROUP_FULL = 0;
const int ROOM_GROUP_NAME = 1;
const int ROOM_GROUP_SID = 2;
const int ROOM_GROUP_CHK = 3;
const int ROOM_GROUPS = 4;


/**
 * Helper function for room_parse:
 *   Allocate and extract amtch groups from input string + match offsets.
 */
char * room_group_get(int n, const PCRE2_SPTR subject,
                      const PCRE2_SIZE * const offsets)
{
    char * result;
    char * substring_start = (char *) (subject + offsets[2*n]);
    int substring_length = (int) (offsets[2*n+1] - offsets[2*n]);

    result = (char *) malloc(substring_length + 1);
    if (result == NULL) {
        log_error("room_group_get(): malloc(%d) failed", substring_length + 1);
        return NULL;
    }
    strncpy(result, substring_start, substring_length);
    result[substring_length] = '\0';
    log_debug("room_group_get(%d, ...) -> %s", n, result);
    return result;
}


/**
 * Helper function for room_parse:
 *   Create new room_t from input string + match offsets.
 */
int room_new_from_match(const PCRE2_SPTR subject,
                        const PCRE2_SIZE * const offsets,
                        room_t * room)
{
    char * _room_sid;

    *room = (room_t) {
        .name = room_group_get(ROOM_GROUP_NAME, subject, offsets),
        .chk = room_group_get(ROOM_GROUP_CHK, subject, offsets),
        .sid = 0
    };
    _room_sid = room_group_get(ROOM_GROUP_SID, subject, offsets);

    if (room->name == NULL || room->chk == NULL || _room_sid == NULL) {
        // if any of these pointers are NULL, then something has gone horribly
        // wrong - free it all up and return NULL
        free(room->name);
        free(room->chk);
        free(_room_sid);
        log_error("room_new_from_match(): null value(s) in match");
        return -1;
    }

    room->sid = atoi(_room_sid);
    free(_room_sid);
    return 0;
}


/**
 * Extract room data from an input string.
 *
 * @param int n: the group to extract
 * @param PCRE2_SPTR* subject: the input search string
 * @param PCRE2_SIZE* ovector: the match group offsets
 *
 * @return char*: a newly allocated string with the match group content
 */
int room_parse(const char * const value, room_t * room)
{
    int error_code;
    int match_result;

    pcre2_code * regex;
    PCRE2_SPTR pattern;
    PCRE2_SPTR subject;

    PCRE2_SIZE error_offset;
    PCRE2_SIZE subject_length;
    PCRE2_SIZE * offset_vector;

    pcre2_match_data * match_data;

    pattern = (PCRE2_SPTR) ROOM_PATTERN;
    subject = (PCRE2_SPTR) value;
    subject_length = (PCRE2_SIZE) strlen(value);

    log_debug("room_parse(%s)", value);

    // compile -- options: 0, pcre2_compile_context: NULL
    regex = pcre2_compile(pattern, PCRE2_ZERO_TERMINATED, 0,
                          &error_code, &error_offset, NULL);

    if (regex == NULL) {
        // preg2_compile failed - log error and abort
        PCRE2_UCHAR buffer[256];
        pcre2_get_error_message(error_code, buffer, sizeof(buffer));
        log_error("room_parse(): pcre2_compile failed at offset %d: %s",
                  (int) error_offset, buffer);
        return -1;
    }

    // match result data block -- pcre2_general_context: NULL
    match_data = pcre2_match_data_create_from_pattern(regex, NULL);

    // run regex on subject -- offset: 0, options: 0, context: NULL
    match_result = pcre2_match(regex, subject, subject_length,
                               0, 0, match_data, NULL);

    if (match_result <= 0) {
        switch(match_result) {
            case 0:
                log_error("room_parse(): unable to allocate match data");
                break;
            case PCRE2_ERROR_NOMATCH:
                log_warn("room_parse(): no match for: %s", value);
                break;
            default:
                log_error("room_pare(): pcre2_match failed with error: %d",
                          match_result);
                break;
        }
        pcre2_match_data_free(match_data);
        pcre2_code_free(regex);
        return -1;
    }

    offset_vector = pcre2_get_ovector_pointer(match_data);
    if (offset_vector[0] > offset_vector[1]) {
        // Sanity check on match group 0:  Somehow it ends before it starts
        log_error("room_parse(): invalid offset vector (matched %d bytes)",
                  (int) (offset_vector[1] - offset_vector[0]));
        pcre2_match_data_free(match_data);
        pcre2_code_free(regex);
        return -1;
    }

    if (match_result != ROOM_GROUPS) {
        // Santity check: We should have 4 match groups
        // (the whole string + our three capture groups).
        log_error("room_parse(): incomplete match, unable to extract groups");
        pcre2_match_data_free(match_data);
        pcre2_code_free(regex);
        return -1;
    }

    room_new_from_match(subject, offset_vector, room);
    pcre2_match_data_free(match_data);
    pcre2_code_free(regex);
    return 0;
}


/**
 * Destroy and clean up room struct.
 */
void room_clear(room_t * room)
{
    if (room == NULL) {
        return;
    }
    free(room->name);
    free(room->chk);
    room->name = NULL;
    room->chk = NULL;
    room->sid = 0;
}


const char * const ASCII_LOWER = "abcdefghijklmnopqrstuvwxyz";
#define ASCII_LEN 26


#define char_to_index(c) (size_t) (c - ASCII_LOWER[0])
#define char_from_index(i) (char) i + ASCII_LOWER[0]


/**
 * Calculate checksum for a given room name.
 *
 * char * name: name to get checksum for
 * char * checksum: buffer for checksum result (at least checksum_size big).
 * size_t checksum_size: length of checksum
 */
size_t room_calc_checksum(
        const char * const name,
        size_t checksum_size,
        char * checksum)
{
    log_debug("room_checksum_calc(%s)", name);

    int letters[ASCII_LEN] = { 0 };
    size_t namelen = strlen(name);
    size_t checklen = 0;

    // track highest, second highest counts
    int max = 0, next_max = 0;

    // Count letters, and keep track of the highest value
    for (size_t i = 0; i < namelen; i++) {
        if (strchr(ASCII_LOWER, name[i]) == NULL) {
            // not a letter
            continue;
        }
        letters[char_to_index(name[i])] += 1;
        if (letters[char_to_index(name[i])] > max) {
            max = letters[char_to_index(name[i])];
        }
    }

    while (checklen < checksum_size) {
        for (int i = 0; i < ASCII_LEN; i++) {
            if (letters[i] == max) {
                // this char has the *max* occurences (although it might share
                // that with other chars)
                checksum[checklen] = char_from_index(i);
                letters[i] = -1;  // invalidate this char
                if (++checklen == checksum_size) {
                    break;
                }
            }
            if (letters[i] < max && letters[i] > next_max) {
                // so far, the second highest count in this round is letters[i]
                next_max = letters[i];
            }
        }
        // we went through all the letters, there are currently no more chars
        // with a letter count of *max*, let's continue with a new, lower *max*.
        max = next_max;
        next_max = 0;
    }
    checksum[checklen] = '\0';
    return checklen;
}


char shift_char(char c, int n) {
    char * offset;
    int size = strlen(ASCII_LOWER);
    if (c == '-') {
        return ' ';
    }
    offset = strchr(ASCII_LOWER, c);
    if (offset == NULL) {
        // probably an error, but we just don't shift this char;
        return c;
    }
    return ASCII_LOWER[(offset - ASCII_LOWER + n) % size];
}


/**
 * Calculate checksum for a given room name.
 *
 * char * encrypted: name to decrypt
 * int n: rot n
 */
char * room_decrypt(const char * const encrypted, int n)
{
    char * plaintext;
    int length = 0;
    length = strlen(encrypted);
    plaintext = (char *) malloc(length + 1);
    if (plaintext == NULL) {
        log_error("room_decrypt(): malloc(%d) failed", length + 1);
        return NULL;
    }
    for (int i = 0; i < length; i++) {
        plaintext[i] = shift_char(encrypted[i], n);
    }
    plaintext[length] = '\0';
    return plaintext;
}


const char * SEARCH_TERMS[] = { "north", "pole", "object" };


int room_is_storage(const char * const name)
{
    char * match = NULL;
    for (int i = 0; i < 3; i++ ) {
        match = strstr(name, SEARCH_TERMS[i]);
        if (match != NULL) {
            return 1;
        }
    }
    return 0;
}
