from turtle import Turtle

class Scoreboard(Turtle):
    """Represents the score display for the Pong game."""

    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.l_score = 0
        self.r_score = 0
        self.update_score()

    def update_score(self):
        """Clear and redraw the scores on the screen."""
        self.clear()
        self.goto(-100, 200)
        self.write(self.l_score, align="center", font=("Courier", 70, "bold"))
        self.goto(100, 200)
        self.write(self.r_score, align="center", font=("Courier", 70, "bold"))

    def l_point(self):
        """Increment left player score and update display."""
        self.l_score += 1
        self.update_score()

    def r_point(self):
        """Increment right player score and update display."""
        self.r_score += 1
        self.update_score()
