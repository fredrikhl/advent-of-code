#!/usr/bin/env bats

source "${BATS_TEST_DIRNAME}/shortest.bash"


#
# logging (stderr output)
#
@test "debug enabled" {
    export DEBUG_OUT=2
    run debug "foo" "bar" "baz"
    [ "$status" -eq 0 ]
    [ "$output" = "DEBUG: foo bar baz" ]
}

@test "debug disabled" {
    export DEBUG_OUT=1
    run debug "foo" "bar" "baz"
    [ "$status" -eq 0 ]
    [ "$output" = "" ]
}

@test "info enabled" {
    export DEBUG_OUT=1
    run info "foo" "bar" "baz"
    [ "$status" -eq 0 ]
    [ "$output" = "INFO: foo bar baz" ]
}

@test "info disabled" {
    export DEBUG_OUT=0
    run info "foo" "bar" "baz"
    [ "$status" -eq 0 ]
    [ "$output" = "" ]
}

@test "error" {
    run error "foo" "bar" "baz"
    [ "$status" -eq 0 ]
    [ "$output" = "ERROR: foo bar baz" ]
}


#
# instructions
#

@test "get-turn R5" {
    run get-turn R5
    [ "$status" -eq 0 ]
    [ "$output" = "R" ]
}

@test "get-turn L5" {
    run get-turn L5
    [ "$status" -eq 0 ]
    [ "$output" = "L" ]
}

@test "get-turn error" {
    run get-turn X5
    [ "$status" -ne 0 ]
}


@test "get-steps R0" {
    run get-steps R0
    [ "$status" -eq 0 ]
    [ "$output" = "0" ]
}

@test "get-steps R5" {
    run get-steps R5
    [ "$status" -eq 0 ]
    [ "$output" = "5" ]
}

@test "get-steps error" {
    run get-steps LR1
    [ "$status" -ne 0 ]
}


@test "get-heading NR" {
    run get-heading NR
    [ "$status" -eq 0 ]
    [ "$output" = "E" ]
}

@test "get-heading WL" {
    run get-heading WL
    [ "$status" -eq 0 ]
    [ "$output" = "S" ]
}

@test "get-heading error" {
    run get-heading XY
    [ "$status" -eq 1 ]
}


#
# serialization
#

@test "encode-state 0,0" {
    run encode-state 0 0
    [ "$status" -eq 0 ]
    [ "$output" = "0,0" ]
}

@test "encode-state -1,1,N" {
    run encode-state -1 1 N
    [ "$status" -eq 0 ]
    [ "$output" = "-1,1,N" ]
}

@test "encode-state many fields" {
    run encode-state 1 2 3 4 5 6
    [ "$status" -eq 0 ]
    [ "$output" = "1,2,3,4,5,6" ]
}

@test "get-state first of one" {
    run get-state 0 1
    [ "$status" -eq 0 ]
    [ "$output" -eq 1 ]
}

@test "get-state first of two" {
    run get-state 0 "1,2"
    [ "$status" -eq 0 ]
    [ "$output" -eq 1 ]
}

@test "get-state second of two" {
    run get-state 1 -1,-2
    [ "$status" -eq 0 ]
    [ "$output" -eq -2 ]
}

@test "get-state second in empties" {
    run get-state 2 ,,-1,,,,
    [ "$status" -eq 0 ]
    [ "$output" -eq -1 ]
}

@test "get-state out-of-bounds" {
    run get-state 2 1,2
    [ "$status" -ne 0 ]
}

@test "get-pos" {
    run get-pos "3,-1,N"
    [ "$status" -eq 0 ]
    [ "$output" = "3,-1" ]
}


#
# calculation
#

@test "abs 23" {
    run abs 23
    [ "$status" -eq 0 ]
    [ "$output" -eq 23 ]
}

@test "abs -32" {
    run abs -32
    [ "$status" -eq 0 ]
    [ "$output" -eq 32 ]
}


@test "distance with default offset" {
    run distance 10,10
    [ "$status" -eq 0 ]
    [ "$output" -eq 20 ]
}

@test "distance with offset" {
    run distance 10,-11 -1,1
    [ "$status" -eq 0 ]
    [ "$output" -eq 23 ]
}


@test "turn 2,3,N R" {
    run turn 2,3,N R
    [ "$status" -eq 0 ]
    [ "$output" = "2,3,E" ]
}

@test "turn 2,3,N L" {
    run turn 2,3,N L
    [ "$status" -eq 0 ]
    [ "$output" = "2,3,W" ]
}


@test "step 2,3,N" {
    run step 2,3,N
    [ "$status" -eq 0 ]
    [ "$output" = "2,4,N" ]
}

@test "step 2,-3,W" {
    run step 2,-3,W
    [ "$status" -eq 0 ]
    [ "$output" = "1,-3,W" ]
}


@test "move 2,3,N R2" {
    run move 2,3,N R2
    [ "$status" -eq 0 ]
    [ "${#lines[@]}" -eq 2 ]
    [ "${lines[-1]}" = "4,3,E" ]
}

@test "move -2,3,W L4" {
    run move -2,3,W L4
    [ "$status" -eq 0 ]
    [ "${#lines[@]}" -eq 4 ]
    [ "${lines[-1]}" = "-2,-1,S" ]
}


#
# parsing
#

@test "trim" {
    run trim "   foo "
    [ "$status" -eq 0 ]
    [ "$output" = "foo" ]
}


@test "parse" {
    run parse "R1, R2" "R3,R4, "
    [ "$status" -eq 0 ]
    [ "${#lines[@]}" -eq 4 ]
    [ "${lines[0]}" = "R1" ]
    [ "${lines[1]}" = "R2" ]
    [ "${lines[2]}" = "R3" ]
    [ "${lines[3]}" = "R4" ]
}


#
# examples
#

@test "travel R2,L3" {
    run travel <(echo "R2,L3")
    echo "${lines[*]}"
    [ "$status" -eq 0 ]
    [ "${#lines[@]}" -eq 1 ]
    [ "${lines[0]}" = "Shortest: 5 steps" ]
}

@test "travel R2,R2,R2" {
    run travel <(echo "R2,R2,R2")
    echo "${lines[*]}"
    [ "$status" -eq 0 ]
    [ "${#lines[@]}" -eq 1 ]
    [ "${lines[0]}" = "Shortest: 2 steps" ]
}

@test "travel R5,L5,R5,R3" {
    run travel <(echo "R5,L5,R5,R3")
    echo "${lines[*]}"
    [ "$status" -eq 0 ]
    [ "${#lines[@]}" -eq 1 ]
    [ "${lines[0]}" = "Shortest: 12 steps" ]
}


@test "travel R8,R4,R4,R8 with limit=2" {
    run travel <(echo "R8, R4, R4, R8") 2
    echo "${lines[*]}"
    [ "$status" -eq 0 ]
    [ "${#lines[@]}" -eq 1 ]
    [ "${lines[0]}" = "Shortest: 4 steps" ]
}
