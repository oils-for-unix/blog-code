use std::env;
use std::fs;
use std::path::Path;
use std::path::PathBuf;
use std::error::Error;

fn find_deepest_directory(path: &Path, deepest: &mut Option<PathBuf>) {
    if let Ok(entries) = fs::read_dir(path) {
        for entry in entries.flatten() {
            if let Ok(metadata) = entry.metadata() {
                if metadata.is_dir() {
                    let entry_path = entry.path();
                    if deepest.is_none() || entry_path.components().count() > deepest.as_ref().unwrap().components().count() {
                        *deepest = Some(entry_path.clone());
                    }
                    find_deepest_directory(&entry_path, deepest);
                }
            }
        }
    }
}

fn load_shell_environment(dir: &Path) -> Result<(), Box<dyn Error>> {
    // Get the $SHELL
    let shell = std::env::var("SHELL")?;

    // Construct the command we want the $SHELL to execute
    let command = format!("cd {:?}; /usr/bin/env -0;", dir);

    println!("Command {}", command);
    println!("");

    // Launch the $SHELL as an interactive shell (so the user's rc files are used)
    // and execute `command`:
    let output = std::process::Command::new(&shell)
        .args(["-i", "-c", &command])
        .output()?;

    println!("Shell output {:?}", output);
    println!("");

    return Ok(());
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let root_dir = Path::new(&args[1]);

    let mut deepest_directory: Option<PathBuf> = None;
    find_deepest_directory(&root_dir, &mut deepest_directory);

    match deepest_directory {
        Some(path) => {
        println!("Deepest directory: {}", path.display());
            let _ = load_shell_environment(Path::new(&path));
            println!("");
            println!("I printed your environ, from your interactive shell.  What else did I do?");
        }
        None => println!("No directory found"),
    }
}

