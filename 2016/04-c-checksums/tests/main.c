/*
 * Cmocha unit test entry point
 */
#include <setjmp.h>
#include <stdarg.h>
#include <stddef.h>
#include <cmocka.h>

#include "../src/room.h"
#define CHECKSUM_LEN 5


static void test_room_parse_ex3()
{
    int result;
    room_t room_data;
    room_t * room = &room_data;

    char * input_str = "not-a-real-room-404[oarel]";
    char * is_name = "not-a-real-room";
    char * is_chk = "oarel";
    int is_sid = 404;

    result = room_parse(input_str, room);
    assert_int_equal(result, 0);
    assert_string_equal(room->name, is_name);
    assert_int_equal(room->sid, is_sid);
    assert_string_equal(room->chk, is_chk);
}


static void test_room_parse_ex4()
{
    int result;
    room_t room_data;
    room_t * room = &room_data;

    char * input_str = "totally-real-room-200[decoy]";
    char * is_name = "totally-real-room";
    char * is_chk = "decoy";
    int is_sid = 200;

    result = room_parse(input_str, room);
    assert_int_equal(result, 0);
    assert_string_equal(room->name, is_name);
    assert_int_equal(room->sid, is_sid);
    assert_string_equal(room->chk, is_chk);
}


static void test_room_calc_checksum_ex1()
{
    char checksum[CHECKSUM_LEN + 1] = { '\0' };
    size_t result;
    char * name = "aaaaa-bbb-z-y-x";
    char * is_chk = "abxyz";

    result = room_calc_checksum(name, CHECKSUM_LEN, checksum);
    assert_int_equal(result, CHECKSUM_LEN);
    assert_string_equal(checksum, is_chk);
}


static void test_room_calc_checksum_ex4()
{
    char checksum[CHECKSUM_LEN + 1] = { '\0' };
    size_t result;
    char * name = "totally-real-room";
    char * is_chk = "decoy";

    result = room_calc_checksum(name, CHECKSUM_LEN, checksum);
    assert_int_equal(result, CHECKSUM_LEN);
    assert_string_not_equal(checksum, is_chk);
}


static void test_room_decrypt()
{
    char * name = "qzmt-zixmtkozy-ivhz";
    int sid = 343;
    char * real_name;
    char * is_real_name = "very encrypted name";

    real_name = room_decrypt(name, sid);
    assert_string_equal(real_name, is_real_name);
}



/*
 * Test runner function
 */
int main(void)
{

    // TODO: Do we have to manually add each test here?
    const struct CMUnitTest tests[] = {
        cmocka_unit_test(test_room_parse_ex3),
        cmocka_unit_test(test_room_parse_ex4),
        cmocka_unit_test(test_room_calc_checksum_ex1),
        cmocka_unit_test(test_room_calc_checksum_ex4),
        cmocka_unit_test(test_room_decrypt),
    };

    // Run tests
    return cmocka_run_group_tests(tests, NULL, NULL);
}
