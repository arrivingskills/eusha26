// Bring the `io` (input/output) library from the standard library into scope.
// This is needed to read user input from the terminal.
use std::io;

// `main` is the entry point of every Rust program.
fn main() {
    // `println!` is a macro (indicated by the `!`) that prints text to the console,
    // followed by a newline.
    println!("Guess the number!");

    println!("Please input your guess.");

    // `let` declares a new variable. By default, variables in Rust are immutable,
    // so `mut` is required to allow `guess` to be changed later.
    // `String::new()` creates a new, empty growable UTF-8 string.
    let mut guess = String::new();

    // `io::stdin()` returns a handle to the standard input stream.
    // `.read_line(&mut guess)` reads a line of input and appends it to `guess`.
    // `&mut guess` passes a mutable reference so `read_line` can modify the string.
    // `.expect(...)` handles the `Result` returned by `read_line` —
    // if it's an `Err`, the program will panic with the given message.
    io::stdin()
        .read_line(&mut guess)
        .expect("Failed to read line");

    // `{guess}` inside the string is Rust's inline format syntax,
    // which inserts the value of `guess` directly into the output.
    println!("You guessed: {guess}");
}
