use std::collections::HashMap;

use super::color_board_bot::custom_data;

pub const WALL: u8 = 255;
pub const WHITE_TILE: u8 = 254;

/**
This struct contains all parameters for a board.

*/
pub struct Board {
    ///  Walls = 255, white tiles = 254 
    pub map: Vec<Vec<u8>>,
    /// Contains all the players postions on the board, including your own
    /// {player number: (x, y)}. Example: positions\[1\] => [(1, 5)]
    pub positions: HashMap<u8, (u8, u8)>, 
    /// Your own player number. Use this in conjuction with positions to get your position on the board
    pub player_number: u8,

    pub player_data: custom_data
}

impl Board {
    pub fn new(map: Vec<Vec<u8>>, positions: HashMap<u8, (u8, u8)>, player_number: u8) -> Self {
        Self { map, positions, player_number, player_data: custom_data::new() }
    }
    
    pub fn print_map(&self) {
        let mut s: String = String::new();
        println!("{:?}", self.map);
        
        for _ in 0..self.map[0].len() {
            print!("-");
        }
        println!();
        for row in &self.map {
            for col in row {
                match col.clone() {
                    WALL => s.push('#'),
                    WHITE_TILE => s.push(' '),
                    _ => s = format!("{}{}", s, col)
                }
            }
            s.push('\n');
        }
        s.remove(s.len()-1);
        println!("{}", s);
        for _ in 0..self.map[0].len() {
            print!("-");
        }
        println!();
    }
}