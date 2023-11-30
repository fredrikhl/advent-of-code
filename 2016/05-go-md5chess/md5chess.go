package main

import (
    "crypto/md5"
    "encoding/hex"
    "flag"
    "fmt"
    "io/ioutil"
    "log"
    "strconv"
    "strings"
    "time"
)


// md5hex gets a hex-encoded md5 digest for a string.
func md5hex(input string) string {
    data := []byte(input)
    sum := md5.Sum(data)
    // sum[:] - byte array to byte slice
    return hex.EncodeToString(sum[:])
}


// nexthash gets the next "00000"-prefixed hash, starting at a given index.
//
// Returns the un-prefixed hex-encoded hash, as well as the next unprocescced
// index (i.e. where to resume).
//
// Example:
//   partial, next := nexthash("abc", 0)
//   partial, next := nexthash("abc", next)
func nexthash(door string, index int) (string, int) {
    for {
        hash := md5hex(fmt.Sprintf("%s%d", door, index))
        index++
        if hash[:5] == "00000" {
            return hash[5:], index
        }
    }
}


// placeholder char for getPasswordBuffer(length)
const placeholder = '_'


// getPasswordBuffer creates a rune slice of a given size, filled with a
// placeholder runes.
func getPasswordBuffer(length int) []rune {
    return []rune(strings.Repeat(string(placeholder), length))
}


// FindPassword1 finds a password of a given length for a given door.
//
// For each nexthash(door, index), it uses the first byte from the partial
// hash as the next password character.
func FindPassword1(door string, length int) string {
    var hash string
    index, pos := 0, 0
    password := getPasswordBuffer(length)

    for pos < length {
        hash, index = nexthash(door, index)
        password[pos] = rune(hash[0])
        pos++
        log.Printf("pt1 partial: %s", string(password))
    }
    return string(password)
}


// FindPassword2 finds a password of a given length for a given door.
//
// For each nexthash(door, index), it places the second byte from the partial
// hash at the position indicated by the first byte, as long as the first byte
// is within range for the wanted password length.
func FindPassword2(door string, length int) string {
    var hash string
    index, found := 0, 0
    password := getPasswordBuffer(length)

    for found < length {
        hash, index = nexthash(door, index)
        pos, posErr := strconv.Atoi(string(hash[0]))
        if posErr != nil || pos >= length {
            // invalid position: not a number/out of range
            continue
        }
        if password[pos] == placeholder {
            password[pos] = rune(hash[1])
            found++
            log.Printf("pt2 partial: %s", string(password))
        }
    }
    return string(password)
}


func main() {
    log.SetFlags(log.Lshortfile)
    log.SetPrefix("DEBUG:")

    var (
        length int
        debug bool
        door string
        start time.Time
    )

    flag.IntVar(&length, "len", 8, "password length")
    flag.BoolVar(&debug, "debug", false, "verbose output (progress, etc...)")
    flag.StringVar(&door, "door", "abc", "door id")
    flag.Parse()

    if !debug {
        log.SetOutput(ioutil.Discard)
    }

    log.Printf("door id: %v", door)
    log.Printf("length: %v", length)

    start = time.Now()
    pt11 := FindPassword1(door, 8)
    log.Printf("part 1 timer: %v", time.Since(start))
    fmt.Println("Part 1:", pt11)

    start = time.Now()
    pt2 := FindPassword2(door, 8)
    log.Printf("part 2 timer: %v", time.Since(start))
    fmt.Println("Part 2:", pt2)
}
