# Tic Tac Toe

This is an implementetion of the classic game 'Tic-Tac-Toe' in Python, where the opponent is the computer and is programmed to decide the next move based on the Minimax Algorithm (with Alfa-Beta Pruning).

## How to Play

When the program is started, the player is given instructions for how to play (how to give the coordinates of the next move etc). Also the player decides the difficulty of the game by setting the searching depth of the Minimax Algorithm (for example with depth=1 the computer does not play very optimally).

## Heuristic Function

As the searching depth of the Minimax Algorithm is given by the player, there must be a heuristic function, that gives a value to a move. The one we use is not other than the number of possible wins that use that specific block:

![Alt text](/heuristic.png?raw=true "Heuristic Function for Tic-Tac-Toe (eg the center has value 4, becuase there are 4 ways to win using the center - 1 horizontal, 1 vertical and 2 diagonal)")
