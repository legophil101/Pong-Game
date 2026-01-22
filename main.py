from turtle import Screen
from paddle import Paddle, MOVE_DISTANCE
from ball import Ball
from scoreboard import Scoreboard
from menu import Menu
import time
import pygame
import random

# Initialize pygame mixer for sound effects
pygame.mixer.init()
intro_sound = pygame.mixer.Sound("sounds/pong_game_intro.wav")
bounce_sound = pygame.mixer.Sound("sounds/bounce.wav")
score_sound = pygame.mixer.Sound("sounds/score.wav")
wall_sound = pygame.mixer.Sound("sounds/wall.wav")
win_sound = pygame.mixer.Sound("sounds/win.wav")
lose_sound = pygame.mixer.Sound("sounds/lose.wav")

# ----------------------------------------------
# SETUP: initialize the screen and all game objects
# ----------------------------------------------
screen = Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.title("Pong")
screen.tracer(0)  # Turn off auto-refresh (we manually control updates)

# Create menu (shown at the start)
menu = Menu()
game_state = "MENU"  # Can be "MENU", "GAME", or "PAUSED"

# ----------------------------------------------
# CPU DIFFICULTY SETTINGS
# ----------------------------------------------
CPU_SPEED = {"Easy": 2, "Medium": 4, "Hard": 6}
REACTION_MARGIN = {"Easy": 80, "Medium": 40, "Hard": 20}
HESITATION_CHANCE = {"Easy": 0.6, "Medium": 0.3, "Hard": 0.1}


# ----------------------------------------------
# MENU KEYBINDS — selecting game modes / difficulty
# ----------------------------------------------
def pick_1p():
    """Choose single-player mode → show match length options first."""
    global game_state
    if game_state == "MENU" and menu.selected_mode is None:
        menu.select_1p()
        menu.show_ball_mode_menu()


def pick_2p():
    """Choose two-player mode → show match length options immediately."""
    global game_state
    if game_state == "MENU" and menu.selected_mode is None:
        menu.select_2p()
        menu.show_ball_mode_menu()


def classic_mode():
    # Ensure this only works on the correct screen
    if game_state == "MENU" and menu.current_screen == "BALL_MODE":
        menu.set_classic()
        menu.match_length_options()  # This sets current_screen to "LENGTH"


def modern_mode():
    if game_state == "MENU" and menu.current_screen == "BALL_MODE":
        menu.set_modern()
        menu.match_length_options()


def easy():
    # Only start the game if we are actually ON the difficulty screen
    if game_state == "MENU" and menu.current_screen == "DIFFICULTY":
        menu.set_easy()
        start_game()


def medium():
    if game_state == "MENU" and menu.current_screen == "DIFFICULTY":
        menu.set_medium()
        start_game()


def hard():
    if game_state == "MENU" and menu.current_screen == "DIFFICULTY":
        menu.set_hard()
        start_game()


# ----------------------------------------------
# MENU KEYBINDS — selecting game modes / difficulty
# ----------------------------------------------
# Helper function to handle point selection logic
def set_points(points):
    # FIX: Added check for menu.current_screen == "LENGTH"
    if game_state == "MENU" and menu.current_screen == "LENGTH":
        menu.match_points = points
        if menu.selected_mode == "P1":
            menu.show_cpu_options()  # Moves to "DIFFICULTY"
        else:
            start_game()  # P2 starts immediately


def pick_3(): set_points(3)


def pick_5(): set_points(5)


def pick_7(): set_points(7)


def pick_10(): set_points(10)


