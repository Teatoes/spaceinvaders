import pygame
from laser import Laser
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, screen_width, screen_height, speed):
        super().__init__()
        #PLAYER
        self.image = pygame.image.load('graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = speed
        self.max_x_constraint = screen_width
        self.screen_height = screen_height
        #LASER TIMER
        self.ready = True
        self.laser_time = 0
        self.laser_cd = 600
        #LASER GROUP
        self.lasers = pygame.sprite.Group()
        self.laser_sound = pygame.mixer.Sound('audio/laser.wav')
        self.laser_sound.set_volume(.2)

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed

        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()

    def cooldown(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cd:
                self.ready = True
    
    def check_border(self):
        if self.rect.left <= 0: self.rect.left = 0
        if self.rect.right >= self.max_x_constraint: self.rect.right = self.max_x_constraint

    def shoot_laser(self):
        #ADDS NEW LASER INTO SPRITE GROUP
        self.lasers.add(Laser(self.rect.center,self.screen_height, -8))
        self.laser_sound.play()

    def update(self):
        self.get_input()
        self.check_border()
        self.cooldown()
        self.lasers.update()