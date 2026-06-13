# Snake Game Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 用 Python `curses` 标准库实现一个基础版终端贪吃蛇游戏，单文件零依赖。

**Architecture:** 三个类 `Snake`、`Food`、`Game` 各自职责清晰，`main()` 负责初始化 curses 并启动游戏，主循环在 `Game.run()` 中驱动。

**Tech Stack:** Python 3.x 标准库（`curses`、`random`），`pytest` 用于单元测试。

---

## 文件结构

| 文件 | 职责 |
|------|------|
| `snake.py` | 游戏全部逻辑（`Snake`、`Food`、`Game`、`main`） |
| `tests/test_snake.py` | `Snake` 和 `Food` 的单元测试（不依赖 curses） |

---

### Task 1: Snake 类 — 移动与碰撞

**Files:**
- Create: `snake.py`
- Create: `tests/test_snake.py`

- [ ] **Step 1: 创建测试文件，写 Snake 移动的失败测试**

```python
# tests/test_snake.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from snake import Snake

def test_snake_initial_state():
    snake = Snake(start=(10, 20), length=3)
    assert len(snake.body) == 3
    assert snake.body[0] == (10, 20)
    # 初始向右，身体向左延伸
    assert snake.body[1] == (10, 19)
    assert snake.body[2] == (10, 18)

def test_snake_move_right():
    snake = Snake(start=(10, 20), length=3)
    snake.move((0, 1))  # direction: (row_delta, col_delta)
    assert snake.body[0] == (10, 21)
    assert len(snake.body) == 3  # 长度不变

def test_snake_move_down():
    snake = Snake(start=(10, 20), length=3)
    snake.move((1, 0))
    assert snake.body[0] == (11, 20)
    assert len(snake.body) == 3

def test_snake_grow():
    snake = Snake(start=(10, 20), length=3)
    snake.grow((0, 1))
    assert snake.body[0] == (10, 21)
    assert len(snake.body) == 4  # 长度增加

def test_snake_no_self_collision_initially():
    snake = Snake(start=(10, 20), length=3)
    assert snake.check_self_collision() == False

def test_snake_self_collision():
    snake = Snake(start=(10, 20), length=3)
    # 手动造成碰撞：将蛇头位置复制到身体中
    snake.body.insert(0, snake.body[1])
    assert snake.check_self_collision() == True
```

- [ ] **Step 2: 运行测试，确认失败**

```bash
pytest tests/test_snake.py -v
```

预期输出：`ERROR` 或 `ImportError: cannot import name 'Snake'`

- [ ] **Step 3: 创建 `snake.py`，实现 `Snake` 类**

```python
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
```

- [ ] **Step 4: 运行测试，确认通过**

```bash
pytest tests/test_snake.py -v
```

预期输出：6 个测试全部 PASS

- [ ] **Step 5: 提交**

```bash
git add snake.py tests/test_snake.py
git commit -m "feat: add Snake class with move, grow, collision detection"
```

---

### Task 2: Food 类 — 随机生成食物

**Files:**
- Modify: `snake.py`
- Modify: `tests/test_snake.py`

- [ ] **Step 1: 追加 Food 的失败测试**

在 `tests/test_snake.py` 末尾追加：

```python
from snake import Food

def test_food_initial_position():
    food = Food()
    food.respawn(snake_body=[(10, 20), (10, 19), (10, 18)], bounds=(24, 80))
    row, col = food.pos
    # 食物在边界内（边界行/列本身是墙，食物不能在墙上）
    assert 1 <= row <= 22
    assert 1 <= col <= 78

def test_food_not_on_snake():
    food = Food()
    snake_body = [(r, c) for r in range(1, 23) for c in range(1, 79)]  # 填满内部
    snake_body = snake_body[:100]  # 取前 100 格
    food.respawn(snake_body=snake_body, bounds=(24, 80))
    assert food.pos not in snake_body

def test_food_respawn_avoids_snake():
    food = Food()
    food.respawn(snake_body=[], bounds=(24, 80))
    first_pos = food.pos
    # respawn 后位置随机，多次调用应能得到不同位置（概率极高）
    positions = set()
    for _ in range(20):
        food.respawn(snake_body=[], bounds=(24, 80))
        positions.add(food.pos)
    assert len(positions) > 1
```

