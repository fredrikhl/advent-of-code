<?php
/**
 *
 *  Advent of Code 2016
 *  Day 3: Squares With Three Sides
 *
 *  http://adventofcode.com/2016/day/3
 */


/**
 * get argv[$i] or $default
 */
function getarg($i, $default = null) {
    global $argv;

    if (!ini_get('register_argc_argv')) {
        throw new Exception("unable to read command line arguments");
    }

    if ((count($argv) - 1) < $i) {
        return $default;
    }
    return $argv[$i];
}


/**
 * Parse an input file with numbers into an array of arrays.
 *
 * Each array in the return value *should* contain three lengths, one for each
 * side in a triangle. If the file is properly formatted...
 */
function parse_file($filename) {
    $content = file_get_contents($filename);



    if ($content === false) {
        throw new Exception("Unable to read file");
    }

    $split = function ($r, $c) {
        return preg_split($r, trim($c), null, PREG_SPLIT_NO_EMPTY);
    };

    $rows = array();

    foreach ($split('/\s*\R\s*/', $content) as $line) {
        $rows[] = $split('/\s+/', $line);
    }
    return $rows;
}


/**
 * Flips a 2-dimensional array into row-length chunks of columns.
 */
function flip(array $rows) {
    $new = array();
    $offset = count($rows);
    foreach ($rows as $idx => $row) {
        foreach ($row as $i => $value) {
            $new[($offset * $i) + $idx] = $value;
        }
    }
    ksort($new);
    return array_chunk($new, 3);
}


/**
 * Count number of valid triangle values in an array of triangle values.
 */
function count_valid(array $rows) {
    $valid = function($a, $b, $c) {
        $longest = max($a, $b, $c);
        $rest = $a + $b + $c - $longest;
        return $longest < $rest;
    };
    $valid_cnt = 0;
    foreach ($rows as $row) {
        if (call_user_func_array($valid, $row)) {
            $valid_cnt += 1;
        }
    }
    return $valid_cnt;
}


function main() {
    $content = parse_file(getarg(1, 'php://stdin'));

    $pt1 = count_valid($content);
    echo "Part 1, {$pt1}\n";

    $pt2 = count_valid(flip($content));
    echo "Part 2, {$pt2}\n";
}

main();
