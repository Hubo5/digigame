"""The McHugo's game."""

# Importing pygame into the program
import pygame

# Allows optional type hint returns and multiple different return types.
from typing import Optional, Union

# Used for distance calculations when checking mouse clicks.
import math

# Used for changing the windows onscreen position
import os

# Used to choose random items in the list.
import random

# The x and y of the windows position after the main menu.
WINDOW_X: int = 25
WINDOW_Y: int = 18
# Sets the position of the window onscreen.
os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (WINDOW_X, WINDOW_Y)
# Activating pygame
pygame.init()

# PROGRAM STATES


# These define what part of the program the user is up to, used for calling the
# correct function corresponding to the program state.
class ProgramState:
    GAME_OPEN: int = 0
    MAIN_MENU: int = 1
    ENTER_NAME: int = 2
    GAME_MENU: int = 5
    DRINKS: int = 6
    GRILL: int = 7
    BFM: int = 8
    MAKE_GRILL: int = 9
    MAKE_BFM: int = 10
    GAME_LOST: int = 11
    CREDITS: int = 12
    TUTORIAL: int = 13
    SHIFT_FINISH: int = 14


# The state is initially set to the first phase so the program starts.
current_state: int = ProgramState.GAME_OPEN
game_end: int = 0
# CONSTANTS

# The rgb code for each color.
YELLOW: tuple[int, int, int] = (255, 255, 0)
DARK_YELLOW: tuple[int, int, int] = (254, 221, 0)
BLACK: tuple[int, int, int] = (0, 0, 0)
RED: tuple[int, int, int] = (255, 0, 0)
WHITE: tuple[int, int, int] = (255, 255, 255)
BLUE: tuple[int, int, int] = (8, 98, 168)
GREEN: tuple[int, int, int] = (80, 200, 120)
ORANGE: tuple[int, int, int] = (255, 127, 0)
GREY: tuple[int, int, int] = (128, 128, 128)
# Outline for most of the boxes displayed in game.
OUTLINE_WIDTH: int = 5
# Width and height of boxes on the second kiosk screen.
BUTTON2_WIDTH: int = 149
BUTTON2_HEIGHT: int = 56
BUTTON2_HEIGHT_EXTENDED: int = 96
# Size of the icons used on the second kiosk screen.
ICON: tuple[int, int] = 50, 50
# The window dimensions before the game officially begins.
PREGAME_SCREEN_WIDTH: int = 1000
PREGRAME_SCREEN_HEIGHT: int = 900
# The dimensions of the Drive-Thru boxes.
DTHRU_WIDTH: int = 200
DTHRU_HEIGHT: int = 100
DTHRU_OUTLINE: int = 3
# Size of the menu items.
MENU_ICON: tuple[int, int] = 60, 60
PATTY_ICON: tuple[int, int] = 65, 65
# For the total stock display.
TOTAL_PATTY_ICON: tuple[int, int] = 55, 55
TOTAL_MENU_ICON: tuple[int, int] = 50, 50
# FND: Fries, nuggets, drinks
TOTAL_FND_ICON: tuple[int, int] = 70, 70
NAVIGATION_ICON: tuple[int, int] = 40, 40
XS_NAVIGATION_ICON: tuple[int, int] = 30, 30
# For display on the creation menus.
ORDER_ICON: tuple[int, int] = 35, 35
CREATED_ICON: tuple[int, int] = 130, 130
# The amount of time to wait before moving 1 space.
WAIT_INTERVAL: int = 1


# PREDEFINED VARIABLES

# The desired screen dimensions.
screen_width = PREGAME_SCREEN_WIDTH
screen_height = PREGRAME_SCREEN_HEIGHT
# The current screen dimensions.
current_screen_width = screen_width
current_screen_height = screen_height
# The variable responsible for creating the game window with the parameters
# provided.
screen = pygame.display.set_mode((screen_width, screen_height))
# Sets the users name to none so they can make their own.
user_name: str = ""
# The title of the game window.
pygame.display.set_caption("McHugo's")
# This boolean controls the flashing start order button, and when its visible.
visible: bool = True
# This variable initially defines the time since the last switch from visible
# to not visible (part of the blinking order variable)
last_switch: int = 0
# This boolean controls whether the game is running or not.
running: bool = True
# This boolean checks if an error has been triggered so another variable can
# act off it.
error: bool = False
# This variable states what the error was in a variable so an action can be
# taken depending on what it is.
error_type: str = ""
# The positions of the boxes in the drive thru.
dthru_box_x_positions: list[int] = [120, 270, 420, 570, 720, 870]
dthru_text_x_positions: list[int] = [1090, 925, 775, 625, 475, 325, 175]
# The positions of the circles for the total stock.
total_stock_circle_x_positions: list[int] = [640, 740, 840, 940]
total_stock_circle_y_positions: list[int] = [230, 410]
# A dictionary of the menu items.
total_stock_items: dict[str, int] = {
    "Big Hugo": 0,
    "Francie Frenzy": 0,
    "5/4 Slammer": 0,
    "2 5/4 Slammer": 0,
    "Almighty Florida": 0,
    "Keanu Krunch": 0,
    "Devious Chicken": 0,
    "Chicken Little": 0,
    "10:1": 0,
    "4:1": 0,
    "Angus": 0,
    "Chicken": 0,
    "Fries": 0,
    "McBullets": 0,
    "Hugo Juice": 0,
}
# All of the menu items with their values put into a list.
menu_list = list(total_stock_items.items())
# Dictionary for individual rectangles so they can be used specifically.
station_bases: dict = {}
# To define which station was triggered. Global variable used to maintain
# status. This becomes a 2d dictionary.
station_status: dict[str, dict] = {}
# The variables are globablly used to prevent a glitch where a button appears
# as another one closes, resulting in them clicking it unintentionally. Wait
# prevents that button from being clicked.
pause: bool = False
skip: bool = False
wait: int = 0
wait2: int = 0
# A dictionary of lists to keep track of expiring items.
expiring_items: dict[str, list:int] = {}
# The prices of the items at McHugo's.
item_prices: dict[str, float] = {
    "Big Hugo": 4.6,
    "Francie Frenzy": 6.8,
    "5/4 Slammer": 5.0,
    "2 5/4 Slammer": 7.2,
    "Almighty Florida": 5.4,
    "Keanu Krunch": 7.6,
    "Devious Chicken": 4.9,
    "Chicken Little": 7.1,
    "Fries": 2.8,
    "Hugo Juice": 2.0,
    "McBullets": 3.5,
}
# The cost to make everything, used to balance the game.
production_cost: dict[str, float] = {
    "Big Hugo": 1.15,
    "Francie Frenzy": 1.7,
    "5/4 Slammer": 1.25,
    "2 5/4 Slammer": 1.8,
    "Almighty Florida": 1.35,
    "Keanu Krunch": 1.9,
    "Devious Chicken": 1.3,
    "Chicken Little": 1.78,
    "Fries": 0.5,
    "Hugo Juice": 0.3,
    "McBullets": 0.87,
    "10:1": 0.2,
    "4:1": 0.4,
    "Angus": 0.6,
    "Chicken": 0.45,
}
# Keeps track of the users money.
money: int = 0.00
# Classifies burgers to check if they have the resources to be made.
burger_type: dict[str, dict[str, int]] = {
    "10:1": {"Big Hugo": 1, "Francie Frenzy": 2},
    "4:1": {"5/4 Slammer": 1, "2 5/4 Slammer": 2},
    "Angus": {"Almighty Florida": 1, "Keanu Krunch": 2},
    "Chicken": {"Devious Chicken": 1, "Chicken Little": 2},
}
# Used for determing what patty is required when not enough have been made.
# Global variable.
patty_needed: str = None
quantity_patty_needed: int = None
# Indicates whether the AI should begin ordering,
begin_ordering: bool = False
# Indicates if the AI has obtained a number for waiting to prevent constant
# looping.
obtained_wait: bool = False
# The time to wait before placing an order.
wait_order: int = 0
# All the orders from the AI combined.
total_items_required: dict[str, int] = {
    "Big Hugo": 0,
    "Francie Frenzy": 0,
    "5/4 Slammer": 0,
    "2 5/4 Slammer": 0,
    "Almighty Florida": 0,
    "Keanu Krunch": 0,
    "Devious Chicken": 0,
    "Chicken Little": 0,
    "Fries": 0,
    "McBullets": 0,
    "Hugo Juice": 0,
    "10:1": 0,
    "4:1": 0,
    "Angus": 0,
    "Chicken": 0,
}
# Each individual order. Becomes a 2D Dict.
individual_orders: dict[str, dict[str, int]] = {}
# Keeps track of the order number. Global variable.
order_index: int = 0
# The menu for the AI to order from.
ordering_menu: list[str] = [
    "Big Hugo",
    "Francie Frenzy",
    "5/4 Slammer",
    "2 5/4 Slammer",
    "Almighty Florida",
    "Keanu Krunch",
    "Devious Chicken",
    "Chicken Little",
    "Fries",
    "McBullets",
    "Hugo Juice",
]
# Various combos that the AI can order.
combos: dict[str, dict[str, int]] = {
    "The Classic": {"Big Hugo": 1, "Fries": 1, "Hugo Juice": 1},
    "The HugoBox": {"Big Hugo": 2, "Fries": 2, "Hugo Juice": 2},
    "The Achieved": {"5/4 Slammer": 1, "Fries": 1},
    "The Merit": {"2 5/4 Slammer": 1, "Fries": 1},
    "The Excellence": {
        "2 5/4 Slammer": 1,
        "Fries": 1,
        "Hugo Juice": 1,
        "McBullets": 1,
    },
    "Francie": {
        "Francie Frenzy": 1,
        "Devious Chicken": 1,
        "McBullets": 2,
        "Fries": 1,
    },
    "Devious David": {
        "Almighty Florida": 1,
        "Chicken Little": 1,
        "Big Hugo": 2,
        "Fries": 3,
        "McBullets": 1,
        "Hugo Juice": 2,
    },
    "Invincible Ira": {
        "Keanu Krunch": 1,
        "Fries": 4,
        "Chicken Little": 2,
        "Hugo Juice": 2,
    },
    "Ravenous Rueben": {
        "5/4 Slammer": 3,
        "Big Hugo": 2,
        "Hugo Juice": 3,
        "McBullets": 4,
        "Fries": 6,
    },
    "Light Snack": {"McBullets": 1, "Fries": 1},
    "The Biggie": {
        "Francie Frenzy": 1,
        "McBullets": 2,
        "Hugo Juice": 1,
        "Fries": 3,
    },
    "Anything Yellow": {
        "Devious Chicken": 1,
        "McBullets": 1,
        "Fries": 1,
        "Chicken Little": 1,
    },
    "Yellow Is My Favourite Colour": {
        "Chicken Little": 2,
        "McBullets": 2,
        "Fries": 2,
    },
    "America": {"Almighty Florida": 2, "McBullets": 1},
    "Keanu Badiger": {"Keanu Krunch": 2},
    "I Love Hugo": {"Big Hugo": 4, "Hugo Juice": 4},
    "Big Snack": {"Fries": 3, "McBullets": 3},
    "Chicken Lover": {
        "Devious Chicken": 1,
        "Chicken Little": 1,
        "McBullets": 1,
    },
    "Pleaseburgercheese": {"Big Hugo": 1},
    "Frugo": {"Big Hugo": 1, "Francie Frenzy": 1, "Fries": 2, "Hugo Juice": 2},
    "Big And Small": {
        "5/4 Slammer": 2,
        "Big Hugo": 2,
        "McBullets": 3,
        "Hugo Juice": 4,
    },
    "Biden": {
        "Almighty Florida": 2,
        "Devious Chicken": 1,
        "Fries": 2,
        "Hugo Juice": 1,
    },
    "Basic Angus": {"Almighty Florida": 1, "Fries": 1, "Hugo Juice": 1},
    "Advanced Keanu": {"Keanu Krunch": 1, "Fries": 1, "Hugo Juice": 1},
    "Chicken Little": {"Chicken Little": 1, "McBullets": 1},
    "Angry Chicken": {
        "Chicken Little": 2,
        "Devious Chicken": 1,
        "Keanu Krunch": 1,
    },
    "Seb's Synopsis": {
        "Francie Frenzy": 1,
        "Almighty Florida": 1,
        "2 5/4 Slammer": 1,
        "Fries": 4,
    },
    "Skibidi Toilet": {
        "2 5/4 Slammer": 2,
        "Hugo Juice": 3,
        "McBullets": 3,
        "Almighty Florida": 1,
    },
    "Threesome": {
        "Francie Frenzy": 1,
        "2 5/4 Slammer": 1,
        "Keanu Krunch": 1,
        "Chicken Little": 1,
        "Fries": 4,
        "Hugo Juice": 4,
    },
    "Nui": {
        "Big Hugo": 1,
        "5/4 Slammer": 1,
        "Almighty Florida": 1,
        "Devious Chicken": 1,
        "McBullets": 4,
        "Hugo Juice": 4,
    },
    "Maths Nerd": {"5/4 Slammer": 1, "2 5/4 Slammer": 1},
    "Dropout": {"5/4 Slammer": 2, "McBullets": 2},
    "Drunk": {"Hugo Juice": 8},
    "Doom": {
        "Francie Frenzy": 1,
        "5/4 Slammer": 1,
        "2 5/4 Slammer": 1,
        "Almighty Florida": 1,
        "Keanu Krunch": 1,
        "Devious Chicken": 1,
        "Chicken Little": 1,
        "Fries": 3,
        "McBullets": 3,
        "Hugo Juice": 6,
    },
}
# Used to check if the time since the game has started has been obtained.
obtained_start_time: bool = False
# The time remaining in the game.
time_left: int = 0
# Checks if an order was placed.
ordered: bool = False
# The coordinates for the cars to move to.
car_coords: list[int] = [
    1065,
    900,
    750,
    600,
    450,
    300,
    150,
    -50,
    -50,
    -50,
    -50,
    -50,
    -50,
]
# The 2D dict of cars.
cars: dict[int, dict] = {}
# The amount of current orders.
total_orders: int = 0
# The order number used to identify the car.
order_number: int = 0
# The list of orders stored in a list for the cars.
orders_list = None
# The amount of items in an order. Global.
total_items: int = 0
# Used to animate the cars moving.
last_tick: int = pygame.time.get_ticks()
# The amount of excess cars.
excess: int = 0
# Checks if a car has been deleted.
deleted: bool = False
# Signifies the car is currently being deleted.
deleting: bool = False
# Position of the danger boxes.
danger_box_positions: list[int] = [885, 735, 585, 435, 285, 135]
# Contains what is in the current order. Global variable used for checking whats
# in the order. It is a list aquired with a key.
order_stats: str = []
# Global dict to assign orders to combos so they can be displayed.
order_combo: dict[str, str] = {}
# Keeps track of when a car was served.
car_served_times: list[int] = []
# This variable determines if the AI ordering cycle should begin.
hold_orders: bool = True
# 10 seconds plus the current time to wait to order.
wait_time: int = 0
# Controls which tutorial image to display using the position in the list.
tutorial_select: int = 0
# The total items ordered.
total_items_ordered: int = 0

# SOUNDS
order_sfx = pygame.mixer.Sound("sounds/order.mp3")
cooking_sfx = pygame.mixer.Sound("sounds/startgrillbmf.mp3")
burnt_sfx = pygame.mixer.Sound("sounds/burnt.mp3")
# FONTS AND IMAGES


