use std::collections::HashMap;

pub const WALL: u8 = 255;
pub const WHITE_TILE: u8 = 254;

pub struct Board {
    pub map: Vec<Vec<u8>>, // Walls = 255, white tiles = 254
    pub positions: HashMap<u8, (u8, u8)>
}


impl Board {
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