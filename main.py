import pygame, sys
from player import Player
import obstacle
from alien import Alien, Extra
from random import choice,randint
from laser import Laser

class Game:
    def __init__(self):
        #PLAYER SETUP
        player_sprite = Player((screen_w/2, screen_h), screen_w, screen_h, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        #OBSTACLE SETUP
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_pos = [num * (screen_w /self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_all_obstacles(self.obstacle_x_pos, x_start= screen_w/ 15, y_start= 480)

        #ALIEN SETUP
        self.aliens = pygame.sprite.Group()
        self.alien_setup(rows = 6, cols = 8)
        self.alien_direction = 1
        self.alien_lasers = pygame.sprite.Group()

        self.extra_side = 'left'
        extra = Extra(self.extra_side, screen_w)
        self.extra = pygame.sprite.GroupSingle(extra)

        #HEALTH SETUP
        self.lives = 3
        self.life_surf = pygame.image.load('graphics/player.png').convert_alpha()
        self.life_x_start_pos = screen_w - (self.life_surf.get_size()[0] * 2 + 20)

        #SCORE SETUP
        self.score = 0
        self.score_font = pygame.font.Font('font/Pixeled.ttf', 15)

        #SCREENS SETUP
        self.game_over = False
        self.game_over_font = pygame.font.Font('font/Pixeled.ttf', 40)
        self.you_win = False

        #AUDIO
        music = pygame.mixer.Sound('audio/music.wav')
        music.set_volume(.1)
        music.play(loops=-1)

        self.explosion_sound = pygame.mixer.Sound('audio/explosion.wav')
        self.explosion_sound.set_volume(.2)
        self.laser_sound = pygame.mixer.Sound('audio/laser.wav')
        self.laser_sound.set_volume(.2)

    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == "x":
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacle.Block(self.block_size, (241, 79, 80), x, y)
                    self.blocks.add(block)

    def create_all_obstacles(self,offset,x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def alien_setup(self,rows, cols, spacing_x = 60, spacing_y = 48, offset_x= 70, offset_y= 80):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * spacing_x + offset_x
                y = row_index * spacing_y + offset_y
                if row_index == 0: alien_sprite = Alien('yellow', x, y)
                elif row_index <= 2: alien_sprite = Alien('green', x, y)
                else: alien_sprite = Alien('red', x, y)
                self.aliens.add(alien_sprite)

    def alien_movement(self):
        all_aliens = self.aliens.sprites()
        alien_move_forward = False
        if self.aliens.sprites():
            for alien in all_aliens:
                if alien.rect.right >= screen_w: 
                    self.alien_direction = -1
                    alien_move_forward = True
                if alien.rect.left <= 0: 
                    self.alien_direction = 1
                    alien_move_forward = True
        if self.aliens.sprites():
            for alien in all_aliens:
                if alien_move_forward == True:
                    alien.rect.y += 4
    
        # make a power system for each diff color has diff shooting time
 
    def alien_shooting(self):
        if self.aliens.sprites():
            rand_alien = choice(self.aliens.sprites())
            self.alien_lasers.add(Laser(rand_alien.rect.center,screen_h,8))
            self.laser_sound.play()

    def extra_spawning(self):
        if self.extra_side == 'left': self.extra_side = 'right'
        elif self.extra_side == 'right': self.extra_side = 'left'

        self.extra.add(Extra(self.extra_side, screen_w))

    def collision_checks(self):
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                if pygame.sprite.spritecollide(laser, self.blocks,True):
                    laser.kill()
            for laser in self.player.sprite.lasers:
                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                    self.explosion_sound.play()
                    laser.kill()
            for laser in self.player.sprite.lasers:
                if pygame.sprite.spritecollide(laser, self.extra, True):
                    laser.kill()
                    self.explosion_sound.play()
                    self.score += 500

        if self.alien_lasers:
            for laser in self.alien_lasers:
                if pygame.sprite.spritecollide(laser, self.player, False):
                    self.explosion_sound.play()
                    laser.kill()
                    self.lives -=1
                    if self.lives == 0:
                        self.game_over = True
                        #game over
            for laser in self.alien_lasers:
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
        
        if self.aliens:
            for alien in self.aliens:
                if alien.rect.bottom >= 480:
                    self.game_over = True
        else:
            self.you_win = True
    
    def create_lives(self):
        for live in range(self.lives - 1):
            x = self.life_x_start_pos + (live * (self.life_surf.get_size()[0] + 10))
            screen.blit(self.life_surf,(x,8))

    def display_score(self):
        score_surf = self.score_font.render('Score: '+str(self.score), False, 'White')
        score_rect = score_surf.get_rect(topleft = (10,0))
        screen.blit(score_surf,score_rect)

    def display_game_over(self):
        game_over_surf = self.game_over_font.render('GAME OVER',False , 'White')
        game_over_rect = game_over_surf.get_rect(center = (screen_w/2, screen_h/2))
        screen.blit(game_over_surf, game_over_rect)

    def display_win(self):
        win_surf = self.game_over_font.render('YOU WIN',False , 'White')
        win_rect = win_surf.get_rect(center = (screen_w/2, screen_h/2))
        screen.blit(win_surf, win_rect)
    
    def game_running_check(self):
        if self.game_over == True:
            return False
        elif self.you_win == True:
            return False
        else: return True

    def run(self):
        self.game_running_check()

        if self.game_over: 
            self.display_game_over()
        elif self.you_win: 
            self.display_win()
        else:
            self.player.update()
            self.aliens.update(self.alien_direction)
            self.alien_movement()
            self.alien_lasers.update()
            self.extra.update()
            self.collision_checks()
            self.create_lives()

            self.display_score()
            self.player.sprite.lasers.draw(screen)
            self.player.draw(screen)
            self.blocks.draw(screen)
            self.aliens.draw(screen)
            self.alien_lasers.draw(screen)
            self.extra.draw(screen)
        
class CRT:
    def __init__(self):
        self.tv = pygame.image.load('graphics/tv.png').convert_alpha()
        self.tv = pygame.transform.scale(self.tv,(screen_w, screen_h))

    def crt_lines(self):
        line_height = 3
        line_amount = int(screen_h / line_height)
        for line in range(line_amount):
            y_pos = line * line_height
            pygame.draw.line(self.tv, 'black',(0,y_pos),(screen_w, y_pos),1)

    
    def draw(self):
        self.tv.set_alpha(randint(80,100))
        self.crt_lines()
        screen.blit(self.tv,(0,0))

if __name__ == '__main__':
    pygame.init()
    screen_w = 600
    screen_h = 600
    screen = pygame.display.set_mode((screen_w,screen_h))
    clock = pygame.time.Clock()
    game = Game()
    crt = CRT()
    


    alien_laser = pygame.USEREVENT + 1
    pygame.time.set_timer(alien_laser, 800)

    extra_spawn = pygame.USEREVENT + 2
    pygame.time.set_timer(extra_spawn, randint(6000,8000))

    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if game.game_running_check():
                if event.type == alien_laser:
                    game.alien_shooting()
                
                if event.type == extra_spawn:
                    game.extra_spawning()
        
        screen.fill((30,30,30))
        game.run()
        crt.draw()
        pygame.display.flip()
        clock.tick(60)