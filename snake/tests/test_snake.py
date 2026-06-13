# tests/test_snake.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from snake.snake import Snake, Food

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