# ----------------------------------------------
# CPU PADDLE MOVEMENT
# ----------------------------------------------
def move_cpu():
    """Move the CPU paddle toward the ball with smarter human-like behavior."""
    if menu.selected_mode != "P1":
        return

    speed = CPU_SPEED.get(menu.cpu_difficulty, 5)
    margin = REACTION_MARGIN.get(menu.cpu_difficulty, 20)
    hesitate = HESITATION_CHANCE.get(menu.cpu_difficulty, 0.1)

    if random.random() < hesitate:
        return

    offset = random.randint(-margin // 2, margin // 2)
    diff = ball.ycor() - l_paddle.ycor() + offset

    if abs(diff) > margin:
        steps = max(1, speed // MOVE_DISTANCE)
        if diff > 0:
            for _ in range(steps): l_paddle.up()
        else:
            for _ in range(steps): l_paddle.down()


# ----------------------------------------------
# START GAME — called after menu selection
# ----------------------------------------------
def start_game():
    """Clear menu and start the actual game."""
    global game_state, r_paddle, l_paddle, ball, scoreboard
    intro_sound.stop()  # STOP MENU MUSIC HERE
    menu.clear_menu()
    game_state = "PLAYING"

    # Create game objects now (only once)
    r_paddle = Paddle((350, 0))
    l_paddle = Paddle((-350, 0))
    ball = Ball(mode=menu.ball_mode)
    scoreboard = Scoreboard()


# ----------------------------------------------
# FLAGS FOR SMOOTH (HELD) PADDLE MOVEMENT
# ----------------------------------------------
r_moving_up = False
r_moving_down = False
l_moving_up = False
l_moving_down = False

game_is_on = True


# ----------------------------------------------
# PADDLE MOVEMENT INPUT HANDLERS
# ----------------------------------------------
def r_up_press(): global r_moving_up; r_moving_up = True


def r_up_release(): global r_moving_up; r_moving_up = False


def r_down_press(): global r_moving_down; r_moving_down = True


def r_down_release(): global r_moving_down; r_moving_down = False


def l_up_press(): global l_moving_up; l_moving_up = True


def l_up_release(): global l_moving_up; l_moving_up = False


def l_down_press(): global l_moving_down; l_moving_down = True


def l_down_release(): global l_moving_down; l_moving_down = False


# ----------------------------------------------
# PAUSE SYSTEM
# ----------------------------------------------
def toggle_pause():
    global game_state
    if game_state == "PLAYING":
        game_state = "PAUSED"
        menu.show_pause_menu()
    elif game_state == "PAUSED":
        resume_game()


def resume_game():
    global game_state
    game_state = "PLAYING"
    menu.clear()


def restart_match():
    global game_state
    # FIX: Don't allow restart if we are in the MENU
    if game_state == "MENU":
        return

    game_state = "PLAYING"
    try:
        r_paddle.hideturtle()
        l_paddle.hideturtle()
        ball.hideturtle()
        scoreboard.clear()
    except NameError:
        pass

    menu.clear()
    start_game()


def pause_to_main_menu():
    global game_state
    intro_sound.stop()
    game_state = "MENU"
    try:
        r_paddle.hideturtle()
        l_paddle.hideturtle()
        ball.hideturtle()
        scoreboard.clear()
    except NameError:
        pass

    menu.clear()
    # FIX: Reset selected mode so logic starts fresh
    menu.selected_mode = None
    menu.show_main_menu()


def pause_back():
    if game_state == "PAUSED":
        resume_game()


# ----------------------------------------------
# CONTEXT AWARE KEYS
# ----------------------------------------------
# Update handle_m_key to be more precise
def handle_m_key():
    if game_state == "PAUSED" or game_state == "GAME_OVER":
        pause_to_main_menu()
    elif menu.current_screen == "BALL_MODE":
        modern_mode()
    elif menu.current_screen == "DIFFICULTY":  # Specific check added
        medium()


def handle_b_key():
    """Context-aware back button for Pause and Menu navigation."""
    if game_state == "PAUSED":
        resume_game()

    elif game_state == "MENU":

        if menu.current_screen == "DIFFICULTY":
            # Difficulty -> Match Length
            menu.match_length_options()

        elif menu.current_screen == "LENGTH":
            # Match Length -> Ball Mode
            menu.show_ball_mode_menu()

        elif menu.current_screen == "BALL_MODE":
            # Ball Mode -> Main Menu
            menu.selected_mode = None
            menu.ball_mode = None
            menu.show_main_menu()

        elif menu.current_screen == "MAIN":
            # Already at main menu
            pass


def handle_t_key():
    if game_state == "PAUSED":  # Optional: can add or game_state == "PLAYING" for a quick restart feature
        restart_match()


def handle_r_key():
    """Resume the game if paused; otherwise ignore."""
    if game_state == "PAUSED":
        resume_game()


def handle_n_key():
    """Starts a new match with same settings if game is over."""
    if game_state == "GAME_OVER":
        restart_match()


# ----------------------------------------------
# KEY BINDINGS
# ----------------------------------------------
screen.listen()

# Movement (Always active, but paddles only move if PLAYING)
screen.onkeypress(r_up_press, "Up")
screen.onkeyrelease(r_up_release, "Up")
screen.onkeypress(r_down_press, "Down")
screen.onkeyrelease(r_down_release, "Down")
screen.onkeypress(l_up_press, "w")
screen.onkeyrelease(l_up_release, "w")
screen.onkeypress(l_down_press, "s")
screen.onkeyrelease(l_down_release, "s")

# Contextual Menu & System Keys
screen.onkey(toggle_pause, "Escape")
screen.onkey(handle_b_key, "b")  # Handles both "back" and "resume"
screen.onkey(handle_m_key, "m")  # Handles Modern Mode AND Medium Difficulty
screen.onkey(handle_r_key, "r")
screen.onkey(handle_t_key, "t")
screen.onkey(handle_n_key, "n")

# Mode Selection
screen.onkey(pick_1p, "1")
screen.onkey(pick_2p, "2")
screen.onkey(classic_mode, "c")
screen.onkey(easy, "e")
screen.onkey(hard, "h")

# Match Length (The numbers)
screen.onkey(pick_3, "3")
screen.onkey(pick_5, "5")
screen.onkey(pick_7, "7")
screen.onkey(pick_10, "0")

# ----------------------------------------------
# MAIN GAME LOOP
# ----------------------------------------------
menu_drawn = False

while game_is_on:
    screen.update()

    if game_state == "MENU":
        if not menu_drawn:
            menu.clear()
            menu.show_main_menu()
            intro_sound.play(loops=-1)
            menu_drawn = True
        continue
    else:
        menu_drawn = False

    if game_state == "PLAYING":
        time.sleep(ball.ball_speed)

        move_cpu()
        ball.move()

        # Paddle Movement
        if r_moving_up: r_paddle.up()
        if r_moving_down: r_paddle.down()
        if l_moving_up: l_paddle.up()
        if l_moving_down: l_paddle.down()

        # Walls
        if ball.ycor() > 280 or ball.ycor() < -280:
            ball.bounce_y()
            bounce_sound.stop();
            wall_sound.play()

        # Paddles
        if (ball.distance(r_paddle) < 50 and ball.xcor() > 320) or \
                (ball.distance(l_paddle) < 50 and ball.xcor() < -320):
            ball.increase_speed()
            ball.bounce_x(r_paddle if ball.xcor() > 0 else l_paddle)
            if ball.xcor() > 0:
                ball.setx(r_paddle.xcor() - 50)
            else:
                ball.setx(l_paddle.xcor() + 50)
            bounce_sound.stop();
            bounce_sound.play()

        # Scoring
        # Scoring Logic (Inside the while loop)
        if ball.xcor() > 400:  # Ball passed Right Player (P1)
            ball.reset_position()
            scoreboard.l_point()
            score_sound.play()
            if scoreboard.l_score >= menu.match_points:
                game_state = "GAME_OVER"
                # If P1 mode, Left Paddle is CPU
                winner_name = "CPU" if menu.selected_mode == "P1" else "Player 2"
                r_paddle.hideturtle();
                l_paddle.hideturtle();
                ball.hideturtle()

                if winner_name == "CPU":
                    lose_sound.play()
                else:
                    win_sound.play()
                menu.show_game_over(winner_name)

        elif ball.xcor() < -400:  # Ball passed Left Player (CPU/P2)
            ball.reset_position()
            scoreboard.r_point()
            score_sound.play()
            if scoreboard.r_score >= menu.match_points:
                game_state = "GAME_OVER"
                winner_name = "Player 1"
                r_paddle.hideturtle();
                l_paddle.hideturtle();
                ball.hideturtle()
                win_sound.play()  # Player 1 always wins here
                menu.show_game_over(winner_name)
    elif game_state == "PAUSED" or game_state == "GAME_OVER":
        screen.update()

screen.exitonclick()
