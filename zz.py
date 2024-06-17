import pygame
import random

# 初始化 Pygame
pygame.init()

# 设置屏幕尺寸和颜色
WIDTH, HEIGHT = 300, 350
GRID_SIZE = 10
BOMB_COUNT = 15
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 创建屏幕
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("扫雷游戏")

# 创建地雷图和显示图
bomb_grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
display_grid = [[" " for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
revealed_grid = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# 初始化地雷位置
bomb_positions = random.sample([(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE)], BOMB_COUNT)
for pos in bomb_positions:
    bomb_grid[pos[0]][pos[1]] = 1

# 计算周围地雷数量
def count_neighbor_bombs(row, col):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if 0 <= row + i < GRID_SIZE and 0 <= col + j < GRID_SIZE and bomb_grid[row + i][col + j] == 1:
                count += 1
    return count

for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        if bomb_grid[i][j] == 0:
            display_grid[i][j] = str(count_neighbor_bombs(i, j))

# 渲染格子
def draw_grid():
    block_size = WIDTH // GRID_SIZE
    for i in range(GRID_SIZE+1):
        pygame.draw.line(screen, BLACK, (0, i * block_size), (WIDTH, i * block_size))
        pygame.draw.line(screen, BLACK, (i * block_size, 0), (i * block_size, HEIGHT - 50))

# 渲染文本
def draw_text():
    block_size = WIDTH // GRID_SIZE
    font = pygame.font.Font(None, 36)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if revealed_grid[i][j]:
                text = font.render(display_grid[i][j], True, BLACK)
                screen.blit(text, (j * block_size + 10, i * block_size + 10))

# 扫雷逻辑
def reveal_cell(row, col):
    if revealed_grid[row][col]:
        return
    revealed_grid[row][col] = True
    if bomb_grid[row][col] == 1:
        print("you lose")
        game_over()
    elif display_grid[row][col] == "0":
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= row + i < GRID_SIZE and 0 <= col + j < GRID_SIZE:
                    reveal_cell(row + i, col + j)
def check_win():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if bomb_grid[i][j] == 0 and not revealed_grid[i][j]:
                return False
    return True
def game_over():
    pygame.quit()
    sys.exit()
# 主游戏循环
run = True
while run:
    screen.fill(WHITE)
    draw_grid()
    draw_text()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            row, col = y // (WIDTH // GRID_SIZE), x // (WIDTH // GRID_SIZE)
            if event.button == 1:  # 左键点击
                reveal_cell(row, col)
                if check_win():
                    print("You win!")

    pygame.display.flip()

pygame.quit()
