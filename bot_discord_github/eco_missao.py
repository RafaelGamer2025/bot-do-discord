import pygame
import random
import sys
import os

# --- Configurações ---
WIDTH, HEIGHT = 800, 600
FPS = 60

# Cores para o Plano B (Fallback)
DIRTY_SKY = (100, 110, 120)
CLEAN_SKY = (135, 206, 235)
DIRTY_GROUND = (80, 70, 60)
CLEAN_GROUND = (34, 139, 34)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def load_image(name, width, height, color):
    """
    Plano A: Tenta carregar a imagem do disco.
    Plano B: Se falhar, cria uma imagem colorida em memória.
    """
    path = os.path.join('images', name)
    try:
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, (width, height))
    except Exception as e:
        print(f"Erro ao carregar {name}: {e}")
    
    # Plano B: Gerar imagem procedural
    surf = pygame.Surface((width, height))
    surf.fill(color)
    if name == "lixo.png":
        pygame.draw.rect(surf, (100, 50, 0), [5, 5, 10, 10]) # Detalhe no lixo
    elif name == "player.png":
        pygame.draw.circle(surf, WHITE, (width//2, height//4), 5) # Olhos
    return surf

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("player.png", 40, 60, (50, 150, 255))
        self.rect = self.image.get_rect(midbottom=(100, HEIGHT - 50))
        self.vel = pygame.math.Vector2(0, 0)
        self.speed = 6
        self.jump_power = -16
        self.on_ground = False

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        self.vel.x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel.x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel.x = self.speed

        # Movimento X
        self.rect.x += self.vel.x
        self.check_collision(platforms, 'x')

        # Movimento Y (Gravidade)
        self.vel.y += 0.8
        self.rect.y += self.vel.y
        self.on_ground = False
        self.check_collision(platforms, 'y')

    def check_collision(self, platforms, direction):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        for hit in hits:
            if direction == 'x':
                if self.vel.x > 0: self.rect.right = hit.rect.left
                elif self.vel.x < 0: self.rect.left = hit.rect.right
            else:
                if self.vel.y > 0:
                    self.rect.bottom = hit.rect.top
                    self.vel.y = 0
                    self.on_ground = True
                elif self.vel.y < 0:
                    self.rect.top = hit.rect.bottom
                    self.vel_y = 0

    def jump(self):
        if self.on_ground:
            self.vel.y = self.jump_power

class Trash(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image("lixo.png", 30, 30, (150, 75, 0))
        self.rect = self.image.get_rect(center=(x, y))

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Eco-Missão PRO: Híbrido")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 28, bold=True)

    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    trash_group = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    # Chão
    ground = Platform(0, HEIGHT - 40, WIDTH, 40, DIRTY_GROUND)
    platforms.add(ground)
    all_sprites.add(ground)

    # Plataformas extras
    p1 = Platform(200, 400, 150, 20, (100, 100, 100))
    p2 = Platform(450, 300, 150, 20, (100, 100, 100))
    platforms.add(p1, p2)
    all_sprites.add(p1, p2)

    # Gerar lixo
    total_trash = 15
    for _ in range(total_trash):
        t = Trash(random.randint(50, WIDTH-50), random.randint(100, HEIGHT-100))
        trash_group.add(t)
        all_sprites.add(t)

    score = 0
    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_SPACE, pygame.K_w, pygame.K_UP]:
                    player.jump()

        all_sprites.update(platforms)

        # Coleta
        collected = pygame.sprite.spritecollide(player, trash_group, True)
        score += len(collected)

        # Evolução Visual (Interpolação de Cores)
        progress = score / total_trash
        current_sky = [int(DIRTY_SKY[i] + (CLEAN_SKY[i] - DIRTY_SKY[i]) * progress) for i in range(3)]
        current_ground = [int(DIRTY_GROUND[i] + (CLEAN_GROUND[i] - DIRTY_GROUND[i]) * progress) for i in range(3)]
        ground.image.fill(current_ground)

        # Desenho
        screen.fill(current_sky)
        all_sprites.draw(screen)

        # HUD
        hud_bg = pygame.Surface((220, 40))
        hud_bg.set_alpha(150)
        hud_bg.fill(WHITE)
        screen.blit(hud_bg, (10, 10))
        
        score_text = font.render(f"LIMPEZA: {int(progress*100)}%", True, BLACK)
        screen.blit(score_text, (20, 15))
        
        if score == total_trash:
            msg = font.render("MISSÃO CUMPRIDA! O PLANETA AGRADECE!", True, (0, 100, 0))
            screen.blit(msg, (WIDTH//2 - 250, HEIGHT//2))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()