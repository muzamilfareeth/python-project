import pygame
import os #helps to finding path
pygame.font.init()
pygame.mixer.init ()

WIDTH ,HEIGHT = 900,500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("space war")

WHITE = (255,255,255) 
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW =(255,255,0)
 
HEALTH_FONT = pygame.font.SysFont('comicsans', 20)
WINNER_FONT = pygame.font.SysFont('comicsans',100)


BORDER = pygame.Rect((WIDTH // 2)- 5 ,0,10,HEIGHT)
FPS = 60
bullet_vel = 7
max_bullet = 5

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets','Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets','Gun+Silencer.mp3'))

Y_SPACESHIP = pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))
Y_SHIP = pygame.transform.rotate(pygame.transform.scale(Y_SPACESHIP,(55,40)),90)
R_SPACESHIP = pygame.image.load(os.path.join('Assets','spaceship_red.png'))
R_SHIP = pygame.transform.rotate(pygame.transform.scale(R_SPACESHIP,(55,40)),270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.png')),(WIDTH,HEIGHT))


def draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health):
    WIN.blit(SPACE,(0,0))  
    pygame.draw.rect(WIN,BLACK,BORDER)

    red_health_txt = HEALTH_FONT.render("HEALTH: " + str(red_health),1,WHITE)
    yellow_health_txt = HEALTH_FONT.render("HEALTH: " + str(yellow_health),1,WHITE)
    WIN.blit(red_health_txt,(WIDTH - red_health_txt.get_width() - 10,10 ))
    WIN.blit(yellow_health_txt,(10,10))

    WIN.blit(Y_SHIP,(yellow.x,yellow.y)) #used to display the object , and its coordinate
    WIN.blit(R_SHIP,(red.x,red.y))


    for bullet in red_bullets:
        pygame.draw.rect(WIN,RED,bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN,YELLOW,bullet)

    pygame.display.update()


def draw_font(txt):
    DW = WINNER_FONT.render(txt,1,WHITE)
    WIN.blit(DW,(WIDTH // 2 - DW.get_width()/ 2,HEIGHT // 2 - DW.get_height()// 2))
    pygame.display.update()
    pygame.time.delay(5000)

def yellow_movements(kp,yellow):
    if kp[pygame.K_a] and yellow.x - 5 > 0: 
        yellow.x -= 5
    if kp[pygame.K_d] and yellow.x +  yellow.width < BORDER.x: 
        yellow.x += 5
    if kp[pygame.K_w]  and yellow.y - 5 > 0: 
        yellow.y -= 5
    if kp[pygame.K_s] and yellow.y + yellow.height < HEIGHT - 15: 
        yellow.y += 5


def red_movements(kp,red):
    if kp[pygame.K_LEFT] and red.x - 5 > BORDER.x + BORDER.width: 
        red.x -= 5
    if kp[pygame.K_RIGHT] and red.x +  red.width < WIDTH: 
        red.x += 5
    if kp[pygame.K_UP] and red.y - 5 > 0: 
        red.y -= 5
    if kp[pygame.K_DOWN] and red.y + red.height < HEIGHT - 15: 
        red.y += 5


def handle_bullets(yellow_bullets,red_bullets,yellow,red):
    for bullet in yellow_bullets:
        bullet.x += bullet_vel
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH :
            yellow_bullets.remove(bullet)


    for bullet in red_bullets:
        bullet.x -= bullet_vel
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)





def main():

    red = pygame.Rect(700,300,55,40)
    yellow = pygame.Rect(100,300,55,40)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10


    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < max_bullet:
                    bullet = pygame.Rect(yellow.x + yellow.width,yellow.y + yellow.height // 2 - 2,10,5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()


                if event.key == pygame.K_0  and len(red_bullets) < max_bullet:
                     bullet = pygame.Rect(red.x ,red.y + red.height // 2 - 2,10,5)
                     red_bullets.append(bullet)
                     BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            
            if event.type == YELLOW_HIT:
                yellow_health  -= 1
                BULLET_HIT_SOUND.play()

        winner_txt = ""
        if red_health <= 0:
            winner_txt ="YELLOW WINS!"
        if yellow_health <= 0:
            winner_txt = "red wins!"
        if winner_txt != "":
            draw_font(winner_txt)
            break
        

        kp = pygame.key.get_pressed()
        yellow_movements(kp,yellow)
        red_movements(kp,red)

        handle_bullets(yellow_bullets,red_bullets,yellow,red)
            
        draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health)
    
main()

if __name__ == '__main__':
    main()