import pygame
import sys
import traceback
import myplane
import enemy
import bullet
import supply
from pygame.locals import *
from random import *

pygame.init()
pygame.mixer.init()

bg_size = width,height = 480,700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption('期末作业————————飞机大战')

background = pygame.image.load('images/background.png').convert()

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,2)
RED = (255,0,0)
#载入游戏音乐
pygame.mixer.music.load("sound/game_music.ogg")
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3_fly_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.5)
me_down_sound = pygame.mixer.Sound("sound/me_down.wav")
me_down_sound.set_volume(0.2)

def add_small_enemies(group1,group2,num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def add_mid_enemies(group1,group2,num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)

def add_big_enemies(group1,group2,num):
    for i in range(num):
        e3 = enemy.BigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)
def main():
    pygame.mixer_music.play(-1)
    #生成我方飞机
    me = myplane.MyPlane(bg_size)
    #生成敌方飞机，大。中。小共三类
    enemies = pygame.sprite.Group()

    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies,enemies,15)

    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 4)

    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies, enemies,2)

    #生成子弹
    bullet1 = []
    bullet1_index = 0
    BULLET1_NUM = 4
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))

    clock = pygame.time.Clock()

    #中弹图片索引
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0
    #统计用户得分
    score = 0
    score_font = pygame.font.Font("font/font.ttf",36)
    # 全屏炸弹
    bomb_image = pygame.image.load('images/bomb.png').convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font("font/font.ttf", 48)
    bomb_num = 3

    # 每30秒发放一个补给包
    bomb_supply = supply.Bomb_Supply(bg_size)

   # SUPPLY_TIME = USEREVENT
   # pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)
    #用于切换图片
    switch_image = True
    #生命数量
    life_num = 1
    # 游戏结束画面
    gameover_font = pygame.font.Font("font/font.TTF", 48)
    again_image = pygame.image.load("images/again.png").convert_alpha()
    again_rect = again_image.get_rect()
    gameover_image = pygame.image.load("images/gameover.png").convert_alpha()
    gameover_rect = gameover_image.get_rect()

    #用于延迟
    delay = 100
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False
        #检测用户键盘操作
        key_pressed = pygame.key.get_pressed()

        if key_pressed[K_w] or key_pressed[K_UP]:
            me.moveUp()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            me.moveDown()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            me.moveLeft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            me.moveRight()

        # 绘制全屏炸弹补给
        bomb_supply.move()
        screen.blit(bomb_supply.image, bomb_supply.rect)
        screen.blit(background,(0,0))
        #发射子弹
        if not(delay%10):
            bullet_sound.play()
            bullet1[bullet1_index].reset(me.rect.midtop)
            bullet1_index = (bullet1_index + 1) % BULLET1_NUM
        #检测子弹是否击中敌机
        for b in bullet1:
            if b.active:
                b.move()
                screen.blit(b.image,b.rect)
                enemy_hit = pygame.sprite.spritecollide(b,enemies,False,pygame.sprite.collide_mask)
                if enemy_hit:
                    b.active = False
                    for e in enemy_hit:
                        if e in mid_enemies or e in big_enemies:
                            e.energy -= 1
                            if e.energy == 0:
                                e.active = False
                        else:
                            e.active =False

        #绘制敌方大型飞机
        for each in big_enemies:
            if each.active:
                each.move()
                if switch_image:
                    screen.blit(each.image1,each.rect)
                else:
                    screen.blit(each.image2, each.rect)
                #绘制血槽
                pygame.draw.line(screen,BLACK,\
                                 (each.rect.left,each.rect.top - 5),\
                                 (each.rect.right,each.rect.top - 5),\
                                    2)
                #当生命值大于20%，血条现实绿色，否则显示红色
                energy_remain = each.energy/enemy.BigEnemy.energy
                if energy_remain > 0.2:
                    energy_color = GREEN
                else:
                    energy_color = RED
                pygame.draw.line(screen,energy_color,\
                                 (each.rect.left,each.rect.top - 5),\
                                 (each.rect.left + each.rect.width * energy_remain,\
                                 each.rect.top - 5),\
                                    2
                                 )
                # 当大型飞机出现之前，播放音效
                if each.rect.bottom == -50:
                    enemy3_fly_sound.play(-1)
            else:
                #飞机损毁
                if not (delay%3):
                    if e3_destroy_index == 0:
                        enemy3_down_sound.play()
                    screen.blit(each.destroy_images[e3_destroy_index],each.rect)
                    e3_destroy_index = (e3_destroy_index+1) % 6
                    if e3_destroy_index == 0:
                        enemy3_fly_sound.stop()
                        score += 10000
                        each.reset()

        # 绘制敌方中型飞机
        for each in mid_enemies:
            if each.active:
                each.move()
                screen.blit(each.image, each.rect)
                # 绘制血槽
                pygame.draw.line(screen, BLACK, \
                                 (each.rect.left, each.rect.top - 5), \
                                 (each.rect.right, each.rect.top - 5), \
                                 2)
                # 当生命值大于20%，血条现实绿色，否则显示红色
                energy_remain = each.energy / enemy.MidEnemy.energy
                if energy_remain > 0.2:
                    energy_color = GREEN
                else:
                    energy_color = RED
                pygame.draw.line(screen, energy_color, \
                                 (each.rect.left, each.rect.top - 5), \
                                 (each.rect.left + each.rect.width * energy_remain, \
                                  each.rect.top - 5), \
                                 2
                                 )
            else:
                #敌方中型飞机毁灭
                if not (delay%3):
                    if e2_destroy_index == 0:
                        enemy2_down_sound.play()
                    screen.blit(each.destroy_images[e2_destroy_index],each.rect)
                    e2_destroy_index = (e2_destroy_index+1) % 4
                    if e2_destroy_index == 0:
                        score += 6000
                        each.reset()

        # 绘制敌方小型飞机
        for each in small_enemies:
            if each.active:
                each.move()
                screen.blit(each.image, each.rect)
            else:
                #敌方小型飞机毁灭
                if not (delay % 3):
                    if e1_destroy_index == 0:
                        enemy1_down_sound.play()
                    screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                    e1_destroy_index = (e1_destroy_index + 1) % 4
                    if e1_destroy_index == 0:
                        score += 1000
                        each.reset()
        #检测飞机是否被碰撞
        enemy_down = pygame.sprite.spritecollide(me,enemies,False)
        if enemy_down:
            me.active = False
            for e in enemy_down:
                e.active = False
        #绘制我的飞机
        if me.active:
            if switch_image:
                screen.blit(me.image1,me.rect)
            else:
                screen.blit(me.image2,me.rect)
        else:
            #我方飞机毁灭
            if not (delay%3):
                if me_destroy_index ==0:
                    me_down_sound.play()
                screen.blit(me.destroy_images[me_destroy_index],me.rect)
                me_destroy_index = (me_destroy_index+1) % 4
                if me_destroy_index == 0:
                    life_num =0
                    me.reset()

            # 绘制全屏炸弹数量
        bomb_text = bomb_font.render("× %d" % bomb_num, True, WHITE)
        text_rect = bomb_text.get_rect()
        screen.blit(bomb_image, (10, height - 10 - bomb_rect.height))
        screen.blit(bomb_text, (20 + bomb_rect.width,
                                height - 5 - text_rect.height))

        #绘制得分
        score_text = score_font.render("Score : %s" % str(score),True,WHITE)
        screen.blit(score_text,(10,5))
        # 绘制结束界面
        if life_num == 0:
            # 背景音乐停止
            pygame.mixer.music.stop()
            # 停止全部音效
            pygame.mixer.stop()

            gameover_text1 = gameover_font.render("Your Score", True, (255, 255, 255))
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = \
                (width - gameover_text1_rect.width) // 2, height // 3
            screen.blit(gameover_text1, gameover_text1_rect)

            gameover_text2 = gameover_font.render(str(score), True, (255, 255, 255))
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = \
                (width - gameover_text2_rect.width) // 2, \
                gameover_text1_rect.bottom + 10
            screen.blit(gameover_text2, gameover_text2_rect)

        #切换图片，60帧，一秒切换12次
        if not (delay % 5):
            switch_image = not switch_image

        delay -=1
        if not delay:
            delay = 100
            
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()