//! RS-CAN-PROJ-018: Result-returning main demonstrating Termination.

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("result main");
    Ok(())
}
