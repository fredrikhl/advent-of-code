//! Advent of Code 2016, Day 6: Signals and Noise.
//!
//! Provides a solution to the AoC problem.
use std::env;
use std::error::Error;
use std::fs;

use crate::matrix::TextMatrix;
use crate::letters::LetterCount;
mod matrix;
mod letters;


fn main() -> Result<(), Box<dyn Error>> {
    let args: Vec<String> = env::args().collect();
    let usage = format!("Usage: {} <filename>", args[0]);
    let filename = &args.get(1).ok_or(usage)?;

    let content = fs::read_to_string(filename)?;
    let matrix = TextMatrix::from_text(&content).transpose();

    let mut most_common = String::with_capacity(matrix.nrows());
    let mut least_common = String::with_capacity(matrix.nrows());
    for text in matrix.get_text_rows() {
        let letters = LetterCount::new(&text);
        if let Some(ch) = letters.most_common() {
            most_common.push(ch);
        }
        if let Some(ch) = letters.least_common() {
            least_common.push(ch);
        }
    }
    println!("Part 1: {:}", &most_common);
    println!("Part 2: {:}", &least_common);
    Ok(())
}
