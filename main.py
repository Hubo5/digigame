from typing import Tuple
# Importing pygame into the program
import pygame

# Activating pygame
pygame.init()

# PROGRAM STATES

# These define what part of the program the user is up to, used for calling
# the correct function corresponding to the program state.
class ProgramState:
    GAME_OPEN: int = 0
    MAIN_MENU: int = 1
    ENTER_NAME: int = 2
    CHOOSE_GAMEMODE: int = 3
    DAY_STATS: int = 4
    GAME_MENU: int = 5
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
PATTY_ICON: tuple[int, int] = 80, 80
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
dthru_box_y_positions: list[int] = [0, 100, 200, 300, 400]

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
# TBR (Testing only, To Be Removed)
burger_notdone = body_font.render("burger", True, RED)
burger_done = body_font.render("burger", True, GREEN)
fries = body_font.render("fries", True, GREEN)
mcbullets = body_font.render("mcbullets", True, RED)
drink = body_font.render("hugo juice", True, GREEN)
counter_1 = body_font.render("3/5", True, WHITE)

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
# Menu items (all from Freepik)
improper_slammer = pygame.image.load("images/improper slammer.png")
colosall_hugo = pygame.image.load("images/colossal hugo.png")

# Patties
hugo_patty = pygame.image.load("images/10 to 1.png") # Reference: Icon by Erifqi Zetiawan
slammer_patty = pygame.image.load("images/4 to 1.png") # Reference: Icon by Freepik
angus_patty = pygame.image.load("images/angus.png") # Reference: Icon by Smashicons
chicken_patty = pygame.image.load("images/chicken.png") # Reference: Icon by Freepik

# These are images that have had their size altered.
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
improper_slammer_sized = pygame.transform.scale(improper_slammer, (MENU_ICON))
colosall_hugo_sized = pygame.transform.scale(colosall_hugo, (MENU_ICON))
hugo_patty_sized = pygame.transform.scale(hugo_patty, (PATTY_ICON))
slammer_patty_sized = pygame.transform.scale(slammer_patty, (PATTY_ICON))
angus_patty_sized = pygame.transform.scale(angus_patty, (PATTY_ICON))
chicken_patty_sized = pygame.transform.scale(chicken_patty, (PATTY_ICON))

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
    current_event = handle_events(event, "click", start_order_position, ProgramState.MAIN_MENU)
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
    menu_box_1 = handle_events(event, "hover", play_rect, None)
    menu_box_2 = handle_events(event, "hover", first_shift_rect, None)
    menu_box_3 = handle_events(event, "hover", scoreboard_rect, None)
    menu_box_4 = handle_events(event, "hover", settings_rect, None)  
    
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
    current_event = handle_events(event, "click", play, ProgramState.ENTER_NAME)
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
    
    # In order to be continously updated, the pygame event handling for loop must be 
    # used.
    for event in events:
        # If the user types, the event handling function handles the inputs appropiately.
        user_name = handle_events(event, "type", None, None)
        # Checks if the user clicked the back button, returning to the previous menu.
        previous_event = handle_events(event, "click", back, ProgramState.MAIN_MENU)
        # Checks if the user pressed enter. The desired state of GAME_MENU is only used if
        # the requirements in the handle_events function is met.
        current_event = handle_events(event, "enter", None, ProgramState.GAME_MENU)
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
    
