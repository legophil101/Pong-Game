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
bounce_sound = pygame.mixer.Sound("bounce.wav")
score_sound = pygame.mixer.Sound("score.wav")

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
game_state = "MENU"  # Can be "MENU" or "GAME"

# ----------------------------------------------
# CPU difficulty settings (tuned harder)
# ----------------------------------------------
# Paddle speed per difficulty level (lower = slower, easier to beat)
CPU_SPEED = {
    "Easy": 2,  # much slower → very beatable
    "Medium": 4,  # moderate → can challenge, but not too hard
    "Hard": 6  # still challenging, but not impossible
}

# Reaction margin per difficulty level (higher = more “lazy” CPU, easier)
REACTION_MARGIN = {
    "Easy": 80,  # lazy → makes more mistakes, easier to score
    "Medium": 40,  # tracks better
    "Hard": 20  # precise tracking
}

# Hesitation chance per difficulty level (higher = more likely to “hesitate”)
HESITATION_CHANCE = {
    "Easy": 0.6,  # 60% chance to hesitate → very forgiving
    "Medium": 0.3,  # occasional mistakes
    "Hard": 0.1  # very few mistakes
}


# ----------------------------------------------
# MENU KEYBINDS — selecting game modes / difficulty
# ----------------------------------------------
def pick_1p():
    """Choose single-player mode → show CPU difficulty options."""
    menu.select_1p()
    menu.show_cpu_options()


def pick_2p():
    """Choose two-player mode → start game immediately."""
    menu.select_2p()
    start_game()


def easy():
    """If 1P mode selected → start game on EASY difficulty."""
    if menu.selected_mode == "P1":
        menu.set_easy()
        start_game()


def medium():
    """If 1P mode selected → start game on MEDIUM difficulty."""
    if menu.selected_mode == "P1":
        menu.set_medium()
        start_game()


def hard():
    """If 1P mode selected → start game on HARD difficulty."""
    if menu.selected_mode == "P1":
        menu.set_hard()
        start_game()


# ----------------------------------------------
# CPU PADDLE MOVEMENT
# ----------------------------------------------
def move_cpu():
    """Move the CPU paddle toward the ball with smarter human-like behavior."""
    if menu.selected_mode != "P1":
        return  # CPU only active in single-player mode

    speed = CPU_SPEED.get(menu.cpu_difficulty, 5)
    margin = REACTION_MARGIN.get(menu.cpu_difficulty, 20)
    hesitate = HESITATION_CHANCE.get(menu.cpu_difficulty, 0.1)

    # Random hesitation
    if random.random() < hesitate:
        return

    # Add a little random offset to simulate human imperfection
    offset = random.randint(-margin // 2, margin // 2)

    diff = ball.ycor() - l_paddle.ycor() + offset

    if abs(diff) > margin:
        steps = speed // MOVE_DISTANCE
        steps = max(1, steps)  # ensure at least 1 step
        if diff > 0:
            for _ in range(steps):
                l_paddle.up()
        else:
            for _ in range(steps):
                l_paddle.down()


# ----------------------------------------------
# START GAME — called after menu selection
# ----------------------------------------------
def start_game():
    """Clear menu and start the actual game."""
    global game_state, r_paddle, l_paddle, ball, scoreboard
    menu.clear_menu()
    game_state = "GAME"

    # Create game objects now (only once)
    r_paddle = Paddle((350, 0))
    l_paddle = Paddle((-350, 0))
    ball = Ball()
    scoreboard = Scoreboard()


# ----------------------------------------------
# FLAGS FOR SMOOTH (HELD) PADDLE MOVEMENT
# ----------------------------------------------
r_moving_up = False
r_moving_down = False
l_moving_up = False
l_moving_down = False

# Pause and game loop flags
game_is_paused = False
game_is_on = True


# ----------------------------------------------
# PADDLE MOVEMENT INPUT HANDLERS
# (keypress = start movement, keyrelease = stop)
# ----------------------------------------------
def r_up_press():
    """Right paddle moves up while key is held."""
    global r_moving_up
    r_moving_up = True


def r_up_release():
    """Stop right paddle upward movement."""
    global r_moving_up
    r_moving_up = False


def r_down_press():
    global r_moving_down
    r_moving_down = True


def r_down_release():
    global r_moving_down
    r_moving_down = False


def l_up_press():
    global l_moving_up
    l_moving_up = True


def l_up_release():
    global l_moving_up
    l_moving_up = False


def l_down_press():
    global l_moving_down
    l_moving_down = True


def l_down_release():
    global l_moving_down
    l_moving_down = False


# ----------------------------------------------
# PAUSE SYSTEM
# ----------------------------------------------
def toggle_pause():
    """Toggle pause on/off and update scoreboard display. Only works in GAME state."""
    global game_is_paused
    if game_state != "GAME":
        return  # Don't pause when in menu or other states

    game_is_paused = not game_is_paused

    if game_is_paused:
        scoreboard.show_pause()
    else:
        scoreboard.hide_pause()


# ----------------------------------------------
# KEY BINDINGS
# ----------------------------------------------
screen.listen()

# Continuous paddle movement
screen.onkeypress(r_up_press, "Up")
screen.onkeyrelease(r_up_release, "Up")

screen.onkeypress(r_down_press, "Down")
screen.onkeyrelease(r_down_release, "Down")

screen.onkeypress(l_up_press, "w")
screen.onkeyrelease(l_up_release, "w")

screen.onkeypress(l_down_press, "s")
screen.onkeyrelease(l_down_release, "s")

# Pause button
screen.onkeypress(toggle_pause, "p")

# MENU button keybinds
screen.onkey(pick_1p, "1")
screen.onkey(pick_2p, "2")
screen.onkey(easy, "e")
screen.onkey(medium, "m")
screen.onkey(hard, "h")

# ----------------------------------------------
# MAIN GAME LOOP
# Only runs if: game_is_on == True AND game_state == "GAME"
# ----------------------------------------------

while game_is_on:
    screen.update()

    if game_state == "MENU":
        # Do nothing or animate the menu if you want
        screen.update()  # keeps menu interactive/animated
        continue

    if game_state == "GAME":
        time.sleep(ball.ball_speed)  # control speed per frame

        if not game_is_paused:
            # CPU movement only in 1P mode
            move_cpu()

            # --- Ball movement ---
            ball.move()

            # --- Paddle movement (smooth / continuous) ---
            if r_moving_up:
                r_paddle.up()
            if r_moving_down:
                r_paddle.down()
            if l_moving_up:
                l_paddle.up()
            if l_moving_down:
                l_paddle.down()

            # --- Ball collision with top/bottom walls ---
            if ball.ycor() > 280 or ball.ycor() < -280:
                ball.bounce_y()
                bounce_sound.stop()
                bounce_sound.play()

            # --- Ball collision with paddles ---
            if (ball.distance(r_paddle) < 50 and ball.xcor() > 320) or \
                    (ball.distance(l_paddle) < 50 and ball.xcor() < -320):

                ball.increase_speed()
                ball.bounce_x()

                # Prevent the ball from getting stuck inside the paddle
                if ball.xcor() > 0:
                    ball.setx(r_paddle.xcor() - 50)
                else:
                    ball.setx(l_paddle.xcor() + 50)

                bounce_sound.stop()
                bounce_sound.play()

            # --- Scoring system: ball passes the paddle ---
            if ball.xcor() > 400:
                ball.reset_position()
                scoreboard.l_point()
                score_sound.play()

            elif ball.xcor() < -400:
                ball.reset_position()
                scoreboard.r_point()
                score_sound.play()

screen.exitonclick()
