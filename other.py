class Tank():
    def  __init__(self):
        pass

    # 坦克的移动方法
    def move(self):
        pass

    # 碰撞墙壁的方法
    def hitWalls(self):

        pass


# 射击方法
    def shot(self):
        pass


# 展示坦克
    def displayTank(self):
        pass
class MyTank(Tank):
    def  __init__(self):
        pass
#碰撞敌方坦克的方法
    def hitEnemyTank(self):
        pass

class EnemyTank(Tank):
    def  __init__(self):
        pass
    def hitMyTank(self):
        pass

class Bullet():
    def __init__(self):
        pass
#子弹的移动方法 def
    def bulletMove(self):
        pass
#展示子弹的方法 def
    def displayBullet(self):
        pass
#我方子弹碰撞敌方坦克的方法
    def hitEnemyTank(self):
        pass
#敌方子弹与我方坦克的碰撞方法
    def hitMyTank(self):
        pass
#子弹与墙壁的碰撞
    def hitWalls(self):
        pass

class Wall():
    def __init__(self):
        pass
#展示墙壁的方法
    def displayWall(self):
        pass

class Explode():
    def __init__(self):
        pass
#展示墙壁的方法
    def  displayExplode(self):
        pass

class Music():
    def __init__(self):
        pass
#开始播放音乐
    def play(self):
        pass
