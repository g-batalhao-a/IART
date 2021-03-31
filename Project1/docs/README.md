# Ball Sort Puzzle

## Requirements

- [Python 3.9](https://www.python.org/downloads/)
- [pygame](https://www.pygame.org/wiki/GettingStarted#Pygame%20Installation)
- [xlwt](https://pypi.org/project/xlwt/)

## Building and Running

Run `python ui.py`

When the program starts, the user will be presented with the following screen:

![Main Screen](https://i.imgur.com/XJIhxok.png)

- Play - The user has at his disposal 30 levels to play
- Watch - The user can see the solution of a level, using an algorithm of his choosing
- Settings - Disable Music and SFX; Choose an algorithm

When playing, the user clicks a tube to remove a ball and clicks on another tube to move to that tube.
If the user is stuck, he can click on the Hint button to get a suggested move, by the algorithm he has chosen.
This button becomes disabled if the user has made a move that doesn't lead to a solution.