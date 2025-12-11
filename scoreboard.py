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
        self.paused = False
        self.update_score()

    def update_score(self):
        """Clear and redraw the scores on the screen."""
        self.clear()
        self.goto(-100, 200)
        self.write(self.l_score, align="center", font=("Courier", 70, "bold"))
        self.goto(100, 200)
        self.write(self.r_score, align="center", font=("Courier", 70, "bold"))

        # If game is paused, redraw the pause text
        if self.paused:
            self.show_pause()

    def l_point(self):
        """Increment left player score and update display."""
        self.l_score += 1
        self.update_score()

    def r_point(self):
        """Increment right player score and update display."""
        self.r_score += 1
        self.update_score()

    def show_pause(self):
        """Display PAUSED at the center of the screen."""
        self.paused = True
        self.goto(0, 0)
        self.write("PAUSED", align="center", font=("Courier", 40, "bold"))

    def hide_pause(self):
        """Remove the PAUSED text and redraw the scores."""
        self.paused = False
        self.update_score()
