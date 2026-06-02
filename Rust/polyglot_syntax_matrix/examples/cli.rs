//! Example: CLI for polyglot_syntax_matrix

use polyglot_syntax_matrix::SyntaxMatrix;

fn main() {
    let matrix = SyntaxMatrix::new();

    println!("{}", matrix.generate_report());
}