# The fonts for the game.
title_font = pygame.font.Font("fonts/game title.ttf", 150)
title_font_xs = pygame.font.Font("fonts/game title.ttf", 120)
heading_font = pygame.font.Font("fonts/heading text.ttf", 40)
body_font = pygame.font.Font("fonts/body text.ttf", 25)
start_order_font = pygame.font.Font("fonts/important button.ttf", 53)
start_order_font_xs = pygame.font.Font("fonts/important button.ttf", 49)
main_menu_options = pygame.font.Font("fonts/important button.ttf", 44)
main_menu_options_xs = pygame.font.Font("fonts/important button.ttf", 38)
main_menu_options_xs2 = pygame.font.Font("fonts/important button.ttf", 34)
main_menu_options_xs3 = pygame.font.Font("fonts/important button.ttf", 28)
name_font = pygame.font.Font("fonts/enter name.ttf", 80)
stats_font = pygame.font.Font("fonts/body text.ttf", 20)
dthru_heading_font = pygame.font.Font("fonts/important button.ttf", 25)
quantity_font = pygame.font.Font("fonts/body text.ttf", 20)
burger_name_font = pygame.font.Font("fonts/body text.ttf", 14)
total_stock_name_font = pygame.font.Font("fonts/body text.ttf", 12)
stock_required_font = pygame.font.Font("fonts/important button.ttf", 19)
navigation_font = pygame.font.Font("fonts/important button.ttf", 18)
number_font = pygame.font.Font("fonts/important button.ttf", 45)
money_font = pygame.font.Font("fonts/important button.ttf", 34)
status_heading_font = pygame.font.Font("fonts/important button.ttf", 16)
status_font = pygame.font.Font("fonts/important button.ttf", 11)
item_font = pygame.font.Font("fonts/body text.ttf", 11)
time_remaining_font = pygame.font.Font("fonts/important button.ttf", 25)
combo_font = pygame.font.Font("fonts/important button.ttf", 35)
credits_text = pygame.font.Font("fonts/important button.ttf", 25)

# This is the text displayed in the game.
# First main menu screen
game_title = title_font.render("McHugo's", True, YELLOW)
kiosk_heading_1 = heading_font.render("Welcome to", True, BLACK)
kiosk_heading_2 = heading_font.render("McHugo's.", True, BLACK)
hungry_hugo = body_font.render("Hungry for Hugo?", True, BLACK)
start_order_1 = start_order_font.render("START", True, DARK_YELLOW)
start_order_2 = start_order_font_xs.render("ORDER", True, DARK_YELLOW)
start_order_3 = start_order_font.render("HERE", True, DARK_YELLOW)
start_order_4 = start_order_font.render("!!!", True, DARK_YELLOW)
version = heading_font.render("VERSION: FULL 1.06", True, RED)

# Second main menu screen
play_button = main_menu_options.render("PLAY", True, DARK_YELLOW)
tutorial_button_1 = main_menu_options.render("FIRST", True, DARK_YELLOW)
tutorial_button_2 = main_menu_options.render("SHIFT", True, DARK_YELLOW)
credits_button = main_menu_options_xs3.render("CREDITS", True, DARK_YELLOW)

# Making a name
enter_name = title_font.render("Enter the name", True, YELLOW)
enter_name_2 = title_font_xs.render("of your McHugo's", True, YELLOW)
enter_name_3 = title_font.render("store: ", True, YELLOW)
no_name = start_order_font.render("you need a name dawg", True, RED)
length_incorrect = start_order_font_xs.render(
    "Name must be between 3-25 characters", True, RED
)
back_name_text = main_menu_options.render("BACK", True, DARK_YELLOW)

# Ingame menu
time_text_2 = body_font.render("EXCESS", True, WHITE)
time_text_3 = body_font.render("CARS", True, WHITE)
time_text_5 = main_menu_options.render("SERVE!", True, WHITE)
current_order_heading = dthru_heading_font.render("CURRENT ORDER", True, YELLOW)
total_stock_heading = dthru_heading_font.render("TOTAL STOCK", True, YELLOW)
navigation_heading = dthru_heading_font.render("NAVIGATION", True, YELLOW)
current_car_heading = navigation_font.render("Current car time:", True, WHITE)
average_car_heading = navigation_font.render("Average: ", True, WHITE)
money_heading = navigation_font.render("Money earnt: ", True, WHITE)
time_heading = navigation_font.render("Time left: ", True, WHITE)
hugo_patty_name = burger_name_font.render("10:1", True, WHITE)
slammer_patty_name = burger_name_font.render("4:1", True, WHITE)
angus_patty_name = burger_name_font.render("Angus", True, WHITE)
chicken_patty_name = burger_name_font.render("Chicken", True, WHITE)
grill_heading = burger_name_font.render("Grill", True, WHITE)
drinks_heading = burger_name_font.render("Drinks", True, WHITE)
bfm_heading = burger_name_font.render("BFM", True, WHITE)

# Drinks, Grill and BFM
status_heading = status_heading_font.render("STATUS:", True, WHITE)
status_standby = status_font.render("STANDBY", True, RED)
status_wait = status_font.render("CREATING", True, DARK_YELLOW)
status_ready = status_font.render("READY!", True, GREEN)
back_name_text_xs = main_menu_options_xs3.render("BACK", True, DARK_YELLOW)
create_name_text_xs = main_menu_options_xs3.render("MAKE", True, DARK_YELLOW)
cook_name_text_xs = main_menu_options_xs3.render("COOK", True, DARK_YELLOW)
current_requirements = heading_font.render("Current:", True, WHITE)
total_requirements = heading_font.render("Total:", True, WHITE)
button_start = dthru_heading_font.render("CREATE!", True, WHITE)
creation_click = status_font.render("CLICK!", True, WHITE)
# If the user loses the game.
your_fired = title_font.render("YOUR FIRED", True, RED)
# If the user wins the game.
shift_over = title_font.render("SHIFT OVER!", True, WHITE)


# These are the images used in the game.
background = pygame.image.load("images/background.jpg")
main_menu_kiosk = pygame.image.load("images/kiosk.png")
logo = pygame.image.load("images/logo.png")
play_icon = pygame.image.load("images/play_icon.png")
first_shift_icon = pygame.image.load("images/first_shift_icon.png")
credits_icon = pygame.image.load("images/scoreboard_icon.png")
name_background = pygame.image.load("images/darkened_background.png")
back_name = pygame.image.load("images/back.png")
forwards = pygame.image.load("images/forward.png")
car = pygame.image.load("images/car_green_side.png")
redlight = pygame.image.load("images/redlight.png")
yellowlight = pygame.image.load("images/yellowlight.png")
greenlight = pygame.image.load("images/greenlight.png")
miniscule_danger = pygame.image.load("images/danger1.PNG")
low_danger = pygame.image.load("images/danger2.PNG")
moderate_danger = pygame.image.load("images/danger3.PNG")
high_danger = pygame.image.load("images/danger4.PNG")
extreme_danger = pygame.image.load("images/danger5.PNG")

# Tutorial
tutorial_1 = pygame.image.load("images/tutorial/tutorial1-removebg-preview.png")
tutorial_2 = pygame.image.load("images/tutorial/tutorial2-removebg-preview.png")
tutorial_3 = pygame.image.load("images/tutorial/tutorial3-removebg-preview.png")
tutorial_5 = pygame.image.load("images/tutorial/tutorial5-removebg-preview (1).png")
tutorial_6 = pygame.image.load("images/tutorial/tutorial6-removebg-preview.png")
tutorial_7 = pygame.image.load("images/tutorial/Capture-removebg-preview.png")
tutorial_8 = pygame.image.load("images/tutorial/tutorial8-removebg-preview (2).png")

# Menu items (all from Freepik)
big_hugo = pygame.image.load("images/menu items/big hugo.png")
francie_frenzy = pygame.image.load("images/menu items/francie frenzy.png")
improper_slammer = pygame.image.load("images/menu items/improper slammer.png")
double_improper_slammer = pygame.image.load("images/menu items/double improper.png")
almighty_florida = pygame.image.load("images/menu items/florida.png")
keanu_krunch = pygame.image.load("images/menu items/keanu krunch.png")
radioactive_mcr = pygame.image.load("images/menu items/radioactive.png")
chicken_little = pygame.image.load("images/menu items/lil chicken.png")
mcbullets = pygame.image.load("images/menu items/mcbullets.png")
fries = pygame.image.load("images/menu items/fries.png")
juice = pygame.image.load("images/menu items/juice.png")
# Icon by Smashicons
bfm_icon = pygame.image.load("images/menu items/bfm.png")

# Patties
hugo_patty = pygame.image.load(
    "images/menu items/10 to 1.png"
)  # Reference: Icon by Erifqi Zetiawan
slammer_patty = pygame.image.load(
    "images/menu items/4 to 1.png"
)  # Reference: Icon by Freepik
angus_patty = pygame.image.load(
    "images/menu items/angus.png"
)  # Reference: Icon by Smashicons
chicken_patty = pygame.image.load(
    "images/menu items/chicken.png"
)  # Reference: Icon by Freepik

# These are images that have had their size altered.
# "t" means for the total stock display.
logo_1 = pygame.transform.scale(logo, (400, 400))
logo_2 = pygame.transform.scale(logo, (51, 51))
logo_3 = pygame.transform.scale(logo, (80, 80))
play_icon_sized = pygame.transform.scale(play_icon, (ICON))
first_shift_icon_sized = pygame.transform.scale(first_shift_icon, (ICON))
scoreboard_icon_sized = pygame.transform.scale(credits_icon, (ICON))
back_name_sized = pygame.transform.scale(back_name, (ICON))
# For the tutorial previous and next buttons.
previous_image = pygame.transform.scale(back_name, (100, 100))
next_image = pygame.transform.scale(forwards, (100, 100))


forward_sized = pygame.transform.scale(forwards, (ICON))
car_sized = pygame.transform.scale(car, (85, 45))
redlight_sized = pygame.transform.scale(redlight, (50, 135))
yellowlight_sized = pygame.transform.scale(yellowlight, (50, 135))
greenlight_sized = pygame.transform.scale(greenlight, (50, 135))

# Menu items
# Current order display
big_hugo_sized = pygame.transform.scale(big_hugo, (MENU_ICON))
francie_frenzy_sized = pygame.transform.scale(francie_frenzy, (MENU_ICON))
improper_slammer_sized = pygame.transform.scale(improper_slammer, (MENU_ICON))
double_improper_slammer_sized = pygame.transform.scale(
    double_improper_slammer, (MENU_ICON)
)
almighty_florida_sized = pygame.transform.scale(almighty_florida, (MENU_ICON))
keanu_krunch_sized = pygame.transform.scale(keanu_krunch, (MENU_ICON))
radioactive_mcr_sized = pygame.transform.scale(radioactive_mcr, (MENU_ICON))
chicken_little_sized = pygame.transform.scale(chicken_little, (MENU_ICON))
juice_sized = pygame.transform.scale(juice, (MENU_ICON))
fries_sized = pygame.transform.scale(fries, (MENU_ICON))
mcbullets_sized = pygame.transform.scale(mcbullets, (MENU_ICON))
# Total stock display
big_hugo_sized_t = pygame.transform.scale(big_hugo, (TOTAL_MENU_ICON))
francie_frenzy_sized_t = pygame.transform.scale(francie_frenzy, (TOTAL_MENU_ICON))
improper_slammer_sized_t = pygame.transform.scale(improper_slammer, (TOTAL_MENU_ICON))
double_improper_slammer_sized_t = pygame.transform.scale(
    double_improper_slammer, (TOTAL_MENU_ICON)
)
almighty_florida_sized_t = pygame.transform.scale(almighty_florida, (TOTAL_MENU_ICON))
keanu_krunch_sized_t = pygame.transform.scale(keanu_krunch, (TOTAL_MENU_ICON))
radioactive_mcr_sized_t = pygame.transform.scale(radioactive_mcr, (TOTAL_MENU_ICON))
chicken_little_sized_t = pygame.transform.scale(chicken_little, (TOTAL_MENU_ICON))
fries_sized_t = pygame.transform.scale(fries, (TOTAL_FND_ICON))
mcbullets_sized_t = pygame.transform.scale(mcbullets, (TOTAL_FND_ICON))
juice_sized_t = pygame.transform.scale(juice, (TOTAL_FND_ICON))
hugo_patty_sized = pygame.transform.scale(hugo_patty, (PATTY_ICON))
hugo_patty_sized_t = pygame.transform.scale(hugo_patty, (TOTAL_PATTY_ICON))
slammer_patty_sized = pygame.transform.scale(slammer_patty, (PATTY_ICON))
slammer_patty_sized_t = pygame.transform.scale(slammer_patty, (TOTAL_PATTY_ICON))
angus_patty_sized = pygame.transform.scale(angus_patty, (PATTY_ICON))
angus_patty_sized_t = pygame.transform.scale(angus_patty, (TOTAL_PATTY_ICON))
chicken_patty_sized = pygame.transform.scale(chicken_patty, (PATTY_ICON))
chicken_patty_sized_t = pygame.transform.scale(chicken_patty, (TOTAL_PATTY_ICON))
grill_icon = pygame.transform.scale(big_hugo, (NAVIGATION_ICON))
grill_menu_icon = pygame.transform.scale(big_hugo, (MENU_ICON))
bfm_menu_icon = pygame.transform.scale(bfm_icon, (MENU_ICON))
drinks_icon = pygame.transform.scale(juice, (NAVIGATION_ICON))
fries_icon = pygame.transform.scale(fries, (XS_NAVIGATION_ICON))
nuggets_icon = pygame.transform.scale(mcbullets, (XS_NAVIGATION_ICON))

# Icons for displaying the order on respective menus.
juice_order_icon = pygame.transform.scale(juice, (ORDER_ICON))
hugopatty_order_icon = pygame.transform.scale(hugo_patty, (ORDER_ICON))
slammerpatty_order_icon = pygame.transform.scale(slammer_patty, (ORDER_ICON))
anguspatty_order_icon = pygame.transform.scale(angus_patty, (ORDER_ICON))
fries_order_icon = pygame.transform.scale(fries, (ORDER_ICON))
mcbullets_order_icon = pygame.transform.scale(mcbullets, (ORDER_ICON))
chicken_order_icon = pygame.transform.scale(chicken_patty, (ORDER_ICON))
bighugo_order_icon = pygame.transform.scale(big_hugo, (ORDER_ICON))
improperslammer_order_icon = pygame.transform.scale(improper_slammer, (ORDER_ICON))
almightyflorida_order_icon = pygame.transform.scale(almighty_florida, (ORDER_ICON))
francie_frenzy_order_icon = pygame.transform.scale(francie_frenzy, (ORDER_ICON))
doubleimproperslammer_order_icon = pygame.transform.scale(
    double_improper_slammer, (ORDER_ICON)
)
keanu_krunch_order_icon = pygame.transform.scale(keanu_krunch, (ORDER_ICON))
radioactivechicken_order_icon = pygame.transform.scale(radioactive_mcr, (ORDER_ICON))
chickenlittle_order_icon = pygame.transform.scale(chicken_little, (ORDER_ICON))
# Icons for the finished product on respective menus.
juice_creation_icon = pygame.transform.scale(juice, (CREATED_ICON))
hugopatty_creation_icon = pygame.transform.scale(hugo_patty, (CREATED_ICON))
slammerpatty_creation_icon = pygame.transform.scale(slammer_patty, (CREATED_ICON))
anguspatty_creation_icon = pygame.transform.scale(angus_patty, (CREATED_ICON))
fries_creation_icon = pygame.transform.scale(fries, (CREATED_ICON))
mcbullets_creation_icon = pygame.transform.scale(mcbullets, (CREATED_ICON))
chicken_creation_icon = pygame.transform.scale(chicken_patty, (CREATED_ICON))
bighugo_creation_icon = pygame.transform.scale(big_hugo, (CREATED_ICON))
improperslammer_creation_icon = pygame.transform.scale(improper_slammer, (CREATED_ICON))
almightyflorida_creation_icon = pygame.transform.scale(almighty_florida, (CREATED_ICON))
franciefrenzy_creation_icon = pygame.transform.scale(francie_frenzy, (CREATED_ICON))
doubleimproperslammer_creation_icon = pygame.transform.scale(
    double_improper_slammer, (CREATED_ICON)
)
keanu_krunch_creation_icon = pygame.transform.scale(keanu_krunch, (CREATED_ICON))
radioactivechicken_creation_icon = pygame.transform.scale(
    radioactive_mcr, (CREATED_ICON)
)
chickenlittle_creation_icon = pygame.transform.scale(chicken_little, (CREATED_ICON))

