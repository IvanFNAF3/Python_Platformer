#HJRGFKLDRJLFKRD:LF
#;de;kf
#АКИМОВ ФОРЕВЕР
#kf;jsdflksdjfklj
#zvbif
#rfvsojxtrvbi,thnf
#AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA#
####################################################################################
# Данный код представляет собой каркас для игры в жанре платформер                 #
# В нем определены: классы главного героя, врагов, собираемых предметов и платформ #
# управление с помощью клавиатуры, проверка коллизий объектов                      #
# Проект можно запустить для демонстрации функционала                              #
####################################################################################

################################################################
#При запуске:                                                  #
# синие элементы - платформы,                                  #
# красный элемент - враг,                                      #
# зеленый элемент - игрок,                                     #
# желтый элемент - собираемый предмет                          #
#                                                              #
#Управление: стрелки клавиатуры для движения, пробел для прыжка#
################################################################

#подключние бибилиотек
import pygame
from audiofiles import*
from platforms import*
from enemy import*
from coin import*
from player import*
from energy import*
from const import*
from interface import*
from init import*


#инициализация Pygame
pygame.init()

#константы-параметры окна
WIDTH = 1920
HEIGHT = 1080

#константы-цвета
BG = (34, 139, 34)
SCORE_COLOR = (0, 0, 0)

#Создаём меню
def menu():
    global is_music_playing
    pygame.mixer.music.play(-1)
    screen.blit(bg_menu, (0, 0))

    start_button = Button("sprites/play_ui_1.png", 900, 745)
    exit_button = Button("sprites/exit_ui.png", 910, 981)
    aboutgame_button = Button("sprites/aboutgame_ui.png", 910, 875)

    if is_music_playing == True:
        msc_off_button = Button("sprites/msc_off_ui.png", 60, HEIGHT - 60)
        msc_on_button = Button("sprites/msc_on_ui_selected.png", 200, HEIGHT - 60)
    else:
        msc_off_button = Button("sprites/msc_off_ui_selected.png", 60, HEIGHT - 60)
        msc_on_button = Button("sprites/msc_on_ui.png", 200, HEIGHT - 60)

    buttons = [start_button, exit_button, msc_on_button, msc_off_button, aboutgame_button]

    init_but(screen, buttons)
    pygame.display.update()

    while True:
        init_but(screen, buttons)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if start_button.rect.collidepoint(x, y):
                    game()
                elif exit_button.rect.collidepoint(x, y):
                    pygame.quit()
                    quit()
                elif msc_off_button.rect.collidepoint(x, y):
                    pygame.mixer.music.set_volume(0.0)
                    msc_off_button.change_img("sprites/msc_off_ui_selected.png") 
                    msc_on_button.change_img("sprites/msc_on_ui.png")
                    is_music_playing = False 
                elif msc_on_button.rect.collidepoint(x, y):
                    pygame.mixer.music.set_volume(0.4)
                    msc_off_button.change_img("sprites/msc_off_ui.png") 
                    msc_on_button.change_img("sprites/msc_on_ui_selected.png")
                    is_music_playing = True
                elif aboutgame_button.rect.collidepoint(x, y):
                    tutorial()

def tutorial():
    global is_music_playing
    screen.blit(bg_aboutgame, (0, 0))

    close_button = Button("sprites/exit_menu_ui.png", 900, 800)

    buttons = [close_button]

    init_but(screen, buttons)
    pygame.display.update()

    while True:
        init_but(screen, buttons)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if close_button.rect.collidepoint(x, y):
                    menu()

#функция для проверки коллизий c платформой
def check_h_collision_platforms(object, platform_list):
    #перебираем все платформы из списка (не группы спрайтов)
    for platform in platform_list:
        if object.rect.colliderect(platform.rect):
            if object.y_velocity > 0: # Если спрайт падает
                #меняем переменную-флаг
                object.on_ground = True
                #ставим его поверх платформы и сбрасываем скорость по оси Y
                object.rect.bottom = platform.rect.top
                object.y_velocity = 0
            elif object.y_velocity < 0: # Если спрайт движется вверх
                #ставим спрайт снизу платформы
                object.rect.top = platform.rect.bottom
                object.y_velocity = 0.6
            elif object.x_velocity > 0: # Если спрайт движется вправо
                #ставим спрайт слева от платформы
                object.rect.right = platform.rect.left
            elif object.x_velocity < 0: # Если спрайт движется влево
                #ставим спрайт справа от платформы
                object.rect.left = platform.rect.right

def check_v_collision_platforms(object, platform_list):
    for platform in platform_list:
        if object.rect.colliderect(platform.rect):
            object.y_velocity = 0.6
            if object.x_velocity > 0: # Если спрайт движется вправо
                #ставим спрайт слева от платформы
                object.rect.right = platform.rect.left
            elif object.x_velocity < 0: # Если спрайт движется влево
                #ставим спрайт справа от платформы
                object.rect.left = platform.rect.right

#функция проверки коллизии выбранного объекта с объектами Enemies
def check_collision_enemies(object, enemies_list):
    #running делаем видимой внутри функции чтобы было возможно
    #завершить игру
    global running
    #в списке проверяем
    for enemy in enemies_list:
        #при коллизии
        if object.rect.colliderect(enemy.rect):
            #объект пропадает из всех групп спрайтов и игра заканчивается
            object.kill()
            running = False

