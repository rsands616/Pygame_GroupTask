import pygame, os, threading, menu;
import maps as mp

global screen
screen = pygame.display.set_mode((1024, 576))

'''
Credit
    Background music:
        Royalty Free Music: "8 Bit Win!" by HeatleyBros
        "https://youtube.com/vX1xq4Ud2z8"

    Royalty free sound effects obtained from "https://www.zapsplat.com"
    Background images courtesy of kurtgesagt.org  
    Text fonts sourced from fontsquirrel.com
'''

MAP_UNIT_X = screen.get_width() / 40.96
MAP_UNIT_Y = screen.get_height() / 23.04
MAP_UNIT_X1 = 25
MAP_UNIT_Y1 = 25


class Player(pygame.sprite.Sprite):
    sizex = int(1.2 * MAP_UNIT_X)
    sizey = int(1.2 * MAP_UNIT_Y)
    vy = int(0.08 * MAP_UNIT_Y)  # Velocity in y direction
    vx = -int(0.08 * MAP_UNIT_X)  # Velocity in x direction
    level = None  # The current level the player is within
    score=0

    on_left_wall = False
    on_right_wall = False
    on_ceiling = False
    on_ground = True

    in_jump = False
    in_glue = False
    player_speed = int(0.36 * MAP_UNIT_X)
    speed = player_speed
    glue_speed = 1
    max_time = 200
    glue_timer = max_time

    def __init__(self, image,
                 x=int(8 * MAP_UNIT_X),
                 y=screen.get_height() - int(8 * MAP_UNIT_Y),
                 dead_image=pygame.image.load(os.path.join('images',
                                                       'dead.jpg')),
                 glue_image=pygame.image.load(os.path.join('images',
                                                          'blob.jpg'))):

        super().__init__()
        self.player_image = pygame.transform.smoothscale(image,
                                                         (self.sizex,
                                                          self.sizey))
        self.image = self.player_image
        self.rect = self.image.get_rect(topleft=(x, y))

        self.dead_image = pygame.transform.scale(dead_image,
                                                 (int(1.2 * MAP_UNIT_X),
                                                  int(1.2 * MAP_UNIT_X)))
        self.glue_image = pygame.transform.scale((glue_image), (int(1.2 * MAP_UNIT_X),
                               int(1.2 * MAP_UNIT_X)))

    def handle_x_collisions(self):
        # Update the position based on the velocity
        self.rect.x += self.vx

        x_collision_vector = self.vx
        x_collisions = pygame.sprite.spritecollide(self,
                                                   self.level.obstacle_list,
                                                   False)
        # For right_check, left_check, down_check and up_check the player's
        # avatar is temporarily moved 1 pixel in one direction to see if it
        # collides with anything, if this is the case then the player avatar
        # is at the edge of an object.
        if self.vx == 0:
            # Move 1 pixel to the left
            self.rect.x += 1
            right_check = pygame.sprite.spritecollide(self,
                                                      self.level.obstacle_list,
                                                      False)
            if len(right_check) > 0:
                x_collision_vector = 1
                x_collisions = right_check
                self.rect.x -= 1  # Return to original position
            else:
                self.rect.x -= 2
                left_check = pygame.sprite.spritecollide(self,
                                                         self.level.obstacle_list,
                                                         False)
                if len(left_check) > 0:
                    x_collision_vector = -1
                    x_collisions = left_check
                self.rect.x += 1

        for obstacle in x_collisions:
            # Handle the collisions
            obstacle.collide(self, x_collision_vector, 0)

    def handle_y_collisions(self):
        # Now account for obstacles in the y direction
        self.rect.y += self.vy
        y_collision_vector = self.vy
        y_collisions = pygame.sprite.spritecollide(self,
                                                   self.level.obstacle_list,
                                                   False)
        if self.vy == 0:
            self.rect.y += 1
            down_check = pygame.sprite.spritecollide(self,
                                                     self.level.obstacle_list,
                                                     False)
            if len(down_check) > 0:
                y_collision_vector = 1
                y_collisions = down_check
                self.rect.y -= 1
            else:
                self.on_ground = False
                self.in_jump = True

        for obstacle in y_collisions:
            # Handle the collisions
            obstacle.collide(self, 0, y_collision_vector)

    def update(self):
        self.calc_grav()
        if self.in_jump:
            # Slow the vx for a physical jump arc
            if abs(self.vx - self.level.shift_x) > int(0.36 * MAP_UNIT_X):
                self.vx = self.vx // 2
        self.handle_x_collisions()
        self.handle_y_collisions()

    def handle_glue(self):
        if self.in_glue and self.glue_timer > 0:
            self.image = self.glue_image
            self.glue_timer -= 1
        else:
            self.image = self.player_image
            self.glue_timer = self.max_time
            self.in_glue = False

    def die(self):
        self.image = self.dead_image
        self.vx = 0
        self.vy = 0
        self.level.shift_x = 0
        run = True
        while True:
            screen.blit(self.image, (self.rect.x, self.rect.y))
            font1 = pygame.font.Font('1.ttf', int(2 * MAP_UNIT_X))
            font2 = pygame.font.Font('1.ttf', int(1.2 * MAP_UNIT_X))
            text1 = font1.render("GAME OVER", True, (255, 255, 255))
            text2 = font2.render("Press ENTER To Return to Menu", True,
                                 (255, 255, 255))
            screen.blit(text1, (int(14.4 * MAP_UNIT_X), int(6.4 * MAP_UNIT_Y)))
            screen.blit(text2, (int(10.8 * MAP_UNIT_X), int(10.4 * MAP_UNIT_Y)))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    os._exit(0)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    main_loop()

    def calc_grav(self):
        if (self.on_left_wall or self.on_right_wall) and self.vy > 0:
            self.vy = 0.2 * MAP_UNIT_Y

        elif self.in_jump or not self.on_ground:
            self.vy += 0.016 * MAP_UNIT_Y

    def jump(self, height):
        vx_kick = int(0.3 * MAP_UNIT_X)
        vy_kick = int(0.34 * MAP_UNIT_Y)
        vy_jump = int(0.32 * MAP_UNIT_Y)

        if self.on_ground == True:
            self.vy = -vy_jump
            self.on_ground = False
        elif self.on_ceiling:
            self.vy = vy_jump

        else:
            if self.on_left_wall:
                if self.vx >= 0:
                    self.vx = -vx_kick
                    self.on_left_wall = False
                    if self.on_ceiling:
                        self.vy = vy_jump
                    else:
                        self.vy = -vy_kick
                    self.on_ground = False
            elif self.on_right_wall:
                self.vx = vx_kick
                self.on_right_wall = False
                if self.on_ceiling:
                    self.vy = vy_jump
                else:
                    self.vy = -vy_kick
                self.on_ground = False
        self.in_jump = True

    def move_left(self):
        if self.in_glue:
            self.vx = self.level.shift_x - self.glue_speed
        else:
            self.vx = self.level.shift_x - self.player_speed

    def move_right(self):
        if self.in_glue:
            self.vx = -self.level.shift_x + self.glue_speed
        else:
            self.vx = -self.level.shift_x + self.player_speed

    def stop(self):
        # Make it go at the same rate as the background
        self.vx = self.level.shift_x

    def end_level(self):
            self.in_glue = False
            self.vx = 0
            self.rect.x = int(4.8 * MAP_UNIT_X)
            self.image = pygame.transform.scale(self.image, (int(3 * MAP_UNIT_X),
                                                             int(3 * MAP_UNIT_Y)))
            run = True
            while run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        os.exit(0)
                        #pygame.quit()
                    if event.type == pygame.KEYDOWN and event.key ==pygame.K_RETURN:
                        run = False