# These lists needs to be defined down here where the images have been defined.
menu_images: list[pygame.Surface] = [
    big_hugo_sized_t,
    francie_frenzy_sized_t,
    improper_slammer_sized_t,
    double_improper_slammer_sized_t,
    almighty_florida_sized_t,
    keanu_krunch_sized_t,
    radioactive_mcr_sized_t,
    chicken_little_sized_t,
    hugo_patty_sized_t,
    slammer_patty_sized_t,
    angus_patty_sized_t,
    chicken_patty_sized_t,
    fries_sized_t,
    mcbullets_sized_t,
    juice_sized_t,
]

# Default menu lists for starting
grill_names: list[str] = [
    "10:1",
    "4:1",
    "Angus",
    "10:1",
    "4:1",
    "Angus",
]
grill_creation: list[pygame.Surface] = [
    hugopatty_creation_icon,
    slammerpatty_creation_icon,
    anguspatty_creation_icon,
    hugopatty_creation_icon,
    slammerpatty_creation_icon,
    anguspatty_creation_icon,
]
grill_timers: list[int] = [
    8000,
    8000,
    13000,
    8000,
    8000,
    13000,
]
bfm_names: list[str] = [
    "Fries",
    "McBullets",
    "Chicken",
    "Fries",
    "McBullets",
    "Chicken",
]
bfm_creation: list[pygame.Surface] = [
    fries_creation_icon,
    mcbullets_creation_icon,
    chicken_creation_icon,
    fries_creation_icon,
    mcbullets_creation_icon,
    chicken_creation_icon,
]
bfm_timers: list[int] = [
    5000,
    6000,
    7000,
    5000,
    6000,
    7000,
]
# Menu items linked to images
current_order_images: dict[str, pygame.Surface] = {
    "Big Hugo": big_hugo_sized,
    "Francie Frenzy": francie_frenzy_sized,
    "5/4 Slammer": improper_slammer_sized,
    "2 5/4 Slammer": double_improper_slammer_sized,
    "Almighty Florida": almighty_florida_sized,
    "Keanu Krunch": keanu_krunch_sized,
    "Devious Chicken": radioactive_mcr_sized,
    "Chicken Little": chicken_little_sized,
    "Fries": fries_sized,
    "McBullets": mcbullets_sized,
    "Hugo Juice": juice_sized,
}
# FUNCTIONS

# UTILITY


def toggle_visibility(
    last_switch_local: int, visible_local: bool, time_switch: int, repeat: bool
) -> bool:
    """Control the visibility of a desired element.

    Args:
        last_switch_local (int): The last time the visibility was toggled.
        visible_local (bool): The status of the elements visibility.
        time_switch (int): The time until it takes for visibility to be toggled.
        repeat (bool): Whether the function should be repeated until its no
        longer called.

    Returns:
        bool: The status of the elements visiblity.
    """
    # The global variable is accessed so it can be updated.
    global last_switch

    # The program begins counting from when the funtion was called.
    start_switches = pygame.time.get_ticks()

    # If the timer minus the last visibility switch is greater than the desired
    # time to stay on screen:
    if start_switches - last_switch_local > time_switch:
        # Visibility is changed to none.
        visible_local = not visible_local

        # If the visibility should be repeatedly toggled:
        if repeat:
            # The last switch variable is changed to the amount of time the game
            # has been opened for. The global variable is accessed so the
            # argument provided by the function calling it can be altered.
            last_switch = start_switches

    return visible_local


def timer(time_end: int) -> bool:
    """Time how long a station should remain in its status.

    Args:
        time_end (int): When the timer should end.

    Returns:
        bool: A boolean indicating if the timer has passed its end time.
    """
    time_start = pygame.time.get_ticks()
    # Prevents an error occuring when a timer has expired.
    if time_end is not None:
        return time_start >= time_end


def expiry() -> None:
    """
    Check if an item on the menu has expired.
    """
    global expiring_items, total_stock_items

    if expiring_items != {}:
        # The first value of the list is got, then 20 seconds is added to it
        # (the expiry time).
        for item_name, expiry in expiring_items.items():
            # Makes sure the list isn't empty.
            if expiry:
                first_value = expiry[0] + 80000
                # If the timer has expired:
                if timer(first_value):
                    # Using the item name, stock is updated.
                    total_stock_items[item_name] -= 1
                    # The item is deleted from the expiring items list.
                    del expiry[0]


