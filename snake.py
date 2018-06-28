import tkinter as tk
import random
import time

scr_size_x = 2
scr_size_y = 2
speed = 500  # how often snake moves in ms


class Snake:
    head_x = int(scr_size_x / 2)
    head_y = int(scr_size_y / 2)
    direction = "up"
    end_direction = "down"
    tail = [[head_x, head_y], [head_x, head_y - 1]]

    time_started = time.time()

    food_x = 0
    food_y = 0

    def go(self):
        if self.direction == "up":
            self.head_y += 1
        if self.direction == "down":
            self.head_y -= 1
        if self.direction == "right":
            self.head_x += 1
        if self.direction == "left":
            self.head_x -= 1

        if self.head_x > scr_size_x - 1:
            self.head_x = 0
        if self.head_x < 0:
            self.head_x = scr_size_x
        if self.head_y > scr_size_y - 1:
            self.head_y = 0
        if self.head_y < 0:
            self.head_y = scr_size_y

        if self.head_is_on(self.food_x, self.food_y):
            self.grow()
            self.food_x = random.randint(0, scr_size_x - 1)
            self.food_y = random.randint(0, scr_size_y - 1)
            while self.body_is_on(self.food_x, self.food_y):  # food will never generate on snake
                self.food_x = random.randint(0, scr_size_x - 1)
                self.food_y = random.randint(0, scr_size_y - 1)

        del self.tail[-1]
        self.collision_handle(1)  # this MUST be done AFTER head and back of tail was updated
        # but BEFORE new position of head was added to tail
        self.tail.insert(0, [self.head_x, self.head_y])
        self.end_direction = self.get_end_direction()

    def turn_right(self):
        if self.direction == "up":
            self.direction = "right"

        elif self.direction == "down":
            self.direction = "left"

        elif self.direction == "right":
            self.direction = "down"

        elif self.direction == "left":
            self.direction = "up"

    def turn_left(self):
        if self.direction == "up":
            self.direction = "left"

        elif self.direction == "down":
            self.direction = "right"

        elif self.direction == "right":
            self.direction = "up"

        elif self.direction == "left":
            self.direction = "down"

    def get_end_direction(self):  # if whole snake is up, end is down etc
        if len(self.tail) > 1:
            x_difference = self.tail[-1][0] - self.tail[-2][0]
            y_difference = self.tail[-1][1] - self.tail[-2][1]
            if x_difference > 0:
                return "right"
            if x_difference < 0:
                return "left"
            if y_difference > 0:
                return "up"
            if y_difference < 0:
                return "down"
        else:
            if self.direction == "up":
                return "down"
            if self.direction == "down":
                return "up"
            if self.direction == "left":
                return "right"
            if self.direction == "right":
                return "left"

    def grow(self, how_much=1):
        for x in range(how_much):
            to_append = self.tail[-1]
            if self.end_direction == "up":
                to_append = [to_append[0], to_append[1] + 1]
            if self.end_direction == "down":
                to_append = [to_append[0], to_append[1] - 1]
            if self.end_direction == "right":
                to_append = [to_append[0] - 1, to_append[1]]
            if self.end_direction == "left":
                to_append = [to_append[0] + 1, to_append[1]]

            self.tail.append(to_append)
            if len(self.tail) >= scr_size_x * scr_size_y:
                print("You won! Time:")
                print(time.time() - self.time_started)
                raise SystemExit

    def cut_tail_in_index(self, index: int = 1):
        if len(self.tail) > index:
            del self.tail[index:]
            self.end_direction = self.get_end_direction()
            return True
        else:
            return False

    def cut_tail_in_coords(self, coords: list):
        for tail_fragment, check_cords in enumerate(self.tail):
            if check_cords == coords:
                return self.cut_tail_in_index(tail_fragment)
        return False

    def collision_handle(self, case=1):
        if self.body_is_on(self.head_x, self.head_y, 1):
            print("You've eaten yourself!!!")
            if case == 0:  # do nothing about it
                self
            if case == 1:  # eat yourself
                print(self.cut_tail_in_coords([self.head_x, self.head_y]))
            if case == 2:  # stop whole game
                while True:
                    self

    def body_is_on(self, x, y, body_begin=0):
        for fragment in self.tail[body_begin:]:
            if fragment[0] == x and fragment[1] == y:
                return True
        return False

    def head_is_on(self, x, y):
        if self.head_x == x and self.head_y == y:
            return True
        else:
            return False

    def food_is_on(self, x, y):
        if self.food_x == x and self.food_y == y:
            return True
        else:
            return False


snake = Snake()


def on_key_press(event):
    key = event.char.lower()
    if key == "\x1b":
        print("ESC")
        raise SystemExit
    if key == "a":
        snake.turn_left()
    if key == "d":
        snake.turn_right()
    if key == "w":
        go(False)

    global speed  # speed controll
    if key == "1":
        speed = 100
    if key == "2":
        speed = 200
    if key == "3":
        speed = 300
    if key == "4":
        speed = 400
    if key == "5":
        speed = 500
    if key == "6":
        speed = 600
    if key == "7":
        speed = 700
    if key == "8":
        speed = 800
    if key == "9":
        speed = 900
    if key == "0":
        speed = 1000


def go(cycle=True):
    snake.go()
    print(get_map("+ ", "* ", "$ ", "0 "))
    if cycle:
        root.after(speed, go)


def get_map(head: str, body: str, food: str, empty: str):
    all_pixels = ""
    for y in reversed(range(scr_size_y)):
        for x in range(scr_size_x):
            if snake.head_is_on(x, y):
                all_pixels += head
            elif snake.body_is_on(x, y):
                all_pixels += body
            elif snake.food_is_on(x, y):
                all_pixels += food
            else:
                all_pixels += empty
        all_pixels += "\n"

    return all_pixels


root = tk.Tk()
root.after(speed, go)
root.bind('<KeyPress>', on_key_press)
root.mainloop()
