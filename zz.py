import random
import pygame
import tkinter as tk
from tkinter import Tk, messagebox

# 初始化 Pygame
pygame.init()
# 设置屏幕尺寸和颜色
font = pygame.font.Font(None, 36)
width, height = 300, 350
grid_size = 10
bomb_count = 15
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
block_size = width // grid_size
wol = 0
screen = pygame.display.set_mode((width, height))
img10 = pygame.image.load(r".\images\10.jpg")
img9 = pygame.image.load(r".\images\9.jpg")
img11 = pygame.image.load(r".\images\11.jpg")
img1 = pygame.image.load(r".\images\1.jpg")
img2 = pygame.image.load(r".\images\2.jpg")
img3 = pygame.image.load(r".\images\3.jpg")
img4 = pygame.image.load(r".\images\4.jpg")
img5 = pygame.image.load(r".\images\5.jpg")
img6 = pygame.image.load(r".\images\6.jpg")
img0 = pygame.image.load(r".\images\0.jpg")
img7 = pygame.image.load(r".\images\7.jpg")
img8 = pygame.image.load(r".\images\8.jpg")
r_img11 = pygame.transform.scale(img11, (30, 30))
r_img9 = pygame.transform.scale(img9, (30, 30))
r_img10 = pygame.transform.scale(img10, (30, 30))
r_img1 = pygame.transform.scale(img1, (30, 30))
r_img2 = pygame.transform.scale(img2, (30, 30))
r_img3 = pygame.transform.scale(img3, (30, 30))
r_img4 = pygame.transform.scale(img4, (30, 30))
r_img5 = pygame.transform.scale(img5, (30, 30))
r_img6 = pygame.transform.scale(img6, (30, 30))
r_img0 = pygame.transform.scale(img0, (30, 30))
r_img7 = pygame.transform.scale(img7, (30, 30))
r_img8 = pygame.transform.scale(img8, (30, 30))
pygame.display.set_caption("扫雷游戏")

# 创建地雷图和显示图
bomb_grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
display_grid = [[" " for _ in range(grid_size)] for _ in range(grid_size)]
revealed_grid = [[False for _ in range(grid_size)] for _ in range(grid_size)]
flag_grid = [[False for _ in range(grid_size)] for _ in range(grid_size)]

# 初始化地雷位置
bomb_positions = random.sample([(i, j) for i in range(grid_size) for j in range(grid_size)], bomb_count)
for pos in bomb_positions:
    bomb_grid[pos[0]][pos[1]] = 1


# 计算周围地雷数量
def count_neighbor_bombs(row, col):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if 0 <= row + i < grid_size and 0 <= col + j < grid_size and bomb_grid[row + i][col + j] == 1:
                count += 1
    return count


for i in range(grid_size):
    for j in range(grid_size):
        if bomb_grid[i][j] == 0:
            display_grid[i][j] = str(count_neighbor_bombs(i, j))
            # screen.blit(eval("r_img{}".format(count_neighbor_bombs(i, j))), (j * block_size, i * block_size))


# 渲染格子
def draw_grid():
    # for i in range(GRID_SIZE+1):
    #     pygame.draw.line(screen, BLACK, (0, i * block_size), (WIDTH, i * block_size))
    #     pygame.draw.line(screen, BLACK, (i * block_size, 0), (i * block_size, HEIGHT - 50))
    #
    for i in range(grid_size):
        for j in range(grid_size):
            screen.blit(r_img10, (j * block_size, i * block_size))


# 渲染图片
def draw_text():
    for i in range(grid_size):
        for j in range(grid_size):
            if revealed_grid[i][j] and display_grid[i][j] != " ":
                screen.blit(eval("r_img{}".format(display_grid[i][j])), (j * block_size, i * block_size))
            elif revealed_grid[i][j] and display_grid[i][j] == " ":
                game_over()
            elif flag_grid[i][j]:
                screen.blit(r_img11, (j * block_size, i * block_size))


