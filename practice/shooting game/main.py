# two player chess in python with Pygame!
# part one, set up variables images and game loop

import pygame
import os

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH*0.8)
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption('Shooter')

clock = pygame.time.Clock()
FPS = 60
GRAVITY = 0.75

# define player action variables
moving_left = False
moving_right = False
shoot = False

#load images
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()

#define colours
BG = (144, 201, 120)
RED = (255, 0, 0)


def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))


class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.shoot_cooldown = 0
        self.health = 100
        self.max_health = self.health
        self.ammo = ammo
        self.start_ammo = ammo
        self.direction = 1
        self.jump = False
        self.in_air = True
        self.flip = False
        self.vel_y = 0
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for anim in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{anim}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.char_type}/{anim}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.update_animation()
        self.check_alive()
        # update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        

    def move(self, moving_left, moving_right):
        # reset movement variables
        dx = 0
        dy = 0

        #assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        # jumb
        if self.jump and not self.in_air:
            self.vel_y = -11
            self.jump = False
            self.in_air = True
        # apply gravity
        
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y
        
        # check collision with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False
        
        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 100
        # check if enought time passed since last update
        
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list[self.action]):
                if self.action == 3:
                    self.frame_index = len(self.animation_list[self.action]) -1
                else:
                    self.frame_index = 0



    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <=0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)
    
    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def shoot(self):
        if not self.shoot_cooldown and self.ammo>0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + self.rect.size[0]*0.6*self.direction, self.rect.centery, self.direction)
            bullet_group.add(bullet)
            self.ammo -=1

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        self.rect.x+=(self.direction * self.speed)
        # check if bullet has gone off screen

        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        # check collision with characters
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                self.kill()
                
        if pygame.sprite.spritecollide(enemy, bullet_group, False):
            if enemy.alive:
                enemy.health -= 20
                self.kill()
    
# create sprite groups
bullet_group = pygame.sprite.Group()



player = Soldier('player', 200, 200, 3, 5, 20)
enemy = Soldier('enemy', 200, 200, 3, 5, 20)

run = True
while run:
    clock.tick(FPS)
    draw_bg()


    player.update()
    player.draw()
    
    enemy.update()
    enemy.draw()

    # update and draw groups
    bullet_group.update()
    bullet_group.draw(screen)

    if player.alive:
        # shoot bullets
        if shoot:
            player.shoot()
        if player.in_air:
            player.update_action(2)
        elif moving_left or moving_right:
            player.update_action(1)
        else:
            player.update_action(0)

    # update player actions
    player.move(moving_left, moving_right)



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_w and player.alive:
                player.jump = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
    pygame.display.update()
pygame.quit()
