import pygame, os;



def menu_screen(screen, intro_screen = False):
    
    run = True
    screen_scroll = 0
    menu_counter = 0
    avatar_list = [os.path.join('images','ryan.png'), 
                   os.path.join('images','josh.png'), 
                   os.path.join('images','anni.png'), 
                   os.path.join('images','jack.png')]

    # Load images and fonts prior to loop
    rocket_image = pygame.transform.smoothscale(pygame.image.load(os.path.join('images','rocket.png')), (80,140))
    ufo_image = pygame.transform.smoothscale(pygame.image.load(os.path.join('images','ufo.png')), (90,90))
    left_arrow = pygame.transform.smoothscale(pygame.image.load(os.path.join('images','left.png')),(40,40))
    right_arrow = pygame.transform.smoothscale(pygame.image.load(os.path.join('images','right.png')),(40,40))
    menu_image = pygame.image.load(os.path.join('images','menu_image.jpg'))
    moon_image = pygame.transform.smoothscale(pygame.image.load(os.path.join('images','moon.png')), (160,160))
    mars_image =  pygame.transform.smoothscale(pygame.image.load(os.path.join('images','mars.png')), (80,80))
    
    menu_bg = 0
    menu_bg2 = menu_image.get_width()
    
    text1 = pygame.font.Font('1.ttf', 50).render("MAIN MENU", True, (255, 255, 255))
    text2 = pygame.font.Font('1.ttf', 34).render("Press ENTER To Start", True, (255, 255, 255))
    text3 = pygame.font.Font('1.ttf', 28).render("Select your character", True, (255, 255, 255))
    text4 = pygame.font.Font('3.ttf', 20).render("[Left]", True, (255, 255, 255))
    text5 = pygame.font.Font('3.ttf', 20).render("[Right]", True, (255, 255, 255))  

    for i, image in enumerate(avatar_list):
        avatar_list[i] = pygame.transform.smoothscale(pygame.image.load(image), (140,140))
              
    while run:
        pygame.time.wait(2)
        menu_counter += 1
        # Prints background image to screen
        screen.blit(menu_image, (menu_bg,0))
        screen.blit(menu_image, (menu_bg2,0))
        menu_bg -= 0.5
        menu_bg2 -= 0.5
        if menu_bg < menu_image.get_width() * -1:
            menu_bg = menu_image.get_width()
        if menu_bg2 < menu_image.get_width() * -1:
            menu_bg2 = menu_image.get_width()
        
        # Prints moving objects
        screen.blit(mars_image, (screen.get_width() - menu_counter, 
                          (screen.get_height()*0.15 + menu_counter*0.15))) 
        screen.blit(ufo_image, (-180 + (menu_counter*0.5), 
                          (screen.get_height()*0.65))) 
        screen.blit(rocket_image, ((screen.get_width()*0.75), 
                          (screen.get_height()/2) + 700 - menu_counter))
        # Prints text to screen
        screen.blit(text1, (372, 50))
        screen.blit(text2, (337, 200))
        screen.blit(text3, (370, 250))
        screen.blit(text4, (305, 345))
        screen.blit(text5, (650, 345))

        # Prints arrows and moon
        screen.blit(left_arrow, ((screen.get_width())/2 + 90, 
                    (screen.get_height())/2 + 120))
        screen.blit(right_arrow, ((screen.get_width())/2 - 135, 
                    (screen.get_height())/2 + 120))
        screen.blit(moon_image,((screen.get_width())/2 - 80, (screen.get_height())/2 + 60))

        # Prints character selection
        screen.blit(avatar_list[screen_scroll], ((screen.get_width())/2 - 65, 
                    (screen.get_height())/2 + 70))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                os._exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_RIGHT:
                    if screen_scroll >= len(avatar_list)-1:
                        screen_scroll = 0
                    else:
                        screen_scroll += 1
                if event.key==pygame.K_LEFT:
                    if screen_scroll < 0:
                        screen_scroll = len(avatar_list)-1
                    else:
                        screen_scroll -= 1
                if event.key == pygame.K_RETURN:
                    return avatar_list[screen_scroll]
                    run = False
                    
        pygame.display.flip()


def pause_screen(screen):            
    font1 = pygame.font.Font('1.ttf', 50)
    font2 = pygame.font.Font('1.ttf', 30)
    Text1 = font1.render("PAUSE", True, (255, 255, 255))
    Text2 = font2.render("Press ENTER To Resume", True, (255, 255, 255))
    run = True
    while run:
        screen.blit(Text1, (420, 150))
        screen.blit(Text2, (330, 250))
            
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                os._exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    run = False

