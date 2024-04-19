extends Node

@export var default_server_ip := "localhost" ## Default server IP
@export var default_server_port := 9080 ## Default server port

var client_tcp_stream : StreamPeerTCP = null

func connect_to_server(server_ip := default_server_ip, server_port := default_server_port):
	client_tcp_stream = StreamPeerTCP.new()
	client_tcp_stream.connect_to_host(server_ip, server_port)
	

# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
