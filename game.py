import pygame
import random

pygame.init()

WIDTH, HEIGHT = 500, 700

screen = pygame.Surface((WIDTH, HEIGHT))

# Images
road_img = pygame.image.load(r"assets/road.png")
player_img = pygame.transform.scale(
    pygame.image.load(r"assets/car.jpg"), (60, 100)
)

enemy_img = pygame.transform.scale(
    pygame.image.load(r"assets/enemy.gif"), (60, 100)
)

fuel_img = pygame.transform.scale(
    pygame.image.load(r"assets/fuel.png"), (40, 40)
)

font = pygame.font.SysFont(None, 36)


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed


class Player(GameSprite):
    def __init__(self):
        super().__init__(player_img, 220, 550, 0)
        self.move_speed = 6

    def move_left(self):
        if self.rect.x > 100:
            self.rect.x -= self.move_speed

    def move_right(self):
        if self.rect.x < 340:
            self.rect.x += self.move_speed


class Enemy(GameSprite):
    def __init__(self):
        x = random.randint(100, 340)
        super().__init__(enemy_img, x, -100, 6)

    def update(self):
        super().update()
        if self.rect.y > HEIGHT:
            self.reset()

    def reset(self):
        self.rect.y = -100
        self.rect.x = random.randint(100, 340)


class Fuel(GameSprite):
    def __init__(self):
        x = random.randint(100, 360)
        super().__init__(fuel_img, x, -200, 5)

    def update(self):
        super().update()

        if self.rect.y > HEIGHT:
            self.reset()

    def reset(self):
        self.rect.y = -200
        self.rect.x = random.randint(100, 360)


player = Player()
enemy = Enemy()
fuel = Fuel()

all_sprites = pygame.sprite.Group(player, enemy, fuel)
enemy_group = pygame.sprite.Group(enemy)
fuel_group = pygame.sprite.Group(fuel)

scroll = 0
score = 0


def update_game(keys):

    global scroll, score

    if "left" in keys:
        player.move_left()

    if "right" in keys:
        player.move_right()

    scroll += 5

    if scroll >= HEIGHT:
        scroll = 0

    screen.blit(road_img, (0, scroll - HEIGHT))
    screen.blit(road_img, (0, scroll))

    all_sprites.update()

    if pygame.sprite.spritecollide(player, enemy_group, False):
        score = 0
        enemy.reset()

    if pygame.sprite.spritecollide(player, fuel_group, False):
        score += 1
        fuel.reset()

    all_sprites.draw(screen)

    text = font.render(f"Fuel: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    return screen