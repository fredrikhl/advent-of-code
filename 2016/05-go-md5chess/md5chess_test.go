package main


import (
    "reflect"
    "testing"
)


func TestMd5hex(t *testing.T) {
    plain := "Hello, World"
    expect := "82bb413746aee42f89dea2b59614f9ef"
    hex := md5hex(plain)
    if hex != expect {
        t.Fatalf("md5hex(%s) = %q, expected %q", plain, hex, expect)
    }
}

func TestGetPasswordBuffer(t *testing.T) {
    expect := []rune{'_', '_'}
    buffer := getPasswordBuffer(2)
    if !reflect.DeepEqual(buffer, expect) {
        t.Fatalf("getPasswordBuffer(2) = %q, expected %q", buffer, expect)
    }
}

func TestNexthashForAbc0(t *testing.T) {
    expectNext := 3231929 + 1
    expectChars:= "15..."
    partial, next := nexthash("abc", 0)
    chars := partial[0:2] + "..."
    if chars != expectChars {
        t.Fatalf(
            "nexthash(\"abc\", 0) = %q %d, expected %q %d",
            chars, next, expectChars, expectNext,
        )
    }
}

func TestNexthashForAbc3231930(t *testing.T) {
    expectNext := 5017308 + 1
    expectChars:= "8f82..."
    partial, next := nexthash("abc", 3231930)
    chars := partial[0:4] + "..."
    if chars != expectChars {
        t.Fatalf(
            "nexthash(\"abc\", 3231930) = %q %d, expected %q %d",
            chars, next, expectChars, expectNext,
        )
    }
}
