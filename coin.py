#класс для поднимаемых предметов
import pygame
from const import*

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        #создание изображения для спрайта
        self.image = coin

        #создание хитбокса для спрайта
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y