# Pong Game in Python

![Pong Game Demo](pong_demo.gif)

A classic **Pong game** built in Python using the `turtle` module, featuring **OOP structure**, **smooth two-player controls**, and **sound effects** with `pygame`.

This version includes improvements for a better gameplay experience:
- Smooth, continuous paddle movement for two players
- Paddles cannot move off-screen
- Ball no longer sticks to paddles
- Sound effects for bouncing and scoring
- Live score tracking
- Menu system for selecting game mode and CPU difficulty

---

## Features

- **Single-player vs CPU** with three difficulty levels: Easy, Medium, Hard
- **Two-player mode**
- **Customizable match length**: first to 3, 5, 7, or 10 points
- **Pause and restart** functionality
- **Context-aware menu navigation** (Main Menu → Match Length → CPU Difficulty)
- **Sound effects** for ball bounce and scoring
- **Smooth paddle movement** with continuous key press support

## Controls

**Player 1 / CPU (left paddle):**  
- Up: `W`  
- Down: `S`  

**Player 1 / Player 2 (right paddle):**  
- Up: `Up Arrow`  
- Down: `Down Arrow`  

**Global / Context Keys:**  
- `Escape` → Pause / Resume  
- `B` → Back (in menu or pause screen)  
- `R` → Resume from pause  
- `T` → Restart match from pause  
- `N` → Restart match after game over  
- `M` → Medium CPU difficulty / go to main menu  

**Menu Keys:**  
- `1` → Player vs CPU  
- `2` → Player vs Player  
- `E` → Easy CPU  
- `M` → Medium CPU  
- `H` → Hard CPU  
- `3, 5, 7, 0` → Match length (First to 3, 5, 7, or 10)

---

## How to Run
1. Clone the repository:

```bash
git clone https://github.com/legophil101/Pong-Game.git
```
2. Navigate to the project folder:
```bash
cd pong_game
```
3. Install dependencies:
```bash
pip install pygame
```
4. Run the game:
```bash
python main.py
```