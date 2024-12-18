extends Node2D

@onready var main_container := $CenterContainer
@onready var button_grid := %ButtonGrid
@onready var label_attempts := %AttemptsLeft
@onready var req := %HTTPRequest
@onready var new_button := %NewButton
@onready var connect_button := %ConnectButton
@onready var deselect_button := %DeselectButton
@onready var view_results_button := %ViewResultsButton
@onready var words := button_grid.get_children()
var toggled: Array[bool] = []

# WORDS PER GROUP
var groups_size := 4

func _ready() -> void:
	req.request_completed.connect(_create_new)
	new_button.pressed.connect(_new)
	view_results_button.pressed.connect(_view_results)
	deselect_button.pressed.connect(_deselect_words)
	for i in words:
		toggled.append(false)

func _deselect_words():
	for w in words:
		(w as Button).button_pressed = false
	for i in toggled:
		i = false

var t := 0.0
var lerping := false
var to: float
var lerp_duration := 0.3

func _process(delta: float) -> void:
	# LIMIT BUTTONS TOGGLED
	for i in range(len(words)):
		var w := words[i] as Button
		
		if w.button_pressed && !toggled[i]:
			if toggled.count(true) == groups_size:
				w.button_pressed = false
			else:
				toggled[i] = true
			break
		
		if !w.button_pressed && toggled[i]:
			toggled[i] = false
			break
	
	# RESIZING
	var window := get_window()
	main_container.size = window.size
	%BottomBar.position.y = window.size.y * 0.98 - %BottomBar.size.y
	%BottomBar.size.x = window.size.x

	# ANIMATION TEST
	if t >= 1.0:
		lerping = false
		t = 0.0
	
	if Input.is_action_just_pressed("ui_accept"):
		lerping = true
		var b := (button_grid.get_child(0) as Button)
		to = b.position.x + 200
	
	if lerping:
		t += delta * (1 / lerp_duration)
		var b := (button_grid.get_child(0) as Button)
		b.position.x = lerpf(b.position.x, to, t)

# HTTP REQUEST FOR NEW PUZZLE
func _new():
	req.request("http://127.0.0.1:6969/new")

func _view_results():
	pass

func _create_new(result, _response_code, _headers, body):
	if result != HTTPRequest.RESULT_SUCCESS: return
	
	var json = JSON.parse_string(body.get_string_from_utf8())
	print(json)
