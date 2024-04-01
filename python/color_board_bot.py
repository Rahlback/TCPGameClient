from random import randint
from random import shuffle
from color_bot_base import ColorBotBase

class ColorBot(ColorBotBase):
    def calculate_next_move(self):
        print("------------------------")
        print(self.player_number, ": ", self.positions[self.player_number])

        valid_moves = self.get_valid_moves()
        shuffle(valid_moves)
        rand_move = valid_moves[randint(0, len(valid_moves)-1)]
        if not self.has_moved():
            print("         Sending random move: first. valid_moves= ", valid_moves, ". has_moved()=", self.has_moved())
            return self.translate_move_list_to_char(rand_move)
        

        for move in valid_moves:
            next_pos = self.positions[self.player_number].copy()
            next_pos[0] += move[0]
            next_pos[1] += move[1]
            print("Testing ", move, ". Next_pos = ", next_pos)

            if self.map[next_pos[1]][next_pos[0]] != str(self.player_number):
                print("Found non-self tile: ", next_pos)
                return self.translate_move_list_to_char(move)
            if self.map[next_pos[1]][next_pos[0]] == ' ':
                return self.translate_move_list_to_char(move)
        
        print("         Sending random move: second")
        return self.translate_move_list_to_char(rand_move)
        