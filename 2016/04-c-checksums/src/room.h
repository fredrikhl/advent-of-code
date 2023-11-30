#pragma once

#include "pcre-setup.h"
#include "log.h"

#include <stdio.h>
#include <string.h>


typedef struct {
    char * name;
    int sid;
    char * chk;
} room_t;


#define room_debug(hint, room) log_debug("room %s: name=%s, sid=%d, chk=%s", hint, room->name, room->sid, room->chk)

int room_parse(const char * const value, room_t * room);
void room_clear(room_t *room);

char * room_decrypt(const char * const encrypted, int n);
size_t room_calc_checksum(const char * const name, size_t checksum_size, char * checksum);
int room_is_storage(const char * const name);
