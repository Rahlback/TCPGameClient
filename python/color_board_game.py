from yaml import safe_load
from tcp_client import TCPClient
from time import sleep
from math import ceil
from random import randint
from color_board_bot import ColorBot

bytes_per_player_position = 3

class BoardGame:
    def __init__(self, user_id, name="name", server_ip="127.0.0.1", server_port=9080) -> None:
        self.state = 0
        self.boards = []

        self.prev_move = ""

        self.client = TCPClient(user_id)
        user_name = name # + "-" + str(user_id)
        self.client.setup_connection(user_id, user_name, server_ip, server_port)

        # Wait until board game starts?
        # self.client.get_message()
    

    def deserialize_boards(self, serialized_boards) -> list:
        """Deserializes the boards received from the game server.
        The serialized data is of the form:
            4 bytes = number of boards
                block of board [
                    2 bytes = width, gives the number of bits needed for each row
                        'bytes_per_row' = ceil(width / 8)
                    2 bytes = height, number of blocks that will follow
                    
                    block of row [
                        bytes_per_row bytes = row_data, data in bytes. 
                                             0x0ff0 -> [0x0f, 0xf0]. (Needs to be reversed during assembly)
                    ]
                    
            ]
        """
        boards = []
        number_of_boards = 0
        for x in range(0, 4):
            number_of_boards <<= 8
            number_of_boards += serialized_boards[x]
        print("Number of boards: ", number_of_boards)

        byte_index = 4
        for board_i in range(0, number_of_boards):
            board = []
            width = serialized_boards[byte_index] << 8 
            width += serialized_boards[byte_index + 1]
            bytes_per_row = ceil(width / 8)
            print("Bytes per row: ", bytes_per_row)

            byte_index += 2
            height = serialized_boards[byte_index] << 8
            height += serialized_boards[byte_index + 1]
            print("Height: ", height)

            byte_index += 2

            for row in range(0, height):
                board_row_data = list(serialized_boards[byte_index:byte_index+bytes_per_row])
                board_row_data = board_row_data.reverse()
                board_row = []

                row_data = 0
                for byte in range(bytes_per_row):
                    row_data += (serialized_boards[byte_index] << (8 * byte))
                    byte_index += 1
        
                for col in range(0, width):
                    # print(col)
                    if ((row_data & (1 << col)) > 0):
                        board_row.append("#")
                    else:
                        board_row.append(" ")
                board.append(board_row)

            boards.append(board)
        # for b in boards:
        #     for row in b:
        #         print(row)
        #     print("------")
        return boards
        
    def deserialize_player_positions_and_update_boards(self, serialized_positions):
        total_bytes_expected = bytes_per_player_position * 4 * len(self.boards)
        if len(serialized_positions) != total_bytes_expected:
            print("Missing bytes for player positions: ",
                   len(serialized_positions), " ", total_bytes_expected)
        
        offset = 0
        for board in self.boards:
            # [1, x, y, 2, x, y, 3, x, y, 4, x, y]
            board_data = serialized_positions[offset:offset+12]
            player_positions = {}
            player_offset = 0
            for player_pos in range(4):
                player_positions[player_pos+1] = [board_data[player_offset+1], board_data[player_offset+2]]
                player_offset += 3
            
            board.update_player_positions(player_positions)
            offset += 12
            


    def setup_game(self):
        self.boards.clear()
        print("Start game received. Waiting for boards")
        board_buffer = self.client.get_message()
        temp_boards = self.deserialize_boards(board_buffer)
        for board in temp_boards:
            new_board_obj = ColorBot(board)
            self.boards.append(new_board_obj)
        
        print("Waiting for player positions")
        player_positions_buffer = list(self.client.get_message())
        self.deserialize_player_positions_and_update_boards(player_positions_buffer)
        print(len(player_positions_buffer), player_positions_buffer)

        print("Waiting for my player number")
        player_number = list(self.client.get_message())
        for board in self.boards:
            board.set_player_number(player_number[0])
            board.print_board_info()
        sleep(0.001)
        self.state = 1

    def send_moves(self):
        possible_moves = ['R', 'L', 'U', 'D']
        number_of_boards = len(self.boards)
        move_string = ""
        board: ColorBot
        for board in self.boards:
            move_string += str(board.calculate_next_move())

        # print("Sending " + move_string)
        self.client.send(move_string)
        self.prev_move = move_string

    def tick(self):
        data_buffer = self.client.get_message()
        if bytearray("GAME_STARTING", "ASCII") == data_buffer[0:13]:
            self.setup_game()
        elif bytearray("GAME_OVER", "ASCII") == data_buffer[0:9]:
            print("All games are now over. Expect a new GAME_STARTING to begin")
        elif bytearray("SEND_MOVES", "ASCII") == data_buffer[0:10] \
            or bytearray("SETUP_COMPLETE_SEND_MOVES", "ASCII") == data_buffer[0:25]:
            # print("Send moves received. Sending moves")
            self.send_moves()

        elif bytearray("RESEND_MOVE", "ASCII") == data_buffer[0:11]:
            print("Got RESEND_MOVE.", " resending: ", self.prev_move)
            # self.client.send(self.prev_move)
            self.client.send(self.prev_move)
            # sleep(10)
        elif bytearray("HEARTBEAT", "ASCII") == data_buffer[0:9]:
            # We just need to pass the time
            print("HEARTBEAT signal received. " + str(self.client.user_id))
            pass
        else: # New board state (Just the updates positions of players)
            # print("Waiting for updated player positions")
            # print(list(data_buffer))
            self.deserialize_player_positions_and_update_boards(data_buffer)
            self.send_moves()
            # player_positions_buffer = list(self.client.get_message())
            # print(len(player_positions_buffer), player_positions_buffer)


        # elif data_buffer == bytearray("GAME_STARTING", "ASCII"):
        
    
def main():
    try:
        with open('config.yml', 'r') as file:
            config = safe_load(file)
    except IOError:
        print("No config.yml file found!")
        return

    
    id = config["user_id"] 
    if id < 100 or id > 2**30:
        id = randint(100, 268435455) # 0x64 - 0xfffffff

    boards = []
    for x in range(0,config["num_of_players"]):
        id += 100
        boards.append(BoardGame(
            user_id=id, 
            name=config["name"], 
            server_ip=config["server_ip"], 
            server_port=config["server_port"]))
        

    while True:
        # sleep(0.001)
        for board in boards:
            board.tick()

        

if __name__ == "__main__":
  main()