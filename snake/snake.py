# snake.py
import curses
import random


class Snake:
    def __init__(self, start: tuple[int, int], length: int = 3):
        row, col = start
        # body[0] 是蛇头，初始向右，身体向左延伸
        self.body: list[tuple[int, int]] = [(row, col - i) for i in range(length)]

    def move(self, direction: tuple[int, int]):
        dr, dc = direction
        new_head = (self.body[0][0] + dr, self.body[0][1] + dc)
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self, direction: tuple[int, int]):
        dr, dc = direction
        new_head = (self.body[0][0] + dr, self.body[0][1] + dc)
        self.body.insert(0, new_head)

    def check_self_collision(self) -> bool:
        return self.body[0] in self.body[1:]


class Food:
    def __init__(self):
        self.pos: tuple[int, int] = (1, 1)

    def respawn(self, snake_body: list[tuple[int, int]], bounds: tuple[int, int]):
        height, width = bounds
        max_attempts = (height - 2) * (width - 2) * 10
        for _ in range(max_attempts):
            row = random.randint(1, height - 2)
            col = random.randint(1, width - 2)
            if (row, col) not in snake_body:
                self.pos = (row, col)
                return
        # 无空位可放，兜底扫描找空位
        for row in range(1, height - 1):
            for col in range(1, width - 1):
                if (row, col) not in snake_body:
                    self.pos = (row, col)
                    return


# 方向常量：(row_delta, col_delta)
UP    = (-1, 0)
DOWN  = (1, 0)
LEFT  = (0, -1)
RIGHT = (0, 1)

OPPOSITE = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}


class Game:
    def __init__(self, window):
        self.window = window
        self.height, self.width = window.getmaxyx()
        start_row = self.height // 2
        start_col = self.width // 2
        self.snake = Snake(start=(start_row, start_col), length=3)
        self.food = Food()
        self.food.respawn(self.snake.body, (self.height, self.width))
        self.score = 0
        self.direction = RIGHT

    def run(self):
        self.window.timeout(150)
        curses.curs_set(0)
        while True:
            key = self.window.getch()
            if not self.handle_input(key):
                return
            if not self.update():
                self.game_over()
                return
            self.draw()

    def handle_input(self, key: int):
        if key in (ord('q'), ord('Q')):
            self.game_over()
            return False
        key_map = {
            curses.KEY_UP: UP,
            curses.KEY_DOWN: DOWN,
            curses.KEY_LEFT: LEFT,
            curses.KEY_RIGHT: RIGHT,
        }
        new_dir = key_map.get(key)
        if new_dir and new_dir != OPPOSITE[self.direction]:
            self.direction = new_dir
        return True

    def update(self) -> bool:
        """返回 False 表示游戏结束。"""
        dr, dc = self.direction
        head_row, head_col = self.snake.body[0]
        new_head = (head_row + dr, head_col + dc)

        # 撞墙检测
        r, c = new_head
        if r <= 0 or r >= self.height - 1 or c <= 0 or c >= self.width - 1:
            return False

        # 吃到食物？
        if new_head == self.food.pos:
            self.snake.grow(self.direction)
            self.score += 1
            self.food.respawn(self.snake.body, (self.height, self.width))
        else:
            self.snake.move(self.direction)

        # 撞自身检测（move/grow 之后）
        if self.snake.check_self_collision():
            return False

        return True

    def draw(self):
        self.window.clear()

        # 绘制边界
        for col in range(self.width):
            self.window.addch(0, col, '#')
        for col in range(self.width - 1):
            self.window.addch(self.height - 1, col, '#')
        for row in range(1, self.height - 1):
            self.window.addch(row, 0, '#')
            self.window.addch(row, self.width - 1, '#')

        # 绘制蛇
        for i, (row, col) in enumerate(self.snake.body):
            ch = 'O' if i == 0 else 'o'
            self.window.addch(row, col, ch)

        # 绘制食物
        self.window.addch(self.food.pos[0], self.food.pos[1], '*')

        # 绘制分数
        self.window.addstr(self.height - 1, 2, f' Score: {self.score} ')

        self.window.refresh()

    def game_over(self):
        self.window.clear()
        msg = f'GAME OVER  Score: {self.score}  Press Q to quit'
        row = self.height // 2
        col = max(0, (self.width - len(msg)) // 2)
        self.window.addstr(row, col, msg)
        self.window.refresh()
        while True:
            key = self.window.getch()
            if key in (ord('q'), ord('Q')):
                return


def main(stdscr):
    curses.start_color()
    game = Game(stdscr)
    game.run()


if __name__ == '__main__':
    curses.wrapper(main)