# ChaojiAI

## settings.json

`settings.json` 是一个解放 Claude 所有权限的配置。除了定 SPEC 和 `git push`，其它所有权限它都有，可以几乎全自动地完成任务。

## 贪吃蛇游戏

这是一个终端贪吃蛇游戏，专门为了测试 `settings.json` 的性能而编写。**整个开发过程除了定 SPEC 和 `git push` 外，全部由 Claude 自动完成。**

### 运行方式

在项目根目录下运行：

```bash
python3 snake/snake.py
```

> 游戏需要真实终端环境（支持 curses），请使用系统终端（如 gnome-terminal、konsole、iTerm2 等）运行。项目只使用 Python 标准库，不需要创建 venv 或安装依赖。

### 操作方式

- **方向键** 控制蛇的移动方向
- **Q 键** 随时退出游戏
- 吃到 `*` 食物后蛇身增长，分数 +1
- 撞墙或撞到自身 → Game Over