class Level:
    background = None  # Background image for the level
    world_shift = 0  # The total amount the level has 'shifted'
    shift_x = -int(
        0.12 * MAP_UNIT_X)  # The rate at which the level scrolls/shifts
    bg_x = 0  # First coord of the background image
    #level_limit = -400  # -int(120 * MAP_UNIT_X)
    complete = False  # The coordinates of the end of the level

    def __init__(self, number, Player, level_map,background, level_limit=-400):
        self.obstacle_list = pygame.sprite.Group()
        self.Player = Player
        self.number = number
        self.background = pygame.transform.scale(pygame.image.load(background),
                                                 (screen.get_width(),
                                                  screen.get_height()))
        self.level_map = level_map
        self.level_limit=level_limit
        self.add_obstacles()
        self.bg_x2 = self.background.get_width()

    def add_obstacles(self):
        for obstacle in self.level_map:
            self.obstacle_list.add(obstacle)

    def draw(self, screen):
        screen.blit(self.background, (self.bg_x, 0))
        screen.blit(self.background, (self.bg_x2, 0))
        self.obstacle_list.draw(screen)

    def shift_world(self):
        self.world_shift += self.shift_x
        for platform in self.obstacle_list:
            platform.rect.x += self.shift_x
        self.bg_x += (self.shift_x // 3)
        self.bg_x2 += (self.shift_x // 3)
        if self.bg_x < self.background.get_width() * -1:
            self.bg_x = self.background.get_width()
        if self.bg_x2 < self.background.get_width() * -1:
            self.bg_x2 = self.background.get_width()

    def ob_update(self):
        # Call object update for each unqiue instance of object
        for obstacle in self.obstacle_list:
            obstacle.ob_update()

    def is_complete(self, current_position):
        if current_position <= self.level_limit:
            self.complete = True
        else:
            self.complete = False
        return self.complete

    def end_animation(self, clock):
        # When the level has ended
        if self.number == "end":
            screen.fill((0, 0, 0))
            blit_text(text="MISSION SUCCESS", size=50)
        blit_text(text="Press enter to continue", size=20, x_c=100, y_c=150)
        blit_text(text="LEVEL " + str(self.number) + " COMPLETE",
                  size=30, x_c=100, y_c=50)
        self.shift_x = 0

    def end_screen(self):
        screen.fill(color=(0, 0, 0))
        blit_text("MISSION SUCCESS")


def get_current_level(levels):
    current_level = next(level for level in levels if level.complete == False)
    return current_level


def blit_text(text, size=30, colour=(255, 255, 255),
              x_c=screen.get_width() // 2, y_c=screen.get_height() // 2):
    font_text = pygame.font.Font('1.ttf', size).render(
        text, True, colour)
    screen.blit(font_text, (x_c - size, y_c))
    pygame.display.flip()



def main_loop():
    pygame.init()
    pygame.display.set_caption('Ground ctrl')

    # Create clock and time for event handling
    clock_tick = pygame.USEREVENT + 1
    pygame.time.set_timer(clock_tick, 20)

    # Instantiate the Players
    player = Player(menu.menu_screen(screen))

    # Instantiate the levels
    level_1_map = mp.build_obj_map_tutorial()
    level_2_map = mp.build_obj_map_level_2()
    level_3_map = mp.build_obj_map_level_3()
    level_4_map = mp.build_obj_map_level_5()
  
    
    level_01 = Level(number=1, Player=player, level_map=level_1_map,level_limit=mp.limit,
                     background=os.path.join('images', 'stars.png'))
    level_02 = Level(number=2, Player=player, level_map=level_2_map,level_limit=mp.limit,
                     background=os.path.join('images', 'stars.png'))
    level_03 = Level(number=3, Player=player, level_map=level_3_map,level_limit=mp.limit,
                     background=os.path.join('images', 'stars.png'))
    level_04 = Level(number=4, Player=player, level_map=level_4_map,level_limit=mp.limit,
                     background=os.path.join('images', 'stars.png'))
    # Set up the end level
    end_level = Level(number="END", Player=player, level_map=[],level_limit=-4000,
                      background='images/ejiri.jpg')
    end_level.vx = 0
    end_level.shift_x = 0
    # blit(source, dest, area=None, special_flags=0)
    ms_text = pygame.font.Font('1.ttf', 60).render("MISSION SUCCESS", True,
                                                   (0, 0, 0))
    menu_text = pygame.font.Font('1.ttf', 30).render(
        "Press ENTER to return to MENU", True, (0, 0, 0))
    end_level.background.blit(ms_text, (
    screen.get_width() // 4, screen.get_height() // 2 - 60))
    end_level.background.blit(menu_text, (
    screen.get_width() // 4, screen.get_height() // 2))
    #level_01, level_02, level_03,
    level_list = [ level_01,level_02,level_03,level_04, end_level]
    current_level = get_current_level(level_list)
    player.level = current_level
    active_sprite_list = pygame.sprite.Group()
    active_sprite_list.add(player)
    clock = pygame.time.Clock()
    pygame.display.flip()

    # Begins playing background music
    pygame.mixer.music.load(
        os.path.join(os.getcwd(), 'images', '8-bit-win.mp3'))
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(loops=-1)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move_left()
                if event.key == pygame.K_RIGHT:
                    player.move_right()
                if event.key == pygame.K_UP:
                    player.jump(5.6)
                if event.key == pygame.K_RETURN:
                    if current_level.number == "END":
                        menu.menu_screen(screen)
                    else:
                        menu.pause_screen(screen)
            if event.type == clock_tick:
                #if clockTick event is met then call an update method for ob's
                player.handle_glue()
                blit_text(text="Score:" + str(player.score), size=20,
                          x_c=int(MAP_UNIT_X),
                          y_c=int(MAP_UNIT_Y))
                current_level.ob_update()
            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_LEFT and player.vx <0) or (event.key == pygame.K_RIGHT and player.vx > 0):# and player.vx < 0  and player.vx > 0
                #if (event.key == pygame.K_LEFT and player.vy <0) or (event.key == pygame.K_RIGHT and player.vx > 0):# and player.vx < 0  and player.vx > 0

                    player.stop()

        if player.rect.right <= 0:  # if the player goes off the edge of the screen
            player.die()

        # If the player gets to the end of the level, go to the next level
        current_position =  current_level.world_shift - player.rect.x 

        if current_level.is_complete(current_position):
            current_level.end_animation(clock)
            player.end_level()
            current_level = get_current_level(level_list)
            player.level = current_level
        else:
            current_level.shift_world()
            # Make this not run for the end level
            current_level.draw(screen)
            active_sprite_list.update()
            active_sprite_list.draw(screen)
        clock.tick(40)
        pygame.display.flip()


main_loop()
pygame.quit()
os._exit(0)
