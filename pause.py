import pygame
import sys

BTN_W       = 260
BTN_H       = 80
BTN_GAP     = 20
BTN_START_Y = 380

PANEL_W      = 400
PANEL_H      = 420
TITLE_SIZE   = (495, 71)

OVERLAY_ALPHA  = 140
COLOR_RESUME   = (72,  187, 55)
COLOR_RESTART  = (220, 160, 40)
COLOR_QUIT     = (200, 60,  60)
COLOR_HOVER_DIM = 40
COLOR_TEXT     = (255, 255, 255)

BUTTON_DEFS = [
    ("Resume",  "RESUME",  COLOR_RESUME,  "asset/menu/resume_n.png",     "asset/menu/resume_h.png"),
    ("Restart", "RESTART", COLOR_RESTART, "asset/menu/restart_n.png",    "asset/menu/restart_h.png"),
    ("Quit",    "QUIT",    COLOR_QUIT,    "asset/menu/exit_n.png",   "asset/menu/exit_h.png"),
]


# ============================================================

class PauseMenu:
    def __init__(self, screen):
        self.screen   = screen
        self.center_x = screen.get_width()  // 2
        self.center_y = screen.get_height() // 2

        self.font_title = pygame.font.SysFont("Arial", 42, bold=True)
        self.font_btn   = pygame.font.SysFont("Arial", 26, bold=True)

        self.panel_rect = pygame.Rect(
            self.center_x - PANEL_W // 2,
            self.center_y - PANEL_H // 2,
            PANEL_W, PANEL_H
        )

        self.bg_img, self.use_custom_bg = self._load_background()
        self.title_img                  = self._load_title()
        self.buttons                    = self._build_buttons()

    def _load_background(self):
        try:
            img = pygame.image.load("asset/menu/bg_pause.png").convert()
            bg  = pygame.transform.smoothscale(img, (self.screen.get_width(), self.screen.get_height()))
            return bg, True
        except Exception:
            overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, OVERLAY_ALPHA))
            return overlay, False

    def _load_title(self):
        try:
            raw = pygame.image.load("asset/menu/pause_judul.png").convert_alpha()
            return pygame.transform.smoothscale(raw, TITLE_SIZE)
        except Exception:
            return None

    def _build_buttons(self):
        buttons = []
        for i, (label, action, color, path_n, path_h) in enumerate(BUTTON_DEFS):
            y    = BTN_START_Y + i * (BTN_H + BTN_GAP)
            rect = pygame.Rect(self.center_x - BTN_W // 2, y, BTN_W, BTN_H)
            img_n = img_h = None
            try:
                img_n = pygame.transform.smoothscale(
                    pygame.image.load(path_n).convert_alpha(), (BTN_W, BTN_H))
                img_h = pygame.transform.smoothscale(
                    pygame.image.load(path_h).convert_alpha(), (BTN_W, BTN_H))
            except Exception:
                pass
            buttons.append({"label": label, "action": action,
                             "color": color, "rect": rect,
                             "img_n": img_n, "img_h": img_h})
        return buttons

    def run(self):
        clock = pygame.time.Clock()
        while True:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "RESUME"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for btn in self.buttons:
                        if btn["rect"].collidepoint(mouse):
                            return btn["action"]
            self._draw(mouse)
            pygame.display.flip()
            clock.tick(60)

    def _draw(self, mouse):
        self.screen.blit(self.bg_img, (0, 0))
        self._draw_title()
        for btn in self.buttons:
            self._draw_button(btn, mouse)

    def _draw_title(self):
        title_y = self.panel_rect.y + 30
        if self.title_img:
            self.screen.blit(self.title_img,
                self.title_img.get_rect(midtop=(self.center_x, title_y)))
        else:
            ts = self.font_title.render("PAUSE", True, COLOR_TEXT)
            self.screen.blit(ts, ts.get_rect(midtop=(self.center_x, title_y)))

    def _draw_button(self, btn, mouse):
        hovered = btn["rect"].collidepoint(mouse)
        if btn["img_n"] and btn["img_h"]:
            self.screen.blit(btn["img_h"] if hovered else btn["img_n"], btn["rect"])
        else:
            r, g, b = btn["color"]
            color   = (max(r - COLOR_HOVER_DIM, 0),
                       max(g - COLOR_HOVER_DIM, 0),
                       max(b - COLOR_HOVER_DIM, 0)) if hovered else btn["color"]
            pygame.draw.rect(self.screen, color, btn["rect"], border_radius=14)
            ls = self.font_btn.render(btn["label"], True, COLOR_TEXT)
            self.screen.blit(ls, ls.get_rect(center=btn["rect"].center))