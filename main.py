from turtle import Screen
from paddle import Paddle
from ball import Ball
import time
from scoreboard import Scoreboard
import pygame

# Sound Effects
pygame.mixer.init()
bounce_sound = pygame.mixer.Sound("bounce.wav")
score_sound = pygame.mixer.Sound("score.wav")

screen = Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.title("Pong")
screen.tracer(0)

r_paddle = Paddle((350, 0))
l_paddle = Paddle((-350, 0))
ball = Ball()
scoreboard = Scoreboard()

screen.listen()
screen.onkeypress(r_paddle.up, "Up")
screen.onkeypress(r_paddle.down, "Down")
screen.onkeypress(l_paddle.up, "w")
screen.onkeypress(l_paddle.down, "s")

game_is_on = True
while game_is_on:
    time.sleep(ball.ball_speed)
    screen.update()
    ball.move()

    # detect collision with wall
    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.bounce_y()
        bounce_sound.stop()
        bounce_sound.play()

    # detect collision with r_paddle
    if ball.distance(r_paddle) < 50 and ball.xcor() > 320 or ball.distance(l_paddle) < 50 and ball.xcor() < -320:
        ball.increase_speed()
        ball.bounce_x()
        bounce_sound.stop()
        bounce_sound.play()

    # detect when the paddle misses
    if ball.xcor() > 400:
        ball.reset_position()
        scoreboard.l_point()
        score_sound.play()

    elif ball.xcor() < -400:
        ball.reset_position()
        scoreboard.r_point()
        score_sound.play()

screen.exitonclick()
