import pygame
import random

DICE_X             = 1209
DICE_Y             = 337
DICE_SIZE          = 114
DICE_ANIM_DURATION = 1200   # ms total animasi
DICE_ANIM_FAST     = 40     # ms per frame awal
DICE_ANIM_SLOW     = 180    # ms per frame akhir


# ============================================================

class Dice:

    def __init__(self):
        self.dice_value     = 1
        self.is_rolling     = False
        self.anim_elapsed   = 0
        self.anim_timer     = 0
        self.anim_frame_idx = 0
        self.anim_interval  = DICE_ANIM_FAST
        self.dice_images    = self._load_images()

    def _load_images(self):
        images = {}
        for i in range(1, 7):
            try:
                img = pygame.image.load(f"asset/dice/dice_{i}.png").convert_alpha()
                images[i] = pygame.transform.smoothscale(img, (DICE_SIZE, DICE_SIZE))
            except Exception:
                images[i] = self._make_fallback(i)
        return images

    def _make_fallback(self, value):
        surf = pygame.Surface((DICE_SIZE, DICE_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 255, 255), (0, 0, DICE_SIZE, DICE_SIZE), border_radius=12)
        pygame.draw.rect(surf, (30, 30, 30),    (0, 0, DICE_SIZE, DICE_SIZE), 2, border_radius=12)
        dot_map = {
            1: [(57, 57)],
            2: [(30, 30), (84, 84)],
            3: [(30, 30), (57, 57), (84, 84)],
            4: [(30, 30), (84, 30), (30, 84), (84, 84)],
            5: [(30, 30), (84, 30), (57, 57), (30, 84), (84, 84)],
            6: [(30, 30), (84, 30), (30, 57), (84, 57), (30, 84), (84, 84)],
        }
        for dx, dy in dot_map.get(value, []):
            pygame.draw.circle(surf, (20, 20, 20), (dx, dy), 10)
        return surf

    def start_roll(self):
        if self.is_rolling:
            return
        self.is_rolling     = True
        self.anim_elapsed   = 0
        self.anim_timer     = 0
        self.anim_interval  = DICE_ANIM_FAST

    def update(self, dt):
        if not self.is_rolling:
            return None

        self.anim_elapsed += dt
        self.anim_timer   += dt

        progress = self.anim_elapsed / DICE_ANIM_DURATION
        self.anim_interval = int(
            DICE_ANIM_FAST + (DICE_ANIM_SLOW - DICE_ANIM_FAST) * (progress ** 2)
        )

        if self.anim_timer >= self.anim_interval:
            self.anim_timer     = 0
            self.anim_frame_idx = random.randint(0, 5)

        if self.anim_elapsed >= DICE_ANIM_DURATION:
            self.dice_value = random.randint(1, 6)
            self.is_rolling = False
            return self.dice_value

        return None

    def draw(self, screen):
        img_key = (self.anim_frame_idx + 1) if self.is_rolling else self.dice_value
        img     = self.dice_images.get(img_key)
        if img:
            screen.blit(img, img.get_rect(center=(DICE_X, DICE_Y)))