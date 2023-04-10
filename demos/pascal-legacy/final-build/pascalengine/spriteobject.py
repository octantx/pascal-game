import pygame

class SpriteObject:
    def __init__(self, game, path='final-build/assets/sprites/targetnothit.png', pos=(75, 2, 65)):
        self.game = game
        self.player = game.player
        self.x, self.y, self.z = pos
        self.image = pygame.image.load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2
        
    def get_sprite(self):
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        dz = self.z - self.player.z
        
    
    def update(self):
        self.get_sprite()
        