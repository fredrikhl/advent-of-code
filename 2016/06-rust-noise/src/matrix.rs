//! Text matrix
//!
//! Provides a struct can can represent a string as rows of lines, and columns of characters.
use std::collections::HashMap;


/// A matrix to represent text lines as rows, and char positions as columns.
pub struct TextMatrix {
    values: HashMap<(usize, usize), char>,
}

impl TextMatrix {

    /// Create a new, empty matrix
    fn new() -> Self {
        Self {
            values: HashMap::new(),
        }
    }

    /// Create matrix with rows from text lines
    pub fn from_text(text: &str) -> Self {
        let mut matrix = Self::new();
        for (row, line) in text.lines().enumerate() {
            for (col, ch) in line.chars().enumerate() {
                matrix.values.insert((row, col), ch);
            }
        }
        return matrix;
    }

    /// Number of rows in matrix.
    pub fn nrows(&self) -> usize {
        self.values.keys()
            .max_by(|a, b| a.0.cmp(&b.0)).map(|k| k.0 + 1)
            .unwrap_or_default()
    }

    /// Number of columns in matrix.
    pub fn ncols(&self) -> usize {
        self.values.keys()
            .max_by(|a, b| a.1.cmp(&b.1)).map(|k| k.1 + 1)
            .unwrap_or_default()
    }

    /// Get a transposed copy of this matrix
    pub fn transpose(&self) -> Self {
        let mut values: HashMap<(usize, usize), char> = HashMap::with_capacity(self.values.len());
        for (key, value) in self.values.iter() {
            let (row, col) = *key;
            values.insert((col, row), *value);
        }
        Self {values}
    }

    /// Get each row as a String
    pub fn get_text_rows(&self) -> Vec<String> {
        let rows = self.nrows();
        let cols = self.ncols();
        // TODO: Could probably be done as an iterator
        let mut lines: Vec<String> = Vec::with_capacity(rows);
        for row in 0..rows {
            let mut chars = String::with_capacity(cols);
            for col in 0..cols {
                // TODO: Could probably use BTreeMap and iterate over sorted keys, rather than
                //       checking evey possible row,col combination that *might* exist.
                match self.values.get(&(row, col)) {
                    Some(ch) => chars.push(*ch),
                    None => continue,
                }
            }
            lines.push(chars);
        }
        return lines;
    }
}


#[cfg(test)]
mod tests {

    #[test]
    fn row_count() {
        let m = super::TextMatrix::from_text("hello\nworld");
        let rows = m.nrows();
        assert_eq!(rows, 2);
    }

    #[test]
    fn row_count_empty() {
        let m = super::TextMatrix::from_text("");
        let rows = m.nrows();
        assert_eq!(rows, 0);
    }

    #[test]
    fn col_count() {
        let m = super::TextMatrix::from_text("hello\nworld");
        let rows = m.ncols();
        assert_eq!(rows, 5);
    }

    #[test]
    fn get_text_rows() {
        let m = super::TextMatrix::from_text("hello\nworld");
        let lines = m.get_text_rows();
        assert_eq!(lines.len(), 2);
        assert_eq!(lines[0], "hello");
    }

    #[test]
    fn transpose() {
        let m = super::TextMatrix::from_text("hello\nworld").transpose();
        assert_eq!(m.nrows(), 5);
        assert_eq!(m.ncols(), 2);
        let lines = m.get_text_rows();
        assert_eq!(lines.len(), 5);
        assert_eq!(lines[0], "hw");
        assert_eq!(lines[1], "eo");
    }
}
