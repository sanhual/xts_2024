import sys
import pygame
import random
from tkinter import Tk,messagebox

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
block_size=WIDTH//GRID_SIZE
wol=0
img10=pygame.image.load(r".\images\10.jpg")
img9=pygame.image.load(r".\images\9.jpg")
img11=pygame.image.load(r".\images\11.jpg")
img1=pygame.image.load(r".\images\1.jpg")
img2=pygame.image.load(r".\images\2.jpg")
img3=pygame.image.load(r".\images\3.jpg")
img4=pygame.image.load(r".\images\4.jpg")
img5=pygame.image.load(r".\images\5.jpg")
img6=pygame.image.load(r".\images\6.jpg")
img0=pygame.image.load(r".\images\0.jpg")
img7=pygame.image.load(r".\images\7.jpg")
img8=pygame.image.load(r".\images\8.jpg")
r_img11=pygame.transform.scale(img11,(30,30))
r_img9=pygame.transform.scale(img9,(30,30))
r_img10=pygame.transform.scale(img10,(30,30))
r_img1=pygame.transform.scale(img1,(30,30))
r_img2=pygame.transform.scale(img2,(30,30))
r_img3=pygame.transform.scale(img3,(30,30))
r_img4=pygame.transform.scale(img4,(30,30))
r_img5=pygame.transform.scale(img5,(30,30))
r_img6=pygame.transform.scale(img6,(30,30))
r_img0=pygame.transform.scale(img0,(30,30))
r_img7=pygame.transform.scale(img7,(30,30))
r_img8=pygame.transform.scale(img8,(30,30))

# 创建屏幕
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("扫雷游戏")

# 创建地雷图和显示图
bomb_grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
display_grid = [[" " for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
revealed_grid = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
flag_grid = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


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
    # block_size = WIDTH // GRID_SIZE
    # for i in range(GRID_SIZE+1):
    #     pygame.draw.line(screen, BLACK, (0, i * block_size), (WIDTH, i * block_size))
    #     pygame.draw.line(screen, BLACK, (i * block_size, 0), (i * block_size, HEIGHT - 50))
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            screen.blit(r_img10,(j*block_size,i*block_size))
            
# 渲染文本
def draw_text():
    font = pygame.font.Font(None, 36)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if revealed_grid[i][j] and display_grid[i][j]!="":
                screen.blit(eval("r_img{}".format(display_grid[i][j])),(j*block_size,i*block_size))
            elif revealed_grid[i][j] and display_grid[i][j]=="":
                game_over()
            elif flag_grid[i][j]:
                screen.blit(r_img11,(j*block_size,i*block_size))

# 扫雷逻辑
def reveal_cell(row, col):
    if revealed_grid[row][col] or flag_grid[row][col]:
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
                    
def flag_cell(row,col):
    if not revealed_grid[row][col]:
        flag_grid[row][col] = not flag_grid[row][col]
        
def check_win():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if bomb_grid[i][j] == 0 and not revealed_grid[i][j]:
                return False
    return True
    
def game_over():
    global wol
    wol=2
    for i in range(GRID_SIZE):
        if bomb_grid[i][j]==1:
            revealed_grid[i][j]=True
            screen.blit(r_img9,(j*block_size,i*block_size))

# 弹窗
class PopupWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title("Popup Window")
        self.geometry("200x100")

    def show_message(self,message):
        messagebox.showinfo("Message",message)

popup_window=PopupWindow()

# 主游戏循环
run = True
while run:
    screen.fill(WHITE)
    draw_grid()
    draw_text()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if wol==2:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            row, col = y // (WIDTH // GRID_SIZE), x // (WIDTH // GRID_SIZE)
            if event.button == 1:  # 左键点击
                reveal_cell(row, col)
                if check_win():
                    wol=1
                    run = False
            elif event.button == 3: #右键点击
                flag_cell(row,col)
    pygame.display.flip()

if wol==1:
    popup_window.show_message("y win")
elif wol==2:
    popup_window.show_message("y lose")

pygame.quit()
