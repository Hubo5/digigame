from typing import Tuple
# Importing pygame into the program
import pygame
# Used for distance calculations when checking mouse clicks.
import math

# Activating pygame
pygame.init()

# PROGRAM STATES

# These define what part of the program the user is up to, used for calling the correct function
# corresponding to the program state.
class ProgramState:
    GAME_OPEN: int = 0
    MAIN_MENU: int = 1
    ENTER_NAME: int = 2
    CHOOSE_GAMEMODE: int = 3
    DAY_STATS: int = 4
    GAME_MENU: int = 5
    DRINKS: int = 6


# The state is initially set to the first phase so the program starts.
current_state: int = ProgramState.GAME_OPEN

# CONSTANTS

# The rgb code for each color.
YELLOW = (255, 255, 0)
DARK_YELLOW = (254, 221, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (8, 98, 168)
GREEN = (80, 200, 120)
ORANGE = (255, 127, 0)
# Outline for most of the boxes displayed in game.
OUTLINE_WIDTH: int = 5
# Width and height of boxes on the second kiosk screen.
BUTTON2_WIDTH: int = 149
BUTTON2_HEIGHT: int = 56
BUTTON2_HEIGHT_EXTENDED: int = 96
# Size of the icons used on the second kiosk screen.
ICON: tuple[int, int] = 50, 50
# The window dimensions before the game officially begins.
PREGAME_SCREEN_WIDTH = 1000
PREGRAME_SCREEN_HEIGHT = 900
# The dimensions of the Drive-Thru boxes.
DTHRU_WIDTH = 200
DTHRU_HEIGHT = 100
DTHRU_OUTLINE = 3
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
# PREDEFINED VARIABLES

# The desired screen dimensions.
screen_width = PREGAME_SCREEN_WIDTH 
screen_height = PREGRAME_SCREEN_HEIGHT
# The current screen dimensions.
current_screen_width = screen_width
current_screen_height = screen_height
# The variable responsible for creating the game window with the parameters provided.
screen = pygame.display.set_mode((screen_width, screen_height))
# Sets the users name to none so they can make their own.
user_name = ""
# The title of the game window.
pygame.display.set_caption("McHugo's")
# This boolean controls the flashing start order button, and when its visible.
visible: bool = True
# This variable initially defines the time since the last switch from visible to not visible (part of the blinking order variable)
last_switch: int = 0
# This boolean controls whether the game is running or not.
running: bool = True
# This boolean checks if an error has been triggered so another variable can act off it.
error: bool = False
# This variable states what the error was in a variable so an action can be taken depending on what it is.
error_type: str = ""
# The positions of the boxes in the drive thru.
dthru_box_x_positions: list[int] = [120, 270, 420, 570, 720, 870]
dthru_text_x_positions: list[int] = [175, 325, 475, 625, 775, 925, 1090]
# The positions of the circles for the total stock.
total_stock_circle_x_positions: list[int] = [640, 740, 840, 940]
total_stock_circle_y_positions: list[int] = [230, 410]
# A dictionary of the menu items.
total_stock_items: dict[str, int] = {
    "Big Hugo": 0,
    "Colossal H": 0,
    "5/4 Slammer": 0,
    "2 5/4 Slammer": 0,
    "Almighty. F": 0,
    "Keanu Krunch": 0,
    "Radioactive. McR": 0,
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
station_bases = {}
# To define which station was triggered. Global variable used to maintain status.
station_status = {}
# The variables are globablly used to prevent a glitch where a button appears as another one closes, resulting in them clicking it unintentionally. Wait prevents that button from being clicked.
pause: bool = False
wait: int = 0
# CURRENTLY UNUSED VARIABLES (DELETE IF NOT NEEDED)

# Colours of the circles in the game selection menu. Also used for the circle in the 
# clock in screen.
circle_colour_1: Tuple[int, int, int] = (255, 255, 255)
circle_colour_2: Tuple[int, int, int] = (255, 255, 255)
day: int = 1
# A list containing each day, and the current day. As a list index begins at 0, the minus 1 ensures the correct day
# is displayed.
day_names: list[str] = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
day_current = day_names[day - 1]
day_reduced: bool = False
day_current_updated: bool = False
day_increased: bool = False
# Checks whether to display yesterdays stats or todays.
today_stats: bool = True
yesterday_stats: bool = False
# The length and positioning of the toggle day button.
toggle_day_length: int = 330
toggle_day_x: int = 95
toggle_text_x: int = 115

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
status_heading_font = pygame.font.Font("fonts/important button.ttf", 16)
status_font = pygame.font.Font("fonts/important button.ttf", 11)
item_font = pygame.font.Font("fonts/body text.ttf", 11)
time_remaining_font = pygame.font.Font("fonts/important button.ttf", 25)

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
version = heading_font.render("VERSION: PROTO 2.2", True, RED)
# Second main menu screen
play_button = main_menu_options.render("PLAY", True, DARK_YELLOW)
tutorial_button_1 = main_menu_options.render("FIRST", True, DARK_YELLOW)
tutorial_button_2 = main_menu_options.render("SHIFT", True, DARK_YELLOW)
scoreboard_button_1 = main_menu_options_xs.render("SCORE", True, DARK_YELLOW)
scoreboard_button_2 = main_menu_options_xs2.render("BOARD", True, DARK_YELLOW)
setting_button = main_menu_options_xs3.render("SETTING", True, DARK_YELLOW)
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
time_text_1 = body_font.render("VIEW", True, WHITE)
time_text_2 = body_font.render("EXCESS", True, WHITE)
time_text_3 = body_font.render("CARS", True, WHITE)
time_text_4 = stats_font.render("time", True, WHITE)
time_text_5 = main_menu_options.render("SERVE!", True, WHITE)
current_order_heading = dthru_heading_font.render("CURRENT ORDER", True, YELLOW)
total_stock_heading = dthru_heading_font.render("TOTAL STOCK", True, YELLOW)
navigation_heading = dthru_heading_font.render("NAVIGATION", True, YELLOW)
current_car_heading = navigation_font.render("Current car time:", True, WHITE)
average_car_heading = navigation_font.render("Average: ", True, WHITE)
money_heading = navigation_font.render("Money earnt: ", True, WHITE)
time_heading = navigation_font.render("Time left: ", True, WHITE)
# Drinks, Grill and BFM
status_heading = status_heading_font.render("STATUS:", True, WHITE)
status_standby = status_font.render("STANDBY", True, RED)
status_wait = status_font.render("CREATING", True, DARK_YELLOW)
status_ready = status_font.render("READY!", True, GREEN)
back_name_text_xs = main_menu_options_xs3.render("BACK", True, DARK_YELLOW)
current_requirements = heading_font.render("Current:", True, WHITE)
total_requirements = heading_font.render("Total:", True, WHITE)
button_start = dthru_heading_font.render("CREATE!", True, WHITE)
creation_click = status_font.render("CLICK!", True, WHITE)
# TBR (Testing only, To Be Removed)
burger_notdone_text = body_font.render("burger", True, RED)
burger_done_text = body_font.render("burger", True, GREEN)
fries_text = body_font.render("fries", True, GREEN)
mcbullets_text = body_font.render("mcbullets", True, RED)
drink_text = body_font.render("hugo juice", True, GREEN)
counter_1 = quantity_font.render("3/5", True, WHITE)
burger_name = burger_name_font.render("Chicken Little", True, WHITE)
patty_name = burger_name_font.render("10:1", True, WHITE)
patty_name2 = burger_name_font.render("Chicken", True, WHITE)
current_car_time = number_font.render("0:00", True, WHITE)
average_car_time = number_font.render("0:00", True, WHITE)
money_earnt = number_font.render("$0", True, WHITE)
time_left = number_font.render("6:00", True, WHITE)
grill_heading = burger_name_font.render("Grill", True, WHITE)
drinks_heading = burger_name_font.render("Drinks", True, WHITE)
bfm_heading = burger_name_font.render("BFM", True, WHITE)
needed_juice = main_menu_options_xs2.render("x0", True, WHITE)
# Choosing a game mode (UNUSED)
choose_mode_1 = title_font.render("Choose your", True, YELLOW)
choose_mode_2 = title_font.render("gamemode.", True, YELLOW)
part_time_text = start_order_font.render("Part Time", True, DARK_YELLOW)
part_time_desc = main_menu_options_xs2.render("Play through 5 days", True, DARK_YELLOW)
part_time_desc_2 = main_menu_options_xs2.render("Upgrades available", True, DARK_YELLOW)
part_time_desc_3 = main_menu_options_xs2.render(
    "Difficulty increases", True, DARK_YELLOW
)
on_call_text = start_order_font.render("On Call", True, DARK_YELLOW)
on_call_desc = main_menu_options_xs2.render("Choose a day to play", True, DARK_YELLOW)
on_call_desc_2 = main_menu_options_xs2.render("No upgrades", True, DARK_YELLOW)
on_call_desc_3 = main_menu_options_xs2.render("Fixed difficulty", True, DARK_YELLOW)
# Displaying the day and users stats after clicking 'part time' (UNUSED)
clock_in_text_1 = title_font_xs.render("CLOCK", True, WHITE)
clock_in_text_2 = title_font.render("IN", True, WHITE)
clock_in_text_3 = title_font.render("!", True, WHITE)
stats_title = title_font_xs.render("STATS", True, YELLOW)
stats_1 = heading_font.render("Customers served: ", True, DARK_YELLOW)
stats_2 = heading_font.render("Money earnt: ", True, DARK_YELLOW)
stats_3 = heading_font.render("Biggest order: ", True, DARK_YELLOW)
stats_4 = heading_font.render("Average order time: ", True, DARK_YELLOW)
stats_5 = heading_font.render("Average happiness: ", True, DARK_YELLOW)
stats_6 = heading_font.render("Products served: ", True, DARK_YELLOW)
stats_7 = heading_font.render("Products wasted: ", True, DARK_YELLOW)
stats_8 = heading_font.render("Total score: ", True, DARK_YELLOW)
yesterday_text = main_menu_options.render("YESTERDAY", True, YELLOW)
today_text = main_menu_options.render("TODAY", True, YELLOW)

# These are the images used in the game.
background = pygame.image.load("images/background.jpg")
main_menu_kiosk = pygame.image.load("images/kiosk.png")
logo = pygame.image.load("images/logo.png")
play_icon = pygame.image.load("images/play_icon.png")  # Reference: Icon by Freepik
first_shift_icon = pygame.image.load(
    "images/first_shift_icon.png"
)  # Reference: Icon by Freepik
settings_icon = pygame.image.load(
    "images/settings_icon.png"
)  # Reference: Icon by Freepik
scoreboard_icon = pygame.image.load(
    "images/scoreboard_icon.png"
)  # Reference: Icon by Freepik
name_background = pygame.image.load("images/darkened_background.png")
back_name = pygame.image.load("images/back.png")  # Reference: Icon by Freepik
car = pygame.image.load("images/car_green_side.png") # Reference: Icon by Freepik
view = pygame.image.load("images/view.png") # Reference: Icon by Prosymbols
# Traffic lights (All from macrovector on Freepik)
redlight = pygame.image.load("images/redlight.png")
yellowlight = pygame.image.load("images/yellowlight.png")
greenlight = pygame.image.load("images/greenlight.png")
# Menu items (all from Freepik)
big_hugo = pygame.image.load("images/menu items/big hugo.png")
colossal_h = pygame.image.load("images/menu items/colossal h.png")
improper_slammer = pygame.image.load("images/menu items/improper slammer.png")
double_improper_slammer = pygame.image.load("images/menu items/double improper.png")
almighty_florida = pygame.image.load("images/menu items/florida.png")
keanu_krunch = pygame.image.load("images/menu items/keanu krunch.png")
radioactive_mcr = pygame.image.load("images/menu items/radioactive.png")
chicken_little = pygame.image.load("images/menu items/lil chicken.png")
mcbullets = pygame.image.load("images/menu items/mcbullets.png")
fries = pygame.image.load("images/menu items/fries.png")
juice = pygame.image.load("images/menu items/juice.png")

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

# These are images that have had their size altered. "t" means for the total stock display.
logo_1 = pygame.transform.scale(logo, (400, 400))
logo_2 = pygame.transform.scale(logo, (51, 51))
logo_3 = pygame.transform.scale(logo, (80, 80))
play_icon_sized = pygame.transform.scale(play_icon, (ICON))
first_shift_icon_sized = pygame.transform.scale(first_shift_icon, (ICON))
settings_icon_sized = pygame.transform.scale(settings_icon, (ICON))
scoreboard_icon_sized = pygame.transform.scale(scoreboard_icon, (ICON))
back_name_sized = pygame.transform.scale(back_name, (ICON))
car_sized = pygame.transform.scale(car, (85, 45))
view_sized = pygame.transform.scale(view, (80, 80))
redlight_sized = pygame.transform.scale(redlight, (50, 135))
yellowlight_sized = pygame.transform.scale(yellowlight, (50, 135))
greenlight_sized = pygame.transform.scale(greenlight, (50, 135))

# Menu items
improper_slammer_sized = pygame.transform.scale(improper_slammer, (MENU_ICON))
juice_sized = pygame.transform.scale(juice, (MENU_ICON))
mcbullets_sized = pygame.transform.scale(mcbullets, (MENU_ICON))
big_hugo_sized_t = pygame.transform.scale(big_hugo, (TOTAL_MENU_ICON))
colossal_h_sized_t = pygame.transform.scale(colossal_h, (TOTAL_MENU_ICON))
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
drinks_icon = pygame.transform.scale(juice, (NAVIGATION_ICON))
fries_icon = pygame.transform.scale(fries, (XS_NAVIGATION_ICON))
nuggets_icon = pygame.transform.scale(mcbullets, (XS_NAVIGATION_ICON))

# Icons for displaying the order on respective menus.
juice_order_icon = pygame.transform.scale(juice, (ORDER_ICON))

# Icons for the finished product on respective menus.
juice_creation_icon = pygame.transform.scale(juice, (CREATED_ICON))
keanu_krunch_creation_icon = pygame.transform.scale(keanu_krunch, (CREATED_ICON))
# This list needs to be defined down here where the images have been defined.
menu_images: list = [
    big_hugo_sized_t,
    colossal_h_sized_t,
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


# FUNCTIONS
def main_screen_now(screen) -> None:
    """Display the core elements of the game screen.

    Args:
        screen: The current size of the game window.
    """
    # Draws the various elements on screen.
    screen.blit(background, (0, 0))
    screen.blit(main_menu_kiosk, (0, 35))
    screen.blit(game_title, (325, -25))
    screen.blit(logo_1, (400, 80))
    screen.blit(logo_2, (199, 535))
    screen.blit(version, (620, 840))


def start_order_now(screen) -> bool:
    """Display the start button for access to the main menu.

    Args:
        screen: The current size of the game window.

    Returns:
        bool: What game state the game should be in.
    """
    # Accesses the last_switch and visible variables outside the function so they can
    # be used for visiblity.
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
        screen, BLACK, (44, 240, 200, 200), OUTLINE_WIDTH)
    if not visible:
        # The button is still clickable, but isn't visible.
        start_order_position = pygame.draw.rect(
        screen, WHITE, (44, 240, 200, 200))
    # The events are handled externally, checking if the user has clicked the start_order button,
    # and if they did the desired state to move to is provided.
    current_event = handle_events(
        event, "click", start_order_position, ProgramState.MAIN_MENU, None
    )
    # The state of the game is returned to the main loop so the appropiate function can be called.
    return current_event
    

def main_menu(screen) -> bool:
    """The main menu where the user can choose what they want to do.

    Args:
        screen: The current size of the game window.

    Returns:
        bool: What game state the game should be in.
    """
    # The rectangles must be defined initially so the menu_box variables can draw from them and update
    # thickness. They aren't drawn because the thickness has to be continously updated first and 
    # defined.
    play_rect = pygame.Rect(40, 125, BUTTON2_WIDTH, BUTTON2_HEIGHT)
    first_shift_rect = pygame.Rect(40, 191, BUTTON2_WIDTH, BUTTON2_HEIGHT_EXTENDED)
    scoreboard_rect = pygame.Rect(40, 297, BUTTON2_WIDTH, BUTTON2_HEIGHT_EXTENDED)
    settings_rect = pygame.Rect(40, 403, BUTTON2_WIDTH, BUTTON2_HEIGHT)

    # The events are handled externally, checking if the user is hovering over a menu_box,
    # using the rectangles defined above. No desired event is provided as the game state
    # shouldn't change.
    menu_box_1 = handle_events(event, "hover", play_rect, None, None)
    menu_box_2 = handle_events(event, "hover", first_shift_rect, None, None)
    menu_box_3 = handle_events(event, "hover", scoreboard_rect, None, None)
    menu_box_4 = handle_events(event, "hover", settings_rect, None, None)

    # The buttons are now drawn now the menu_boxes have been defined.
    play = pygame.draw.rect(
        screen, BLACK, play_rect, menu_box_1
    )
    first_shift = pygame.draw.rect(
        screen, BLACK, first_shift_rect, menu_box_2
    )
    scoreboard = pygame.draw.rect(
        screen, BLACK, scoreboard_rect, menu_box_3
    )
    settings = pygame.draw.rect(
        screen, BLACK, settings_rect, menu_box_4
        )
    
    # The text is drawn.
    screen.blit(logo_3, (105, 50))
    screen.blit(play_button, (45, 125))
    screen.blit(tutorial_button_1, (45, 192))
    screen.blit(tutorial_button_2, (45, 232))
    screen.blit(scoreboard_button_1, (45, 297))
    screen.blit(scoreboard_button_2, (45, 342))
    screen.blit(setting_button, (47, 412))
    screen.blit(play_icon_sized, (198, 125))
    screen.blit(first_shift_icon_sized, (198, 215))
    screen.blit(settings_icon_sized, (198, 405))
    screen.blit(scoreboard_icon_sized, (198, 320))

    # The event function checks if the user has clicked play.
    current_event = handle_events(event, "click", play, ProgramState.ENTER_NAME, None)
    return current_event
        
def toggle_visibility(last_switch_local: int, visible_local: bool, time_switch: int, repeat: bool) -> bool:
    """Controls the visibility of a desired element.

    Args:
        last_switch_local (int): The last time the visibility was toggled.
        visible_local (bool): The status of the elements visibility.
        time_switch (int): The time until it takes for visibility to be toggled.
        repeat (bool): Whether the function should be repeated until its no longer called.

    Returns:
        bool: The status of the elements visiblity.
    """
    # The global variable is accessed so it can be updated.
    global last_switch
    # The program begins counting from when the funtion was called.
    start_switches = pygame.time.get_ticks()
    # If the timer minus the last visibility switch is greater than the desired time to stay on screen:
    if start_switches - last_switch_local > time_switch:
        # Visibility is changed to none.
        visible_local = not visible_local
        # If the visibility should be repeatedly toggled:
        if repeat:
            # The last switch variable is changed to the amount of time the game has been opened for.
            # The global variable is accessed so the argument provided by the function calling it
            # can be altered.
            last_switch = start_switches
    return visible_local

def timer(time_end: int) -> bool:
    """A timer for how long a station should remain in its status.

    Args:
        time_end (int): When the timer should end.

    Returns:
        bool: A boolean indicating if the timer has passed its end time.
    """
    time_start = pygame.time.get_ticks()
    return time_start >= time_end


def draw_timer(screen, elapsed_time: int, time_end: int, center, radius: int):
    """This function draws a circle which disappears as time passes.

    Args:
        screen: The surface to be drawn on.
        elapsed_time (int): The elapsed time since the timer was started, provided by caller.
        time_end (int): When the timer should end, and the circle fully disappear.
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
    # The text is centered differently as this function doesn't have access to the station outlines directly (they are in a tuple) for further efficency. The text is made into a rect with its center being = to the circle center.
    text_centering = time_left_text.get_rect(center=center)
    screen.blit(time_left_text, text_centering)


def name_entry(screen, events) -> bool:
    """Where the user can enter their name.

    Args:
        screen: The current size of the game window.
        events: The pygame event enabler.

    Returns:
        bool: What game state the game should be in.
    """
    # The user_name, error, and error_type variables need to be globally accessed because
    # they can't be defined within the function since they need to constantly change.
    # last_switch and visible are again accessed to ensure the toggle_visibility function
    # works properly by defining them.
    global user_name, last_switch, visible, error, error_type
    
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

    # In order to be continously updated, the pygame event handling for loop must be used.
    for event in events:
        # If the user types, the event handling function handles the inputs appropiately.
        user_name = handle_events(event, "type", None, None, None)
        # Checks if the user clicked the back button, returning to the previous menu.
        previous_event = handle_events(
            event, "click", back, ProgramState.MAIN_MENU, None
        )
        # Checks if the user pressed enter. The desired state of GAME_MENU is only used if
        # the requirements in the handle_events function is met.
        current_event = handle_events(
            event, "enter", None, ProgramState.GAME_MENU, None
        )
        # If the handle_events function returns one of these errors instead of the desired state:
        if current_event == "error_no_name" or current_event == "error_length":
            # The error loop is set to true so the program continously displays the error message
            # even after the error has been triggered.
            error = True
            # This is used so the program can tell what error was made as there are two types.
            error_type = current_event
            # visible is initially set to true so the program displays the error.
            visible = True
            # The program updates last_switch with the new time since the error was made.
            last_switch = pygame.time.get_ticks()
        # Only if current_event is the desired state will it return its value, otherwise there would be
        # nothing to return and an error would occur as current_event can't always be returned.
        if current_event == 5:
            return current_event
        # If the handle_events function indicates to the main loop to go back a stage, its value is returned.
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
    # Nothing is returned down here because the returns need to be within the for loop.
    
def ingame_menu(screen, screen_width, screen_height) -> bool:
    # The current screen dimensions are globally accessed so the program knows what
    # the current dimensions are.
    global \
        current_screen_width, \
        current_screen_height, \
        total_stock_circle_x_positions, \
        total_stock_circle_y_positions
    # The below code fixes a flickering bug with content onscreen.
    # If the desired screen dimensions aren't the current dimensions:
    if (screen_width, screen_height) != (current_screen_width, current_screen_height):
        # The screen display is changed accordingly.
        screen = pygame.display.set_mode((screen_width, screen_height))
        # The current dimensions are now updated to be the same as the desired.
        current_screen_width = screen_width
        current_screen_height = screen_height
    # The boxes holding the cars.
    pygame.draw.rect(screen, WHITE, (0, 0, 1200, 60), DTHRU_OUTLINE)
    
    # ALL BELOW CODE IS TBR, ADD FOR LOOPS
    
    # The cars themselves.
    screen.blit(car_sized, (150, 10))
    screen.blit(car_sized, (300, 10))
    screen.blit(car_sized, (450, 10))
    screen.blit(car_sized, (600, 10))
    screen.blit(car_sized, (750, 10))
    screen.blit(car_sized, (900, 10))
    screen.blit(car_sized, (1065, 10))
    # The box for viewing excess cars.
    pygame.draw.rect(screen, WHITE, (0, 0, 120, 150), DTHRU_OUTLINE)
    pygame.draw.rect(screen, DARK_YELLOW, (10, 10, 100, 40))
    screen.blit(time_text_1, (30, 10))
    screen.blit(time_text_2, (18, 60))
    screen.blit(time_text_3, (30, 100))
    # The boxes for each section on the drive thru.
    for x in dthru_box_x_positions:
        pygame.draw.rect(screen, WHITE, (x, 0, 150, 150), DTHRU_OUTLINE)
    pygame.draw.rect(screen, WHITE, (1020, 0, 180, 150), DTHRU_OUTLINE)
    # The text for the boxes in the drive thru.
    for x in dthru_text_x_positions:
        screen.blit(time_text_4, (x, 60))
    screen.blit(time_text_5, (1020, 90))
    # The box containing how big the order is.
    # Box 1.
    pygame.draw.rect(screen, WHITE, (135, 100, 120, 40), DTHRU_OUTLINE)
    pygame.draw.rect(screen, GREEN, (135, 100, 24, 40))
    pygame.draw.rect(screen, WHITE, (159, 100, 24, 40), DTHRU_OUTLINE)
    pygame.draw.rect(screen, WHITE, (183, 100, 24, 40), DTHRU_OUTLINE)
    pygame.draw.rect(screen, WHITE, (207, 100, 24, 40), DTHRU_OUTLINE)
    pygame.draw.rect(screen, WHITE, (231, 100, 24, 40), DTHRU_OUTLINE)
    # Box 2.
    pygame.draw.rect(screen, WHITE, (135 + 150, 100, 120, 40), DTHRU_OUTLINE)
    pygame.draw.rect(screen, GREEN, (135 + 150, 100, 24, 40))
    pygame.draw.rect(screen, GREEN, (159 + 150, 100, 24, 40))
    pygame.draw.rect(screen, YELLOW, (183 + 150, 100, 24, 40))
    pygame.draw.rect(screen, WHITE, (207 + 150, 100, 24, 40), DTHRU_OUTLINE)
    pygame.draw.rect(screen, WHITE, (231 + 150, 100, 24, 40), DTHRU_OUTLINE)
    # Box 3.
    pygame.draw.rect(screen, WHITE, (135 + 300, 100, 120, 40), DTHRU_OUTLINE)
    pygame.draw.rect(screen, GREEN, (135 + 300, 100, 24, 40))
    pygame.draw.rect(screen, GREEN, (159 + 300, 100, 24, 40))
    pygame.draw.rect(screen, WHITE, (183 + 300, 100, 24, 40), DTHRU_OUTLINE)
    pygame.draw.rect(screen, WHITE, (207 + 300, 100, 24, 40), DTHRU_OUTLINE)
    pygame.draw.rect(screen, WHITE, (231 + 300, 100, 24, 40), DTHRU_OUTLINE)
    # Box 4.
    pygame.draw.rect(screen, WHITE, (135 + 450, 100, 120, 40), DTHRU_OUTLINE)
    pygame.draw.rect(screen, GREEN, (135 + 450, 100, 24, 40))
    pygame.draw.rect(screen, GREEN, (159 + 450, 100, 24, 40))
    pygame.draw.rect(screen, YELLOW, (183 + 450, 100, 24, 40))
    pygame.draw.rect(screen, RED, (207 + 450, 100, 24, 40))
    pygame.draw.rect(screen, RED, (231 + 450, 100, 24, 40))
    # Box 5.
    pygame.draw.rect(screen, WHITE, (135 + 600, 100, 120, 40), DTHRU_OUTLINE)
    pygame.draw.rect(screen, GREEN, (135 + 600, 100, 24, 40))
    pygame.draw.rect(screen, GREEN, (159 + 600, 100, 24, 40))
    pygame.draw.rect(screen, YELLOW, (183 + 600, 100, 24, 40))
    pygame.draw.rect(screen, RED, (207 + 600, 100, 24, 40))
    pygame.draw.rect(screen, WHITE, (231 + 600, 100, 24, 40), DTHRU_OUTLINE)
    # Box 6.
    pygame.draw.rect(screen, WHITE, (135 + 750, 100, 120, 40), DTHRU_OUTLINE)
    pygame.draw.rect(screen, GREEN, (135 + 750, 100, 24, 40))
    pygame.draw.rect(screen, GREEN, (159 + 750, 100, 24, 40))
    pygame.draw.rect(screen, WHITE, (183 + 750, 100, 24, 40), DTHRU_OUTLINE)
    pygame.draw.rect(screen, WHITE, (207 + 750, 100, 24, 40), DTHRU_OUTLINE)
    pygame.draw.rect(screen, WHITE, (231 + 750, 100, 24, 40), DTHRU_OUTLINE)

    # The current order box.
    pygame.draw.rect(screen, WHITE, (0, 150, 570, 550), DTHRU_OUTLINE)
    screen.blit(current_order_heading, (160, 150))
    # The box containing the current order in text.
    pygame.draw.rect(screen, WHITE, (0, 180, 570, 143), DTHRU_OUTLINE)
    # Burger display section.
    pygame.draw.rect(screen, RED, (0, 180, 570, 110), DTHRU_OUTLINE)
    # Example order.
    # For 10:1, 4:1, Angus, chicken patties on each row.
    screen.blit(burger_notdone_text, (5, 175))
    screen.blit(burger_done_text, (5, 200))
    screen.blit(burger_notdone_text, (5, 225))
    screen.blit(burger_done_text, (5, 250))
    # Fries and nuggets.
    pygame.draw.rect(screen, YELLOW, (0, 290, 390, 30), DTHRU_OUTLINE)
    screen.blit(fries_text, (5, 285))
    screen.blit(mcbullets_text, (170, 285))
    # Hugo Juice.
    pygame.draw.rect(screen, BLUE, (390, 290, 180, 30), DTHRU_OUTLINE)
    screen.blit(drink_text, (395, 285))

    # The currently needed stock display.
    pygame.draw.circle(screen, WHITE, (80, 370), 40, DTHRU_OUTLINE)
    screen.blit(improper_slammer_sized, (50, 338))
    screen.blit(burger_name, (40, 410))
    screen.blit(counter_1, (65, 430))
    pygame.draw.circle(screen, WHITE, (180, 370), 40, DTHRU_OUTLINE)
    screen.blit(mcbullets_sized, (150, 338))
    screen.blit(burger_name, (140, 410))
    screen.blit(counter_1, (165, 430))
    pygame.draw.circle(screen, WHITE, (280, 370), 40, DTHRU_OUTLINE)
    screen.blit(improper_slammer_sized, (250, 338))
    screen.blit(burger_name, (240, 410))
    screen.blit(counter_1, (265, 430))
    pygame.draw.circle(screen, WHITE, (380, 370), 40, DTHRU_OUTLINE)
    screen.blit(improper_slammer_sized, (350, 338))
    screen.blit(burger_name, (340, 410))
    screen.blit(counter_1, (365, 430))
    pygame.draw.circle(screen, WHITE, (480, 370), 40, DTHRU_OUTLINE)
    screen.blit(improper_slammer_sized, (450, 338))
    screen.blit(burger_name, (440, 410))
    screen.blit(counter_1, (465, 430))
    # Section 2.
    pygame.draw.circle(screen, WHITE, (80, 500), 40, DTHRU_OUTLINE)
    screen.blit(improper_slammer_sized, (50, 468))
    screen.blit(burger_name, (40, 540))
    screen.blit(counter_1, (65, 560))
    pygame.draw.circle(screen, WHITE, (180, 500), 40, DTHRU_OUTLINE)
    screen.blit(mcbullets_sized, (150, 468))
    screen.blit(burger_name, (140, 540))
    screen.blit(counter_1, (165, 560))
    pygame.draw.circle(screen, WHITE, (280, 500), 40, DTHRU_OUTLINE)
    screen.blit(improper_slammer_sized, (250, 468))
    screen.blit(burger_name, (240, 540))
    screen.blit(counter_1, (265, 560))
    pygame.draw.circle(screen, WHITE, (380, 500), 40, DTHRU_OUTLINE)
    screen.blit(improper_slammer_sized, (350, 468))
    screen.blit(burger_name, (340, 540))
    screen.blit(counter_1, (365, 560))
    pygame.draw.circle(screen, WHITE, (480, 500), 40, DTHRU_OUTLINE)
    screen.blit(improper_slammer_sized, (450, 468))
    screen.blit(burger_name, (440, 540))
    screen.blit(counter_1, (465, 560))

    # The section is for patties.
    pygame.draw.line(screen, WHITE, (0, 590), (567, 590), DTHRU_OUTLINE)
    screen.blit(hugo_patty_sized, (50, 590))
    screen.blit(patty_name, (71, 649))
    screen.blit(counter_1, (68, 670))
    screen.blit(slammer_patty_sized, (180, 590))
    screen.blit(patty_name, (201, 649))
    screen.blit(counter_1, (198, 670))
    screen.blit(angus_patty_sized, (310, 590))
    screen.blit(patty_name2, (316, 649))
    screen.blit(counter_1, (328, 670))
    screen.blit(chicken_patty_sized, (440, 590))
    screen.blit(patty_name2, (436, 649))
    screen.blit(counter_1, (448, 670))

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
    pygame.draw.rect(screen, WHITE, (1020, 150, 180, 550), DTHRU_OUTLINE)
    pygame.draw.line(screen, WHITE, (1020, 180), (1200, 180), DTHRU_OUTLINE)
    screen.blit(navigation_heading, (1023, 150))
    screen.blit(current_car_heading, (1030, 190))
    screen.blit(current_car_time, (1055, 210))
    screen.blit(average_car_heading, (1070, 270))
    screen.blit(average_car_time, (1055, 290))
    screen.blit(money_heading, (1050, 350))
    screen.blit(money_earnt, (1055, 370))
    screen.blit(time_heading, (1065, 430))
    screen.blit(time_left, (1055, 450))
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
    current_event = handle_events(event, "click", drinks, ProgramState.DRINKS, None)
    return current_event


def display_menu_items(
    x_positions: list[int],
    y_positions: list[int],
    initial_index: int,
    max_index: int,
    display_type: str,
):
    """Displays the menu images and text for the total stock.

    Args:
        x_positions (list[int]): The x positions of the items to draw.
        y_positions (list[int]): The y positions of the items to draw.
        initial_index (int): The item the function should begin on the dict/list.
        max_index (int): The item the function should end the cycle on the dict/list.
        display_type (str): Whether the item is an image or piece of text to indicate how to place it.
    """
    # The menu in text and image form need to be accessed so the function knows what to display using indexing.
    global menu, menu_images
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
                    # The item name and quantity is taken from the dict with the provided index.
                    item_name, item_quantity = menu_list[initial_index]
                    # A variable assigned to the indexed name and quantity is made with the appropiate font.
                    item_name_text = total_stock_name_font.render(
                        item_name, True, WHITE
                    )
                    item_quantity_text = stock_required_font.render(
                        str(item_quantity), True, WHITE
                    )
                    # Its width is then calculated so it can be centered correctly. 49 is the length of the shortest item, so it is used as a baseline.
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
                    # The current image to be obtained is taken from the global list.
                    current_image = menu_images[initial_index]
                    # The image is displayed using the given x and y.
                    screen.blit(current_image, (x, y))
                    # Cycles to the next item.
                    initial_index += 1

def creation_menu(
    station_names: list[str],
    menu_name: str,
    menu_image,
    order_icons: list,
    creation_icons: list,
    item_names: list[str],
    timer_duration: int,
    x_positions: list[int] = [60, 450, 840],
    y_positions: list[int] = [170, 430],
    button_radius: int = 80,
):
    # The status of each station needs to be globally accessed so it can be maintained. The same goes for pause and wait, and the menu list needs to be accessed so its quantities can be updated.
    global station_status, pause, wait, menu_list
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
    # If the user wishes to go back, the handle events function checks if the button has been clicked.
    previous_event = handle_events(event, "click", back, ProgramState.GAME_MENU, None)
    # Heading text for order requirements.
    screen.blit(current_requirements, (370, 7))
    screen.blit(total_requirements, (370, 77))

    # Index is initially set to 0 to cycle from the start. Multiple are needed for the various for loops.
    index: int = 0
    image_index: int = 0
    text_index: int = 0
    creation_index: int = 0

    # This for loop is for the images when displaying the order stats.
    for image in order_icons:
        # Replace needed_juice with proper variable
        # For each image, it is moved by 50 to the right. The icon is displayed by cycling through the provided list.
        screen.blit(needed_juice, (530 + image_index * 110, 15))
        screen.blit(order_icons[image_index], (585 + image_index * 110, 8))
        # For total requirements (replace needed juice)
        screen.blit(needed_juice, (480 + image_index * 110, 85))
        screen.blit(order_icons[image_index], (535 + image_index * 110, 80))
        image_index += 1

    # A similar loop to the previous, except if the item name requires two lines extra code is added to manually split it.
    for item in item_names:
        # This code splits anything which takes up two lines.
        lines = item.split("\n")
        # This is the position of the text on the y axix. It needs to be in a variable so the new line can be put on a different y.
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
            # Each station is assigned its unique name based on the index so it can be individually targeted.
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

            # If a station has not yet been added to the global dictionary controlling status, it is added.
            if station_name not in station_status:
                station_status[station_name] = {"status": 0, "end_time": None}

            # Each rectangles name is assigned to a dictionary as a key with the following values:
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
        # The current time is documented so the program knows when to stop the timer once activated.
        current_time = pygame.time.get_ticks()
        # If clicking inputs are paused:
        if pause is True:
            # A variable used to stall the input is activated which goes up every time this function repeats.
            wait += 1
        # After 20 repeats:
        if wait > 20:
            # Inputs are unpaused.
            pause = False
        # The local status variable is defined by using the event handling to check if the circle has been clicked.
        # If inputs aren't paused:
        if not pause:
            # The local status is defined by checking if the circle has been clicked.
            rect_info["status"] = handle_events(
                event,
                "click",
                rect_info["button_outline"],
                1,
                rect_info["status"],
                create_button=True,
            )
        # If the local variable is changed to 1 but the global one hasn't been changed yet:
        if rect_info["status"] == 1 and station_status[station_name]["status"] == 0:
            # It is updated to 1.
            station_status[station_name]["status"] = 1
            # The time for the timer to end is made using the current time plus the specified duration.
            station_status[station_name]["end_time"] = current_time + timer_duration

        # If the global status is 1 and the timer has expired (returning True):
        if station_status[station_name]["status"] == 1 and timer(
            station_status[station_name]["end_time"]
        ):
            # Status is sent back to the next stage.
            station_status[station_name]["status"] = 2

        # The rectangle is drawn based on its previous definition.
        pygame.draw.rect(screen, WHITE, rect_info["station_outline"], DTHRU_OUTLINE)

        # If the station status is hasn't been clicked:
        if station_status[station_name]["status"] == 0:
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
            # The traffic light is set to red and the status to standby for later use.
            light = redlight_sized
            creation_status = status_standby

        # If an item is being made:
        if station_status[station_name]["status"] == 1:
            # The elapsed time is calculated for the timer to draw off.
            elapsed_time = current_time - (
                station_status[station_name]["end_time"] - timer_duration
            )
            # The draw timer function is called.
            draw_timer(
                screen,
                elapsed_time,
                timer_duration,
                rect_info["button_outline"],
                button_radius,
            )
            # These are again set to something else.
            light = yellowlight_sized
            creation_status = status_wait

        # If the item has been made:
        if station_status[station_name]["status"] == 2:
            # The text saying to click.
            screen.blit(
                creation_click,
                (
                    rect_info["station_outline"].x + 174,
                    rect_info["station_outline"].y + 220,
                ),
            )
            # A rect of the image of the menu item is aquired. This is used for both centering and click detection.
            item_rect = creation_icons[creation_index].get_rect(
                center=rect_info["button_outline"]
            )
            # Depending on what the item is based on the index, it is displayed at the center of the button outline.
            screen.blit(creation_icons[creation_index], item_rect)
            # Text is changed.
            light = greenlight_sized
            creation_status = status_ready
            # Checks if the item was clicked or not.
            rect_info["status"] = handle_events(
                event,
                "click",
                item_rect,
                0,
                None,
                None,
            )
            # If it was:
            if rect_info["status"] == 0 and station_status[station_name]["status"] == 2:
                # Status is reverted to the original.
                station_status[station_name]["status"] = 0
                # A pause timer is activated so the creation button isn't accidently clicked. A variable is set to the current station so it can have its quantity updated.
                item_station = station_names[creation_index]
                wait = 0
                pause = True
                total_stock_items[item_station] += 1
                # As the items are accessed indirectly through this list, it needs to be updated.
                menu_list = list(total_stock_items.items())

        # The text is drawn, being a certain amount of pixels away from the rect itself for a consistent baseline.
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
    return previous_event


# UNUSED FUNCTIONS ARE BELOW

def choose_gamemode(screen) -> Tuple[Tuple[int, int, int], Tuple[int, int, int], bool]:
    screen.fill(BLACK)
    # These are the circles the user can click on containing info about the gamemodes.
    part_time = pygame.draw.circle(
        screen, circle_colour_1, (240, 600), 200, OUTLINE_WIDTH
    )
    on_call = pygame.draw.circle(
        screen, circle_colour_2, (760, 600), 200, OUTLINE_WIDTH
    )
    screen.blit(choose_mode_1, (100, 60))
    screen.blit(choose_mode_2, (100, 190))
    screen.blit(part_time_text, (115, 440))
    screen.blit(part_time_desc, (80, 540))
    screen.blit(part_time_desc_2, (85, 600))
    screen.blit(part_time_desc_3, (75, 660))
    screen.blit(on_call_text, (660, 440))
    screen.blit(on_call_desc, (590, 540))
    screen.blit(on_call_desc_2, (660, 600))
    screen.blit(on_call_desc_3, (635, 660))
    # If the user is hovering over a circle, it changes yellow.
    if part_time.collidepoint(pygame.mouse.get_pos()):
        circle_colour_1 = (255, 255, 0)
    else:
        circle_colour_1 = (255, 255, 255)
    if on_call.collidepoint(pygame.mouse.get_pos()):
        circle_colour_2 = (255, 255, 0)
    else:
        circle_colour_2 = (255, 255, 255)
    handle_events(event, "click", part_time, ProgramState.DAY_STATS)
    return circle_colour_1, circle_colour_2

def part_time_day(screen, today_stats: bool, yesterday_stats: bool, day: int, day_current: str, ) -> Tuple[bool, bool]:
    toggle_day_x = 0
    toggle_day_length = 0
    toggle_text_x = 0
    toggle_day_x = calculate_stats(toggle_day_x)
    toggle_day_length = calculate_stats(toggle_day_length)
    day = calculate_stats(day)
    day_current = calculate_stats(day_current)
    toggle_text_x = calculate_stats(toggle_text_x)
    screen.fill(BLACK)
    # The box containing the users stats.
    pygame.draw.rect(screen, WHITE, (30, 160, 470, 700), 4)
    screen.blit(stats_title, (100, 150))
    screen.blit(stats_1, (40, 270))
    screen.blit(stats_2, (40, 320))
    screen.blit(stats_3, (40, 370))
    screen.blit(stats_4, (40, 420))
    screen.blit(stats_5, (40, 470))
    screen.blit(stats_6, (40, 520))
    screen.blit(stats_7, (40, 570))
    screen.blit(stats_8, (40, 620))
    # If it isn't the first day, the yesterday button is created.
    if day > 0:
        # A button allowing the user to view their previous stats.
        toggle_day = pygame.draw.rect(screen, RED, (toggle_day_x, 720, toggle_day_length, BUTTON2_HEIGHT))
        pygame.draw.rect(screen, WHITE, (toggle_day_x, 720, toggle_day_length, BUTTON2_HEIGHT), 4)
    # If the user wants to display todays stats:
    if today_stats is True:
        # The clock in circle is drawn, with the text inside.
        clock_in = pygame.draw.circle(screen, BLUE, (750, 485), 225)
        pygame.draw.circle(screen, circle_colour_2, (750, 485), 225, 8)
        screen.blit(clock_in_text_1, (570, 330))
        screen.blit(clock_in_text_2, (650, 480))
        # The exclamation mark inside the clock in circle flashes with the same code as the start order
        # variable, except it flashes faster.
        toggle_visibility(0, True, 3000, False)
        visible = toggle_visibility()
        if visible:
            screen.blit(clock_in_text_3, (810, 480))
        # The time of week is defined by the day's number and the day's name.
        time_of_week = title_font_xs.render("DAY " + str((day)) + ": " + str((day_current)), True, YELLOW)
        # The time of week is displayed.
        screen.blit(time_of_week, (0, -20))
        # The text, 'yesterday' is put inside the button.
        screen.blit(yesterday_text, (toggle_text_x, 720))
    # If the user wants to display yesterdays stats:
    if yesterday_stats is True:
        time_of_week = title_font_xs.render("DAY " + str((day)) + ": " + str((day_current)), True, YELLOW)
        # The time of week is displayed.
        screen.blit(time_of_week, (0, -20))
        # The text, 'today' is put inside the button.
        screen.blit(today_text, (toggle_text_x, 720))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if toggle_day.collidepoint(event.pos):
                if today_stats is True: 
                    today_stats = False
                    yesterday_stats = True
                else:
                    today_stats = True
                    yesterday_stats = False
    current_event = handle_events("click", clock_in, ProgramState.GAME_MENU), ProgramState.DAY_STATS
    return today_stats, yesterday_stats, current_event

def calculate_stats(day: int, day_increased: bool, original_day: int, today_stats: bool, day_reduced: bool, day_current: str, day_current_updated: bool, day_names: list[str]) -> Tuple[int, str, int, int, int]:
    # The day is increased by 1.
    if not day_increased:
        day += 1
        day_increased = True
        original_day = day
    display_todays_stats = part_time_day(today_stats)
    if display_todays_stats:
        day_reduced = False
        day = original_day
        if not day_current_updated:
            day_current = day_names[day - 1]
            day_current_updated = True
        # Dimensions of the button are updated.
        toggle_day_length = 330
        toggle_day_x = 95
        toggle_text_x = 115
    display_yesterdays_stats = part_time_day(yesterday_stats)
    if display_yesterdays_stats:
        day_current_updated = False
        if not day_reduced:
            day = day - 1
            day_current = day_names[day - 1]
            day_reduced = True
        # Dimensions of the button are updated.
        toggle_day_length = 230
        toggle_day_x = 140
        toggle_text_x = 175
    return day, day_current, toggle_day_length, toggle_day_x, toggle_text_x

# END OF UNUSED FUNCTIONS

# EVENT HANDLING

def handle_events(
    event,
    keystroke_type: str,
    button,
    desired_state: int,
    button_state: int,
    create_button: bool = False,
    radius: int = 80,
) -> int:
    """_summary_

    Args:
        event: The pygame event enabler.
        keystroke_type (str): The type of pressed key.
        button: The game element being interacted with.
        desired_state (int): The state to move to.
        button_state (int): The current state of the button. (e.g whether it has been clicked or not, represented in ints.)
        create_button (bool): Whether the button is the create button used for item creation.
        radius: The radius of the creation button, used if create_button is true.

    Returns:
        int | str: The game state to move to, or an errors name.
    """
    # The user name is globally accessed so it can be continously updated.
    global user_name
    # If the caller needs to check if a button was clicked:
    if keystroke_type == "click":
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the create_button is being clicked:
            if create_button:
                # This is the Pythagorean theorem, getting the distance between 2 points (the mouse click, event, and the coordinates of the circle, button. 0 represents x, 1 represents y.)
                distance = math.sqrt(
                    (event.pos[0] - button[0]) ** 2 + (event.pos[1] - button[1]) ** 2
                )
                # If the distance between the 2 points lies within the circles radius, the desired state is returned.
                if distance <= radius:
                    button_state = desired_state
                    return button_state
                else:
                    return button_state
            # If the button is clicked:
            else:
                if button.collidepoint(event.pos):
                    # The desired_state provided in the argument is returned to the caller.
                    # Otherwise, nothing is returned and the state remains intact.
                    return desired_state
        else:
            return button_state

    # If the caller needs to check if the user is hovering over something:        
    if keystroke_type == "hover":
        # If the mouse is hovering over a menu item, its outline is thickened.
        # Otherwise, it remains the same.
        if button.collidepoint(pygame.mouse.get_pos()):
            thickness: int = 8
        else:
            thickness: int = 5
        return thickness
    
    # If the caller needs to check if the user is typing something:
    if keystroke_type == "type":
        if event.type == pygame.KEYDOWN:
            # The user_name variable is reduced by one if the user clicks backspace.
            if event.key == pygame.K_BACKSPACE:
                user_name = user_name[:-1]
            # If the user types something:
            elif event.unicode:
                # The keystroke is added into the variable.
                user_name += event.unicode
            # If the user tries to enter spaces as their name without meeting the character limit:
            if event.key == pygame.K_SPACE:
                # Length of the users_name is calculated.
                name_length = len(user_name)
                if name_length < 4:
                    # Their inputs are deleted.
                    user_name = ""
        # If all is well, the user_name is returned so another function can use it.
        return user_name
    
    # If the caller needs to check if the user pressed enter:
    if keystroke_type == "enter":
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # The name is reduced by 1 as the return key is also added to user_name when pressed.
                # This ensures the users name can be read as empty and the correct amount of characters.
                user_name = user_name[:-1]
                # Length of the users name is calculated.
                name_length = len(user_name)
                # If the user doesn't enter anything for their name:
                if user_name == "":
                    # The program defines the error as being no name, and returns the string.
                    error = "error_no_name"
                    return error
                # If the users name is below or above the following numbers:
                elif name_length < 3 or name_length > 25:
                    # The program defines the error as being a length error, and returns the string.
                    error = "error_length"
                    return error
                else:
                    # If no errors are made then the desired state is returned.
                    return desired_state

# This is the game loop responsible for calling the functions and receiving the returned values,
# then using those returns to call a different function to progress through the game.
while running:
    # A variable is defined as the pygame event enabler for cleanliness, and allows it to be 
    # used globally.
    events = pygame.event.get()
    for event in events:
    # If the user closes the window,
        if event.type == pygame.QUIT:
        # The loop ends.
            running = False   
    # If the game has been opened:
    if current_state == ProgramState.GAME_OPEN:
        # The corresponding function is called.
        main_screen_now(screen)
        # Another variable, state is responsible for the return value of this function.
        # This is because current_state can't also be defined as this otherwise it would
        # no longer equal GAME_OPEN, ending the current phase. So state and current_state
        # are constantly interchanged so the program functions correctly.
        state = start_order_now(screen)
    # As the variables in the ProgramState class have been defined as ints, the program checks
    # if the variables corresponding number has been returned.
    if state == 1:
        # Resets the screen.
        screen.fill(BLACK)
        main_screen_now(screen)
        # Variables interchange.
        current_state = main_menu(screen)
    if current_state == 2:
        screen.fill(BLACK)
        state = name_entry(screen, events)
    if current_state == ProgramState.CHOOSE_GAMEMODE:
        current_state = choose_gamemode(screen)
    if current_state == ProgramState.DAY_STATS:
        current_state = part_time_day(screen)
    if state == 5:
        screen.fill(BLACK)
        current_state = ingame_menu(screen, 1200, 700)
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
            5000,
        )
    # The display is constantly updated.
    pygame.display.flip()
    # The framerate is set to 30 to minimize system resources.
    pygame.time.Clock().tick(30)
# Once the main loop ends, the code moves onto the next piece of code, which is this.
pygame.quit()