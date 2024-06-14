# Importing pygame into the program
import pygame

# Activating pygame
pygame.init()

# CONSTANTS
# ------------#
# Defining the size of the game window in pixels as constants.
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 900
# The rgb code for each color.
YELLOW = (255, 255, 0)
DARK_YELLOW = (254, 221, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
# Outline for the boxes displayed in game.
OUTLINE_WIDTH: int = 5
# Width and height of boxes on the second kiosk screen.
BUTTON2_WIDTH: int = 149
BUTTON2_HEIGHT: int = 56
BUTTON2_HEIGHT_EXTENDED: int = 96
# Size of the icons used on the second kiosk screen.
ICON: tuple[int, int] = 50, 50
# The variable responsible for creating the game window with the parameters provided.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

user_name = ""
# The title of the game window.
pygame.display.set_caption("McHugo's")

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
start_order_1 = start_order_font.render("PRESS", True, DARK_YELLOW)
start_order_2 = start_order_font_xs.render("SPACE", True, DARK_YELLOW)
start_order_3 = start_order_font.render("TO", True, DARK_YELLOW)
start_order_4 = start_order_font_xs.render("ORDER", True, DARK_YELLOW)
prototype2_tutorial = heading_font.render(
    "Use your keys to interact with the", True, YELLOW
)
prototype2_tutorial_2 = heading_font.render("menu!", True, YELLOW)
version = heading_font.render("VERSION: PROTO 1.2", True, RED)
# Second main menu screen
play_button = main_menu_options.render("PLAY", True, DARK_YELLOW)
tutorial_button_1 = main_menu_options.render("FIRST", True, DARK_YELLOW)
tutorial_button_2 = main_menu_options.render("SHIFT", True, DARK_YELLOW)
scoreboard_button_1 = main_menu_options_xs.render("SCORE", True, DARK_YELLOW)
scoreboard_button_2 = main_menu_options_xs2.render("BOARD", True, DARK_YELLOW)
setting_button = main_menu_options_xs3.render("SETTING", True, DARK_YELLOW)
option_1 = main_menu_options.render("1", True, DARK_YELLOW)
option_2 = main_menu_options.render("2", True, DARK_YELLOW)
option_3 = main_menu_options.render("3", True, DARK_YELLOW)
option_4 = main_menu_options.render("4", True, DARK_YELLOW)
# Screen after 'play'
enter_name = title_font.render("Enter the name", True, DARK_YELLOW)
enter_name_2 = title_font_xs.render("of your McHugo's", True, DARK_YELLOW)
enter_name_3 = title_font.render("store: ", True, DARK_YELLOW)

# These are the images used in the game.
background = pygame.image.load("images/background.jpg")
main_menu_kiosk = pygame.image.load("images/kiosk.png")
logo = pygame.image.load("images/logo.png")
play_icon = pygame.image.load(
    "images/play_icon.png"
)  # Reference: "https://www.freepik.com/icon/beef_1720541#fromView=family&page=1&position=39&uuid=904cbd81-764f-428a-8bbc-03b02c310ddf" Icon by Freepik
first_shift_icon = pygame.image.load(
    "images/first_shift_icon.png"
)  # Reference: "https://www.freepik.com/icon/question-mark_5726395" Icon by Freepik
settings_icon = pygame.image.load(
    "images/settings_icon.png"
)  # Reference: "https://www.freepik.com/author/freepik/icons/special-lineal-color_15" Icon by Freepik
scoreboard_icon = pygame.image.load(
    "images/scoreboard_icon.png"
)  # Reference: "https://www.freepik.com/author/freepik/icons/special-lineal-color_15" Icon by Freepik
name_background = pygame.image.load("images/darkened_background.png")

# These are images that have had their size altered.
logo_1 = pygame.transform.scale(logo, (400, 400))
logo_2 = pygame.transform.scale(logo, (51, 51))
logo_3 = pygame.transform.scale(logo, (80, 80))
play_icon_sized = pygame.transform.scale(play_icon, (ICON))
first_shift_icon_sized = pygame.transform.scale(first_shift_icon, (ICON))
settings_icon_sized = pygame.transform.scale(settings_icon, (ICON))
scoreboard_icon_sized = pygame.transform.scale(scoreboard_icon, (ICON))

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
begin_game: bool = False
# Fixes the glitch where a one appears when going to the username screen.
one_glitch_fix: bool = False
# These are rectangles drawn on places on the screen the user can't reach to define the variable for event handling.
# They are not actually used.
play = pygame.draw.rect(screen, BLACK, (0, 0, 0, 0))
# Unless the game is closed, this will always be onscreen.
while running is True:
    if main_screen is True:
        screen.blit(background, (0, 0))
        screen.blit(main_menu_kiosk, (0, 35))
        screen.blit(game_title, (325, -25))
        screen.blit(logo_1, (400, 80))
        screen.blit(logo_2, (199, 535))
        screen.blit(prototype2_tutorial, (325, 450))
        screen.blit(prototype2_tutorial_2, (540, 500))
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
            screen.blit(start_order_3, (110, 330))
            screen.blit(start_order_4, (50, 378))
            start_order_position = pygame.draw.rect(
                screen, BLACK, (44, 240, 200, 200), OUTLINE_WIDTH
            )
    # If the user starts their order, a new menu on the kiosk is drawn with new buttons.
    if start_order is True:
        screen.blit(logo_3, (105, 50))
        play = pygame.draw.rect(
            screen, BLACK, (60, 125, BUTTON2_WIDTH, BUTTON2_HEIGHT), OUTLINE_WIDTH
        )
        first_shift = pygame.draw.rect(
            screen,
            BLACK,
            (60, 191, BUTTON2_WIDTH, BUTTON2_HEIGHT_EXTENDED),
            OUTLINE_WIDTH,
        )
        scoreboard = pygame.draw.rect(
            screen,
            BLACK,
            (60, 297, BUTTON2_WIDTH, BUTTON2_HEIGHT_EXTENDED),
            OUTLINE_WIDTH,
        )
        settings = pygame.draw.rect(
            screen, BLACK, (60, 403, BUTTON2_WIDTH, BUTTON2_HEIGHT), OUTLINE_WIDTH
        )
        screen.blit(play_button, (65, 125))
        screen.blit(tutorial_button_1, (65, 192))
        screen.blit(tutorial_button_2, (65, 232))
        screen.blit(scoreboard_button_1, (65, 297))
        screen.blit(scoreboard_button_2, (65, 342))
        screen.blit(setting_button, (67, 412))
        screen.blit(option_1, (33, 123))
        screen.blit(option_2, (30, 212))
        screen.blit(option_3, (30, 319))
        screen.blit(option_4, (27, 402))
        screen.blit(play_icon_sized, (210, 125))
        screen.blit(first_shift_icon_sized, (210, 215))
        screen.blit(settings_icon_sized, (210, 405))
        screen.blit(scoreboard_icon_sized, (210, 320))
    if one_glitch_fix is True:
        user_name = ""
        one_glitch_fix = False
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
    if begin_game is True:
        screen.fill(BLACK)
    for event in pygame.event.get():
        # If the user closes the window,
        if event.type == pygame.QUIT:
            # The loop ends,
            running = False
        # If the user clicks on 'start order', the following code executes:
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # The program recognises the user has clicked on 'start order' and will no longer run the code requiring start_order to be false.
                start_order = True
        # If the user clicks on the play button:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                # The game changes to the 'type name' phase.
                main_screen = False
                start_order = False
                type_name = True
                one_glitch_fix = True
        # Only if the user is typing their name will the following happen.
        if type_name is True:
            # If the user presses any key:
            if event.type == pygame.KEYDOWN:
                # The user_name variable is reduced by one.
                if event.key == pygame.K_BACKSPACE:
                    user_name = user_name[:-1]
                else:
                    # The keystroke is added into the variable.
                    user_name += event.unicode
            # If the user presses enter:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # The game starts, and the typing phase ends.
                    begin_game = True
                    type_name = False
    pygame.display.flip()
# Therefore moving onto the next bit of code, closing the window.
pygame.quit()