def draw_timer(screen, elapsed_time: int, time_end: int, center, radius: int) -> None:
    """Draw a circle which disappears as time passes.

    Args:
        screen: The surface to be drawn on.
        elapsed_time (int): The elapsed time since the timer was started,
        provided by caller.
        time_end (int): When the timer should end, and the circle fully
        disappear.
        center: The x and y of the circles center.
        radius (int): The radius of the circle.
    """
    # The remaining time left is calculated. 'Max' ensures the remaining time
    # will not be negative by making remaining_time equal at least 0.
    remaining_time = max(0, time_end - elapsed_time)
    # The angle is calculated using a fraction representing the remaining time,
    # and converts it into an angle in radians.
    angle = 2 * math.pi * (remaining_time / time_end)
    # If the angle isn't a full circle:

    if angle < 2 * math.pi:
        # Start point is set to the top of the circle.
        start_angle = -math.pi / 2
        # End of the arc is calculated based on remaining time 'angle'.
        end_angle = start_angle + angle
        # The number of lines used to pinpoint the arc.
        num_segments = 100
        # A list of all the points to draw between.
        points = []
        # This loop uses trigonometry to get each point for each segment.

        for i in range(num_segments + 1):
            theta = start_angle + (end_angle - start_angle) * i / num_segments
            x = center[0] + radius * math.cos(theta)
            y = center[1] + radius * math.sin(theta)
            # Points are added to the list.
            points.append((x, y))

        # If there is more than 1 point remaining:
        if len(points) > 1:
            # The lines creating the circle are drawn.
            pygame.draw.lines(screen, WHITE, False, points, 6)

    # The text for time left is converted to seconds, and a max is again used
    # to prevent errors.
    time_left = max(0, remaining_time // 1000)
    # As the time left constantly changes, the font is rendered within the
    # function.
    time_left_text = time_remaining_font.render(str(time_left), True, WHITE)
    # The text is centered differently as this function doesn't have access to
    # the station outlines directly (they are in a tuple) for further efficency.
    # The text is made into a rect with its center being = to the circle center.
    text_centering = time_left_text.get_rect(center=center)
    screen.blit(time_left_text, text_centering)


def ai_ordering() -> None:
    """Order menu and combo items."""
    # Global variables used to prevent constant redefinition,
    # as well as update orders.
    global \
        obtained_wait, \
        wait_order, \
        order_index, \
        total_items_required, \
        individual_orders, \
        combos, \
        ordered, \
        current_time, \
        order_combo, \
        hold_orders, \
        wait_time

    # The user is given 10 seconds before the AI begins ordering.
    if hold_orders:
        wait_time = current_time + 10000
        hold_orders = False

    # The program waits 10 seconds before beginning ordering.
    if current_time < wait_time:
        print("WAITING")
    else:
        ordered = False

        # The AI waits between 5 and 40 seconds. * 1000 converts to ms.
        if not obtained_wait:
            wait_order = random.randint(5, 40) * 1000 + current_time
            # Only gets the obtained number once.
            obtained_wait = True

        # If it is time for the AI to order:
        if timer(wait_order):
            print("ORDERED")
            # Order sound is played.
            order_sfx.play()
            # The order number.
            order_index += 1
            # The order number is created.
            order_number = f"Order {order_index}"
            # A dict is made under it.
            individual_orders[order_number] = {}
            # A combo is randomly chosen and converted into a list so it can be
            # accessed.
            random_combo_name = random.choice(list(combos.keys()))
            # The combo is chosen.
            random_combo = combos[random_combo_name]

            # The combo is added to the total items list, and the patty is also
            # added.
            for burger, quantity in random_combo.items():
                total_items_required[burger] += quantity
                individual_orders[order_number][burger] = quantity

                for patty_type, burger_stats in burger_type.items():
                    for burger_name, patty_requirements in burger_stats.items():
                        if burger_name == burger:
                            # Using the patty type of the burger, it is updated
                            # with the requirements.
                            total_items_required[patty_type] += (
                                patty_requirements * quantity
                            )

            # The amount of items for the AI to order are chosen.
            items_ordered = random.randint(1, 4)
            # 1 in 3 chance of ordering random items.
            order_random_items_check = random.randint(1, 3)

            if order_random_items_check == 1:
                print("RANDOM ADDED!")
                # The amount of items left to select.
                items_selected = items_ordered

                while items_selected > 0:
                    # The amount of items to buy is randomly determined.
                    item_purchased = random.randint(1, 5)
                    # The item is determined using the index of the purchased
                    # item.
                    item_name = ordering_menu[item_purchased]

                    # If the item has not yet been ordered, it is added.
                    if item_name not in individual_orders[order_number]:
                        individual_orders[order_number][item_name] = 1
                    else:
                        # If it has been, it is added.
                        individual_orders[order_number][item_name] += 1

                    # The items left to order is reduced by 1.
                    items_selected -= 1
                    # The item is added to the total requirements.
                    total_items_required[item_name] += 1

                    # The patty requirements of the burger is located.
                    for patty_type, burger_stats in burger_type.items():
                        for burger_name, patty_requirements in burger_stats.items():
                            if burger_name == item_name:
                                # Using the patty type of the burger, it is
                                # update with the requirements.
                                total_items_required[patty_type] += patty_requirements

                # The combo name is assigned to a dict logging each orders combo
                # with a "+" next to it to signify a random combo has been
                # added.
                order_combo[order_number] = random_combo_name + "+"
            else:
                # Otherwise, it is added normally.
                order_combo[order_number] = random_combo_name

            # The AI orders again.
            obtained_wait = False
            # Signifies to the cars that an order has been placed.
            ordered = True
            print(individual_orders)


def game_time(initial_start: int) -> int:
    """Keep track of how long is left of the game.

    Args:
        initial_start (int): When the game begun.

    Returns:
        time_left (int): The time left in the game.
    """
    global current_time

    # The time the game begun, plus 8 minutes (the duration of the game.)
    begin_time = initial_start + 420000
    # Seconds are calculated and converted.
    seconds = (begin_time - current_time) // 1000
    # How many minutes are left.
    minutes = seconds // 60
    # Remaining seconds are calculated.
    remaining_seconds = seconds % 60
    # Elements are combined.
    time_left = f"{minutes}:{remaining_seconds}"
    # If the time left is 0, 0 is returned.
    if time_left == f"{0}:{0}":
        time_left = 0
    return time_left


def display_cars(display: bool) -> Optional[int]:
    """Display cars representing orders.

    Args:
        display (bool): Whether to display the cars or not.

    Returns:
        Optional[int]: If the user has lost the game, the lose game state is
        returned.
    """
    global \
        ordered, \
        individual_orders, \
        cars, \
        total_orders, \
        orders_list, \
        total_items, \
        car_coords, \
        last_tick, \
        excess, \
        deleted, \
        order_number, \
        current_time, \
        order_stats

    # If an order was placed:
    if ordered:
        total_items = 0
        # The amount of orders there are is measured from the orders dict.
        total_orders = len(individual_orders)
        order_number += 1
        # The orders are converted into a list so they can be accessed with
        # index.
        orders_list = list(individual_orders.keys())
        # As index begins with 0 in python, the order to assign to the car is
        # targeted by making it a index, using the total orders -1.
        aquire_key = orders_list[total_orders - 1]
        # The specific order is then targeted with this index.
        order_stats = individual_orders[aquire_key]

        # For all the burger names and amount ordered:
        for burger_name, burger_value in order_stats.items():
            # If the burger is a double:
            if (
                burger_name == "Francie Frenzy"
                or burger_name == "2 5/4 Slammer"
                or burger_name == "Keanu Krunch"
                or burger_name == "Chicken Little"
            ):
                # Its order value is doubled.
                total_items += burger_value * 2
            # Otherwise it remains the same.
            else:
                total_items += burger_value

        # A dict is made for the current car, named using the amount of orders
        # placed.
        cars[order_number] = {}
        # Order total for the car is defined.
        print(total_items)
        cars[order_number]["order total"] = total_items
        # x initially begins as -50.
        cars[order_number]["x"] = -50
        # Initial start time for the car timer.
        cars[order_number]["car start time"] = current_time
        # The danger meter is set for the order.
        cars[order_number]["danger"] = danger_meter(total_items)
        # The amount of cars currently waiting is calculated.
        total_cars = len(cars) - 1
        # The target for the car to move is defined using the car number in
        # the line and the list of car coordinates.
        cars[order_number]["target"] = car_coords[total_cars]
        # This controls the car movement and the last time it moved.
        cars[order_number]["last tick"] = pygame.time.get_ticks()

        # Excess cars are calculated. If the total is lower than 0, it is set
        # to 0.
        excess = total_cars - 6
        if excess < 0:
            excess = 0

    # If the excess cars have reached 3, the user loses the game.
    if excess == 3:
        return ProgramState.GAME_LOST
    else:
        # For all the car numbers and their stats:
        for car_number, car_stats in cars.items():
            cars[car_number]["car time"] = body_font.render(
                (car_time((cars[car_number]["car start time"]), False)),
                True,
                (car_colour((car_time((cars[car_number]["car start time"]), True)))),
            )

            # If the car needs to move again, defined using the wait interval:
            if current_time - cars[car_number]["last tick"] >= WAIT_INTERVAL:
                # If the car hasn't reached its target:
                if cars[car_number]["x"] < cars[car_number]["target"]:
                    # It moves by 5.
                    cars[car_number]["x"] += 5
                    # Last tick is reset so the car can move again.
                    cars[car_number]["last_tick"] = current_time

        # If the cars should be displayed:
        if display:
            timer_index: int = 0
            # Each one is displayed, for the first 6 cars.
            for car_number, car_stats in cars.items():
                if timer_index < 7:
                    screen.blit(car_sized, (car_stats["x"], 10))
                    screen.blit(
                        car_stats["car time"], (dthru_text_x_positions[timer_index], 60)
                    )
                    if timer_index != 0:
                        screen.blit(
                            car_stats["danger"],
                            (danger_box_positions[timer_index - 1], 100),
                        )
                timer_index += 1

    # If a car has been deleted:
    if deleted:
        delete_index: int = 0
        # Total cars is redefined, as well as excess cars.
        total_cars = len(cars) - 1
        excess = total_cars - 6
        if excess < 0:
            excess = 0
        # The orders_list used by other functions needs to be updated too.
        orders_list = list(individual_orders.keys())
        for car_number, car_stats in cars.items():
            # Targets of all cars are updated accordingly using an index.
            car_stats["target"] = car_coords[delete_index]
            # Update stops.
            deleted = False
            delete_index += 1


def car_time(initial_start: int, return_seconds: bool) -> Union[str, int]:
    """Timer for each car.

    Args:
        initial_start (int): The time when the order was placed.
        return_seconds (bool): If the function should only return seconds.

    Returns:
        Union[str, int]: The car time in the drive thru as a string if
        return_seconds is false, otherwise the car time in seconds as a integer.
    """
    global current_time
    # Time in ms is calculated.
    time = current_time - initial_start
    # Converted to seconds.
    seconds = time // 1000
    # Seconds converted to minutes.
    minutes = seconds // 60
    # Seconds converted into seconds in a minute.
    current_seconds = seconds % 60
    # A variable is made with the current time.
    car_time = f"{minutes}:{current_seconds}"
    # If the current time should be returned:
    if not return_seconds:
        return car_time
    # Otherwise, only seconds are returned.
    else:
        return seconds


def car_colour(time: int) -> tuple:
    """Colour of the car timer.

    Args:
        time (int): Car time in the drive thru.

    Returns:
        The desired colour.
    """
    # Depending on the time, a colour is returned.
    if time < 40:
        colour = GREEN
    if time >= 40:
        colour = ORANGE
    if time >= 70:
        colour = RED
    return colour


def danger_meter(order_total: int) -> pygame.Surface:
    """Calculate danger of the order using size.

    Args:
        order_total: How big the order is.

    Returns:
        pygame.Surface: An image displaying danger.
    """
    # Depending on order size, an image of the order size is returned.
    if order_total <= 5:
        danger = miniscule_danger
    if order_total > 5 and order_total <= 9:
        danger = low_danger
    if order_total > 9 and order_total <= 13:
        danger = moderate_danger
    if order_total > 13 and order_total <= 17:
        danger = high_danger
    if order_total > 17:
        danger = extreme_danger
    return danger


def total_patty_amount(patty_name: str, current_order: bool) -> int:
    """Calculate how many patties are currently in burgers.

    Args:
        patty_name (str): The name of the patty being targeted.
        current_order (bool): If the total patty amount is being calculated for
        the current order.

    Returns:
        int: Returns how much of that patty is in made burgers, so
        needed patties can be correctly calculated.
    """
    global individual_orders, orders_list
    # Total is inititally set to 0.
    patty_total: int = 0
    # Initially, the 3 main dicts are accessed so the program can determine what
    # is needed and what isn't. The total stock of items, and burger stats for
    # each burger are accessed.
    for burger_name, burger_value in total_stock_items.items():
        for patty_type, burger_stats in burger_type.items():
            for burger_name_patties, patty_quantity in burger_stats.items():
                # If the total patties need to be displayed for the current
                # order:
                if current_order:
                    # The current order is accessed.
                    aquire_key = orders_list[0]
                    current_order_stats = individual_orders[aquire_key]
                    # Only burgers in the current order are targeted, and are
                    # matched with their patty type and name in the burger_type
                    # dict.
                    for current_item, current_quantity in current_order_stats.items():
                        if (
                            current_item == burger_name
                            and patty_name == patty_type
                            and burger_name == burger_name_patties
                        ):
                            # Because their are 2 burgers for each patty,
                            # total is added to by multiplying the amount of
                            # patties in that burger by the stock.
                            patty_total += patty_quantity * burger_value
                else:
                    # The same is done, except with the total items required
                    # dict.
                    for total_item, total_quantity in total_items_required.items():
                        # Once the patty to be targeted has been found and a
                        # burger with that matching patty has been found:
                        if (
                            patty_name == patty_type
                            and burger_name == burger_name_patties
                            and total_item == burger_name
                            # The quantity must be greater than 0, signifying
                            # they have been ordered.
                            and total_quantity > 0
                        ):
                            patty_total += patty_quantity * burger_value
    # Once the patty totals have been calculated, the total in burgers is
    # returned.
    return patty_total


def average_car_time(return_seconds: bool) -> Union[str, int]:
    """Calculate the average time to serve a car.

    Args:
        return_seconds (bool): If the function should return seconds or the full
        time.

    Returns:
        Union[str, int]: The average car time in the drive thru as a string if
        return_seconds is false, otherwise the average car time in seconds as a
        integer.
    """
    global car_served_times

    # Average is calculated.
    average = sum(car_served_times) / len(car_served_times)
    seconds = int(average)
    minutes = seconds // 60
    current_seconds = seconds % 60
    average_time = f"{minutes}:{current_seconds}"
    if not return_seconds:
        return average_time
    else:
        return seconds


def serve_items(
    edit_dict: dict[str, int], item_name: str, quantity: int, edit_patties: bool
) -> None:
    """Serve off items from dicts corresponding to the order.

    Args:
        edit_dict (dict[str, int]): The dict to be edited.
        item_name (str): The name of the item to be edited.
        quantity (int): The quantity of the item in the current order.
        edit_patties (bool): Controls if the patty totals in the dict should
        also be edited.
    """
    global burger_type

    # If the item provided is in the current dict:
    if item_name in edit_dict:
        # Its quantity in that dict is altered by subtracting the quantity in
        # the order from it.
        edit_dict[item_name] -= quantity
        if edit_patties:
            # Patties are also removed. This is not needed for the total stock
            # dict.
            for patty_type, burger_stats in burger_type.items():
                if item_name in burger_stats:
                    edit_dict[patty_type] -= burger_stats[item_name] * quantity


# CORE GAME


def main_screen_now(screen: pygame.Surface) -> None:
    """Display the core elements of the game screen.

    Args:
        screen (pygame.Surface): The current size of the game window.
    """
    # Draws the various elements on screen.
    screen.blit(background, (0, 0))
    screen.blit(main_menu_kiosk, (0, 35))
    screen.blit(game_title, (325, -25))
    screen.blit(logo_1, (400, 80))
    screen.blit(logo_2, (199, 535))
    screen.blit(version, (620, 840))


def start_order_now(
    screen: pygame.Surface, mouse_click: bool, mouse_position: tuple[int, int]
) -> int:
    """Display the start button for access to the main menu.

    Args:
        screen (pygame.Surface): The current size of the game window.
        mouse_click (bool): A bool indicating if the mouse has been clicked.
        Used for event handling.
        mouse_position (tuple[int, int]): The current position of the mouse.

    Returns:
        int: What game state the game should be in.
    """
    # Accesses the last_switch and visible variables outside the function
    # so they can be used for visiblity.
    global last_switch, visible

    # Draws elements of the screen not affected by visibility.
    screen.blit(kiosk_heading_1, (38, 55))
    screen.blit(kiosk_heading_2, (48, 90))
    screen.blit(hungry_hugo, (44, 180))

    # Calls the toggle_visibility function.
    visible = toggle_visibility(last_switch, visible, 2000, True)
    # If the toggle_visibility function returns true:
    if visible:
        # The elements are shown.
        screen.blit(start_order_1, (50, 235))
        screen.blit(start_order_2, (50, 285))
        screen.blit(start_order_3, (65, 330))
        screen.blit(start_order_4, (110, 378))
        # The button to start the users order.
        start_order_position = pygame.draw.rect(
            screen, BLACK, (44, 240, 200, 200), OUTLINE_WIDTH
        )
    if not visible:
        # The button is still clickable, but isn't visible.
        start_order_position = pygame.draw.rect(screen, WHITE, (44, 240, 200, 200))

    # The events are handled externally, checking if the user has clicked the
    # start_order button, and if they did the desired state
    # to move to is provided.
    current_event = handle_events(
        mouse_click,
        mouse_position,
        None,
        "click",
        start_order_position,
        ProgramState.MAIN_MENU,
        None,
    )
    # The state of the game is returned to the main loop so the appropiate
    # function can be called.
    return current_event


def main_menu(
    screen: pygame.Surface, mouse_click: bool, mouse_position: tuple[int, int]
) -> int:
    """Display the main menu.

    Args:
        screen (pygame.Surface): The current size of the game window.
        mouse_click (bool): A bool indicating if the mouse has been clicked.
        Used for event handling.
        mouse_position (tuple[int, int]): The current position of the mouse.

    Returns:
        int: What game state the game should be in.
    """
    global pause, wait
    # The rectangles must be defined initially so the menu_box variables can
    # draw from them and update thickness. They aren't drawn because the
    # thickness has to be continously updated first and defined.
    play_rect = pygame.Rect(40, 150, BUTTON2_WIDTH, BUTTON2_HEIGHT)
    first_shift_rect = pygame.Rect(40, 250, BUTTON2_WIDTH, BUTTON2_HEIGHT_EXTENDED)
    credits_rect = pygame.Rect(40, 380, BUTTON2_WIDTH, BUTTON2_HEIGHT)

    # The events are handled externally, checking if the user is hovering over
    # a menu_box, using the rectangles defined above. No desired event is
    # provided as the game state shouldn't change.
    menu_box_1 = handle_events(
        mouse_click, mouse_position, None, "hover", play_rect, None, None
    )
    menu_box_2 = handle_events(
        mouse_click, mouse_position, None, "hover", first_shift_rect, None, None
    )
    menu_box_4 = handle_events(
        mouse_click, mouse_position, None, "hover", credits_rect, None, None
    )

    # The buttons are now drawn now the menu_boxes have been defined.
    play = pygame.draw.rect(screen, BLACK, play_rect, menu_box_1)
    first_shift = pygame.draw.rect(screen, BLACK, first_shift_rect, menu_box_2)
    credits = pygame.draw.rect(screen, BLACK, credits_rect, menu_box_4)

    # The text is drawn.
    screen.blit(logo_3, (105, 50))
    screen.blit(play_button, (45, 150))
    screen.blit(tutorial_button_1, (45, 250))
    screen.blit(tutorial_button_2, (45, 290))
    screen.blit(credits_button, (47, 390))
    screen.blit(play_icon_sized, (198, 150))
    screen.blit(first_shift_icon_sized, (198, 270))
    screen.blit(scoreboard_icon_sized, (198, 385))

    # The event function checks if the user has clicked a button. Pause prevents
    # anything from being accidently clicked.
    if pause:
        wait += 1
    if wait > 5:
        pause = False
        current_event = handle_events(
            mouse_click,
            mouse_position,
            None,
            "click",
            play,
            ProgramState.ENTER_NAME,
            None,
        )
        if current_event == ProgramState.ENTER_NAME:
            return current_event
        current_event = handle_events(
            mouse_click,
            mouse_position,
            None,
            "click",
            credits,
            ProgramState.CREDITS,
            None,
        )
        if current_event == ProgramState.CREDITS:
            return current_event
        current_event = handle_events(
            mouse_click,
            mouse_position,
            None,
            "click",
            first_shift,
            ProgramState.TUTORIAL,
            None,
        )
        if current_event == ProgramState.TUTORIAL:
            return current_event


def credits(
    screen: pygame.Surface, mouse_click: bool, mouse_position: tuple[int, int]
) -> int:
    """Display game credits.

    Args:
        screen (pygame.Surface): The screen to display the game on.
        mouse_click (bool): A bool indicating if the mouse has been clicked.
        Used for event handling.
        mouse_position (tuple[int, int]): The current position of the mouse.

    Returns:
        int: What game state the game should be in.
    """
    global pause, wait
    # The credits are defined.
    credit_names: list[str] = [
        "Kiosk licensed from by Adobe Stock",
        "Background and Logo generated by AI",
        "Play, First Shift, Credits icons made by Freepik",
        "Back button and icons made by Freepik",
        "Traffic Lights made by macrovector on Freepik",
        "All orderable menu items made by Freepik",
        "Francie Frenzy altered by Francie (Origin from Freepik)",
        "BFM icon on BFM menu made by Smashicons on Freepik",
        "Chicken and 4:1 patties made by Freepik",
        "10:1 patty made by Erifqi Zetiawan on Freepik",
        "Angus patty made by Smashicons on Freepik",
        "Sounds used from Jayden White on YouTube",
    ]

    # The kiosk, darkened background, logo and title are displayed.
    screen.blit(name_background, (0, 0))
    screen.blit(main_menu_kiosk, (0, 35))
    screen.blit(game_title, (325, -25))
    screen.blit(logo_2, (199, 535))

    # For each credit, it is displayed.
    for credit in credit_names:
        credit_text = credits_text.render(credit, True, YELLOW)
        # Index of the item is found and it is positioned accordingly.
        screen.blit(credit_text, (290, 700 - credit_names.index(credit) * 50))

    # This is the back buttons textures.
    back = pygame.draw.rect(screen, RED, (32, 250, 220, BUTTON2_HEIGHT))
    # Text for the back button
    screen.blit(back_name_sized, (37, 255))
    screen.blit(back_name_text, (102, 250))
    # It is then checked if the button has been clicked, then if it has the user
    # returns to the main menu.
    current_event = handle_events(
        mouse_click, mouse_position, None, "click", back, ProgramState.MAIN_MENU, None
    )
    if current_event == ProgramState.MAIN_MENU:
        # Prevents first shift button from being accidently clicked.
        pause = True
        wait = 0
    return current_event


def tutorial(
    screen: pygame.Surface, mouse_click: bool, mouse_position: tuple[int, int]
) -> int:
    """Display the tutorial for the game.

    Args:
        screen (pygame.Surface): The screen to display on.
        mouse_click (bool): A bool indicating if the mouse has been clicked.
        Used for event handling.
        mouse_position (tuple[int, int]): The current position of the mouse.

    Returns:
        int: What game state the game should be in.
    """
    global skip, wait2, tutorial_select, pause, wait

    # The images for the tutorial instructions.
    tutorial_images: list = [
        tutorial_1,
        tutorial_2,
        tutorial_3,
        tutorial_5,
        tutorial_6,
        tutorial_7,
        tutorial_8,
    ]

    # The kiosk, darkened background, logo and title are displayed.
    screen.blit(name_background, (0, 0))
    screen.blit(main_menu_kiosk, (0, 35))
    screen.blit(game_title, (325, -25))
    screen.blit(logo_2, (199, 535))

    # This is the back buttons textures.
    back = pygame.draw.rect(screen, RED, (32, 250, 220, BUTTON2_HEIGHT))
    # Text for the back button
    screen.blit(back_name_sized, (37, 255))
    screen.blit(back_name_text, (102, 250))

    # The back and forwards buttons to change between tutorial parts.
    previous_coords = (80, 405)
    next_coords = (210, 400)

    screen.blit(tutorial_images[tutorial_select], (300, 300))

    if skip:
        wait2 += 1
    if wait2 > 5:
        skip = False
        # Arrows are only displayed if the user can actually go back or
        # forwards.
        if tutorial_select > 0:
            previous = previous_image.get_rect(center=previous_coords)
            screen.blit(previous_image, previous)
            scroll = handle_events(
                mouse_click, mouse_position, "click", None, previous, -1, None
            )
            # If the user scrolls backwards, the previous image is displayed,
            # and a pause variable prevents accidental double clicking.
            if scroll == -1:
                tutorial_select -= 1
                skip = True
                wait2 = 0
        if tutorial_select < 6:
            next = next_image.get_rect(center=next_coords)
            screen.blit(next_image, next)
            scroll = handle_events(
                mouse_click, mouse_position, None, "click", next, 1, None
            )
            if scroll == 1:
                tutorial_select += 1
                skip = True
                wait2 = 0
        # It is then checked if the button has been clicked, then if it has the
        # user returns to the main menu.
        current_event = handle_events(
            mouse_click,
            mouse_position,
            None,
            "click",
            back,
            ProgramState.MAIN_MENU,
            None,
        )
        # If user has clicked the back button, anther pause variable is
        # activated so the back button press isn't cancelled out by the second
        # pause variable being reset.
        if current_event == 1:
            pause = True
            wait = 0
        return current_event


def name_entry(
    screen: pygame.Surface, mouse_click: bool, mouse_position: tuple[int, int], events
) -> int:
    """Document the users name.

    Args:
        screen (pygame.Surface): The current size of the game window.
        mouse_click (bool): A bool indicating if the mouse has been clicked.
        Used for event handling.
        mouse_position (tuple[int, int]): The current position of the mouse.
        events: Each possible pygame event.

    Returns:
        int: What game state the game should be in.
    """
    # The user_name, error, and error_type variables need to be globally
    # accessed because they can't be defined within the function since they
    # need to constantly change. last_switch and visible are again accessed to
    # ensure the toggle_visibility function works properly by defining them.
    global user_name, last_switch, visible, error, error_type, expiring_items

    # The text is drawn.
    screen.blit(name_background, (0, 0))
    screen.blit(enter_name, (20, 50))
    screen.blit(enter_name_2, (40, 190))
    screen.blit(enter_name_3, (300, 290))

    # This is the back buttons textures.
    back = pygame.draw.rect(screen, RED, (370, 800, 240, BUTTON2_HEIGHT))
    # This is the outline of the back button.
    pygame.draw.rect(screen, WHITE, (370, 800, 240, BUTTON2_HEIGHT), 4)
    # Text for the back button, drawn after so the button doesn't cover it,
    screen.blit(back_name_sized, (375, 805))
    screen.blit(back_name_text, (440, 800))

    for event in events:
        # If the user types, the event handling function handles the inputs
        # appropiately.
        user_name = handle_events(
            mouse_click, mouse_position, event, "type", None, None, None
        )

        # Checks if the user clicked the back button, returning to the previous
        # menu.
        previous_event = handle_events(
            mouse_click,
            mouse_position,
            None,
            "click",
            back,
            ProgramState.MAIN_MENU,
            None,
        )
        # Checks if the user pressed enter. The desired state of GAME_MENU is
        # only used if the requirements in the handle_events function is met.
        current_event = handle_events(
            mouse_click,
            mouse_position,
            event,
            "enter",
            None,
            ProgramState.GAME_MENU,
            None,
        )

        # If the handle_events function returns one of these errors instead of
        # the desired state:
        if current_event == "error_no_name" or current_event == "error_length":
            # The error loop is set to true so the program continously displays
            # the error message even after the error has been triggered.
            error = True
            # This is used so the program can tell what error was made as there
            # are two types.
            error_type = current_event
            # visible is initially set to true so the program displays the
            # error.
            visible = True
            # The program updates last_switch with the new time since the error
            # was made.
            last_switch = pygame.time.get_ticks()

        # Only if current_event is the desired state will it return its value,
        # otherwise there would be nothing to return and an error would occur as
        # current_event can't always be returned.
        if current_event == 5:
            return current_event
        # If the handle_events function indicates to the main loop to go back a
        # stage, its value is returned.
        if previous_event:
            return previous_event

    # If an error occurs:
    if error:
        # The visible function is called again, noting repeat is False.
        visible = toggle_visibility(last_switch, visible, 3000, False)
        # If the users error was they didn't enter a name:
        if error_type == "error_no_name":
            # An error message is displayed.
            screen.blit(no_name, (200, 630))
        # If the users error was they didn't enter the correct name length:
        if error_type == "error_length":
            screen.blit(length_incorrect, (5, 630))
        # Once the toggle_visibility function returns False:
        if not visible:
            # The loop ends, and the error messages stop displaying.
            error = False

    # A font is assigned to the users name here because it changes constantly.
    username_input = name_font.render(user_name, True, DARK_YELLOW)
    # This is the users input.
    screen.blit(username_input, (30, 430))
    # Nothing is returned down here because the returns need to be within the
    # for loop.


def ingame_menu(
    screen: pygame.Surface,
    screen_width: int,
    screen_height: int,
    mouse_click: bool,
    mouse_position: tuple[int, int],
) -> int:
    """Render the base of the ingame menu.

    Args:
        screen (pygame.Surface): The current size of the game window.
        screen_width (int): The width of the screen.
        screen_height (int): The height of the screen.
        mouse_click (bool): A bool indicating if the mouse has been clicked.
        mouse_position (tuple[int, int]): The current position of the mouse.

    Returns:
        int: What game state the game should be in.
    """
    # The current screen dimensions are globally accessed so the program knows
    # what the current dimensions are. Menu list is needed to update whats on
    # the menu, and everything else is for navigation.
    global \
        current_screen_width, \
        current_screen_height, \
        total_stock_circle_x_positions, \
        total_stock_circle_y_positions, \
        menu_list, \
        money, \
        time_left, \
        excess, \
        cars, \
        deleted, \
        deleting, \
        total_items_required, \
        burger_type, \
        car_served_times, \
        total_items_ordered, \
        expiring_items

    # The below code fixes a flickering bug with content onscreen.
    # If the desired screen dimensions aren't the current dimensions:
    if (screen_width, screen_height) != (current_screen_width, current_screen_height):
        # The screen display is changed accordingly.
        screen = pygame.display.set_mode((screen_width, screen_height))
        # The current dimensions are now updated to be the same as the desired.
        current_screen_width = screen_width
        current_screen_height = screen_height

    # The box holding the cars.
    pygame.draw.rect(screen, WHITE, (0, 0, 1200, 60), DTHRU_OUTLINE)
    # Excess cars.
    excess_font = number_font.render(str(excess), True, WHITE)
    screen.blit(excess_font, (45, 0))
    screen.blit(time_text_2, (18, 60))
    screen.blit(time_text_3, (30, 100))

    # The boxes for each section on the drive thru.
    for x in dthru_box_x_positions:
        pygame.draw.rect(screen, WHITE, (x, 0, 150, 150), DTHRU_OUTLINE)
    pygame.draw.rect(screen, WHITE, (1020, 0, 180, 150), DTHRU_OUTLINE)

    # If there are orders:
    if cars:
        # The current car is found in the dict.
        current_car = next(iter(cars))
        # The order to be deleted is also defined.
        served_order = next(iter(individual_orders))
        # Its current time is taken using similar code to the display cars for
        # loop, then displayed.
        time_font = number_font.render(
            (car_time((cars[current_car]["car start time"]), False)),
            True,
            (car_colour((car_time((cars[current_car]["car start time"]), True)))),
        )
        screen.blit(time_font, (1055, 210))

        # A bool checking if the order has been completed in initally set to
        # false.
        order_complete: bool = False
        # For each required item and its quantity in the first order
        # (the dict is 2d so .values is used)
        for required_item, required_quantity in next(
            iter(individual_orders.values())
        ).items():
            # Patties are not checked.
            if required_item not in ["10:1", "4:1", "Angus", "Chicken"]:
                # If there isn't enough items in the stock compared to the
                # needed quantity for each item:
                if total_stock_items.get(required_item, 0) < required_quantity:
                    # The loop breaks and order_complete is set to false.
                    break
        # Else is attached to the for loop, so if the for loop is completley
        # completed then this happens:
        else:
            # The order is marked as completed.
            order_complete = True

        # If the order has been completed, the serve button is displayed.
        if order_complete:
            serve = time_text_5.get_rect()
            serve.topleft = (1020, 90)
            screen.blit(time_text_5, serve)
            served = handle_events(
                mouse_click, mouse_position, None, "click", serve, "clicked", None
            )
            # If the serve button was clicked:
            if served == "clicked":
                # Served car as the first in the list.
                served_car = next(iter(cars))
                # It is moved offscreen.
                cars[served_car]["target"] = 1250

                # Order is then deleted.

                # Items are scanned for in both dicts and then deleted.
                for item_name, quantity in individual_orders[served_order].items():
                    total_items_ordered += quantity
                    # For each dict to be updated, the serve function is called.
                    serve_items(total_stock_items, item_name, quantity, False)
                    serve_items(total_items_required, item_name, quantity, True)

                    # Each items price is added to the users total money.
                    for item_price_name, item_price_quantity in item_prices.items():
                        if item_name == item_price_name:
                            money += item_price_quantity * quantity

                    # Item expiry is updated.
                    for expiry_item_name, expiry_date in expiring_items.items():
                        if item_name == expiry_item_name:
                            # Depending on the quantity, expiry dates are
                            # cleared.
                            del expiry_date[:quantity]
                # The deleting process begins.
                deleting = True

        if deleting:
            # Served car needs to be redefined.
            served_car = next(iter(cars))
            # If the car has reached its target:
            if cars[served_car]["x"] == 1250:
                # Once the items have been removed from the total items required
                # dict, the order can be deleted.
                del individual_orders[served_order]
                # Its info is deleted, and control is handed to the display cars
                # function to update the rest of the cars.
                # Car serve time is taken by adding it to the list.
                car_served_times.append(
                    car_time(cars[served_car]["car start time"], True)
                )
                # The car is deleted.
                del cars[served_car]

                deleting = False
                deleted = True

    # Drawing circles for unplaced orders.
    order_circles: list[int] = [80, 180, 280, 380, 480]
    for circle_x in order_circles:
        pygame.draw.circle(screen, GREY, (circle_x, 320), 40, DTHRU_OUTLINE)
        pygame.draw.circle(screen, GREY, (circle_x, 480), 40, DTHRU_OUTLINE)

    # The current order box.
    pygame.draw.rect(screen, WHITE, (0, 150, 570, 550), DTHRU_OUTLINE)
    screen.blit(current_order_heading, (160, 150))
    pygame.draw.line(screen, WHITE, (0, 180), (570, 180), DTHRU_OUTLINE)

    # The currently needed stock display.
    current_order_display()

    # The section is for patties.
    pygame.draw.line(screen, WHITE, (0, 590), (567, 590), DTHRU_OUTLINE)

    # This is the total stock section.
    pygame.draw.rect(screen, WHITE, (570, 150, 450, 550), DTHRU_OUTLINE)
    # The box containing the section name.
    pygame.draw.line(screen, WHITE, (570, 180), (1020, 180), DTHRU_OUTLINE)
    screen.blit(total_stock_heading, (700, 150))

    # A for loop drawing all of the circles for the total stock.
    for y in total_stock_circle_y_positions:
        for x in total_stock_circle_x_positions:
            pygame.draw.circle(screen, WHITE, (x, y), 35, DTHRU_OUTLINE)

    # A function is called used to increase efficency.
    # Text for all the circles.
    display_menu_items([615, 715, 815, 915], [265, 445], 0, 7, "text")
    # Text for all the patties.
    display_menu_items([665, 865], [350, 530], 8, 11, "text")
    # Patty images.
    display_menu_items([662, 862], [300, 480], 8, 11, "image")
    # Burger images.
    display_menu_items([615, 715, 815, 915], [205, 385], 0, 7, "image")
    # Fries, nuggets and drinks images.
    display_menu_items([600, 760, 920], [570], 12, 14, "image")
    # FNG text.
    display_menu_items([612, 772, 932], [640], 12, 14, "text")

    # This is the navigation section.
    # These need to be updated constantly as the variables change.
    # Money is rounded to 2 dp.
    money = round(money, 2)

    money_earnt = money_font.render("$" + str(money), True, WHITE)
    time_left_font = number_font.render(str(time_left), True, WHITE)

    # If a car has been served, the average is displayed.
    if car_served_times:
        average_car_time_font = number_font.render(
            average_car_time(False), True, car_colour(average_car_time(True))
        )
        screen.blit(average_car_time_font, (1055, 290))

    pygame.draw.rect(screen, WHITE, (1020, 150, 180, 550), DTHRU_OUTLINE)
    pygame.draw.line(screen, WHITE, (1020, 180), (1200, 180), DTHRU_OUTLINE)

    # Text for navigation is displayed.
    screen.blit(navigation_heading, (1023, 150))
    screen.blit(current_car_heading, (1030, 190))
    screen.blit(average_car_heading, (1070, 270))
    screen.blit(money_heading, (1050, 350))
    screen.blit(money_earnt, (1035, 370))
    screen.blit(time_heading, (1065, 430))
    screen.blit(time_left_font, (1055, 450))

    # Buttons for navigating menus.
    grill = pygame.draw.rect(screen, RED, (1040, 510, 55, 55))
    pygame.draw.rect(screen, WHITE, (1040, 510, 55, 55), 4)
    drinks = pygame.draw.rect(screen, BLUE, (1125, 510, 55, 55))
    pygame.draw.rect(screen, WHITE, (1125, 510, 55, 55), 4)
    bfm = pygame.draw.rect(screen, DARK_YELLOW, (1040, 590, 140, 35))
    pygame.draw.rect(screen, WHITE, (1040, 590, 140, 35), 4)

    # Icons.
    screen.blit(grill_icon, (1047, 518))
    screen.blit(drinks_icon, (1132, 518))
    screen.blit(fries_icon, (1075, 590))
    screen.blit(nuggets_icon, (1110, 590))

    # Button descriptions.
    screen.blit(grill_heading, (1055, 565))
    screen.blit(drinks_heading, (1132, 565))
    screen.blit(bfm_heading, (1097, 620))

    # For each menu button, the program checks if it has been clicked.
    # If it has been, its value is returned. Otherwise, it checks if another
    # button was clicked.
    # This can't be made more efficent as the program needs to check and
    # redefine one at a time.
    current_event = handle_events(
        mouse_click, mouse_position, None, "click", drinks, ProgramState.DRINKS, None
    )
    if current_event == ProgramState.DRINKS:
        return current_event
    current_event = handle_events(
        mouse_click, mouse_position, None, "click", grill, ProgramState.GRILL, None
    )
    if current_event == ProgramState.GRILL:
        return current_event
    current_event = handle_events(
        mouse_click, mouse_position, None, "click", bfm, ProgramState.BFM, None
    )
    if current_event == ProgramState.BFM:
        return current_event

    # Item expiry is checked.
    expiry()
    # As menu_list is the variable being used to display the items, it is
    # updated.
    menu_list = list(total_stock_items.items())


def display_menu_items(
    x_positions: list[int],
    y_positions: list[int],
    initial_index: int,
    max_index: int,
    display_type: str,
) -> None:
    """Display the menu images and text for the total stock.

    Args:
        x_positions (list[int]): The x positions of the items to draw.
        y_positions (list[int]): The y positions of the items to draw.
        initial_index (int): The item the function should begin on the
        dict/list.
        max_index (int): The item the function should end the cycle on the
        dict/list.
        display_type (str): Whether the item is an image or piece of text to
        indicate how to place it.
    """
    # The menu in text and image form need to be accessed so the function knows
    # what to display using indexing.
    global menu_images, total_items_required, total_stock_items, burger_type

    # A nested for loop is used to display everything in a grid format.
    for y in y_positions:
        for x in x_positions:
            # The function keeps cycling until it reaches the specified end.
            if initial_index <= max_index:
                # If the function is displaying text:
                if display_type == "text":
                    # The quantity positions are set.
                    quantity_x: int = x + 21
                    quantity_y: int = y + 20
                    # The item name and quantity is taken from the dict with the
                    # provided index.
                    item_name, item_quantity = menu_list[initial_index]
                    # For each item in game:
                    for burger_name, burger_value in total_items_required.items():
                        # The item is matched between the 2 dicts.
                        if burger_name == item_name:
                            # Quantity is determined by taking the stock minus
                            # the required amount.
                            total_item_quantity = item_quantity - burger_value

                    # If the item is a patty, it needs special treatment because
                    # some patties can already be in burgers and therefore don't
                    # need to be made.
                    for patty_type, burger_stats in burger_type.items():
                        if item_name == patty_type:
                            # A function is used to determine this, then the
                            # patties already in burgers are added to the
                            # quantity needed.
                            total_item_quantity += total_patty_amount(item_name, False)

                    # A variable assigned to the indexed name and quantity is
                    # made with the appropiate font.
                    item_name_text = total_stock_name_font.render(
                        item_name, True, WHITE
                    )
                    item_quantity_text = stock_required_font.render(
                        str(total_item_quantity), True, WHITE
                    )
                    # Its width is then calculated so it can be centered
                    # correctly. 49 is the length of the shortest item,
                    # so it is used as a baseline.
                    item_width = (item_name_text.get_width() - 49) / 2
                    quantity_width = (item_quantity_text.get_width() - 8) / 2
                    # The item is produced on screen with its centering.
                    screen.blit(item_name_text, (x - item_width, y))
                    screen.blit(
                        item_quantity_text, (quantity_x - quantity_width, quantity_y)
                    )
                    # The count is increased so a new variable can be displayed.
                    initial_index += 1

                # If the image needs to be displayed:
                if display_type == "image":
                    # The current image to be obtained is taken from the global
                    # list.
                    current_image = menu_images[initial_index]
                    # The image is displayed using the given x and y.
                    screen.blit(current_image, (x, y))
                    # Cycles to the next item.
                    initial_index += 1


def creation_menu(
    station_names: list[str],
    menu_name: str,
    menu_image: pygame.Surface,
    order_icons: list[pygame.Surface],
    creation_icons: list[pygame.Surface],
    item_names: list[str],
    timer_duration: list[int],
    mouse_click: bool,
    mouse_position: tuple[int, int],
    x_positions: list[int] = [40, 430, 820],
    y_positions: list[int] = [170, 430],
    button_radius: int = 80,
) -> int:
    """Render the menu to make items.

    Args:
        station_names (list[str]): The name of each indivdual station.
        menu_name (str): The name of the current menu.
        menu_image (pygame.Surface): The image representing the menu.
        order_icons (list[pygame.Surface]): The icons for each possible item
        which can be ordered.
        creation_icons (list[pygame.Surface]): The icon for the item when it has
        been made.
        item_names (list[str]): Each items name in the menu.
        timer_duration (list[int]): The duration for each items timer.
        mouse_click (bool): A bool indicating if the mouse has been clicked.
        mouse_position (tuple[int, int]): The current position of the mouse.
        x_positions (list[int]): X Positions to position the station
        at. Defaults to [40, 430, 820].
        y_positions (list[int]): Y Positions to position the station
        at. Defaults to [170, 430].
        button_radius (int): The radius of the button to make items.
        Defaults to 80.

    Returns:
        int: What game state the game should be in.
    """
    # The status of each station needs to be globally accessed so it can be
    # maintained. The same goes for pause and wait, and the menu list needs to
    # be accessed so its quantities can be updated.
    global \
        station_status, \
        pause, \
        wait, \
        menu_list, \
        grill_names, \
        grill_creation, \
        grill_timers, \
        bfm_names, \
        bfm_creation, \
        bfm_timers, \
        skip, \
        wait2, \
        state, \
        money, \
        burger_type, \
        last_switch, \
        visible, \
        error, \
        patty_needed, \
        quantity_patty_needed, \
        current_time, \
        orders_list


    # Totals for each patty.
    patty_totals: dict[str, int] = {type: 0 for type in burger_type}
    # A 2D Dictionary is used for keeping track of each menus station statuses
    # so they don't get muddled up. If a dictionary has not been created under
    # the menu name, one is made.
    if menu_name not in station_status:
        station_status[menu_name] = {}

    # The menu name is displayed using the input supplied.
    menu = heading_font.render(menu_name, True, WHITE)
    # The line seperating the menu name and requirements from the creation.
    pygame.draw.line(screen, WHITE, (0, 150), (1200, 150))
    # The line dividing the menu name and requirements.
    pygame.draw.line(screen, WHITE, (358, 0), (358, 150))
    # The line dividing the total and current requirements.
    pygame.draw.line(screen, WHITE, (358, 75), (1200, 75))

    # Ensures the menu text is centered.
    name_width = (menu.get_width() - 78) / 2
    screen.blit(menu, (135 - name_width, 10))

    # Displays menu icons.
    screen.blit(menu_image, (10, 12))
    screen.blit(menu_image, (280, 12))
    # This is the back buttons textures.
    back = pygame.draw.rect(screen, RED, (20, 80, 150, BUTTON2_HEIGHT))
    # This is the outline of the back button.
    pygame.draw.rect(screen, WHITE, (20, 80, 150, BUTTON2_HEIGHT), 4)
    # Text for the back button, drawn after so the button doesn't cover it,
    screen.blit(back_name_sized, (25, 83))
    screen.blit(back_name_text_xs, (70, 90))

    if menu_name != "Drinks":
        if menu_name != "Make Grill" and menu_name != "Make BFM":
            # This is the create buttons textures.
            create = pygame.draw.rect(screen, BLUE, (190, 80, 150, BUTTON2_HEIGHT))
            screen.blit(create_name_text_xs, (197, 90))
        if menu_name != "Grill" and menu_name != "BFM":
            # Item expiry is checked.
            expiry()
            cook = pygame.draw.rect(screen, BLUE, (190, 80, 150, BUTTON2_HEIGHT))
            screen.blit(cook_name_text_xs, (197, 90))
        pygame.draw.rect(screen, WHITE, (190, 80, 150, BUTTON2_HEIGHT), 4)
        screen.blit(forward_sized, (285, 80))

    # Heading text for order requirements.
    screen.blit(current_requirements, (370, 7))
    screen.blit(total_requirements, (370, 77))

    # Index is initially set to 0 to cycle from the start. Multiple are needed
    # for the various for loops.
    index: int = 0
    image_index: int = 0
    text_index: int = 0
    creation_index: int = 0
    quantity_index: int = 0

    # This for loop is for the images when displaying the order stats.
    for image in order_icons:
        # Replace needed_juice with proper variable
        # For each image, it is moved by 50 to the right. The icon is displayed
        # by cycling through the provided list.
        screen.blit(order_icons[image_index], (585 + image_index * 110, 8))
        # For total requirements (replace needed juice)
        screen.blit(order_icons[image_index], (535 + image_index * 110, 80))
        image_index += 1

    # Because the names provided have \n in their name, this piece of code
    # replaces \n with a space so they can be compared properly.
    proper_items = [name.replace("\n", " ") for name in item_names]

    # If there are orders:
    if orders_list:
        # The current order is aquired for the current order display.
        aquire_key = orders_list[0]
        if aquire_key in individual_orders:
            current_order_stats = individual_orders[aquire_key]

            # For each item and its quantity in the current order:
            for current_item, current_quantity in current_order_stats.items():
                # If the user is in the grill menu:
                if menu_name == "Grill":
                    for patty_type, burger_stats in burger_type.items():
                        # Each patty other than chicken is calculated and
                        # stored in a dict.
                        if patty_type != "Chicken":
                            # The item is matched with one of the burgers:
                            if current_item in burger_stats:
                                # Then its patty is taken and stored in the dict
                                # holding patties. Patties are checked for in
                                # burgers so the user doesn't think they have to
                                # make them again.
                                patty_totals[patty_type] += (
                                    current_quantity * burger_stats[current_item]
                                    - total_patty_amount(patty_type, True)
                                )

                # If the menu is not grill:
                else:
                    # For each item in the current station:
                    for actual_item in proper_items:
                        if actual_item == current_item:
                            # The index is aquired so it can be displayed at the
                            # correct place.
                            quantity_index = proper_items.index(actual_item)

                            # Quantity is defined.
                            quantity = current_quantity - total_stock_items[actual_item]
                            # If quantity required has gone under 0:
                            if quantity < 0:
                                # Rather than showing negative, it shows 0.
                                quantity = 0

                            # Text is defined then displayed at the index point.
                            current_item_text = main_menu_options_xs.render(
                                ("x" + str(quantity)),
                                True,
                                WHITE,
                            )
                            screen.blit(
                                current_item_text, (530 + quantity_index * 110, 15)
                            )

                    # The chicken patty burgers are specially accessed because
                    # the chicken patty is shown in a regular menu instead of
                    # the patty menu.
                    for chicken_burger, value in burger_type["Chicken"].items():
                        # If the item is one of the chicken burgers, chicken is
                        # updated accordingly.
                        if current_item == chicken_burger:
                            patty_totals["Chicken"] += (
                                current_quantity * value
                                - total_patty_amount("Chicken", True)
                            )

            # Once all chicken patties have been accumulated, then they are
            # displayed.
            if patty_totals["Chicken"] > 0:
                # Ensures chicken patties are not displayed for other menus
                # other than BFM.
                if menu_name == "BFM":
                    quantity = patty_totals["Chicken"] - total_stock_items["Chicken"]
                    if quantity < 0:
                        quantity = 0

                    current_item_text = main_menu_options_xs.render(
                        ("x" + str(quantity)),
                        True,
                        WHITE,
                    )
                    screen.blit(current_item_text, (530 + 2 * 110, 15))

            # For each patty in the total dict:
            for patty_type, total_quantity in patty_totals.items():
                # As long as there is something to display:
                if total_quantity > 0:
                    if patty_type != "Chicken":
                        # The patty position in the dict is got so it can be
                        # displayed at the appropiate place.
                        patty_type_index = list(burger_type.keys()).index(patty_type)

                        quantity = total_quantity - total_stock_items[patty_type]
                        if quantity < 0:
                            quantity = 0

                        # The needed patties are calculated and put into a font,
                        # then displayed.
                        current_item_text = main_menu_options_xs2.render(
                            ("x" + str(quantity)),
                            True,
                            WHITE,
                        )
                        screen.blit(
                            current_item_text, (530 + patty_type_index * 110, 15)
                        )

        # This section is for the total section.

        # A list of each item is aquired so the index can be properly determined
        # and so the item can be properly located without the value interfering.
        menu_list_names = [item[0] for item in menu_list]
        # Quantity has to be initially defined.
        display_stock_quantity: int = 0

        # For each item in the current station:
        for actual_item in proper_items:
            # For each item and its quantity in the required items:
            for total_item_name, total_item_quantity in total_items_required.items():
                # The item is targeted using the list of items.
                if actual_item in menu_list_names:
                    # Where to display the quantity is got using the current
                    # items position in the station display parameters.
                    quantity_display_index = proper_items.index(actual_item)
                    # The position of the item in the menu is got.
                    quantity_stock_index = menu_list_names.index(actual_item)
                    # The value and item name is then found using this index.
                    total_stock_name, total_stock_quantity = menu_list[
                        quantity_stock_index
                    ]

                    # The item in the required list is matched with the item in
                    # the menu.
                    if total_item_name == total_stock_name:
                        # Quantity is then defined.
                        display_stock_quantity = (
                            total_item_quantity - total_stock_quantity
                        )

            # This code checks for patties currently in burgers, and alters the
            # quantity correspondingly.
            for patty_type, burger_stats in burger_type.items():
                if actual_item in menu_list_names:
                    if actual_item == patty_type:
                        display_stock_quantity -= total_patty_amount(actual_item, False)

            # If current stock is below 0, it is displayed as 0.
            if display_stock_quantity < 0:
                display_stock_quantity = 0

            # Text is defined and printed.
            total_item_text = main_menu_options_xs.render(
                ("x" + str(display_stock_quantity)), True, WHITE
            )
            screen.blit(total_item_text, (480 + quantity_display_index * 110, 85))

    # A similar loop to the previous, except if the item name requires two lines
    # extra code is added to manually split it.
    for item in item_names:
        # This code splits anything which takes up two lines.
        lines = item.split("\n")
        # This is the position of the text on the y axix. It needs to be in a
        # variable so the new line can be put on a different y.
        y_offset: int = 40
        # For each of the split lines:

        for line in lines:
            # The item is defined and drawn.
            item_surface = item_font.render(line, True, WHITE)
            # Code for making sure text is centered.
            item_width = (item_surface.get_width() - 24) / 2
            screen.blit(item_surface, (590 - item_width + text_index * 110, y_offset))
            screen.blit(
                item_surface, (540 - item_width + text_index * 110, y_offset + 75)
            )
            # Y is updated accordingly to how big the line is.
            y_offset += item_font.get_linesize()
        text_index += 1

    # A similar loop used in the above function.
    for y in y_positions:
        for x in x_positions:
            # Lines are drawn based off the provided positions.
            pygame.draw.line(
                screen, WHITE, (x, y + 50), (x + 298, y + 50), DTHRU_OUTLINE
            )
            pygame.draw.line(
                screen, WHITE, (x + 90, y + 50), (x + 90, y + 248), DTHRU_OUTLINE
            )
            # Each station is assigned its unique name based on the index so it
            # can be individually targeted.
            station_name = f"Station{index}"
            # The size of each box.
            station_outline = pygame.Rect(x, y, 300, 250)
            button_outline = (x + 193, y + 150)
            # The name of the box, using the list provided.
            station = f"Station #{index + 1}: {station_names[index]}"
            # A variable assigned to this name is made.
            station_surface = navigation_font.render(station, True, WHITE)
            # The local status variable, used in event handling.
            status: int = 0

            # If a station has not yet been added to the global dictionary
            # controlling status (inside the corresponding menu), it is added.
            if station_name not in station_status[menu_name]:
                station_status[menu_name][station_name] = {
                    "status": 0,
                    "end_time": None,
                    "check_patty_requirements": False,
                    "expiry_time": None,
                    "play_sound": False,
                    "cooked": pygame.mixer.Sound("sounds/cooked.mp3"),
                    "log_expiry_time": True,
                }

            # Each rectangles name is assigned to a dictionary as a key with
            # the following values:
            station_bases[station_name] = {
                "station_outline": station_outline,
                "station": station,
                "station_surface": station_surface,
                "button_outline": button_outline,
                "status": status,
            }
            # Index moves up one to go to the next item on the list.
            index += 1

    for station_name, rect_info in station_bases.items():
        # For each rectangle, its value is accessed and utilized.
        # A variable is set to the current station so it can have its quantity
        # updated.
        item_station = station_names[creation_index]
        # The time to make each item is stored from the provided values and
        # indexing through them.
        creation_time = timer_duration[creation_index]
        # If clicking inputs are paused:
        if pause is True:
            # A variable used to stall the input is activated which goes up
            # every time this function repeats.
            wait += 1
        # A second different variable is used for menu switching between cook
        # and create to not interfere with the other variable.
        if skip is True:
            wait2 += 1
        # After 20 repeats:
        if wait > 20:
            # Inputs are unpaused.
            pause = False
        if wait2 > 20:
            skip = False

        # The local status variable is defined by using the event handling to
        # check if the circle has been clicked. If inputs aren't paused:
        if not pause:
            # The local status is defined by checking if the circle has been
            # clicked.
            rect_info["status"] = handle_events(
                mouse_click,
                mouse_position,
                None,
                "click",
                rect_info["button_outline"],
                1,
                rect_info["status"],
                create_button=True,
            )

        # If the local variable is changed to 1 but the global one hasn't been
        # changed yet:
        if (
            rect_info["status"] == 1
            and station_status[menu_name][station_name]["status"] == 0
        ):
            # It is updated to 1.
            station_status[menu_name][station_name]["status"] = 1
            # The time for the timer to end is made using the current time plus
            # the specified duration.
            station_status[menu_name][station_name]["end_time"] = (
                current_time + creation_time
            )

        # The rectangle is drawn based on its previous definition.
        pygame.draw.rect(screen, WHITE, rect_info["station_outline"], DTHRU_OUTLINE)

        # If the menu is not drinks:
        if (
            menu_name != "Drinks"
            and menu_name != "Make Grill"
            and menu_name != "Make BFM"
        ):
            # The boxes for toggling.
            toggle1 = pygame.draw.rect(
                screen,
                RED,
                (
                    rect_info["station_outline"].x + 320,
                    rect_info["station_outline"].y + 20,
                    50,
                    50,
                ),
            )
            pygame.draw.rect(
                screen,
                WHITE,
                (
                    rect_info["station_outline"].x + 320,
                    rect_info["station_outline"].y + 20,
                    50,
                    50,
                ),
                DTHRU_OUTLINE,
            )
            screen.blit(
                order_icons[0],
                (
                    rect_info["station_outline"].x + 327,
                    rect_info["station_outline"].y + 27,
                ),
            )
            toggle2 = pygame.draw.rect(
                screen,
                RED,
                (
                    rect_info["station_outline"].x + 320,
                    rect_info["station_outline"].y + 100,
                    50,
                    50,
                ),
            )
            pygame.draw.rect(
                screen,
                WHITE,
                (
                    rect_info["station_outline"].x + 320,
                    rect_info["station_outline"].y + 100,
                    50,
                    50,
                ),
                DTHRU_OUTLINE,
            )
            screen.blit(
                order_icons[1],
                (
                    rect_info["station_outline"].x + 327,
                    rect_info["station_outline"].y + 107,
                ),
            )
            toggle3 = pygame.draw.rect(
                screen,
                RED,
                (
                    rect_info["station_outline"].x + 320,
                    rect_info["station_outline"].y + 180,
                    50,
                    50,
                ),
            )
            pygame.draw.rect(
                screen,
                WHITE,
                (
                    rect_info["station_outline"].x + 320,
                    rect_info["station_outline"].y + 180,
                    50,
                    50,
                ),
                DTHRU_OUTLINE,
            )
            screen.blit(
                order_icons[2],
                (
                    rect_info["station_outline"].x + 327,
                    rect_info["station_outline"].y + 187,
                ),
            )

        # If the station status is hasn't been clicked:
        if station_status[menu_name][station_name]["status"] == 0:
            # If the user doesn't have enough patties:
            if error:
                # This same line is used for the error message in the
                # name_entry function.
                visible = toggle_visibility(last_switch, visible, 3000, False)
                # Burger requirements are displayed using the global variables
                # provided by the code in status 1.
                burger_requirement = start_order_font.render(
                    str("MAKE " + str(quantity_patty_needed) + " MORE " + patty_needed),
                    True,
                    RED,
                )
                screen.blit(burger_requirement, (300, 300))
                # The error message is stopped when the visiblity timer runs
                # out.
                if not visible:
                    error = False

            # Variables are prepared for use by initally setting them to True.
            station_status[menu_name][station_name]["check_patty_requirements"] = True
            station_status[menu_name][station_name]["play_sound"] = True
            # The start circle is drawn with its respective elements.
            pygame.draw.circle(
                screen, GREEN, rect_info["button_outline"], button_radius
            )
            pygame.draw.circle(
                screen, WHITE, rect_info["button_outline"], button_radius, DTHRU_OUTLINE
            )
            screen.blit(
                button_start,
                (
                    rect_info["station_outline"].x + 135,
                    rect_info["station_outline"].y + 130,
                ),
            )
            # The traffic light is set to red and the status to standby for
            # later use.
            light = redlight_sized
            creation_status = status_standby

            # For every menu but drinks:
            if (
                menu_name != "Drinks"
                and menu_name != "Make Grill"
                and menu_name != "Make BFM"
            ):
                # The program checks if the first button was toggeled.
                toggle = handle_events(
                    mouse_click,
                    mouse_position,
                    None,
                    "click",
                    toggle1,
                    "toggeled1",
                    None,
                )
                if toggle == "toggeled1":
                    # If it was, and the user is on the grill menu, the station
                    # is updated respectivley.
                    if menu_name == "Grill":
                        grill_names[creation_index] = "10:1"
                        grill_creation[creation_index] = hugopatty_creation_icon
                        grill_timers[creation_index] = 9000
                    # Same goes for BFM.
                    elif menu_name == "BFM":
                        bfm_names[creation_index] = "Fries"
                        bfm_creation[creation_index] = fries_creation_icon
                        bfm_timers[creation_index] = 6000
                # Same code repeats for the other buttons. This can't be made
                # more efficent due to the different valeus for each and the
                # need to go 1 by 1 through the buttons.
                toggle = handle_events(
                    mouse_click,
                    mouse_position,
                    None,
                    "click",
                    toggle2,
                    "toggeled2",
                    None,
                )
                if toggle == "toggeled2":
                    if menu_name == "Grill":
                        grill_names[creation_index] = "4:1"
                        grill_creation[creation_index] = slammerpatty_creation_icon
                        grill_timers[creation_index] = 9000
                    elif menu_name == "BFM":
                        bfm_names[creation_index] = "McBullets"
                        bfm_creation[creation_index] = mcbullets_creation_icon
                        bfm_timers[creation_index] = 7000
                toggle = handle_events(
                    mouse_click,
                    mouse_position,
                    None,
                    "click",
                    toggle3,
                    "toggeled3",
                    None,
                )
                if toggle == "toggeled3":
                    if menu_name == "Grill":
                        grill_names[creation_index] = "Angus"
                        grill_creation[creation_index] = anguspatty_creation_icon
                        grill_timers[creation_index] = 15000
                    if menu_name == "BFM":
                        bfm_names[creation_index] = "Chicken"
                        bfm_creation[creation_index] = chicken_creation_icon
                        bfm_timers[creation_index] = 8000

        # If an item is being made:
        if station_status[menu_name][station_name]["status"] == 1:
            # The program checks if the burger has the correct patty
            # requirements.
            if station_status[menu_name][station_name]["check_patty_requirements"]:
                # Only for the creation stations:
                if menu_name == "Make Grill" or menu_name == "Make BFM":
                    # For each patty type, and the burgers stats:
                    for patty_type, burger_stats in burger_type.items():
                        # For the burger name and its required amount of
                        # patties:
                        for burger_name, patty_requirements in burger_stats.items():
                            # The current station is individually targeted by
                            # checking the current item station name.
                            if burger_name == item_station:
                                # If the requirements are greater than what the
                                # user has:
                                if patty_requirements > total_stock_items[patty_type]:
                                    # The specific patty needed is defined for
                                    # code in status 0. (display)
                                    patty_needed = patty_type
                                    # The quantity needed is calculated.
                                    quantity_patty_needed = (
                                        patty_requirements
                                        - total_stock_items[patty_type]
                                    )
                                    # The program alerts itself of the error.
                                    visible = True
                                    error = True
                                    # Used to correctly display the error for 3
                                    # seconds.
                                    last_switch = pygame.time.get_ticks()
                                    # Status is returned to 0.
                                    station_status[menu_name][station_name][
                                        "status"
                                    ] = 0
                                # If the user has the correct amount of patties:
                                else:
                                    # The program stops checking if that station
                                    # needs its patties checked.
                                    station_status[menu_name][station_name][
                                        "check_patty_requirements"
                                    ] = False
                                    # The erorr message disappears.
                                    visible = False
                                    # The patty is taken off the users stock,
                                    # and the expiry tracker.
                                    total_stock_items[patty_type] -= patty_requirements
                                    del expiring_items[patty_type][:patty_requirements]
                                    # Display of stock is updated.
                                    menu_list = list(total_stock_items.items())

            # The elapsed time is calculated for the timer to draw off.
            elapsed_time = current_time - (
                station_status[menu_name][station_name]["end_time"] - creation_time
            )
            # The draw timer function is called.
            draw_timer(
                screen,
                elapsed_time,
                creation_time,
                rect_info["button_outline"],
                button_radius,
            )
            # These are again set to something else.
            light = yellowlight_sized
            creation_status = status_wait
            # Makes sure the program correctly logs expiry time.
            if menu_name == "Grill" or menu_name == "BFM":
                if station_status[menu_name][station_name]["play_sound"]:
                    # Sound is played.
                    cooking_sfx.play()
                    station_status[menu_name][station_name]["play_sound"] = False

        # If the item has been made:
        if station_status[menu_name][station_name]["status"] == 2:
            # The text saying to click.
            screen.blit(
                creation_click,
                (
                    rect_info["station_outline"].x + 174,
                    rect_info["station_outline"].y + 220,
                ),
            )
            # A rect of the image of the menu item is aquired. This is used for
            # both centering and click detection.
            item_rect = creation_icons[creation_index].get_rect(
                center=rect_info["button_outline"]
            )
            # Depending on what the item is based on the index, it is displayed
            # at the center of the button outline.
            screen.blit(creation_icons[creation_index], item_rect)
            # Text is changed.
            light = greenlight_sized
            creation_status = status_ready

            # Checks if the item was clicked or not.
            rect_info["status"] = handle_events(
                mouse_click,
                mouse_position,
                None,
                "click",
                item_rect,
                0,
                None,
                None,
            )

            # If it was:
            if (
                rect_info["status"] == 0
                and station_status[menu_name][station_name]["status"] == 2
            ):
                # Cooking sound is stopped.
                station_status[menu_name][station_name]["cooked"].stop()
                # Status is reverted to the original.
                station_status[menu_name][station_name]["status"] = 0
                # A pause timer is activated so the creation button isn't
                # accidently clicked.
                wait = 0
                pause = True
                total_stock_items[item_station] += 1
                cost_to_make = production_cost[item_station]
                money -= cost_to_make
                # As the items are accessed indirectly through this list, it
                # needs to be updated.
                menu_list = list(total_stock_items.items())
                # The time when the item was added to track expiry.
                time_added = pygame.time.get_ticks()
                # If the item already exists in the expiry dict, a new value is
                # added to that item.
                if item_station in expiring_items:
                    expiring_items[item_station].append(time_added)
                    # Otherwise the item is added.
                else:
                    expiring_items[item_station] = [time_added]

        # The text is drawn, being a certain amount of pixels away from the rect
        # itself for a consistent baseline.
        status_width = (creation_status.get_width() - 46) / 2
        screen.blit(
            rect_info["station_surface"],
            (rect_info["station_outline"].x + 10, rect_info["station_outline"].y + 10),
        )
        screen.blit(
            status_heading,
            (rect_info["station_outline"].x + 10, rect_info["station_outline"].y + 60),
        )
        # These draw off what mode the station is in, defined earlier.
        screen.blit(
            creation_status,
            (
                rect_info["station_outline"].x + 23 - status_width,
                rect_info["station_outline"].y + 90,
            ),
        )
        screen.blit(
            light,
            (rect_info["station_outline"].x + 20, rect_info["station_outline"].y + 110),
        )
        creation_index += 1

    # If the user wishes to go back, the handle events function checks
    # if the button has been clicked.
    previous_event = handle_events(
        mouse_click, mouse_position, None, "click", back, ProgramState.GAME_MENU, None
    )
    if previous_event == ProgramState.GAME_MENU:
        # Depending on if the program is in a creation menu or cooking menu,
        # state = 5 also has to be done so the program knows to go back, due to
        # the constant switching between current_state and state. Fixes a bug
        # with the back button not working.
        state = 5
        return previous_event

    # For every menu but drinks (because drinks can't switch to create) the
    # below code executes.
    if menu_name != "Drinks":
        # 'skip' has the same function as 'pause' but they have to be seperate
        # as they are used for different things at the same time. It prevents
        # the button from being accidently clicked, like pause.
        if not skip:
            # If the menu is currently Grill:
            if menu_name == "Grill":
                # The program checks if the create button was clicked.
                current_event = handle_events(
                    mouse_click,
                    mouse_position,
                    None,
                    "click",
                    create,
                    ProgramState.MAKE_GRILL,
                    None,
                )
                # If it was:
                if current_event == ProgramState.MAKE_GRILL:
                    # Skip and wait2 are reset and the change is returned to
                    # the main loop.
                    skip = True
                    wait2 = 0
                    visible = False
                    return current_event
            # Same code repeats with different variables. They have to be
            # seperate to work and return properly.
            if menu_name == "BFM":
                current_event = handle_events(
                    mouse_click,
                    mouse_position,
                    None,
                    "click",
                    create,
                    ProgramState.MAKE_BFM,
                    None,
                )
                if current_event == ProgramState.MAKE_BFM:
                    skip = True
                    wait2 = 0
                    # Gets rid of the current error message.
                    visible = False
                    return current_event
            if menu_name == "Make Grill":
                current_event = handle_events(
                    mouse_click,
                    mouse_position,
                    None,
                    "click",
                    cook,
                    ProgramState.GRILL,
                    None,
                )
                if current_event == ProgramState.GRILL:
                    skip = True
                    wait2 = 0
                    visible = False
                    return current_event
            if menu_name == "Make BFM":
                current_event = handle_events(
                    mouse_click,
                    mouse_position,
                    None,
                    "click",
                    cook,
                    ProgramState.BFM,
                    None,
                )
                if current_event == ProgramState.BFM:
                    skip = True
                    wait2 = 0
                    visible = False
                    return current_event

def constant_creation_menu() -> None:
    """Manage variables that the creation menu uses constantly, even if the user
    isn't on it.
    """
    global station_status, current_time
    for menu_name, station_stats in station_status.items():
        for station_name, station_info in station_stats.items():
            # If the global status is 1 and the timer has expired
            # (returning True):
            if station_info["status"] == 1 and timer(station_info["end_time"]):
                # Status is sent back to the next stage.
                station_info["status"] = 2
                station_info["log_expiry_time"] = True

            # If the item has been made:
            if station_info["status"] == 2:
                if menu_name == "Grill" or menu_name == "BFM":
                    # If the user is on a menu where items can expire:
                    if station_info["log_expiry_time"]:
                        station_info["expiry_time"] = current_time + 5000
                        # The program no longer logs the expiry time, as it only
                        # needs it once.
                        station_info["log_expiry_time"] = False

                    # The system plays the cooked sound effect. A variable in
                    # the 2D Dict is used so it can be looped and stopped at
                    # will.
                    if not station_info["play_sound"]:
                        station_info["cooked"].play(100)
                        station_info["play_sound"] = True
                        # If the item has expired:

                    if timer(station_info["expiry_time"]):
                        station_info["status"] = 0
                        if station_info["play_sound"]:
                            # Cooked sound is stopped.
                            station_info["cooked"].stop()
                            # Burnt sound effect is played.
                            burnt_sfx.play()
                            station_info["play_sound"] = False

def current_order_display() -> None:
    """Display the items required for the current order."""

    global orders_list, menu_list, total_stock_items, burger_type, order_combo

    # The list of circle positions.
    circle_position: list[int] = [80, 180, 280, 380, 480, 80, 180, 280, 380, 480]
    # The list of image positions.
    image_position: list[int] = [50, 150, 250, 350, 450, 50, 150, 250, 350, 450]
    # The list of text positions.
    text_position: list[int] = [65, 165, 265, 365, 465, 65, 165, 265, 365, 465]
    # The list of patty quantity positions.
    patty_quantity_position: list[int] = [80, 210, 340, 460]
    # An index variable to scroll through each position in the list. It starts
    # at -1 because it is triggered as soon as the for loop begins.
    circle_x_count: int = -1
    # The y position of the circle.
    circle_y: int = 320
    # Y position of the image.
    image_y: int = 288
    # Y position of the item name.
    name_y: int = 360
    # Y position of the quantity.
    quantity_y: int = 380
    # A dict holding the patty totals for the current order. For each patty
    # type, it initially sets it as 0.
    patty_totals: dict[str, int] = {type: 0 for type in burger_type}

    # A key is aquired of the current order, if there are orders.
    if orders_list:
        aquire_key = orders_list[0]
        if aquire_key in individual_orders:
            current_order_stats = individual_orders[aquire_key]
            # For each item in the order, a circle is drawn with the coordinates
            # specified above.
            for item, quantity in current_order_stats.items():
                # Count is increased.
                circle_x_count += 1
                # If the row is full, y changes.
                if circle_x_count > 4:
                    circle_y = 480
                    image_y = 448
                    name_y = 520
                    quantity_y = 540

                # If the requirement for a item has been fufilled, the colour is
                # changed.
                if total_stock_items[item] >= quantity:
                    colour = GREEN
                else:
                    colour = WHITE

                # Each circle for each item is drawn.
                pygame.draw.circle(
                    screen,
                    colour,
                    (circle_position[circle_x_count], circle_y),
                    40,
                    DTHRU_OUTLINE,
                )
                # Item name is displayed.
                item_name_text = burger_name_font.render(item, True, colour)
                # Text is centered using the shortest name, then displayed.
                item_name_width = (item_name_text.get_width() - 30) / 2
                screen.blit(
                    item_name_text,
                    (text_position[circle_x_count] - item_name_width, name_y),
                )
                # Item quantity is taken by taking current stock and comparing
                # it the quantity.
                quantity_text = quantity_font.render(
                    str(total_stock_items[item]) + "/" + str(quantity), True, colour
                )
                quantity_width = (quantity_text.get_width() - 21) / 2
                screen.blit(
                    quantity_text,
                    (5 + text_position[circle_x_count] - quantity_width, quantity_y),
                )

                # The current order is compared to the dict with the images for
                # each item.
                for item_name, item_image in current_order_images.items():
                    # If there is a match on both dicts:
                    if item == item_name:
                        # The match is displayed.
                        screen.blit(
                            item_image, (image_position[circle_x_count], image_y)
                        )

                # The ordered item is compared to the item in the burger_type
                # dict.
                for patty_type, burger_stats in burger_type.items():
                    if item in burger_stats:
                        # The patty total is updated using the quantity of the
                        # item ordered and the amount of patties in the burger.
                        patty_totals[patty_type] += quantity * burger_stats[item]

            # Once patty totals have been updated, they are displayed in this
            # for loop.
            for patty_type, total_quantity in patty_totals.items():
                # Display only occurs if that patty has been ordered.
                if total_quantity > 0:
                    # A variable is made by checking the patty type position in
                    # the dict, converted to a list.
                    patty_type_index = list(burger_type.keys()).index(patty_type)
                    # Text for the patty is then defined.
                    patty_quantity_text = quantity_font.render(
                        str(total_quantity), True, WHITE
                    )
                    # Text is centered, then displayed.
                    patty_width = (patty_quantity_text.get_width() - 6) / 2
                    # The index variable is used to display the quantity under
                    # the correct patty.
                    screen.blit(
                        patty_quantity_text,
                        (patty_quantity_position[patty_type_index] - patty_width, 670),
                    )

        # The current order number is targeted from the order_combo dict.
        if aquire_key in order_combo:
            # The current combo is then defined using the matching order number.
            current_combo = combo_font.render(order_combo[aquire_key], True, YELLOW)
            # Centering, then display.
            combo_width = (current_combo.get_width() - 61) / 2
            screen.blit(current_combo, (250 - combo_width, 200))

    # Patty images are displayed.
    screen.blit(hugo_patty_sized, (50, 590))
    screen.blit(slammer_patty_sized, (180, 590))
    screen.blit(angus_patty_sized, (310, 590))
    screen.blit(chicken_patty_sized, (440, 590))
    screen.blit(hugo_patty_name, (70, 650))
    screen.blit(slammer_patty_name, (205, 650))
    screen.blit(angus_patty_name, (322, 650))
    screen.blit(chicken_patty_name, (440, 650))


def end_game() -> None:
    """Display stats for the end of the game."""
    global orders_list, cars, money
    # Shift over text.
    screen.blit(shift_over, (200, 0))
    # A list of the cars is aquired so the order number can be found.
    cars_list = list(cars.keys())
    # Score is defined.
    score = money - average_car_time(True)
    score = round(score, 2)
    # The total orders served is the first car waiting minus 1.
    order_total = cars_list[0] - 1
    # Money is rounded.
    money = round(money, 2)
    # Each variable has its text defined, then displayed.

    final_total_order = main_menu_options_xs3.render(
        "Total orders served: " + str(order_total), True, WHITE
    )
    final_money = main_menu_options_xs3.render(
        "Money earnt: " + str(money), True, WHITE
    )
    final_car_time = main_menu_options_xs3.render(
        "Average car time: " + str(average_car_time(False)), True, WHITE
    )
    final_score = main_menu_options.render("SCORE: " + str(score), True, WHITE)

    screen.blit(final_total_order, (480, 200))
    screen.blit(final_money, (480, 300))
    screen.blit(final_car_time, (480, 400))
    screen.blit(final_score, (480, 500))


# EVENT HANDLING


def handle_events(
    click: bool,
    mouse_pos: tuple[int, int],
    event,
    keystroke_type: str,
    button,
    desired_state: int,
    button_state: int,
    create_button: bool = False,
    radius: int = 80,
) -> int | str:
    """Handle all the pygame related events, such as clicking.

    Args:
        click: A bool indicating if the mouse has been clicked.
        mouse_pos: The position of the mouse.
        event: The key pressed, expressed as event. Used for typing.
        keystroke_type (str): The type of pressed key.
        button: The game element being interacted with.
        desired_state (int): The state to move to.
        button_state (int): The current state of the button.
        (e.g whether it has been clicked or not, represented in ints.)
        create_button (bool): Whether the button is the create button used for
        item creation. Defaulted to False.
        radius (int): The radius of the creation button, used if create_button
        is true. Defaulted to 80.

    Returns:
        int | str: The game state to move to, or an errors name.
    """
    # The user name is globally accessed so it can be continously updated.
    global user_name

    # If the caller needs to check if a button was clicked:
    if keystroke_type == "click":
        if click is True:
            # If the create_button is being clicked:
            if create_button:
                # This is the Pythagorean theorem, getting the distance between
                # 2 points (the mouse click, event, and the coordinates of the
                # circle, button. 0 represents x, 1 represents y.)
                distance = math.sqrt(
                    (mouse_pos[0] - button[0]) ** 2 + (mouse_pos[1] - button[1]) ** 2
                )
                # If the distance between the 2 points lies within the circles
                # radius, the desired state is returned.
                if distance <= radius:
                    button_state = desired_state
                    return button_state
                else:
                    return button_state
            # If the button is clicked:
            else:
                if button.collidepoint(mouse_pos):
                    # The desired_state provided in the argument is returned
                    # to the caller. Otherwise, nothing is returned and the
                    # state remains intact.
                    return desired_state
        else:
            return button_state

    # If the caller needs to check if the user is hovering over something:
    if keystroke_type == "hover":
        # If the mouse is hovering over a menu item, its outline is thickened.
        # Otherwise, it remains the same.
        if button.collidepoint(mouse_pos):
            thickness: int = 8
        else:
            thickness: int = 5
        return thickness

    # If the caller needs to check if the user is typing something:
    if keystroke_type == "type":
        if event.type == pygame.KEYDOWN:
            # The user_name variable is reduced by one if the user clicks
            # backspace.
            if event.key == pygame.K_BACKSPACE:
                user_name = user_name[:-1]
            # If the user types something:
            elif event.unicode:
                # The keystroke is added into the variable.
                user_name += event.unicode
            # If the user tries to enter spaces as their name without meeting
            # the character limit:
            if event.key == pygame.K_SPACE:
                # Length of the users_name is calculated.
                name_length = len(user_name)
                if name_length < 4:
                    # Their inputs are deleted.
                    user_name = ""
        # If all is well, the user_name is returned so another function can use
        # it.
        return user_name

    # If the caller needs to check if the user pressed enter:
    if keystroke_type == "enter":
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # The name is reduced by 1 as the return key is also added to
                # user_name when pressed. This ensures the users name can be
                # read as empty and the correct amount of characters.
                user_name = user_name[:-1]
                # Length of the users name is calculated.
                name_length = len(user_name)
                # If the user doesn't enter anything for their name:
                if user_name == "":
                    # The program defines the error as being no name, and
                    # returns the string.
                    error = "error_no_name"
                    return error
                # If the users name is below or above the following numbers:
                elif name_length < 3 or name_length > 25:
                    # The program defines the error as being a length error,
                    # and returns the string.
                    error = "error_length"
                    return error
                else:
                    # If no errors are made then the desired state is returned.
                    return desired_state


# This is the game loop responsible for calling the functions and receiving
# the returned values, then using those returns to call a different function to
# progress through the game.
while running:
    # Current time is calculated for the program to draw off.
    current_time = pygame.time.get_ticks()
    # A variable is defined as the pygame event enabler for cleanliness, and
    # allows it to be used globally.
    events = pygame.event.get()

    # Pygame events to pass to functions.
    mouse_click: bool = False
    # The mouse position is constantly assessed.
    mouse_position: tuple[int, int] = pygame.mouse.get_pos()

    # It is constantly checked if the mouse has been clicked or not or:
    for event in events:
        # If the user closes the window,
        if event.type == pygame.QUIT:
            # The loop ends.
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click = True

    # If the game has been opened:
    if current_state == ProgramState.GAME_OPEN:
        # The corresponding function is called.
        main_screen_now(screen)
        # Another variable, state is responsible for the return value of this
        # function. This is because current_state can't also be defined as this
        # otherwise it would no longer equal GAME_OPEN, ending the current
        # phase. So state and current_state are constantly interchanged so the
        # program functions correctly.
        # The bool indicating if the mouse has been clicked and its position is
        # passed to the function.
        state = start_order_now(screen, mouse_click, mouse_position)
        # Prevents accidently button clickage.
        pause = True
        wait = 0

    # As the variables in the ProgramState class have been defined as ints,
    # the program checks if the variables corresponding number has
    # been returned.
    if state == 1:
        # Resets the screen.
        screen.fill(BLACK)
        main_screen_now(screen)
        # Variables interchange.
        current_state = main_menu(screen, mouse_click, mouse_position)
        # The other pause variable is combined with the other so the back button
        # can be registered correctly.
        if pause:
            wait += 1
        if wait > 5:
            pause = False
            # A different pause variable needs to be used to they aren't mixed
            # up and access isn't hindered.
            skip = True
            wait2 = 0

    if current_state == 2:
        screen.fill(BLACK)
        # 'Events' allows the function to check for button presses.
        state = name_entry(screen, mouse_click, mouse_position, events)
        # Variables are reverted.
        skip = False
        wait2 = 0

    if state == 5:
        # Errors are cleared.
        error = False
        # Prevents the user from accidently clicking a station.
        pause = True
        # Reset the wait count for the pause.
        wait = 0
        screen.fill(BLACK)
        current_state = ingame_menu(screen, 1200, 700, mouse_click, mouse_position)
        # Signifies the game has started.
        begin_ordering = True
        # Start time is aquired.
        if not obtained_start_time:
            obtain_time = pygame.time.get_ticks()
            obtained_start_time = True
        # Gets rid of the current error message.
        visible = False
        if station_status:
            constant_creation_menu()

    # States for the different creation menus.
    if current_state == 6:
        screen.fill(BLACK)
        state = creation_menu(
            [
                "Hugo Juice",
                "Hugo Juice",
                "Hugo Juice",
                "Hugo Juice",
                "Hugo Juice",
                "Hugo Juice",
            ],
            "Drinks",
            juice_sized,
            [juice_order_icon],
            [
                juice_creation_icon,
                juice_creation_icon,
                juice_creation_icon,
                juice_creation_icon,
                juice_creation_icon,
                juice_creation_icon,
            ],
            ["Hugo\nJuice"],
            [5000, 5000, 5000, 5000, 5000, 5000],
            mouse_click,
            mouse_position,
        )
        constant_creation_menu()

    if current_state == 7:
        screen.fill(BLACK)
        state = creation_menu(
            grill_names,
            "Grill",
            grill_menu_icon,
            [
                hugopatty_order_icon,
                slammerpatty_order_icon,
                anguspatty_order_icon,
            ],
            grill_creation,
            [
                "10:1",
                "4:1",
                "Angus",
            ],
            grill_timers,
            mouse_click,
            mouse_position,
        )
        constant_creation_menu()

    if current_state == 8:
        screen.fill(BLACK)
        state = creation_menu(
            bfm_names,
            "BFM",
            bfm_menu_icon,
            [
                fries_order_icon,
                mcbullets_order_icon,
                chicken_order_icon,
            ],
            bfm_creation,
            [
                "Fries",
                "McBullets",
                "Chicken",
            ],
            bfm_timers,
            mouse_click,
            mouse_position,
        )
        constant_creation_menu()

    if state == 9:
        screen.fill(BLACK)
        current_state = creation_menu(
            [
                "Big Hugo",
                "5/4 Slammer",
                "Almighty Florida",
                "Francie Frenzy",
                "2 5/4 Slammer",
                "Keanu Krunch",
            ],
            "Make Grill",
            grill_menu_icon,
            [
                bighugo_order_icon,
                improperslammer_order_icon,
                almightyflorida_order_icon,
                francie_frenzy_order_icon,
                doubleimproperslammer_order_icon,
                keanu_krunch_order_icon,
            ],
            [
                bighugo_creation_icon,
                improperslammer_creation_icon,
                almightyflorida_creation_icon,
                franciefrenzy_creation_icon,
                doubleimproperslammer_creation_icon,
                keanu_krunch_creation_icon,
            ],
            [
                "Big\nHugo",
                "5/4\nSlammer",
                "Almighty\nFlorida",
                "Francie\nFrenzy",
                "2 5/4\nSlammer",
                "Keanu\nKrunch",
            ],
            [3000, 3000, 3000, 4000, 4000, 4000],
            mouse_click,
            mouse_position,
        )
        constant_creation_menu()

    if state == 10:
        screen.fill(BLACK)
        current_state = creation_menu(
            [
                "Devious Chicken",
                "Devious Chicken",
                "Devious Chicken",
                "Chicken Little",
                "Chicken Little",
                "Chicken Little",
            ],
            "Make BFM",
            bfm_menu_icon,
            [
                radioactivechicken_order_icon,
                chickenlittle_order_icon,
            ],
            [
                radioactivechicken_creation_icon,
                radioactivechicken_creation_icon,
                radioactivechicken_creation_icon,
                chickenlittle_creation_icon,
                chickenlittle_creation_icon,
                chickenlittle_creation_icon,
            ],
            ["Devious\nChicken", "Chicken\nLittle"],
            [3000, 3000, 3000, 4000, 4000, 4000],
            mouse_click,
            mouse_position,
        )
        constant_creation_menu()

    # If the user has lost:
    if game_end == 11:
        current_state = None
        state = None
        screen.fill(BLACK)
        begin_ordering = False
        screen.blit(your_fired, (150, 200))

    # Credits and tutorial.
    if current_state == 12:
        screen.fill(BLACK)
        state = credits(screen, mouse_click, mouse_position)

    if current_state == 13:
        screen.fill(BLACK)
        state = tutorial(screen, mouse_click, mouse_position)

    # If either state is 14, then the end game is executed.
    if current_state == 14 or state == 14:
        screen.fill(BLACK)
        state = end_game()

    # The AI begins ordering, the ingame timer begins, and cars start running.
    if begin_ordering:
        ai_ordering()
        time_left = game_time(obtain_time)
        # If the time left is 0, both states are set to the end of the game.
        if time_left == 0:
            current_state = ProgramState.SHIFT_FINISH
            state = ProgramState.SHIFT_FINISH
            begin_ordering = False
        if state == 5:
            game_end = display_cars(True)
        else:
            game_end = display_cars(False)

    # The display is constantly updated.
    pygame.display.flip()
    # The framerate is set to 30 to minimize system resources.
    pygame.time.Clock().tick(30)
# Once the main loop ends, the code moves onto the next piece of code,
# which is this.)
pygame.quit()
