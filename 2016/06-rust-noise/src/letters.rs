//! Letter counter
//!
//! Provides a struct that can find the most common and least common char in a given string.
use std::collections::HashMap;


/// A letter count
pub struct LetterCount {
    letters: HashMap<char, usize>,
}

impl LetterCount {

    /// Create a new letter count from a string.
    pub fn new(text: &str) -> Self {
        let mut letters: HashMap<char, usize> = HashMap::new();
        for ch in text.chars() {
            letters.entry(ch)
                .and_modify(|count| *count += 1)
                .or_insert(1);
        }
        Self { letters }
    }

    /// Get the most common character.
    ///
    /// Any tie-break will return the char with the lowest code point.
    pub fn most_common(&self) -> Option<char> {
        self.letters.iter()
            .max_by(|a, b| a.1.cmp(&b.1).then(b.0.cmp(&a.0)))
            .map(|entry| *entry.0)
    }

    /// Get the least common character.
    ///
    /// Any tie-break will return the char with the lowest code point.
    pub fn least_common(&self) -> Option<char> {
        self.letters.iter()
            .min_by(|a, b| a.1.cmp(&b.1).then(a.0.cmp(&b.0)))
            .map(|entry| *entry.0)
    }
}


#[cfg(test)]
mod tests {

    #[test]
    fn most_common() {
        let letters = super::LetterCount::new("hello");
        let winner = letters.most_common();
        assert_eq!(winner, Some('l'));
    }

    #[test]
    fn most_common_empty() {
        let letters = super::LetterCount::new("");
        let winner = letters.most_common();
        assert_eq!(winner, None);
    }

    #[test]
    fn most_common_tie_first() {
        let letters = super::LetterCount::new("ab");
        let winner = letters.most_common();
        assert_eq!(winner, Some('a'));
    }

    #[test]
    fn most_common_tie_not_first() {
        let letters = super::LetterCount::new("ba");
        let winner = letters.most_common();
        assert_eq!(winner, Some('a'));
    }

    #[test]
    fn least_common() {
        let letters = super::LetterCount::new("abcba");
        let winner = letters.least_common();
        assert_eq!(winner, Some('c'));
    }

    #[test]
    fn least_common_empty() {
        let letters = super::LetterCount::new("");
        let winner = letters.least_common();
        assert_eq!(winner, None);
    }

    #[test]
    fn least_common_tie_first() {
        let letters = super::LetterCount::new("ab");
        let winner = letters.least_common();
        assert_eq!(winner, Some('a'));
    }

    #[test]
    fn least_common_tie_not_first() {
        let letters = super::LetterCount::new("ba");
        let winner = letters.least_common();
        assert_eq!(winner, Some('a'));
    }
}
