from game_screen.button_data import buton_data
from game_screen.button_object import Button
from game_screen.text import Text
from game_screen.screen_object import WIDTH, HEIGHT, WIN

buton_data = {
    "text": None,
    "size": 18,
    "font": "comicsansms",
    "bold": False,
    "italic": False,
    "color": (0, 0, 0),
    # can be an image or just bg color
    "source": "game_screen/images/",
    "image": None,
    "bg_color": (255, 255, 255),
    "pos_x": 0,
    "pos_y": 0,
    "width": 0,
    "height": 0
}


play_again_button = Button(
    text="Play Again",
    size=18,
    color=(0, 0, 0),
    pos_x=WIDTH // 2 - 100 // 2,
    pos_y=HEIGHT // 2 - 50 // 2,
    width=150, 
    height=50,
    surface=WIN
)

pause_button = Button(
    text="Pause",
    size=18,
    color=(0, 0, 0),
    pos_x=WIDTH - 100,
    pos_y=0,
    width=100, 
    height=50,
    surface=WIN
)

score_text = Text(
    text="Score: ", 
    size=15, 
    font="comicsansms",
    color=(0, 0, 0),
    pos_x=0,
    pos_y=0,
    width=50,
    height=50,
    surface=WIN
)

# menu 

# start button

play_button = Button(
    text="Play",
    size=18,
    color=(0, 0, 0),
    pos_x=WIDTH // 2 - 150 // 2,
    pos_y=150,
    width=150, 
    height=50,
    surface=WIN
)

maps_button = Button(
    text="Maps",
    size=18,
    color=(0, 0, 0),
    pos_x=WIDTH // 2 - 150 // 2,
    pos_y=225,
    width=150, 
    height=50,
    surface=WIN
)

settings_button = Button(
    text="Settings",
    size=18,
    color=(0, 0, 0),
    pos_x=WIDTH // 2 - 150 // 2,
    pos_y=300,
    width=150, 
    height=50,
    surface=WIN
)

hidden_screen_button = Button(
    text="Testing",
    size=18,
    color=(0, 0, 0),
    pos_x=WIDTH // 2 - 150 // 2,
    pos_y=375,
    width=150, 
    height=50,
    surface=WIN
)

exit_button = Button(
    text="Quit",
    size=18,
    color=(0, 0, 0),
    pos_x=WIDTH // 2 - 150 // 2,
    pos_y=450,
    width=150, 
    height=50,
    surface=WIN
)




