import pygame
import sys
from menu    import Menu
from control import GameControl

SCREEN_W = 1600
SCREEN_H = 900
FPS      = 60
TITLE    = "Game Ular Tangga"


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption(TITLE)
        self.clock  = pygame.time.Clock()
        self.menu   = Menu(self.screen)

    def run(self):
        while True:
            action = self.menu.run()
            if action == "PLAY":
                self._run_game()
                self.menu = Menu(self.screen) 
            elif action == "QUIT":
                self._quit()
            self.clock.tick(FPS)

    def _run_game(self):
        data_game = {
            "jumlah": self.menu.jumlah_pemain,
            "pion":   self.menu.pilihan_pion,
        }
        print(f"[LOG] Memulai game: {data_game}")

        while True:
            game    = GameControl(self.screen, data_game)
            result  = game.run()

            if result == "RESTART":
                continue        
            elif result == "QUIT":
                self._quit()
            else:               
                return

    def _quit(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Main().run()