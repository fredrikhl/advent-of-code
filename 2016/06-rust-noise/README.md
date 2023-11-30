# Advent of Code 2016, day 6

Day 6: [Signals and Noise](https://adventofcode.com/2016/day/6)

Solution in Rust.


## Libraries

The solution uses three 3rd party libraries:

- ``log`` - to log debug messages, useful for debugging

- ``stderrlog`` - for writing log messages to stderr

- ``clap`` - for parsing cli arguments - could probably do with
  ``env::args()``, but this is nicer.


## Usage

```bash
# TODO
cargo run <input-file-maybe?>  # whatever
```


## Run

```bash
cargo run example.txt
cargo run input.txt
```


## Tests

```bash
cargo test
```
