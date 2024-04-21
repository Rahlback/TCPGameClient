
mod client;

fn main() {
    println!("Hello, world!");
    let mut x = client::tcp_client::connect_to_server("localhost", "9079");
    x.register("Rust", 200, 1);
    let message = x.get_message();
    println!("{:?}", message);
}
