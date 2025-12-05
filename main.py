from turtle import Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
import time
import pygame

# Initialize pygame mixer for sound effects
pygame.mixer.init()
bounce_sound = pygame.mixer.Sound("bounce.wav")
score_sound = pygame.mixer.Sound("score.wav")

# Set up screen
screen = Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.title("Pong")
screen.tracer(0)

# Create paddles, ball, and scoreboard
r_paddle = Paddle((350, 0))
l_paddle = Paddle((-350, 0))
ball = Ball()
scoreboard = Scoreboard()

# Flags for continuous paddle movement
r_moving_up = False
r_moving_down = False
l_moving_up = False
l_moving_down = False

# Key press/release handlers
def r_up_press():    global r_moving_up; r_moving_up = True
def r_up_release():  global r_moving_up; r_moving_up = False
def r_down_press():  global r_moving_down; r_moving_down = True
def r_down_release():global r_moving_down; r_moving_down = False
def l_up_press():    global l_moving_up; l_moving_up = True
def l_up_release():  global l_moving_up; l_moving_up = False
def l_down_press():  global l_moving_down; l_moving_down = True
def l_down_release():global l_moving_down; l_moving_down = False

# Bind keys for continuous movement
screen.listen()
screen.onkeypress(r_up_press, "Up")
screen.onkeyrelease(r_up_release, "Up")
screen.onkeypress(r_down_press, "Down")
screen.onkeyrelease(r_down_release, "Down")
screen.onkeypress(l_up_press, "w")
screen.onkeyrelease(l_up_release, "w")
screen.onkeypress(l_down_press, "s")
screen.onkeyrelease(l_down_release, "s")

# Main game loop
game_is_on = True
while game_is_on:
    time.sleep(ball.ball_speed)
    screen.update()
    ball.move()

    # Continuous paddle movement
    if r_moving_up: r_paddle.up()
    if r_moving_down: r_paddle.down()
    if l_moving_up: l_paddle.up()
    if l_moving_down: l_paddle.down()

    # Ball collision with top/bottom walls
    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.bounce_y()
        bounce_sound.stop()
        bounce_sound.play()

    # Ball collision with paddles
    if (ball.distance(r_paddle) < 50 and ball.xcor() > 320) or (ball.distance(l_paddle) < 50 and ball.xcor() < -320):
        ball.increase_speed()
        ball.bounce_x()

        # Move ball slightly outside paddle to avoid sticking
        if ball.xcor() > 0:
            ball.setx(r_paddle.xcor() - 50)
        else:
            ball.setx(l_paddle.xcor() + 50)

        bounce_sound.stop()
        bounce_sound.play()

    # Ball goes off the screen: update score
    if ball.xcor() > 400:
        ball.reset_position()
        scoreboard.l_point()
        score_sound.play()
    elif ball.xcor() < -400:
        ball.reset_position()
        scoreboard.r_point()
        score_sound.play()

screen.exitonclick()