def ingame_menu(screen, screen_width, screen_height):
    
    # The current screen dimensions are globally accessed so the program knows what
    # the current dimensions are.
    global current_screen_width, current_screen_height
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
    pygame.draw.rect(screen, WHITE, (120, 0, 150, 150), DTHRU_OUTLINE)
    pygame.draw.rect(screen, WHITE, (270, 0, 150, 150), DTHRU_OUTLINE)
    pygame.draw.rect(screen, WHITE, (420, 0, 150, 150), DTHRU_OUTLINE)
    pygame.draw.rect(screen, WHITE, (570, 0, 150, 150), DTHRU_OUTLINE)
    pygame.draw.rect(screen, WHITE, (720, 0, 150, 150), DTHRU_OUTLINE)
    pygame.draw.rect(screen, WHITE, (870, 0, 150, 150), DTHRU_OUTLINE)
    pygame.draw.rect(screen, WHITE, (1020, 0, 180, 150), DTHRU_OUTLINE)
    # The text for the boxes in the drive thru.
    screen.blit(time_text_4, (175, 60))
    screen.blit(time_text_4, (325, 60))
    screen.blit(time_text_4, (475, 60))
    screen.blit(time_text_4, (625, 60))
    screen.blit(time_text_4, (775, 60))
    screen.blit(time_text_4, (925, 60))
    screen.blit(time_text_4, (1090, 60))
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
    screen.blit(burger_notdone, (5, 175))
    screen.blit(burger_done, (5, 200))
    screen.blit(burger_notdone, (5, 225))
    screen.blit(burger_done, (5, 250))
    # Fries and nuggets.
    pygame.draw.rect(screen, YELLOW, (0, 290, 390, 30), DTHRU_OUTLINE)
    screen.blit(fries, (5, 285))
    screen.blit(mcbullets, (170, 285))
    # Hugo Juice.
    pygame.draw.rect(screen, BLUE, (390, 290, 180, 30), DTHRU_OUTLINE)
    screen.blit(drink, (395, 285))
    
    # The currently needed stock display.
    pygame.draw.rect(screen, RED, (15, 330, 130, 60), DTHRU_OUTLINE)

    # Section 2.
    pygame.draw.circle(screen, WHITE, (55, 370 + 130), 40, DTHRU_OUTLINE)
    screen.blit(improper_slammer_sized, (25, 338 + 130))
    screen.blit(counter_1, (35, 410 + 130))
    pygame.draw.circle(screen, WHITE, (145, 370 + 130), 40, DTHRU_OUTLINE)
    screen.blit(improper_slammer_sized, (115, 338 + 130))
    screen.blit(counter_1, (125, 410 + 130))
    pygame.draw.circle(screen, WHITE, (235, 370 + 130), 40, DTHRU_OUTLINE)
    screen.blit(improper_slammer_sized, (205, 338 + 130))
    screen.blit(counter_1, (215, 410 + 130))
    pygame.draw.circle(screen, WHITE, (235 + 90, 370 + 130), 40, DTHRU_OUTLINE)
    screen.blit(improper_slammer_sized, (205 + 90, 338 + 130))
    screen.blit(counter_1, (215 + 90, 410 + 130))
    pygame.draw.circle(screen, WHITE, (235 + 180, 370 + 130), 40, DTHRU_OUTLINE)
    screen.blit(improper_slammer_sized, (205 + 180, 338 + 130))
    screen.blit(counter_1, (215 + 180, 410 + 130))
    pygame.draw.circle(screen, WHITE, (235 + 270, 370 + 130), 40, DTHRU_OUTLINE)
    screen.blit(improper_slammer_sized, (205 + 270, 338 + 130))
    screen.blit(counter_1, (215 + 270, 410 + 130))
    
    # The section is for patties.
    pygame.draw.line(screen, WHITE, (0, 590), (567, 590), DTHRU_OUTLINE)
    screen.blit(hugo_patty_sized, (30, 590))
    screen.blit(counter_1, (50, 660))
    screen.blit(slammer_patty_sized, (160, 590))
    screen.blit(counter_1, (180, 660))
    screen.blit(angus_patty_sized, (290, 590))
    screen.blit(counter_1, (310, 660))
    screen.blit(chicken_patty_sized, (420, 590))
    screen.blit(counter_1, (430, 660))

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

def handle_events(event, keystroke_type: str, button, desired_state: int) -> int:
    """_summary_

    Args:
        event: The pygame event enabler.
        keystroke_type (str): The type of pressed key.
        button: The game element being interacted with.
        desired_state (int): The game state to move to.

    Returns:
        int | str: The game state to move to, or an errors name.
    """
    # The user name is globally accessed so it can be continously updated.
    global user_name
    # If the caller needs to check if a button was clicked:
    if keystroke_type == "click":
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the button is clicked:
            if button.collidepoint(event.pos):
                # The desired_state provided in the argument is returned to the caller.
                # Otherwise, nothing is returned and the state remains intact.
                return desired_state  
    
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
    # The display is constantly updated.
    pygame.display.flip()
    # The framerate is set to 30 to minimize system resources.
    pygame.time.Clock().tick(30)
# Once the main loop ends, the code moves onto the next piece of code, which is this.
pygame.quit()