import pygame

BOARD_IMAGE_PATH = "asset/board/board.png"
SCREEN_W         = 1600
SCREEN_H         = 900
COLS             = 10
ROWS             = 10
GRID_START_X     = 73
GRID_START_Y     = 873
CELL_W           = 88
CELL_H           = 85

ROLL_BTN_X   = 1340
ROLL_BTN_Y   = 335
ROLL_BTN_W   = 83
ROLL_BTN_H   = 146
TURN_PION_X  = 1110
TURN_PION_Y  = 145
PION_SIZE    = 48
LB_X         = 1100
LB_Y_START   = 550
LB_ROW_H     = 72
LB_PION_SIZE = 36

COLOR_ROLL_BG       = (90, 90, 90)
COLOR_ROLL_HOVER    = (110, 110, 110)
COLOR_ROLL_DISABLED = (60, 60, 60)
COLOR_ROLL_TEXT     = (255, 255, 255)
COLOR_TEXT_MAIN     = (255, 255, 255)
COLOR_TEXT_SUB      = (180, 180, 180)


# ============================================================

def get_cell_center(col, row):
    x = GRID_START_X + col * CELL_W + CELL_W // 2
    y = GRID_START_Y - row * CELL_H - CELL_H // 2
    return x, y


def get_board_number(col, row, cols=COLS):
    if row % 2 == 0:
        return row * cols + col + 1
    return row * cols + (cols - col)


# ============================================================

class Board:
    TRAPS = {
        4: 25, 13: 46, 42: 63, 50: 69, 62: 81, 74: 92, #tangga

        27: 5, 40: 3, 54: 31, 75: 45, 89: 53, 99: 41, #ular
    }

    def __init__(self, screen):
        self.screen = screen
        self.cell_positions = self._build_cell_map()
        self.board_img, self.has_board = self._load_image()

    def _build_cell_map(self):
        positions = {}
        for r in range(ROWS):
            for c in range(COLS):
                num = get_board_number(c, r)
                positions[num] = get_cell_center(c, r)
        return positions

    def _load_image(self):
        try:
            img = pygame.image.load(BOARD_IMAGE_PATH).convert()
            return pygame.transform.smoothscale(img, (SCREEN_W, SCREEN_H)), True
        except Exception as e:
            print(f"[WARNING] Gambar papan tidak ditemukan: {e}")
            return None, False

    def get_position(self, cell_number):
        return self.cell_positions.get(cell_number, self.cell_positions[1])

    def check_trap(self, cell):
        if cell not in self.TRAPS:
            return cell
        target = self.TRAPS[cell]
        if target > cell:
            print(f"[LOG] Tangga! Kotak {cell} → {target} 🚀")
        else:
            print(f"[LOG] Ular!   Kotak {cell} → {target} 🐍")
        return target

    def draw(self):
        if self.has_board:
            self.screen.blit(self.board_img, (0, 0))
        else:
            self._draw_placeholder()

    def _draw_placeholder(self):
        font = pygame.font.SysFont("Arial", 13)
        self.screen.fill((30, 30, 50))
        for r in range(ROWS):
            for c in range(COLS):
                cx, cy = get_cell_center(c, r)
                rect = pygame.Rect(cx - CELL_W // 2, cy - CELL_H // 2, CELL_W, CELL_H)
                color = (60, 80, 100) if (r + c) % 2 == 0 else (50, 65, 85)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (100, 130, 160), rect, 1)
                ns = font.render(str(get_board_number(c, r)), True, (180, 200, 220))
                self.screen.blit(ns, ns.get_rect(center=(cx, cy)))


# ============================================================

