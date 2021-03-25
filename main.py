import tkinter as tk
import random

from gamelib import Sprite, GameApp, Text

from dir_consts import *
from maze import Maze


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600

UPDATE_DELAY = 33

PACMAN_SPEED = 5

class Pacman(Sprite):
    def __init__(self, app, maze, r, c):
        self.r = r
        self.c = c
        self.maze = maze

        self.dot_eaten_observer = []

        self.direction = DIR_STILL
        self.next_direction = DIR_STILL

        self.state = NormalPacmanState(self)

        x, y = maze.piece_center(r,c)
        super().__init__(app, 'images/pacman.png', x, y)

    # def update(self):
    #     if self.maze.is_at_center(self.x, self.y):
    #         r, c = self.maze.xy_to_rc(self.x, self.y)

    #         if self.maze.has_dot_at(r, c):
    #             self.maze.eat_dot_at(r, c)
    #             if random.random() < 0.1:
    #                 if not self.is_super_speed:
    #                     self.is_super_speed = True
    #                     self.super_speed_counter = 0
            
    #         if self.maze.is_movable_direction(r, c, self.next_direction):
    #             self.direction = self.next_direction
    #         else:
    #             self.direction = DIR_STILL

    def update(self):
        if self.maze.is_at_center(self.x, self.y):
            r, c = self.maze.xy_to_rc(self.x, self.y)

            if self.maze.has_dot_at(r, c):
                self.maze.eat_dot_at(r, c)

                ## Notes: 1st operation
                ## 
                self.state.random_upgrade()

                for i in self.dot_eaten_observer:
                    i()
            if self.maze.is_movable_direction(r, c, self.next_direction):
                self.direction = self.next_direction
            else:
                self.direction = DIR_STILL          

        ## Notes: 2nd operation
        ## 
        self.state.move_pacman()

    def set_next_direction(self, direction):
        self.next_direction = direction


class PacmanGame(GameApp):
    def init_game(self):
        self.maze = Maze(self, CANVAS_WIDTH, CANVAS_HEIGHT)
        self.pacman1_score = 0
        self.pacman2_score = 0
        self.pacman1_score_text = Text(self, 'P1: 0', 100, 20)
        self.pacman2_score_text = Text(self, 'P2: 0', 600, 20)
        self.pacman1 = Pacman(self, self.maze, 1, 1)
        self.pacman2 = Pacman(self, self.maze, self.maze.get_height() - 2, self.maze.get_width() - 2)
        
        self.pacman1.dot_eaten_observer.append(self.dot_eaten_by_pacman1)
        self.pacman2.dot_eaten_observer.append(self.dot_eaten_by_pacman2)

        self.elements.append(self.pacman1)
        self.elements.append(self.pacman2)


    def pre_update(self):
        pass

    def post_update(self):
        pass

    def on_key_pressed(self, event):
        if event.char.upper() == 'A':
            self.pacman1.set_next_direction(DIR_LEFT)
        elif event.char.upper() == 'W':
            self.pacman1.set_next_direction(DIR_UP)
        elif event.char.upper() == 'S':
            self.pacman1.set_next_direction(DIR_DOWN)
        elif event.char.upper() == 'D':
            self.pacman1.set_next_direction(DIR_RIGHT)

        if event.char.upper() == 'J':
            self.pacman2.set_next_direction(DIR_LEFT)
        elif event.char.upper() == 'I':
            self.pacman2.set_next_direction(DIR_UP)
        elif event.char.upper() == 'K':
            self.pacman2.set_next_direction(DIR_DOWN)
        elif event.char.upper() == 'L':
            self.pacman2.set_next_direction(DIR_RIGHT)

    def dot_eaten_by_pacman1(self):
        self.pacman1_score += 1
        self.update_scores()

    def dot_eaten_by_pacman2(self):
        self.pacman2_score += 1
        self.update_scores()

    def update_scores(self):
        self.pacman1_score_text.set_text(f'p1 : {self.pacman1_score}')
        self.pacman2_score_text.set_text(f'p2 : {self.pacman2_score}')

class NormalPacmanState:
    def __init__(self,pacman):
        self.pacman = pacman
        self.speed = PACMAN_SPEED

    def random_upgrade(self):
        if random.random() < 0.1:
            self.pacman.state = SuperPacmanState(self.pacman)
        
    def move_pacman(self):
        self.pacman.x += self.speed * DIR_OFFSET[self.pacman.direction][0]
        self.pacman.y += self.speed * DIR_OFFSET[self.pacman.direction][1]

class SuperPacmanState:
    def __init__(self,pacman):
        self.pacman = pacman
        self.counter = 0
        self.speed = PACMAN_SPEED*2

    def random_upgrade(self):
        pass

    def move_pacman(self):
        # TODO:
        #   - update the pacman's location with super speed
        #   - update the counter, if the counter >= 50, set state back to NormalPacmanState
        if self.counter > 50:
            self.pacman.state = NormalPacmanState(self.pacman)
        else:
            self.pacman.x += self.speed * DIR_OFFSET[self.pacman.direction][0]
            self.pacman.y += self.speed * DIR_OFFSET[self.pacman.direction][1]
            self.counter += 1


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Monkey Banana Game")

    # do not allow window resizing
    root.resizable(False, False)
    app = PacmanGame(root, CANVAS_WIDTH, CANVAS_HEIGHT, UPDATE_DELAY)
    app.start()
    root.mainloop()
