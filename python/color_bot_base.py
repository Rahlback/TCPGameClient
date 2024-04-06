class ColorBotBase:
    def __init__(self, board_map, player_positions={}) -> None:
        self.map = board_map # [ [], [], [], ...]
        self.positions = player_positions # Name: [x, y]
        self.prev_positions = {}
        self.player_number = 0

    
    def has_moved(self):
        """ Returns true if the bots current position is different than the bots previous position.
        Else returns false.
        """
        if not self.prev_positions:
            return True
        # print(" ", self.prev_positions)
        # print(" ", self.positions)
        return self.prev_positions[self.player_number] != self.positions[self.player_number]
    
    def update_player_positions(self, player_positions):
        # print(" before: ", self.positions)
        for key in self.positions:
            self.prev_positions[key] = self.positions[key].copy()

        self.positions = player_positions.copy()
        # print("update_palyer_positions: ", player_positions)
        # print(" self.positions=", self.positions)
        # print(" self.prev_positions=", self.prev_positions)
        for name in self.positions:
            pos = self.positions[name]
            self.map[pos[1]][pos[0]] = str(name)
    
    def set_player_number(self, player_number):
        self.player_number = player_number

    def print_board_info(self):
        print("Player number: ", self.player_number)
        print("Positions: ", self.positions)
    
    def print_map(self):
        for row in self.map:
            print(row)

    def get_valid_moves(self):
        """ Returns possible moves that doesn't end up in a wall or out of bounds.
        """

        moves = [
            [-1, 0], [0, -1], [1, 0], [0, 1]
        ]
        valid_moves = []

        current_pos = self.positions[self.player_number]

        for move in moves:
            next_pos = [move[0] + current_pos[0], move[1] + current_pos[1]]
            
            if next_pos[0] < 0 or next_pos[0] >= len(self.map[0]):
                continue
            if next_pos[1] < 0 or next_pos[1] >= len(self.map):
                continue
            if self.map[next_pos[1]][next_pos[0]] == '#':
                continue
            valid_moves.append(move)

        return valid_moves

    def translate_move_list_to_char(self, move):
        """ move = 
        [1, 0] -> 'R'
        [-1, 0]-> 'L'
        [0, -1]-> 'U'
        [0, 1] -> 'D'
        """
        match move:
            case [1, 0]:
                return 'R'
            case [-1, 0]:
                return 'L'
            case [0, -1]:
                return 'U'
            case [0, 1]:
                return 'D'

    def calculate_next_move(self):
        pass