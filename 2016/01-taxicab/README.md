# Advent of Code 2016, day 1

Day 1: [No Time for a Taxicab](https://adventofcode.com/2016/day/1)

Solution in Bash (v4 or newer), with unit tests for bats.


## Part 1

```bash
bash shortest.bash input.txt
# actual: 913 steps
# position: 136,-151
# shortest: 287 steps
```


## Part 2

```bash
bash shortest.bash input.txt 2
# actual: 489 steps
# position: -14,-119
# shortest: 133 steps
```


## Tests

```bash
bats tests.bats
```
