#!/usr/bin/env bash
#
# Global state
#
DEBUG_OUT="${DEBUG_OUT:-0}"
ERR_INVALID_VALUE=1

error()
{
    >&2 echo "ERROR: $*"
}

info()
{
    [ "${DEBUG_OUT}" -gt 0 ] && >&2 echo "INFO: $*"
    true
}

debug()
{
    [ "${DEBUG_OUT}" -gt 1 ] && >&2 echo "DEBUG: $*"
    true
}


# Get turn direction from instruction
#
#   get-turn L23  # outputs 'L'
#   get-turn R    # outputs 'R'
#   get-turn 23   # error
get-turn()
{
    local op="${1}"
    [[ "${op::1}" =~ ^[RL]$ ]] && echo "${op::1}" && return 0
    error "Invalid instruction: '${op}'"
    return $ERR_INVALID_VALUE;
}


# Get number of steps from instruction
#
#   get-steps R23  # outputs '23'
#   get-steps X23  # outputs '23'
#   get-steps 23   # error
get-steps()
{
    local op="${1}"
    [[ "${op:1}" =~ ^[0-9]+$ ]] && echo "${op:1}" && return 0
    error "Invalid instruction: '${op}'"
    return $ERR_INVALID_VALUE;
}


# Get a new heading from current heading and turn direction
#
#   get-heading N R  # outputs: 'E'
#   get-heading N L  # outputs: 'W'
get-heading()
{
    local heading="$1" direction="$2"

    case "${heading}${direction}" in
        NR) echo E;;
        NL) echo W;;
        SR) echo W;;
        SL) echo E;;
        ER) echo S;;
        EL) echo N;;
        WR) echo N;;
        WL) echo S;;
        *)
            error "Invalid turn: '${heading}${direction}'"
            return $ERR_INVALID_VALUE
            ;;
    esac
}


# Encode coordinates and heading as a comma-separated string
#
#   encode-state 1 -1    # outputs '1,-1'
#   encode-state 1 -1 N  # outputs '1,-1,N'
encode-state()
{
    local IFS=','
    echo "$*"
}


# Get field from encoded state
#
#   get-state 0 a,b,c  # outputs 'b'
#   get-state 1 a,b,c  # outputs 'b'
#   get-state 3 a,b,c  # error
get-state()
{
    local IFS="," idx="$1" string="$2"
    local -a parts
    read -r -a parts <<< "$string"
    [ "${idx}" -ge "${#parts[@]}" ] && return $ERR_INVALID_VALUE
    echo "${parts[$idx]}"
}


# Get encoded position from encoded state
#
#   get-pos x,y    # outputs 'x,y'
#   get-pos x,y,d  # outputs 'x,y'
get-pos()
{
    encode-state "$(get-state 0 "$1")" "$(get-state 1 "$1")"
}


# Get absolute value of a number
#
#   abs -31  # outputs: '31'
abs() {
    echo "${1#-}"
}


# Trim surrounding whitespace from a string
#
#   trim "   foo "  # outputs: 'foo'
trim() {
    local s="$1"
    s="${s#"${s%%[![:space:]]*}"}"
    s="${s%"${s##*[![:space:]]}"}"
    echo "$s"
}


# Calculate shortest distance between two points
#
#  distance 1,-3 -1,1  # outputs: '6'
#  distance 1,-3       # outputs: '4'
distance()
{
    local pos="$1" rel="${2:-0,0}" steps x y dx dy

    x="$(get-state 0 "$rel")"
    y="$(get-state 1 "$rel")"
    dx="$(get-state 0 "$pos")"
    dy="$(get-state 1 "$pos")"
    (( x=x-dx ))
    (( y=y-dy ))
    x="$(abs "$x")"
    y="$(abs "$y")"
    (( steps=x+y ))
    echo "${steps}"
}



# Get a new state from turning
#
#   turn 0,0,N R  # outputs: '0,0,E'
#   turn 0,0,N L  # outputs: '0,0,W'
turn()
{
    local state="$1" direction="$2" x y d newstate

    x="$(get-state 0 "$state")" || return $?
    y="$(get-state 1 "$state")" || return $?
    d="$(get-state 2 "$state")" || return $?
    d="$(get-heading "$d" "$direction")" || return $?

    newstate="$(encode-state "$x" "$y" "$d")"
    debug "turn ${direction}: ${state} -> ${newstate}"
    echo "$newstate"
}



# Get a new state by continuing from the current state
#
#  step 0,0,N   # outputs '0,1,N'
#  step -2,4,E  # outputs '-1,4,E'
step()
{
    local state="$1" x y d

    x="$(get-state 0 "$state")" || return $?
    y="$(get-state 1 "$state")" || return $?
    d="$(get-state 2 "$state")" || return $?

    case "$d" in
        N)  (( y+=1 ));;
        S)  (( y-=1 ));;
        E)  (( x+=1 ));;
        W)  (( x-=1 ));;
        *)
            error "Invalid heading: '${d}'"
            return $ERR_INVALID_VALUE
            ;;
    esac

    encode-state "$x" "$y" "$d"
}


# Get new state for each step when applying an instruction to a given state
#
#   move 0,0,N R1  # outputs '1,0,E\n'
#   move 0,0,N R2  # outputs '1,0,E\n2,0,E\n'
move()
{
    local state="$1" op="$2" direction steps current
    direction="$(get-turn "$op")" || return $?
    steps="$(get-steps "$op")" || return $?

    # Turn in $direction
    current="$(turn "$state" "$direction")" || return $?

    # Move $steps
    for (( i=0; i < steps; i++ ))
    do
        current="$(step "$current")" || return $?
        echo "$current"
    done
    info "move ${op}: ${state} -> ${current}"
}


# Split input strings into instructions
#
#   parse "R1, R2" "R3,R4, "  # outputs 'R1\nR2\nR3\nR4\n'
parse()
{
    local op line IFS=','

    for line in "$@";
    do
        [[ "$line" =~ ^[:space:]*#.* ]] && continue
        for op in $line;
        do
            op="$(trim "$op")"
            [[ "$op" =~ ^$ ]] && continue
            echo "$op"
        done
    done
}


# Split input file into instructions
#
#   parse-file < <(echo -e "R1, R2\nR3,R4, ")  # outputs 'R1\nR2\nR3\nR4\n'
parse-file()
{
    local filename="$1"
    while read -r line
    do
        parse "$line"
    done < "$filename"
}


travel()
{
    local filename="$1" limit="${2:-0}" op current pos cnt steps
    local -a ops
    local -A poscount

    current="$(encode-state 0 0 N)"
    info "max-visits: ${limit}"

    mapfile -t ops < <(parse-file "$filename")
    info "operations: ${#ops[@]}"

    info "start: ${current}"
    for op in "${ops[@]}"
    do
        for current in $( move "$current" "$op" )
        do
            (( steps+=1 ))

            # part 2 calculation
            if [ "$limit" -gt 0 ]
            then
                pos="$(get-pos "$current")"
                cnt="${poscount[$pos]:-0}"
                (( cnt+=1 ))
                poscount+=( ["$pos"]="$cnt" )
                debug visits "$cnt"
                if [ "$cnt" -ge "$limit" ]
                then
                    info "limit ($limit) reached for position '$pos'"
                    break 2
                fi
            fi
        done
        debug "steps: $steps"
    done

    echo "actual: ${steps} steps"
    echo "position: $(get-pos "${current}")"
    echo "shortest: $(distance "$current") steps"
}


if [ -n "$*" ]
then
    travel "$@"
fi
