# runner game {} | [] @

import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        hamster_walk1 = pygame.image.load('pythonProject\pygame\hamster.walk1170.png').convert_alpha()
        hamster_walk2 = pygame.image.load('pythonProject\pygame\hamster.walk2170.png').convert_alpha()
        self.hamster_walk = [hamster_walk1,hamster_walk2]
        self.player_index = 0
        self.hamster_jump = pygame.image.load('pythonProject\pygame\hamster.jump170.png').convert_alpha()
        
        self.image = self.hamster_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,350))
        self.grav = 0

        self.jump_sound = pygame.mixer.Sound('pythonProject\pygame\jump_sound.mp3')
        self.jump_sound.set_volume(0.2)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 350:
            self.grav = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.grav += 1
        self.rect.y += self.grav
        if self.rect.bottom >= 350:
            self.rect.bottom = 350

    def animation_state(self):
        if self.rect.bottom < 350:
            self.image = self.hamster_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.hamster_walk):self.player_index = 0
            self.image = self.hamster_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == 'gost':
            gost1 = pygame.image.load('pythonProject\pygame\gost1100.png').convert_alpha()
            gost2 = pygame.image.load('pythonProject\pygame\gost2100.png').convert_alpha()
            self.frames = [gost1,gost2]
            y_pos = 200
        else:
            octopus1 = pygame.image.load('pythonProject\pygame\octopus1180.png').convert_alpha()
            octopus2 = pygame.image.load('pythonProject\pygame\octopus2180.png').convert_alpha()
            self.frames = [octopus1,octopus2]
            y_pos = 400

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index  >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 5
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():

    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'SCORE: {current_time}',False, 'Orange')
    score_rect = score_surf.get_rect(center = (425,60))
    screen.blit(score_surf,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 350: screen.blit(octopus1,obstacle_rect)
            else: screen.blit(gost_surf,obstacle_rect)

            

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else: return []

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
        return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else: return True

def player_animation():
    global hamster_surf, player_index

    if hamster1_rect.bottom < 350: hamster_surf = hamster_jump
    else: 
        player_index += 0.1
        if player_index >= len(hamster_walk): player_index = 0
        hamster_surf = hamster_walk[int(player_index)]

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Hamsters Run')
clock = pygame.time.Clock()
test_font = pygame.font.Font('pythonProject\pygame\Pixeltype.ttf',50)
game_active = False
start_time = 0
score = 0

bg_music = pygame.mixer.Sound('pythonProject\pygame\music.wav')
bg_music.play(loops = -1)
bg_music.set_volume(0.5)

#group
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('pythonProject\pygame\Sky.png').convert()
ground_surface = pygame.image.load('pythonProject\pygame\ground.png').convert()

octopus1 = pygame.image.load('pythonProject\pygame\octopus1180.png').convert_alpha()
octopus2 = pygame.image.load('pythonProject\pygame\octopus2180.png').convert_alpha()
octopus_frames = [octopus1,octopus2]
octopus_index = 0
octopus_surf = octopus_frames[octopus_index]

gost1 = pygame.image.load('pythonProject\pygame\gost1100.png').convert_alpha()
gost2 = pygame.image.load('pythonProject\pygame\gost2100.png').convert_alpha()
gost_frames = [gost1,gost2]
gost_index = 0
gost_surf = gost_frames[gost_index]

obstacle_rect_list = []

hamster_walk1 = pygame.image.load('pythonProject\pygame\hamster.walk1170.png').convert_alpha()
hamster_walk2 = pygame.image.load('pythonProject\pygame\hamster.walk2170.png').convert_alpha()
hamster_walk = [hamster_walk1,hamster_walk2]
player_index = 0
hamster_jump = pygame.image.load('pythonProject\pygame\hamster.jump170.png').convert_alpha()

hamster_surf = hamster_walk[player_index]
hamster1_rect = hamster_surf.get_rect(midbottom = (80,350)) #80,300
hamster1_grav = 0

#Intro screen
hamster_stand = pygame.image.load('pythonProject\pygame\hamster.stand170.png').convert_alpha()
hamster_stand = pygame.transform.rotozoom(hamster_stand,0,2)
hamster_stand_rect = hamster_stand.get_rect(center = (400,200)) 

game_name = test_font.render('Hamster Run', False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,60))

game_message = test_font.render('Press space to run.', False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,350))

# Timer
obstacle_timer = pygame.USEREVENT + 1 
pygame.time.set_timer(obstacle_timer, 1500)

octopus_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(octopus_animation_timer, 500)

gost_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(gost_animation_timer, 200)

while True:
    # draw element and update everything
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if hamster1_rect.collidepoint(event.pos) and hamster1_rect.bottom >= 350: 
                    hamster1_grav = -20
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and hamster1_rect.bottom >= 350:
                    hamster1_grav = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['gost','octopus','octopus','octopus'])))
                # if randint(0,2):
                #     obstacle_rect_list.append(octopus_surf.get_rect(bottomright = (randint(900,1100),300)))
                # else:
                #     obstacle_rect_list.append(gost_surf.get_rect(bottomright = (randint(900,1100),210)))
            else: 
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = int(pygame.time.get_ticks() / 1000)

            if event.type == octopus_animation_timer:
                if octopus_index == 0: octopus_index = 1
                else: octopus_index = 0
                octopus_surf = octopus_frames[octopus_index]
            if event.type == gost_animation_timer:
                if gost_index == 0: gost_index = 1
                else: gost_index = 0
                gost_surf = gost_frames[gost_index]



        
    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        # pygame.draw.rect(screen, 'White', score_rect)
        # pygame.draw.rect(screen, 'Green', score_rect, 800)
        # screen.blit(score_surf, score_rect)
        score = display_score()
     
        # octopus1_rect.x -= 6
        # if octopus1_rect.right <= 0: octopus1_rect.left = 850
        # screen.blit(octopus1_surf, octopus1_rect)

        # hamster1_grav += 1
        # hamster1_rect.y += hamster1_grav
        # if hamster1_rect.bottom >= 350: hamster1_rect.bottom = 350
        # player_animation()
        # screen.blit(hamster_surf, hamster1_rect)
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        # Obstacle movement
        # obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        game_active = collision_sprite()
        # game_active = collisions(hamster1_rect,obstacle_rect_list)

    
    else:
        screen.fill(('Black'))
        screen.blit(hamster_stand,hamster_stand_rect)
        obstacle_rect_list.clear()
        hamster1_rect.midbottom = (80,350)
        hamster1_grav = 0

        score_message = test_font.render(f'Your Score: {score}',False,(111,196,169))
        score_message_rect = score_message.get_rect(center = (400,350))
        screen.blit(game_name,game_name_rect)

        if score == 0: screen.blit(game_message,game_message_rect)
        else: screen.blit(score_message,score_message_rect)

    pygame.display.update()
    clock.tick(60) 