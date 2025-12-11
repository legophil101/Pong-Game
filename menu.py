from turtle import Turtle

class Menu(Turtle):
    """A simple menu system for choosing game mode and CPU difficulty."""

    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()

        # Will store the player's chosen game mode:
        # "P1" = Player vs CPU
        # "P2" = Player vs Player
        # Starts as None because user hasn't picked yet.
        self.selected_mode = None

        # Will store difficulty level if P1 mode is chosen.
        # Could be "Easy", "Medium", or "Hard".
        self.cpu_difficulty = None

        # Draw the main menu on initialization.
        self.show_main_menu()

    # ----------------------------------------------------------- #
    # MAIN MENU
    # ----------------------------------------------------------- #
    def show_main_menu(self):
        """Displays title and initial game mode options."""
        self.clear()

        # Title
        self.goto(0, 100)
        self.write("PONG", align="center", font=("Courier", 40, "bold"))

        # Option: Player vs CPU
        self.goto(0, 0)
        self.write("Press 1 for Player vs CPU",
                   align="center", font=("Courier", 20, "normal"))

        # Option: Player vs Player
        self.goto(0, -40)
        self.write("Press 2 for Player vs Player",
                   align="center", font=("Courier", 20, "normal"))

    # These functions DO NOT bind keys.
    # They only set variables.
    # Keybinding happens inside main.py.
    def select_1p(self):
        """Called when player presses '1': choose Player vs CPU mode."""
        self.selected_mode = "P1"

    def select_2p(self):
        """Called when player presses '2': choose Player vs Player mode."""
        self.selected_mode = "P2"

    # ----------------------------------------------------------- #
    # CPU DIFFICULTY MENU
    # ----------------------------------------------------------- #
    def show_cpu_options(self):
        """Displays difficulty menu after selecting Player vs CPU."""
        self.clear()

        self.goto(0, 100)
        self.write("CPU Difficulty",
                   align="center", font=("Courier", 30, "bold"))

        self.goto(0, 0)
        self.write("Press E for Easy",
                   align="center", font=("Courier", 20, "normal"))

        self.goto(0, -40)
        self.write("Press M for Medium",
                   align="center", font=("Courier", 20, "normal"))

        self.goto(0, -80)
        self.write("Press H for Hard",
                   align="center", font=("Courier", 20, "normal"))

    # Again—these functions DO NOT listen for keypress.
    # main.py will call them when keys E/M/H are pressed.
    def set_easy(self):
        """Sets CPU difficulty to Easy."""
        self.cpu_difficulty = "Easy"

    def set_medium(self):
        """Sets CPU difficulty to Medium."""
        self.cpu_difficulty = "Medium"

    def set_hard(self):
        """Sets CPU difficulty to Hard."""
        self.cpu_difficulty = "Hard"

    # ----------------------------------------------------------- #
    # CLEAR MENU
    # ----------------------------------------------------------- #
    def clear_menu(self):
        """Erase all menu text before starting the game."""
        self.clear()
