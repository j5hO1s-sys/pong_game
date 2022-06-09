import random
import sys
import pygame


WIDTH, HEIGHT = 858, 525
BACKGROUND_COLOR = (30, 30, 30)
PLAYGROUND_COLOR = (220, 220, 220)
PLAYER_COLOR = (220, 220, 220)
BALL_COLOR = (220, 220, 220)

FPS = 60

pygame.init()

FONT = pygame.font.Font('font\ARCADECLASSIC.ttf', 65)



class Ball:
    def __init__(self, screen):
        self.screen = screen
        self.init_pos()
        self.build_sprite()
    
    def init_pos(self):
        self.x, self.y = int(WIDTH//2), int(HEIGHT//2)
        
        self.movex = random.choice([-5, 5])
        self.movey = random.choice([-5, 5])
    
    def move(self):
        self.x += self.movex
        self.y += self.movey
    
    def change_x(self):
        self.movex *= -1
    
    def change_y(self):
        self.movey *= -1

    def build_sprite(self):
        self.sprite = pygame.draw.rect(self.screen, PLAYER_COLOR, (self.x, self.y, 10, 10))
    
    def blit(self):
        if self.y < 10 or self.y > HEIGHT-20:
            self.change_y()
        self.move()
        self.build_sprite()


class Player:
    def __init__(self, screen, x, y, width=15, height=65, speed=10):
        self.x, self.y = x, y
        self.width = width
        self.height = height
        self.speed = speed
        self.screen = screen
        self.score = 0

        self.build_sprite()
    
    def move_up(self):
        if self.y > 15:
            self.y -= self.speed
    
    def move_down(self):
        if self.y < HEIGHT - 20 - self.height:
            self.y += self.speed
    
    def build_sprite(self):
        self.sprite = pygame.draw.line(self.screen, PLAYER_COLOR, (self.x, self.y), (self.x, self.y+self.height), self.width)
    
    def blit(self):
        self.build_sprite()



def build_playground(screen):
    screen.fill(BACKGROUND_COLOR)

    # top and bottom lines
    pygame.draw.line(screen, PLAYER_COLOR, (5, 5), (WIDTH-5, 5), 5)
    pygame.draw.line(screen, PLAYER_COLOR, (5, HEIGHT-10), (WIDTH-5, HEIGHT-10), 5)

    # middle dotted line
    # width is 5 pixels
    center = int((WIDTH/2)+5/2)
    top = 15
    
    while 1:
        bottom = top+10
        pygame.draw.line(screen, PLAYER_COLOR, (center, top), (center, bottom), 5)

        top += 20

        if top+15 >= HEIGHT:
            break

def build_score_viewer(screen, player1, player2):
    p1_score = FONT.render(str(player1.score), True, PLAYGROUND_COLOR)
    p2_score = FONT.render(str(player2.score), True, PLAYGROUND_COLOR)

    p1_rect = p1_score.get_rect()
    p2_rect = p2_score.get_rect()

    p1_rect.center = (int(WIDTH * 0.25), 50)
    p2_rect.center = (int(WIDTH * 0.75), 50)

    screen.blit(p1_score, p1_rect)
    screen.blit(p2_score, p2_rect)


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PONG")

    clock = pygame.time.Clock()

    player1 = Player(screen, 20, 30)
    player2 = Player(screen, WIDTH-20, 30)

    ball = Ball(screen)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            player1.move_up()
        if keys[pygame.K_s]:
            player1.move_down()
        if keys[pygame.K_UP]:
            player2.move_up()
        if keys[pygame.K_DOWN]:
            player2.move_down()

        build_playground(screen)
        build_score_viewer(screen, player1, player2)

        player1.blit()
        player2.blit()
        ball.blit()

        if player1.sprite.colliderect(ball.sprite) or player2.sprite.colliderect(ball.sprite):
            ball.change_x()

        if ball.x > WIDTH-10:
            player1.score += 1
            ball = Ball(screen)
        
        if ball.x < 0:
            player2.score += 1
            ball = Ball(screen)
        
        
        clock.tick(FPS)
        pygame.display.flip()


    return "Quited."


if __name__ == "__main__":
    sys.exit(main())