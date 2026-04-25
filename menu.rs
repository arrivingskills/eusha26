// `use` brings items into scope. The curly braces `{self, Write}` import
// multiple items from the same module in one line:
//   - `self` refers to the `io` module itself (so we can write `io::stdin()`)
//   - `Write` is a trait that provides the `.flush()` method for output streams
use std::io::{self, Write};
// `Command` is a struct for spawning and configuring external processes.
use std::process::Command;

// `fn main()` defines the program's entry point. Every Rust program starts here.
fn main() {
    // `loop` creates an infinite loop. It runs forever until a `break` statement
    // is reached. This keeps the menu showing after each command.
    loop {
        // `println!` is a macro (the `!` marks it as a macro, not a regular function).
        // Macros are expanded at compile time. `\n` is an escape sequence for a newline.
        println!("\n===== Command Menu =====");
        println!("1. List files (ls -la)");
        println!("2. Show current directory (pwd)");
        println!("3. Show disk usage (df -h)");
        println!("4. Show memory usage (free -h)");
        println!("5. Show running processes (ps aux)");
        println!("6. Show date and time (date)");
        println!("7. Show system info (uname -a)");
        println!("8. Show network interfaces (ip addr)");
        println!("9. Quit");
        // `print!` is like `println!` but without a trailing newline, so the
        // cursor stays on the same line for the user to type their input.
        print!("\nEnter your choice: ");
        // `io::stdout()` gets a handle to standard output. `.flush()` forces
        // any buffered output to be written immediately. Without this, the
        // `print!` text might not appear before waiting for input.
        // `.expect()` unwraps the `Result` — if flushing fails, the program
        // panics with the given message.
        io::stdout().flush().expect("Failed to flush stdout");

        // `let` declares a variable. `mut` makes it mutable (changeable).
        // Without `mut`, Rust variables are immutable by default.
        // `String::new()` creates a new empty `String` on the heap.
        let mut choice = String::new();
        // `io::stdin()` returns a handle to standard input.
        // `.read_line(&mut choice)` reads a line into `choice`.
        //   - `&mut` creates a mutable reference, letting `read_line` modify
        //     `choice` without taking ownership of it.
        // `.expect()` handles the `Result` — panics with the message on error.
        io::stdin()
            .read_line(&mut choice)
            .expect("Failed to read input");

        // `match` is Rust's pattern matching — like a switch statement but more
        // powerful. It must handle every possible case (exhaustive matching).
        // `.trim()` removes leading/trailing whitespace (including the newline
        // from pressing Enter).
        // Each arm uses `=>` to map a pattern to an expression.
        // The result is a tuple `(&str, Vec<&str>)`:
        //   - `("ls", vec!["-la"])` is a tuple with a string slice and a `Vec`
        //   - `vec!` is a macro that creates a `Vec` (growable array) with the
        //     given elements
        let command = match choice.trim() {
            "1" => ("ls", vec!["-la"]),
            "2" => ("pwd", vec![]),
            "3" => ("df", vec!["-h"]),
            "4" => ("free", vec!["-h"]),
            "5" => ("ps", vec!["aux"]),
            "6" => ("date", vec![]),
            "7" => ("uname", vec!["-a"]),
            "8" => ("ip", vec!["addr"]),
            "9" => {
                // Curly braces `{}` create a block expression. This arm runs
                // multiple statements before using `break` to exit the `loop`.
                println!("Goodbye!");
                break;
            }
            // `_` is the wildcard/catch-all pattern — it matches anything not
            // already matched above. `continue` skips back to the top of the loop.
            _ => {
                println!("Invalid choice, please try again.");
                continue;
            }
        };

        println!("\n--- Output ---");
        // `Command::new(...)` creates a new process builder for the given program.
        // `command.0` and `command.1` access the first and second elements of the
        // tuple using dot syntax with positional indices.
        // `.args(...)` adds command-line arguments. `&command.1` borrows the Vec.
        // `.output()` runs the command and captures its stdout, stderr, and exit status.
        // It returns `Result<Output, io::Error>` — either success or an error.
        let output = Command::new(command.0)
            .args(&command.1)
            .output();

        // `match` on the `Result` to handle success (`Ok`) and failure (`Err`).
        // `Ok(result)` destructures the Ok variant, binding the inner value to `result`.
        // `Err(e)` destructures the Err variant, binding the error to `e`.
        match output {
            Ok(result) => {
                // `String::from_utf8_lossy()` converts bytes to a string, replacing
                // any invalid UTF-8 with the replacement character (�).
                // `result.stdout` is a `Vec<u8>` containing the command's output bytes.
                // `{}` in the format string is a placeholder that calls `.to_string()`
                // on the argument.
                print!("{}", String::from_utf8_lossy(&result.stdout));
                let stderr = String::from_utf8_lossy(&result.stderr);
                // `.is_empty()` returns `true` if the string has zero length.
                if !stderr.is_empty() {
                    // `eprint!` prints to stderr instead of stdout.
                    // `{stderr}` is inline format syntax — the variable name goes
                    // directly inside the braces.
                    eprint!("{stderr}");
                }
            }
            // `eprintln!` prints to stderr with a trailing newline.
            // `{e}` formats the error using its `Display` implementation.
            Err(e) => eprintln!("Failed to run command: {e}"),
        }
    }
}


// Ownership
// fn print_len(s: String) { println!("{}", s.len()); }
// let s = String::from("hello");
// print_len(s);
// // s is GONE here — it was moved into the function

// fn print_len(s: &String) { println!("{}", s.len()); }
// let s = String::from("hello");
// print_len(&s);
// // s is still usable here