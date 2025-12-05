from turtle import Turtle

class Ball(Turtle):
    """Represents the ball in the Pong game with movement, collisions, and speed control."""

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.x_move = 10
        self.y_move = 10
        self.ball_speed = 0.1

    def move(self):
        """Move the ball according to its x and y velocities."""
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_y(self):
        """Invert the y-direction velocity (bounce off top/bottom wall)."""
        self.y_move *= -1

    def bounce_x(self):
        """Invert the x-direction velocity (bounce off paddle)."""
        self.x_move *= -1

    def reset_position(self):
        """Reset ball to center and reset speed."""
        self.home()
        self.ball_speed = 0.1
        self.bounce_x()

    def increase_speed(self):
        """Increase ball speed slightly after each paddle hit."""
        self.ball_speed *= 0.9