class UiPanel:

    def __init__(self, screen, data_game):
        self.screen = screen
        self._init_fonts()
        self._init_players(data_game)
        self._load_pion_assets()
        self._init_roll_button()

    def _init_fonts(self):
        self.font_name  = pygame.font.SysFont("Arial", 22, bold=True)
        self.font_rank  = pygame.font.SysFont("Arial", 16, bold=True)
        self.font_label = pygame.font.SysFont("Arial", 15)

    def _init_players(self, data_game):
        self.current_turn = 0
        self.players = [
            {"name": f"Player {i + 1}", "pion": data_game["pion"][i], "cell": 1}
            for i in range(data_game["jumlah"])
        ]

    def _load_pion_assets(self):
        self.pion_turn_images = self._load_pion_images(PION_SIZE)
        self.pion_lb_images   = self._load_pion_images(LB_PION_SIZE)

    def _load_pion_images(self, size):
        images = {}
        for p in self.players:
            name = p["pion"]
            if name in images:
                continue
            try:
                img = pygame.image.load(f"asset/board/{name}_profile.png").convert_alpha()
                images[name] = pygame.transform.smoothscale(img, (size, size))
            except Exception as e:
                print(f"[WARNING] Pion '{name}' tidak ditemukan: {e}")
                surf = pygame.Surface((size, size), pygame.SRCALPHA)
                pygame.draw.circle(surf, (100, 200, 100), (size // 2, size // 2), size // 2)
                images[name] = surf
        return images

    def _init_roll_button(self):
        self.roll_btn_rect = pygame.Rect(
            ROLL_BTN_X - ROLL_BTN_W // 2,
            ROLL_BTN_Y - ROLL_BTN_H // 2,
            ROLL_BTN_W, ROLL_BTN_H
        )

    def draw(self, is_dice_rolling, current_turn):
        """Gambar seluruh panel UI ke layar."""
        self.current_turn = current_turn
        mouse = pygame.mouse.get_pos()
        self._draw_player_turn()
        self._draw_roll_button(mouse, is_dice_rolling)
        self._draw_leaderboard()

    def _draw_player_turn(self):
        p   = self.players[self.current_turn]
        img = self.pion_turn_images.get(p["pion"])
        x   = TURN_PION_X

        if img:
            rect = img.get_rect(midleft=(x, TURN_PION_Y))
            self.screen.blit(img, rect)
            x = rect.right + 10

        try:
            name_img = pygame.image.load(
                f"asset/board/player{self.current_turn + 1}.png").convert_alpha()
            name_img = pygame.transform.smoothscale(name_img, (140, 55))
            self.screen.blit(name_img, name_img.get_rect(midleft=(x, TURN_PION_Y)))
        except Exception:
            ns = self.font_name.render(p["name"], True, COLOR_TEXT_MAIN)
            self.screen.blit(ns, ns.get_rect(midleft=(x, TURN_PION_Y)))

    def _draw_roll_button(self, mouse, is_rolling):
        try:
            path = "asset/board/roll_h.png" if (
                self.roll_btn_rect.collidepoint(mouse) and not is_rolling
            ) else "asset/board/roll_n.png"
            img = pygame.transform.smoothscale(
                pygame.image.load(path).convert_alpha(), (ROLL_BTN_W, ROLL_BTN_H))
            self.screen.blit(img, img.get_rect(center=(ROLL_BTN_X, ROLL_BTN_Y)))
        except Exception:
            hover = self.roll_btn_rect.collidepoint(mouse) and not is_rolling
            color = (COLOR_ROLL_DISABLED if is_rolling
                     else COLOR_ROLL_HOVER if hover
                     else COLOR_ROLL_BG)
            pygame.draw.rect(self.screen, color, self.roll_btn_rect, border_radius=25)
            rs = self.font_name.render("Roll", True, COLOR_ROLL_TEXT)
            self.screen.blit(rs, rs.get_rect(center=self.roll_btn_rect.center))

    def _draw_leaderboard(self):
        sorted_players = sorted(self.players, key=lambda p: p["cell"], reverse=True)
        for rank, p in enumerate(sorted_players):
            y = LB_Y_START + rank * LB_ROW_H
            x = LB_X

            img = self.pion_lb_images.get(p["pion"])
            if img:
                rect = img.get_rect(midleft=(x, y))
                self.screen.blit(img, rect)
                x = rect.right + 8

            try:
                idx      = int(p["name"].split(" ")[1])
                name_img = pygame.image.load(f"asset/board/player{idx}.png").convert_alpha()
                name_img = pygame.transform.smoothscale(name_img, (100, 38))
                self.screen.blit(name_img, name_img.get_rect(midleft=(x, y)))
            except Exception:
                ns = self.font_label.render(p["name"], True, COLOR_TEXT_MAIN)
                self.screen.blit(ns, ns.get_rect(midleft=(x, y)))

            cs = self.font_label.render(f"#{p['cell']}", True, COLOR_TEXT_SUB)
            self.screen.blit(cs, cs.get_rect(midright=(SCREEN_W - 20, y)))