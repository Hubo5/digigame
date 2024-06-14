# Importing pygame into the program
import pygame

# Activating pygame
pygame.init()


# CONSTANTS ------------------


# Defining the size of the game window in pixels as constants.
SCREEN_WIDTH = 1000  # 1200
SCREEN_HEIGHT = 900  # 700
# The rgb code for each color.
YELLOW = (255, 255, 0)
DARK_YELLOW = (254, 221, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
# Outline for most of the boxes displayed in game.
OUTLINE_WIDTH: int = 5
# Width and height of boxes on the second kiosk screen.
BUTTON2_WIDTH: int = 149
BUTTON2_HEIGHT: int = 56
BUTTON2_HEIGHT_EXTENDED: int = 96
# Size of the icons used on the second kiosk screen.
ICON: tuple[int, int] = 50, 50

# PREDEFINED VARIABLES ------------------


# The variable responsible for creating the game window with the parameters provided.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Sets the users name to none so they can make their own.
user_name = ""
# The title of the game window.
pygame.display.set_caption("McHugo's")
# The outlines for different shapes. These all have to be seperate because their values
# are indivdually modified.
menu_box_1: int = 5
menu_box_2: int = 5
menu_box_3: int = 5
menu_box_4: int = 5
# Colours of the circles in the game selection menu.
circle_colour_1: tuple[int, int, int] = (255, 255, 255)
circle_colour_2: tuple[int, int, int] = (255, 255, 255)
# This boolean controls the flashing start order button, and when its visible.
visible: bool = True
# This boolean sets the time since the last switch from visible to not visible (part of the blinking order variable)
last_switch: int = 0
# This boolean controls whether the game is running or not.
running: bool = True
# These booleans check if various buttons have been clicked or if values have been entered.
# All are defaulted as false so the game goes through its phases periodically.
start_order: bool = False
type_name: bool = False
main_screen: bool = True
choose_game_type: bool = False
# Checks what day it is, and displays the day.
part_time_day: bool = False
day: int = 0
# The
day_names: list[str] = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
# These are rectangles drawn on places on the screen the user can't reach to define the variable for event handling.
# They are not actually used.
play = pygame.draw.rect(screen, BLACK, (0, 0, 0, 0))
back = pygame.draw.rect(screen, BLACK, (0, 0, 0, 0))
part_time = pygame.draw.rect(screen, BLACK, (0, 0, 0, 0))
on_call = pygame.draw.rect(screen, BLACK, (0, 0, 0, 0))
# Checks if the user didn't enter a name.
error_no_name: bool = False
# Checks if the length is too short or long of the users name.
error_length: bool = False
# Controls how long the error message is visible for.
error_triggered: int = 0
# FONTS AND IMAGES ------------------


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
version = heading_font.render("VERSION: PROTO 1.1", True, RED)
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
# Choosing a game mode
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

# These are images that have had their size altered.
logo_1 = pygame.transform.scale(logo, (400, 400))
logo_2 = pygame.transform.scale(logo, (51, 51))
logo_3 = pygame.transform.scale(logo, (80, 80))
play_icon_sized = pygame.transform.scale(play_icon, (ICON))
first_shift_icon_sized = pygame.transform.scale(first_shift_icon, (ICON))
settings_icon_sized = pygame.transform.scale(settings_icon, (ICON))
scoreboard_icon_sized = pygame.transform.scale(scoreboard_icon, (ICON))
back_name_sized = pygame.transform.scale(back_name, (ICON))

# GAME CODE ------------------


# Unless the game is closed, this will always be onscreen.
while running is True:
    if main_screen is True:
        screen.blit(background, (0, 0))
        screen.blit(main_menu_kiosk, (0, 35))
        screen.blit(game_title, (325, -25))
        screen.blit(logo_1, (400, 80))
        screen.blit(logo_2, (199, 535))
        screen.blit(version, (620, 840))
    # Only if the user has not clicked 'start order' will these lines of code execute.
    if start_order is False:
        screen.blit(kiosk_heading_1, (38, 55))
        screen.blit(kiosk_heading_2, (48, 90))
        screen.blit(hungry_hugo, (44, 180))
        # Checks how long it was until the game was opened, for a future variable.
        game_opened = pygame.time.get_ticks()
        # If the game running minus the last visibility switch equals 2:
        if game_opened - last_switch > 2000:
            # Visibility is changed to none.
            visible = not visible
            # The last switch variable is changed to the amount of time the game has been opened for.
            last_switch = game_opened
        # If visibility of the box has been toggled to on, the box is drawn.
        if visible:
            screen.blit(start_order_1, (50, 235))
            screen.blit(start_order_2, (50, 285))
            screen.blit(start_order_3, (65, 330))
            screen.blit(start_order_4, (110, 378))
            start_order_position = pygame.draw.rect(
                screen, BLACK, (44, 240, 200, 200), OUTLINE_WIDTH
            )
    # If the user starts their order, a new menu on the kiosk is drawn with new buttons.
    if start_order is True:
        screen.blit(logo_3, (105, 50))
        play = pygame.draw.rect(
            screen, BLACK, (40, 125, BUTTON2_WIDTH, BUTTON2_HEIGHT), menu_box_1
        )
        first_shift = pygame.draw.rect(
            screen,
            BLACK,
            (40, 191, BUTTON2_WIDTH, BUTTON2_HEIGHT_EXTENDED),
            menu_box_2,
        )
        scoreboard = pygame.draw.rect(
            screen,
            BLACK,
            (40, 297, BUTTON2_WIDTH, BUTTON2_HEIGHT_EXTENDED),
            menu_box_3,
        )
        settings = pygame.draw.rect(
            screen, BLACK, (40, 403, BUTTON2_WIDTH, BUTTON2_HEIGHT), menu_box_4
        )
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
        # If the mouse is hovering over a menu item, its outline is thickened.
        # Otherwise, it remains the same.
        if play.collidepoint(pygame.mouse.get_pos()):
            menu_box_1 = 8
        else:
            menu_box_1 = 5
        if first_shift.collidepoint(pygame.mouse.get_pos()):
            menu_box_2 = 8
        else:
            menu_box_2 = 5
        if scoreboard.collidepoint(pygame.mouse.get_pos()):
            menu_box_3 = 8
        else:
            menu_box_3 = 5
        if settings.collidepoint(pygame.mouse.get_pos()):
            menu_box_4 = 8
        else:
            menu_box_4 = 5
    # If the user presses play, the background is darkened, and all previous material is removed.
    if type_name is True:
        # This piece of text has to be stored in the while loop so its constantly updated with new inputs.
        username_input = name_font.render(user_name, True, DARK_YELLOW)
        screen.blit(name_background, (0, 0))
        screen.blit(enter_name, (20, 50))
        screen.blit(enter_name_2, (40, 190))
        screen.blit(enter_name_3, (300, 290))
        # This is the users input.
        screen.blit(username_input, (30, 430))
        # This is the back buttons textures.
        back = pygame.draw.rect(screen, RED, (370, 800, 240, BUTTON2_HEIGHT))
        back_outline = pygame.draw.rect(
            screen, WHITE, (370, 800, 240, BUTTON2_HEIGHT), 4
        )
        screen.blit(back_name_sized, (375, 805))
        screen.blit(back_name_text, (440, 800))
        # If the user doesn't enter a name:
        if error_no_name is True:
            # The time since the error was triggered is noted (/1000 to convert milliseconds)
            elapsed_time = pygame.time.get_ticks() - error_triggered
            if elapsed_time < 3000:
                # An error message is displayed.
                screen.blit(no_name, (200, 630))
            else:
                error_no_name = False
        # If the user entered the incorrect amount of characters while typing their name:
        if error_length is True:
            elapsed_time = pygame.time.get_ticks() - error_triggered
            if elapsed_time < 3000:
                # A different message is displayed.
                screen.blit(length_incorrect, (5, 630))
            else:
                error_length = False
    if choose_game_type is True:
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
    if part_time_day is True:
        screen.fill(BLACK)
        day = day + 1
    # EVENT HANDLING ------------------

    for event in pygame.event.get():
        # If the user closes the window,
        if event.type == pygame.QUIT:
            # The loop ends,
            running = False
        # If the user clicks on 'start order', the following code executes:
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_order_position.collidepoint(event.pos):
                # The program recognises the user has clicked on 'start order' and will no longer run the code requiring start_order to be false.
                start_order = True
        # If the user clicks on the play button:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play.collidepoint(event.pos):
                # The game changes to the 'type name' phase.
                type_name = True
                main_screen = False
                start_order = False
        # Only if the user is typing their name will the following happen.
        if type_name is True:
            # If the user clicks the back button:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.collidepoint(event.pos):
                    # They return to the main menu.
                    main_screen = True
                    start_order = True
                    type_name = False
            # If the user presses any key:
            if event.type == pygame.KEYDOWN:
                # The user_name variable is reduced by one.
                if event.key == pygame.K_BACKSPACE:
                    user_name = user_name[:-1]
                else:
                    # The keystroke is added into the variable.
                    user_name += event.unicode
                # If the presses enter while typing:
                if event.key == pygame.K_RETURN:
                    # The name is reduced by 1 as the return key is also added to the variable when pressed.
                    # This ensures the users name can be read as empty and the correct amount of characters.
                    user_name = user_name[:-1]
                    # Length of the users name is calculated.
                    name_length = len(user_name)
                    # If the user doesn't enter anything for their name:
                    if user_name == "":
                        # The no name error message is triggered, and if the length message is showing, it is disabled.
                        error_no_name = True
                        error_length = False
                        # The program begins counting the amount of time since the error was triggered.
                        error_triggered = pygame.time.get_ticks()
                    # If the users name is below or above the following numbers:
                    elif name_length < 3 or name_length > 25:
                        # The opposites of the other error is triggered.
                        error_length = True
                        error_no_name = False
                        error_triggered = pygame.time.get_ticks()
                    else:
                        # The game starts, and the typing phase ends.
                        choose_game_type = True
                        type_name = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if part_time.collidepoint(event.pos):
                part_time_day = True
                choose_game_type = False
    pygame.display.flip()
# Therefore moving onto the next bit of code, closing the window.
pygame.quit()
