extends Node2D

@export var user_name := "GodotUser"

## This user id should be within the range 100 < user_id < 2^30 
@export var user_id := 126783



# Called when the node enters the scene tree for the first time.
func _ready():
	if ClientApi.connect_to_server("10.40.190.48") == 0:
		print_rich("[color=green]Successfully connected to server!")
	else:
		print_rich("[color=red]Failed to connect to server!")

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
