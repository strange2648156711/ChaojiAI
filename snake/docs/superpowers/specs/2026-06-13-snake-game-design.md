# 贪吃蛇游戏设计文档

## 概述

用 Python `curses` 标准库实现一个基础版终端贪吃蛇游戏。单文件，零外部依赖，运行于 Linux/Mac 终端。

## 功能范围

- 蛇在边界内移动（上下左右方向键控制）
- 吃到食物后蛇身增长，分数 +1
- 撞墙或撞自身触发 Game Over
- 实时显示当前分数
- Game Over 后显示最终分数，按 Q 退出

## 界面布局

```
┌─────────────────────────────┐
│         curses 窗口          │
│  ┌───────────────────────┐  │
│  │  # # # # # # # # # #  │  │
│  │  #                 #  │  │
│  │  #   ●●●●○         #  │  │
│  │  #         *       #  │  │
│  │  #                 #  │  │
│  │  # # # # # # # # # #  │  │
│  └───────────────────────┘  │
│  Score: 3                   │
└─────────────────────────────┘

● = 蛇身  ○ = 蛇头  * = 食物  # = 边界
```

## 组件设计

### `Snake` 类

- 数据：`body: list[tuple[int,int]]`，`body[0]` 为蛇头
- 方法：
  - `move(direction)` — 在头部插入新坐标，删除尾部（不吃食物时）
  - `grow()` — 在头部插入新坐标，保留尾部
  - `check_self_collision() -> bool` — 蛇头是否在蛇身其余部分中
- 初始状态：蛇头在屏幕中央，长度为 3，方向向右

### `Food` 类

- 数据：`pos: tuple[int,int]`
- 方法：
  - `respawn(snake_body, bounds)` — 随机选取不在蛇身上且在边界内的坐标

### `Game` 类

- 数据：`window`、`snake: Snake`、`food: Food`、`score: int`、`direction`
- 方法：
  - `run()` — 主循环
  - `handle_input(key)` — 更新方向（禁止反向掉头）
  - `update()` — 移动蛇、检测碰撞、处理吃食物
  - `draw()` — 重绘边界、蛇、食物、分数
  - `game_over()` — 显示结束界面，等待 Q 退出

### `main()`

- 初始化 curses（隐藏光标、非阻塞输入、颜色对）
- 包裹 `curses.wrapper(main)` 确保异常时终端状态恢复

## 数据流

```
键盘输入 → handle_input() 更新方向
         → update() 移动蛇头
              ├── 撞墙或撞自身 → game_over()
              └── 否 → 吃到食物？
                            ├── 是 → grow()，food.respawn()，score+1
                            └── 否 → move()
         → draw() 重绘屏幕
         → window.timeout(150) 等待下一帧
```

## 帧率与输入

- `window.timeout(150)` — 每帧 150ms（约 6.7 FPS）
- `window.getch()` 返回 `ERR` 时保持当前方向继续移动

## 碰撞检测

- **撞墙**：蛇头 `row <= 0 or row >= height-1 or col <= 0 or col >= width-1`
- **撞自身**：`snake.body[0] in snake.body[1:]`

## 文件结构

```
snake.py   # 全部逻辑，单文件
```

## 运行方式

```bash
python snake.py
```