class Button:
    def __init__(self, text, pos, size, color, hover_color):
        self.text = text
        self.pos = pos
        self.size = size
        self.color = color
        self.hover_color = hover_color
        self.rect = pygame.Rect(pos, size)
        self.font = pygame.font.Font(None, 36)
        self.text_surf = self.font.render(self.text, True, BLACK)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surf, self.text_rect)

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]


# 创建按钮实例
start_button = Button('START', (100, 100), (100, 50), BLUE, (0, 100, 255))
quit_button = Button('QUIT', (100, 200), (100, 50), BLUE, (0, 100, 255))
level_button = Button('LEVEL', (100, 150), (100, 50), BLUE, (0, 100, 255))
# 计数器
count = bomb_count
# 计时器
start_time = pygame.time.get_ticks()  # 用于控制游戏循环速度的时钟对象


# 扫雷逻辑
def reveal_cell(row, col):
    if revealed_grid[row][col] or flag_grid[row][col]:
        return
    revealed_grid[row][col] = True
    if bomb_grid[row][col] == 1:
        game_over()
    elif display_grid[row][col] == "0":
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= row + i < grid_size and 0 <= col + j < grid_size:
                    reveal_cell(row + i, col + j)


def flag_cell(row, col):
    if not revealed_grid[row][col]:
        flag_grid[row][col] = not flag_grid[row][col]


def check_win():
    for i in range(grid_size):
        for j in range(grid_size):
            if bomb_grid[i][j] == 0 and not revealed_grid[i][j]:
                return False
    return True


def game_over():
    global wol
    wol = 2
    for i in range(grid_size):
        for j in range(grid_size):
            if bomb_grid[i][j] == 1:
                revealed_grid[i][j] = True
                screen.blit(r_img9, (j * block_size, i * block_size))


# 弹窗
class PopupWindow(Tk):
    def show_message(self, message):
        messagebox.showinfo("Message", message)


def on_ok_clicked():
    if var_difficulty.get() == 1:
        return 0
    elif var_difficulty.get() == 2:
        return 90
    elif var_difficulty.get() == 3:
        return 30
    else:
        return 0


root = tk.Tk()
root.title("难度选择")
var_difficulty = tk.IntVar(value=0)
popup_window = PopupWindow()
# 主游戏循环
run1 = True
run = True
while run:
    while run1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run1 = False
                run = False
            screen.fill(WHITE)
            if start_button.is_clicked():
                run1 = False
            if quit_button.is_clicked():
                run1 = False
                run = False
            if level_button.is_clicked():
                # 创建单选按钮并绑定到同一个变量上
                tk.Radiobutton(root, text="简单", variable=var_difficulty, value=1).pack(anchor=tk.W)
                tk.Radiobutton(root, text="中等", variable=var_difficulty, value=2).pack(anchor=tk.W)
                tk.Radiobutton(root, text="困难", variable=var_difficulty, value=3).pack(anchor=tk.W)
                # 创建一个确定按钮来触发难度选择的结果
                tk.Button(root, text="确定", command=on_ok_clicked).pack(pady=20)
                root.mainloop()
            start_button.draw(screen)
            level_button.draw(screen)
            quit_button.draw(screen)
            pygame.display.flip()
    screen.fill(WHITE)
    draw_grid()
    draw_text()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if wol == 2:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            row, col = y // (width // grid_size), x // (width // grid_size)
            if event.button == 1:  # 左键点击
                reveal_cell(row, col)
                if check_win():
                    wol = 1
                    run = False
            elif event.button == 3:  # 右键点击
                flag_cell(row, col)
                count = count - 1
    count_text = font.render(f"Count: {str(count)}", True, (0, 0, 0))
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
    time_text = font.render(f"Time: {elapsed_time:.1f}s", True, (0, 0, 0))
    screen.blit(time_text, (0, 320))
    screen.blit(count_text, (150, 320))
    pygame.display.flip()
    #根据难度限时
    if on_ok_clicked() != 0 and elapsed_time > on_ok_clicked():
        wol = 3
        run = False
if wol == 1:
    popup_window.show_message("y win")
elif wol == 2:
    popup_window.show_message("y lose")
elif wol == 3:
    popup_window.show_message("time out")
pygame.quit()
