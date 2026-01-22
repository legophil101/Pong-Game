from turtle import Turtle
import random
import math


class Ball(Turtle):
    """Represents the ball in the Pong game with movement, collisions, and speed control."""

    def __init__(self, mode="MODERN"):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()

        self.mode = mode  # "CLASSIC" or "MODERN"

        self.base_speed = 10
        self.max_speed = 16

        self.x_move = self.base_speed
        self.y_move = random.choice([-8, 8])
        self.ball_speed = 0.1

    def move(self):
        """Move the ball according to its x and y velocities."""
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_y(self):
        """Invert the y-direction velocity (bounce off top/bottom wall)."""
        self.y_move *= -1

    def bounce_x(self, paddle=None):
        """Invert the x-direction velocity (bounce off paddle)."""
        if self.mode == "CLASSIC" or paddle is None:
            self.x_move *= -1
            return

        # ----- MODERN PHYSICS -----

        # Hit position relative to paddle center (-1 to 1)
        offset = (self.ycor() - paddle.ycor()) / 50
        offset = max(-1, min(1, offset))

        # Max bounce angle
        angle = offset * 60
        rad = math.radians(angle)

        # Preserve total speed (important fix)
        current_speed = math.sqrt(self.x_move ** 2 + self.y_move ** 2)
        speed = min(self.max_speed, current_speed + 0.5)

        # Determine horizontal direction
        direction = -1 if self.x_move > 0 else 1

        # Recalculate velocity components
        self.x_move = speed * math.cos(rad) * direction
        self.y_move = speed * math.sin(rad)

        # Very small randomness to avoid patterns (safe)
        self.y_move += random.uniform(-0.3, 0.3)

        # ✅ IMPORTANT: push ball outside paddle to prevent re-collision
        buffer = 15
        if direction == -1:  # Hit right paddle
            self.setx(paddle.xcor() - buffer)
        else:  # Hit left paddle
            self.setx(paddle.xcor() + buffer)

    def reset_position(self):
        """Reset ball to center and reset speed."""
        self.home()
        self.ball_speed = 0.1
        self.bounce_x()

    def increase_speed(self):
        """Increase ball speed slightly after each paddle hit."""
        self.ball_speed *= 0.9
