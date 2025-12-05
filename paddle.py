from turtle import Turtle

# Constants for movement and screen boundaries
MOVE_DISTANCE = 20
UPPER_LIMIT = 250
LOWER_LIMIT = -250

class Paddle(Turtle):
    """Represents a paddle in the Pong game."""

    def __init__(self, position):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.setheading(90)
        self.turtlesize(stretch_len=5)
        self.penup()
        self.goto(position)

    def up(self):
        """Move the paddle up, respecting the upper screen limit."""
        new_y = self.ycor() + MOVE_DISTANCE
        if new_y > UPPER_LIMIT:
            new_y = UPPER_LIMIT
        self.goto(self.xcor(), new_y)

    def down(self):
        """Move the paddle down, respecting the lower screen limit."""
        new_y = self.ycor() - MOVE_DISTANCE
        if new_y < LOWER_LIMIT:
            new_y = LOWER_LIMIT
        self.goto(self.xcor(), new_y)
