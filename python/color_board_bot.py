from random import randint
class ColorBot:
    @staticmethod 
    def calculate_next_move(board, self_position, player_positions):
        possible_moves = ['R', 'L', 'U', 'D']
        return possible_moves[randint(0, 3)]
