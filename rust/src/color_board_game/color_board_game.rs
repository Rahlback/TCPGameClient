use std::{error::Error, net::TcpStream};

use crate::{client::{self, tcp_client::TCPClient}, color_board_game::parameters};
use rand::{self, Rng};

pub struct ColorBoardGame {
    // Connect TCPClient
    // Register with server
    // 
}

fn game_tick(game_client: &mut TCPClient) -> bool {
    let message = game_client.get_message();
    if message.is_empty() { // Connection to server is probably broken.
        return false;
    }
    
    // HEARTBEAT
    if message == [72, 69, 65, 82, 84, 66, 69, 65, 84] {
        println!("Heartbeat message received!");
    }

    // GAME_STARTING
    else if message == [71, 65, 77, 69, 95, 83, 84, 65, 82, 84, 73, 78, 71] { 
        // Hand over control to board builder
    }

    // SETUP_COMPLETE_SEND_MOVES
    else if message == [83, 69, 84, 85, 80, 95, 67, 79, 77, 80, 76, 69, 84, 69, 95, 83, 69, 78, 68, 95, 77, 79, 86, 69, 83] {
        // Send first move
    }

    else {
        // Send move
    }

    if message.is_ascii() {
        println!("{}", String::from_utf8(message.clone()).unwrap());
    }


    println!("{:?}", message);
    return true;
}

pub fn game_loop(mut game_clients: Vec<TCPClient>) {
    loop {
        for mut client in &mut game_clients {
            if !game_tick(client) {
                return;
            }
        }

    }
}

pub fn run_game() {

    let mut game_clients: Vec<TCPClient> = vec![];

    for _ in 0..parameters::NUMBER_OF_PLAYERS {
        let mut game_client = client::tcp_client::connect_to_server(parameters::SERVER_IP, parameters::PORT);
        let mut user_id = parameters::USER_ID;
        if user_id < 100 {
            let mut rng = rand::thread_rng();
            user_id = rng.gen_range(100..2147483647);
        }
    
        game_client.register(parameters::USER_NAME, user_id,parameters::BIG_ENDIAN);
        game_clients.push(game_client);
    }


    game_loop(game_clients);
}