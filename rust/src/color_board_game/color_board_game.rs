// use std::{error::Error, net::TcpStream};

use std::{collections::HashMap, thread::sleep, time};

use crate::{client::{self, tcp_client::TCPClient}, color_board_game::parameters};
use rand::{self, Rng};

use super::board::Board;

pub struct ColorBoardGame {
    // Connect TCPClient
    // Register with server
    // 
    tcp_client: TCPClient,
    boards: Vec<Board>
}


fn deserialize_boards(serialized_boards: Vec<u8>) -> Result<Vec<Board>, &'static str> {
    let mut boards: Vec<Board> = vec![];
    let mut number_of_boards = 0;
    for x in &serialized_boards[0..4] {
        number_of_boards <<= 8;
        number_of_boards += usize::from(x.clone());
    }

    // println!("Number of boards = {}", &number_of_boards);
    for _ in 0..number_of_boards {
        game_client.boards.push(Board{map: vec![], positions: HashMap::new()});
    }

    return Err("NOPE");
}

fn setup_game(game_client: &mut ColorBoardGame) {
    
    // Get serialized boards
    let serialized_boards = game_client.tcp_client.get_message();
    println!("Serialized boards: {:?}", serialized_boards);





    // Player positional data
    let serialized_positional_data = game_client.tcp_client.get_message();

    // Player number
    let player_number = game_client.tcp_client.get_message();
}

fn game_tick(game_client: &mut ColorBoardGame) -> bool {
    let message = game_client.tcp_client.get_message();
    if message.is_empty() { // Connection to server is probably broken.
        return false;
    }
    

    let moves = vec!["U", "D","L","R"];

    // HEARTBEAT
    if message == [72, 69, 65, 82, 84, 66, 69, 65, 84] {
        println!("Heartbeat message received!");
    }

    // GAME_STARTING
    else if message == [71, 65, 77, 69, 95, 83, 84, 65, 82, 84, 73, 78, 71] { 
        // Hand over control to board builder
        println!("Received GAME_STARTING. Setting up game!");
        game_client.boards.clear();
        setup_game(game_client);
    }

    // SETUP_COMPLETE_SEND_MOVES
    else if message == [83, 69, 84, 85, 80, 95, 67, 79, 77, 80, 76, 69, 84, 69, 95, 83, 69, 78, 68, 95, 77, 79, 86, 69, 83] {
        // Send first move
        // let moves = vec!["U", "D","L","R"];
        let mut player_move: String = "".to_string();
        for _ in 0..game_client.boards.len() {
            let mut rng = rand::thread_rng();
            let pick_move = rng.gen_range(0..moves.len());

            player_move += moves[pick_move];
        }
        game_client.tcp_client.send_message(player_move.to_string());
    }
    
    // Resend move
    else if message == [82, 69, 83, 69, 78, 68, 95, 77, 79, 86, 69] {
        let mut player_move: String = "".to_string();
        for _ in 0..game_client.boards.len() {
            let mut rng = rand::thread_rng();
            let pick_move = rng.gen_range(0..moves.len());

            player_move += moves[pick_move];
        }
        let res = game_client.tcp_client.send_message(player_move.to_string());
        if res.is_err() {
            println!("Error: {}", res.err().unwrap().to_string());
        }
    }
    else {
        // Send move
        let mut player_move: String = "".to_string();
        for _ in 0..game_client.boards.len() {
            let mut rng = rand::thread_rng();
            let pick_move = rng.gen_range(0..moves.len());

            player_move += moves[pick_move];
        }
        let res = game_client.tcp_client.send_message(player_move.to_string());
        if res.is_err() {
            println!("Error: {}", res.err().unwrap().to_string());
        }
    }

    if message.is_ascii() {
        //println!("Message = {} <-- {:?}", String::from_utf8(message.clone()).unwrap(), message.clone());
    }


    // println!("{:?}", message);
    return true;
}

pub fn game_loop(mut game_clients: Vec<ColorBoardGame>) {
    loop {
        let sleep_duration = time::Duration::from_millis(1);
        // sleep(sleep_duration);
        for client in &mut game_clients {
            if !game_tick(client) {
                return;
            }
        }

    }
}

pub fn run_game() {

    let mut game_clients: Vec<ColorBoardGame> = vec![];

    let mut user_id = parameters::USER_ID;
    let mut rng = rand::thread_rng();
    if user_id < 100 {
        user_id = rng.gen_range(100..2147413647);
    }
    for _ in 0..parameters::NUMBER_OF_PLAYERS {
        let game_client_r = client::tcp_client::connect_to_server(parameters::SERVER_IP, parameters::PORT);

        if game_client_r.is_err() {
            match game_client_r.err() {
                Some(s) => println!("{}", s),
                None => println!("Unknown error occured")
            }
            println!("Exiting");
            return;
        }

        let mut game_client = game_client_r.unwrap();
        // game_client.set_no_delay(true);
    
        game_client.register(parameters::USER_NAME, user_id,parameters::BIG_ENDIAN);
        let color_board_game_client = ColorBoardGame{tcp_client: game_client, boards: vec![]};
        game_clients.push(color_board_game_client);
        user_id += 100;
    }


    game_loop(game_clients);
}