import pygame
import math

PAWN_W        = 40
PAWN_H        = 60
STACK_RADIUS  = 15  

FALLBACK_COLORS = {
    1: (220, 60,  60),
    2: (60,  160, 220),
    3: (60,  200, 90),
    4: (220, 180, 50),
}


# ============================================================

class Player:
    def __init__(self, player_id, pion_name):
        self.player_id = player_id  
        self.pion_name = pion_name  
        self.cell      = 1           
        self.image     = self._load_image()

    def _load_image(self):
        try:
            img = pygame.image.load(f"asset/pawn/{self.pion_name}_n.png").convert_alpha()
            return pygame.transform.smoothscale(img, (PAWN_W, PAWN_H))
        except Exception as e:
            print(f"[WARNING] Pion '{self.pion_name}' tidak ditemukan: {e}")
            return self._make_fallback()

    def _make_fallback(self):
        surf  = pygame.Surface((PAWN_W, PAWN_H), pygame.SRCALPHA)
        color = FALLBACK_COLORS.get(self.player_id, (200, 200, 200))
        pygame.draw.rect(surf, color, (0, 0, PAWN_W, PAWN_H), border_radius=8)
        font  = pygame.font.SysFont("Arial", 14, bold=True)
        label = font.render(str(self.player_id), True, (255, 255, 255))
        surf.blit(label, label.get_rect(center=(PAWN_W // 2, PAWN_H // 2)))
        return surf

    def move_to(self, cell_number):
        self.cell = max(1, min(100, cell_number))

    def draw(self, screen, pixel_x, pixel_y):
        rect = self.image.get_rect(midbottom=(pixel_x, pixel_y + PAWN_H // 2))
        screen.blit(self.image, rect)


# ============================================================

def get_stack_offsets(total_players, cx, cy):
    if total_players == 1:
        return [(cx, cy)]

    return [
        (
            cx + int(STACK_RADIUS * math.cos(math.radians(-90 + (360 / total_players) * i))),
            cy + int(STACK_RADIUS * math.sin(math.radians(-90 + (360 / total_players) * i))),
        )
        for i in range(total_players)
    ]