#проверка 
def check_collision_collectibles(object, collectibles_list):
    #делаем видимыми объекты для подбора в игре и очки
    global score
    #если object касается collictible 
    for collectible in collectibles_list:
        if object.rect.colliderect(collectible.rect):
            #убираем этот объект из всех групп
            collectible.kill()
            #убираем этот объект из списка (чтобы не было проверки коллизии)
            collectibles_list.remove(collectible)
            #прибавляем одно очко
            score += 1

def check_collision_energies(object, energies_list, _maxReloadEnergy):
    global speed
    global reload_energy
    for energy in energies_list:
        if object.rect.colliderect(energy.rect):
            energy.kill()
            energies_list.remove(energy)
            if(reload_energy <= 0):
                object.speed = 10
                reload_energy = _maxReloadEnergy
                object.change_image(monkey_crazy)


#создаем экран, счетчик частоты кадров и очков
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
is_music_playing = True

def game():
    global score
    score = 0
    global reload_energy
    reload_energy = 0
    maxReload_energy = 5


#создаем игрока, платформы, врагов и то, что будем собирать в игре
    player = Player(50, 50)
    player_sprite = player.image
    h_platforms_list = [H_Platform(0, HEIGHT-25, WIDTH, 50),H_Platform(50, 150, 100, 20), H_Platform(100, 350, 100, 20), H_Platform(250, 170, 100, 20), H_Platform(750, 180, 400, 20), H_Platform(950, 280, 450, 20), H_Platform(1250, 400, 190, 20), H_Platform(450, 400, 100, 20), H_Platform(500, 650, 350, 20), H_Platform(700, 540, 200, 20), H_Platform(1000, 450, 170, 20)]
    v_platforms_list = [V_Platform(1900, 0, 20, 2 * HEIGHT - 50), V_Platform(0, 0, 20, 2 * HEIGHT - 50)]
    enemies_list = [Enemy(120, 325), Enemy(1300, 255),Enemy(1100,255), Enemy(575,625), Enemy(1300,375)]
    collectibles_list = [Collectible(280, 145), Collectible(150, 325), Collectible(770, 160 ), Collectible(1050, 260 ),Collectible(1150, 260), Collectible(500, 380), Collectible(600, 630)]
    energies_list = [Energy(320, 145), Energy(1000, 260), Energy(550, 630)]

    #счёт игры
    font = pygame.font.Font(None, 36) # создание объекта, выбор размера шрифта
    score_text = font.render("Счёт: 0", True, SCORE_COLOR) # выбор цвета и текст
    score_rect = score_text.get_rect() # создание хитбокса текста
    score_rect.topleft = (WIDTH - 100, 20) # расположение хитбокса\текста на экране

    #создаем групп спрайтов
    player_and_platforms = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    collectibles = pygame.sprite.Group()
    energies = pygame.sprite.Group()

    #в четырех циклах добавляем объекты в соответствующие группы
    for i in enemies_list:
        enemies.add(i)

    for i in h_platforms_list:
        player_and_platforms.add(i)

    for i in v_platforms_list:
        player_and_platforms.add(i)

    for i in collectibles_list:
        collectibles.add(i)

    for i in energies_list:
        energies.add(i)

    #игровой цикл
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        #проверяем нажатие на клавиши для перемещения
        keys = pygame.key.get_pressed()
        player.x_velocity = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.x_velocity = -player.speed
            player_sprite = pygame.transform.flip(player.image, True, False)
            #screen.blit(player.image, player.rect)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.x_velocity = player.speed
            player_sprite = pygame.transform.flip(player.image, False, False)
        #условие прыжка более сложное
        if(keys[pygame.K_SPACE] or reload_energy > 0) and player.on_ground == True:
            player.y_velocity = -9
            player.on_ground = False

        #гравитация для игрока
        player.y_velocity += 0.3 

        # screen.blit(player.image, player.rect)

        #обновляем значения атрибутов игрока и врагов
        player.update()
        enemies.update()

        #отрисовываем фон, платформы, врагов и собираемые предметы
        screen.blit(bg_gameplay, (0, 0))
        
        screen.blit(player_sprite, player.rect)
        player_and_platforms.draw(screen)
        for enemy in enemies:
            screen.blit(enemy.image, enemy.rect)
        collectibles.draw(screen)
        for energy in energies:
            screen.blit(energy.image, energy.rect)

        #проверяем все возможные коллизии
        check_h_collision_platforms(player, h_platforms_list)
        check_v_collision_platforms(player, v_platforms_list)
        check_collision_enemies(player, enemies_list)
        check_collision_collectibles(player, collectibles_list)
        check_collision_energies(player, energies_list, maxReload_energy)

        print(player.y_velocity)

        #уменьшаем перезарядку если есть
        if(reload_energy > 0):
            reload_energy -= 1/60
        elif(reload_energy <= 0):
            player.speed = 5
            player.change_image(monkey_static)


        #обновление счёта на экране
        score_text = font.render("Счёт: " + str(score), True, SCORE_COLOR)
        screen.blit(score_text, score_rect)
        #обновление экрана и установка частоты кадров
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

menu()