use std::collections::HashMap;

pub struct Board {
    pub map: Vec<Vec<u8>>, // Walls = 255, white tiles = 254
    pub positions: HashMap<u8, (u8, u8)>
    
}