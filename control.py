import pygame
import sys
from board  import Board, UiPanel, get_board_number, COLS, ROWS
from player import Player, get_stack_offsets
from dice   import Dice
from pause  import PauseMenu

WIN_TITLE_PATH    = "asset/menu/winner_title.png"
WIN_TITLE_W       = 500
WIN_TITLE_H       = 120
WIN_TITLE_X       = 800
WIN_TITLE_Y       = 80
WIN_PION_X        = 800
WIN_PION_Y        = 380
WIN_PION_W        = 200
WIN_PION_H        = 300
WIN_NAME_X        = 800
WIN_NAME_Y        = 570
WIN_BTN_W         = 260
WIN_BTN_H         = 80
WIN_BTN_MENU_X    = 580
WIN_BTN_MENU_Y    = 720
WIN_BTN_RESTART_X = 1020
WIN_BTN_RESTART_Y = 720
WIN_BG_COLOR      = (255, 255, 255)


# ============================================================

class GameControl:
    def __init__(self, screen, data_game):
        self.screen    = screen
        self.data_game = data_game

        self.board      = Board(screen)
        self.ui_panel   = UiPanel(screen, data_game)
        self.dice       = Dice()
        self.pause_menu = PauseMenu(screen)
        self.players    = self._create_players(data_game)

        self.turn   = 0    
        self.winner = None  

        self.font_win = pygame.font.SysFont("Arial", 42, bold=True)
        self.font_btn = pygame.font.SysFont("Arial", 26, bold=True)
        self._load_win_assets()

    def _create_players(self, data_game):
        return [
            Player(player_id=i + 1, pion_name=data_game["pion"][i])
            for i in range(data_game["jumlah"])
        ]

    def _load_win_assets(self):
        self.win_bg = None

        self.win_title_img = None
        try:
            raw = pygame.image.load(WIN_TITLE_PATH).convert_alpha()
            self.win_title_img = pygame.transform.smoothscale(raw, (WIN_TITLE_W, WIN_TITLE_H))
        except Exception:
            pass

        self.win_btn_menu_rect = pygame.Rect(
            WIN_BTN_MENU_X    - WIN_BTN_W // 2,
            WIN_BTN_MENU_Y    - WIN_BTN_H // 2,
            WIN_BTN_W, WIN_BTN_H)
        self.win_btn_restart_rect = pygame.Rect(
            WIN_BTN_RESTART_X - WIN_BTN_W // 2,
            WIN_BTN_RESTART_Y - WIN_BTN_H // 2,
            WIN_BTN_W, WIN_BTN_H)

        self.win_btn_menu_imgs    = self._load_btn_pair(
            "asset/menu/exit_n.png",  "asset/menu/exit_h.png")
        self.win_btn_restart_imgs = self._load_btn_pair(
            "asset/menu/play_again_n.png", "asset/menu/play_again_h.png")

    def _load_btn_pair(self, path_n, path_h):
        try:
            n = pygame.transform.smoothscale(
                pygame.image.load(path_n).convert_alpha(), (WIN_BTN_W, WIN_BTN_H))
            h = pygame.transform.smoothscale(
                pygame.image.load(path_h).convert_alpha(), (WIN_BTN_W, WIN_BTN_H))
            return (n, h)
        except Exception:
            return None

    # Game Loop

    def run(self):
        clock = pygame.time.Clock()
        while True:
            dt = clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    result = self._handle_pause()
                    if result != "RESUME":
                        return result
                self._handle_event(event)

            result = self._update(dt)
            if result:
                return result

            self._draw()
            pygame.display.flip()

    # Event Handling

    def _handle_pause(self):
        result = self.pause_menu.run()
        return "MENU" if result == "QUIT" else result

    def _handle_event(self, event):
        self._check_roll_click(event)
        self._check_debug_key(event)

    def _check_roll_click(self, event):
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                and self.ui_panel.roll_btn_rect.collidepoint(event.pos)
                and not self.dice.is_rolling):
            self.dice.start_roll()

    def _check_debug_key(self, event):
        if event.type != pygame.KEYDOWN or event.key != pygame.K_w:
            return
        player = self.players[self.turn]
        player.move_to(100)
        self.ui_panel.players[self.turn]["cell"] = 100
        if self.winner is None:
            self.winner = player
        self._advance_turn()

    # Update Logika

    def _update(self, dt):
        result = self.dice.update(dt)
        if result is None:
            return None
        self._process_turn(result)
        return self._check_game_over()

    def _process_turn(self, dice_value):
        player = self.players[self.turn]

        target = player.cell + dice_value
        if target > 100:
            target = 100 - (target - 100)
            print(f"[LOG] Player {player.player_id} memantul ke kotak {target}")
        player.move_to(target)

        after_trap = self.board.check_trap(player.cell)
        if after_trap != player.cell:
            player.move_to(after_trap)

        self.ui_panel.players[self.turn]["cell"] = player.cell

        if player.cell == 100 and self.winner is None:
            self.winner = player
            print(f"🎉 Player {player.player_id} finish pertama!")

        self._advance_turn()

    def _advance_turn(self):
        original = self.turn
        while True:
            self.turn = (self.turn + 1) % len(self.players)
            if self.players[self.turn].cell < 100:
                break
            if self.turn == original:
                break 

    def _check_game_over(self):
        total_finish = sum(1 for p in self.players if p.cell == 100)
        if total_finish >= len(self.players) - 1 and self.winner is not None:
            print(f"🏆 Game selesai! Pemenang: Player {self.winner.player_id}")
            self._draw()
            pygame.display.flip()
            return self._show_win_screen(self.winner)
        return None

    # Draw

    def _draw(self):
        self.board.draw()
        self._draw_players()
        self.dice.draw(self.screen)
        self.ui_panel.draw(self.dice.is_rolling, self.turn)

    def _draw_players(self):
        cell_groups = {}
        for player in self.players:
            cell_groups.setdefault(player.cell, []).append(player)

        for cell_num, group in cell_groups.items():
            cx, cy    = self.board.get_position(cell_num)
            positions = get_stack_offsets(len(group), cx, cy)
            for player, (px, py) in zip(group, positions):
                player.draw(self.screen, px, py)

    # Win Screen

    def _show_win_screen(self, winner):
        clock    = pygame.time.Clock()
        pion_img = self._load_winner_pion(winner)
        name_img = self._load_winner_name(winner)

        while True:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.win_btn_menu_rect.collidepoint(mouse):
                        return "MENU"
                    if self.win_btn_restart_rect.collidepoint(mouse):
                        return "RESTART"

            self._draw_win_screen(mouse, pion_img, name_img, winner)
            pygame.display.flip()
            clock.tick(60)

    def _load_winner_pion(self, winner):
        try:
            raw = pygame.image.load(f"asset/pawn/{winner.pion_name}_n.png").convert_alpha()
            return pygame.transform.smoothscale(raw, (WIN_PION_W, WIN_PION_H))
        except Exception:
            return None

    def _load_winner_name(self, winner):
        try:
            raw = pygame.image.load(f"asset/win/player{winner.player_id}.png").convert_alpha()
            return pygame.transform.smoothscale(raw, (220, 70))
        except Exception:
            return None

    def _draw_win_screen(self, mouse, pion_img, name_img, winner):
        if self.win_bg:
            self.screen.blit(self.win_bg, (0, 0))
        else:
            self.screen.fill(WIN_BG_COLOR)

        if self.win_title_img:
            self.screen.blit(self.win_title_img,
                self.win_title_img.get_rect(center=(WIN_TITLE_X, WIN_TITLE_Y)))
        else:
            ts = self.font_win.render("WINNER!", True, (255, 220, 50))
            self.screen.blit(ts, ts.get_rect(center=(WIN_TITLE_X, WIN_TITLE_Y)))

        if pion_img:
            self.screen.blit(pion_img, pion_img.get_rect(center=(WIN_PION_X, WIN_PION_Y)))

        if name_img:
            self.screen.blit(name_img, name_img.get_rect(center=(WIN_NAME_X, WIN_NAME_Y)))
        else:
            ns = self.font_win.render(
                f"Player {winner.player_id} ({winner.pion_name})", True, (50, 50, 50))
            self.screen.blit(ns, ns.get_rect(center=(WIN_NAME_X, WIN_NAME_Y)))

        self._draw_win_button(self.win_btn_menu_rect,    self.win_btn_menu_imgs,
                               mouse, "Menu",      (72, 187, 55))
        self._draw_win_button(self.win_btn_restart_rect, self.win_btn_restart_imgs,
                               mouse, "Main Lagi", (220, 160, 40))

    def _draw_win_button(self, rect, imgs, mouse, label, color):
        hovered = rect.collidepoint(mouse)
        if imgs:
            self.screen.blit(imgs[1] if hovered else imgs[0], rect)
        else:
            r, g, b = color
            c = (max(r - 40, 0), max(g - 40, 0), max(b - 40, 0)) if hovered else color
            pygame.draw.rect(self.screen, c, rect, border_radius=14)
            ls = self.font_btn.render(label, True, (255, 255, 255))
            self.screen.blit(ls, ls.get_rect(center=rect.center))