- [ ] **Step 2: 运行测试，确认失败**

```bash
pytest tests/test_snake.py::test_food_initial_position -v
```

预期输出：`ImportError: cannot import name 'Food'`

- [ ] **Step 3: 在 `snake.py` 中追加 `Food` 类**

在 `Snake` 类定义之后追加：

```python
class Food:
    def __init__(self):
        self.pos: tuple[int, int] = (1, 1)

    def respawn(self, snake_body: list[tuple[int, int]], bounds: tuple[int, int]):
        height, width = bounds
        while True:
            row = random.randint(1, height - 2)
            col = random.randint(1, width - 2)
            if (row, col) not in snake_body:
                self.pos = (row, col)
                return
```

- [ ] **Step 4: 运行测试，确认通过**

```bash
pytest tests/test_snake.py -v
```

预期输出：全部 PASS（包含 Task 1 的 6 个 + 本 Task 的 3 个，共 9 个）

- [ ] **Step 5: 提交**

```bash
git add snake.py tests/test_snake.py
git commit -m "feat: add Food class with respawn logic"
```

---

### Task 3: Game 类 — 初始化与绘制

**Files:**
- Modify: `snake.py`（追加 `Game` 类骨架和 `main()`）

注意：`Game` 类依赖 curses 窗口，不写单元测试，用手动运行验证。

- [ ] **Step 1: 在 `snake.py` 末尾追加 `Game` 类和 `main()`**

在 `Food` 类之后追加：

```python
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
            self.handle_input(key)
            if not self.update():
                self.game_over()
                return
            self.draw()

    def handle_input(self, key: int):
        key_map = {
            curses.KEY_UP: UP,
            curses.KEY_DOWN: DOWN,
            curses.KEY_LEFT: LEFT,
            curses.KEY_RIGHT: RIGHT,
        }
        new_dir = key_map.get(key)
        if new_dir and new_dir != OPPOSITE[self.direction]:
            self.direction = new_dir

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
            self.window.addch(self.height - 1, col, '#')
        for row in range(self.height):
            self.window.addch(row, 0, '#')
            try:
                self.window.addch(row, self.width - 1, '#')
            except curses.error:
                pass  # 右下角写入时 curses 会抛异常，忽略即可

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
```

- [ ] **Step 2: 确认已有单元测试仍然通过**

```bash
pytest tests/test_snake.py -v
```

预期输出：9 个测试全部 PASS

- [ ] **Step 3: 手动运行游戏，验证画面正常**

```bash
python snake.py
```

验证清单：
- 边界 `#` 正确绘制
- 蛇头显示 `O`，蛇身显示 `o`
- 食物显示 `*`
- 分数显示在底部
- 方向键可以控制蛇移动
- 撞墙后显示 GAME OVER 界面
- 按 Q 正常退出

- [ ] **Step 4: 提交**

```bash
git add snake.py
git commit -m "feat: add Game class with main loop, drawing, input handling, game over"
```

---

### Task 4: 集成验证与最终提交

**Files:**
- No new files

- [ ] **Step 1: 运行全部测试**

```bash
pytest tests/ -v
```

预期输出：9 个测试全部 PASS

- [ ] **Step 2: 完整游戏流程验证**

```bash
python snake.py
```

验证清单：
- 蛇初始长度为 3，向右移动
- 吃到 `*` 后蛇身变长，分数 +1
- 撞墙 → GAME OVER
- 撞自身 → GAME OVER
- GAME OVER 界面显示正确分数
- 按 Q 退出后终端恢复正常（无残留字符）

- [ ] **Step 3: 最终提交**

```bash
git add .
git commit -m "feat: complete snake game implementation"
```
