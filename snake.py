"""
Snake Game, written by Martin Ristovski, August 2020
https://github.com/martinristovski/snake

Use ARROW KEYS to move, SPACE to toggle pause and ESC to exit.
"""

import curses
from curses import KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT
from random import randint

valid_keys = [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, 27]

curses.initscr()
curses.noecho()
curses.curs_set(0)

win = curses.newwin(20,72,0,0)
win.keypad(1)
win.nodelay(1)
win.border(0)

score = 0

key = KEY_RIGHT # initial move
snake = [[10, 13], [10, 12], [10, 11]] # initial snake location
food = [randint(1, 18), randint(1, 70)] # initial food location

win.addch(food[0], food[1], '%') # Draw initial food

while key != 27: # 27 == Esc
    win.border(0)
    win.addstr(0, 2, 'Score : ' + str(score) + ' ')
    win.addstr(0, 42, ' Snake, by Martin Ristovski ')

    win.timeout(150 - (len(snake)//10)%40) # make longer snakes go faster

    prev_key = key
    event = win.getch()
    key = key if event == -1 else event

    if key == ord(' '): # press Space to toggle pause
        key = -1
        while key != ord(' '):
            key = win.getch()
        key = prev_key
        continue

    if key not in valid_keys: # ignore invalid input
        key = prev_key

    snake.insert(
        0,
        [snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1),
         snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)]
    )
    
    # make snake enter from other side if it crosses borders
    if snake[0][0] == 0: snake[0][0] = 18
    if snake[0][0] == 19: snake[0][0] = 1
    if snake[0][1] == 0: snake[0][1] = 70
    if snake[0][1] == 71: snake[0][1] = 1

    # end if snake runs over itself
    if snake[0] in snake[1:]: break

    # extend snake by 1 if it eats the food
    if snake[0] == food:
        food = []
        score += 1

        while food == []:
            food = [randint(1, 18), randint(1, 70)]
            if food in snake: food = []
        
        win.addch(food[0], food[1], '%')
    else:
        last = snake.pop()
        win.addch(last[0], last[1], ' ')
    
    win.addch(snake[0][0], snake[0][1], 'X')

curses.endwin()

print("Your score: " + str(score))