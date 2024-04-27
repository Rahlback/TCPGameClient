use std::collections::HashMap;

use rand::Rng;

use super::board::Board;

/// Modify this struct to contain any data you want to save.
/// Adding a field of data in this struct requires you to also update the "impl custom_data::new() function"
pub struct custom_data {
    num_of_moves: u16,
    prev_positions: HashMap<u8, (u8, u8)>, 

}

impl custom_data {
    pub fn new() -> Self {
        Self { num_of_moves: 0, prev_positions: HashMap::new()}
    }
}

impl Board {

    fn get_pos(&self) -> (u8, u8) {
        self.positions[&self.player_number]
    }

    fn get_prev_pos(&self) -> Option<(u8, u8)> {
        match self.player_data.prev_positions.is_empty() {
            false => Some(self.player_data.prev_positions[&self.player_number]),
            true => None
        }
    }

    pub fn calculate_next_move(&mut self) -> &'static str {
        if self.get_prev_pos().is_some() && self.get_pos() == self.get_prev_pos().unwrap() {
            // We didn't move since the last frame
            // println!("Calculate_next_move: Haven't moved since last frame!");
        }
        self.player_data.prev_positions = self.positions.clone();

        let moves = vec!["U", "D","L","R"];

        let mut rng = rand::thread_rng();
        let pick_move = rng.gen_range(0..moves.len());
        return moves[pick_move];
    }
}