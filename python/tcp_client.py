import socket
import time
import datetime

class TCPClient:

    def __init__(self, user_id=0):
        # self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.user_id = user_id
        self.end_of_message = bytearray([0])
    
    def connect(self, server_ip: str, server_port: int, time_out_seconds: float = 1) -> bool:
        """ Connects to the server. Timeouts after time_out_seconds.
        Returns true if a connection was established, otherwise returns false.
        """
        try:
            self.client = socket.create_connection((server_ip, server_port), time_out_seconds)
            return True
        except TimeoutError as e:
            print("Failed to established a connection: " + str(e))
            return False

    def send(self, message: str, add_prelude=False, debug_print=False):
        """ Formats the message string as ASCII and sends it to the server.
        """
        message = message.encode('ascii')
        if debug_print:
            print("Trying to send message: ", message)
        
            

        data = bytearray(message)
        if add_prelude:
            length = len(data)
            len_bytes = length.to_bytes()
            while len(len_bytes) < 4:
                len_bytes = bytearray([0]) + len_bytes
            data = len_bytes + data
            print(list(data), " len=", length)

            

        # data.append(self.end_of_message as byte)
        self.client.sendall(data)
        self.client.send(self.end_of_message)

    def get_message(self):
        """ This function will block until a message has been received
        """
        # The server will send 4 bytes of data containing the length of the next message
        length_of_message = 4
        data_buffer = bytearray()
        while len(data_buffer) < length_of_message:
            data_buffer += self.client.recv(length_of_message - len(data_buffer))
        
        length_of_message = 0
        for byte in data_buffer:
            length_of_message = (length_of_message << 8) + byte
        
        data_buffer = bytearray()
        while len(data_buffer) < length_of_message:
            data_buffer += self.client.recv(length_of_message - len(data_buffer))

        return data_buffer.decode()
    
    def get_message(self):
        """ This function will block until a message has been received
        """
        # The server will send 4 bytes of data containing the length of the next message
        length_of_message = 4
        data_buffer = bytearray()
        while len(data_buffer) < length_of_message:
            data_buffer += self.client.recv(length_of_message - len(data_buffer))
            # print(list(data_buffer))
        
        length_of_message = 0
        for byte in data_buffer:
            length_of_message = (length_of_message << 8) + byte
        
        data_buffer = bytearray()
        while len(data_buffer) < length_of_message:
            data_buffer += self.client.recv(length_of_message - len(data_buffer))

        return data_buffer



    def setup_connection(self, user_id: int, name: str, server_ip: str, server_port: int, 
                         time_out_seconds: float = 10):
        result = self.connect(server_ip, server_port, time_out_seconds)
        if result:
            message = f'REGISTER:user_id={user_id},name={name},big_endian=1'
            print("Sending message: ", message)
            self.send(message)
            # message = self.client.recv(4096) # Wait for "REGISTER" signal from server
            # m2 = self.client.recv(0)
            confirmation_message = self.get_message() # Get confirmation.
            if confirmation_message == "NOK":
                print("Failed to connect")
                result = False
            else:
                print(confirmation_message.decode())
            # time.sleep(0.01)
        
        return result
    
        def init_game():
            pass


if __name__ == '__main__':
    server_ip = "192.168.50.162"
    server_port = 9080

    user_id = 15
    name = "Rasmus"

    clients = []
    start_time = datetime.datetime.now()
    for x in range(4):
        client = TCPClient(user_id) # TODO Fix this init to not need user_id
        user_name = name + "-" + str(user_id)
        client.setup_connection(user_id, user_name, server_ip, server_port)
        clients.append(client)
        user_id += 100
        # print(client.get_message())
    print("Time to complete all requests: ", datetime.datetime.now() - start_time)

    for client in clients:
        print(client.get_message().decode())
    
    for client in clients:
        data = [x for x in client.get_message()]
        print(data)


    # clients.pop(1)
    # time.sleep(1)

    # user_id = 115

    # client = TCPClient(user_id) # TODO Fix this init to not need user_id
    # user_name = name + "-" + str(user_id)
    # client.setup_connection(user_id, user_name, server_ip, server_port)
    # clients.append(client)
    print("Enter infinite loop")
    while True:
        pass

