import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# kk_dict = {   #課題３
#     ( 0,  0): pg.transform.rotozoom(kk_img, 90, -1.0), #キー押下がない場合
#     (+5,  0): pg.transform.rotozoom(90), #右
#     (+5, -5): pg.transform.rotozoom(45), #右上
#     ( 0, -5): pg.transform.rotozoom(0), #上
#     (-5, -5): pg.transform.rotozoom(315), #左上
#     (-5,  0): pg.transform.rotozoom(270), #左
#     (-5, +5): pg.transform.rotozoom(225), #左下
#     ( 0, +5): pg.transform.rotozoom(180), #下
#     (+5, +5): pg.transform.rotozoom(135), #右下
# }

def gameover(screen: pg.Surface) -> None: #課題１
    haikei_img = pg.Surface((WIDTH, HEIGHT))
    fonto = pg.font.Font(None, 80)
    kouka_img = pg.image.load("fig/8.png") 
    kk2_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    kk2_rct = kouka_img.get_rect()
    kk3_rct = kouka_img.get_rect()
    kk2_rct.center = 750, 320
    kk3_rct.center = 350, 320
    txt = fonto.render("Game over",
            True, (255, 255, 255))
    haikei_img.set_alpha(200)
    pg.draw.rect(haikei_img, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    screen.blit(haikei_img, [0,0])
    screen.blit(txt, [400,300])
    screen.blit(kk2_img, kk2_rct)
    screen.blit(kk2_img, kk3_rct)
    pg.display.update()
    time.sleep(5)
    return


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRect or 爆弾Rect
    戻り値：判定結果タプル（横方向、縦方向）
    画面内ならTrue/画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right: #横にはみでていたら
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20)) #練習２
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0)) #黒いやつを消す
    bb_rct = kk_img.get_rect() #爆弾Rect
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0,HEIGHT)
    vx, vy = +5, +5

    clock = pg.time.Clock()
    tmr = 0
    # kaiten_img = kk_dict #課題３
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):
            
            return gameover(screen)#ゲームオーバー　課題１

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0] #横方向の移動量を加算
                sum_mv[1] += mv[1] #縦方向の移動量を加算
        
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko: #横方向にはみ出ていたら
            vx *= -1
        if not tate: #縦方向にはみ出ていたら
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
