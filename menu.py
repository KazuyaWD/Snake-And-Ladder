import pygame

class Button:
    def __init__(self, x, y, width, height, img_normal_path, img_hover_path):
        self.img_n = pygame.transform.smoothscale(pygame.image.load(img_normal_path).convert_alpha(), (width, height))
        self.img_h = pygame.transform.smoothscale(pygame.image.load(img_hover_path).convert_alpha(), (width, height))
        self.rect = self.img_n.get_rect(center=(x, y))

    def draw(self, screen, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            screen.blit(self.img_h, self.rect)
        else:
            screen.blit(self.img_n, self.rect)

    def is_clicked(self, mouse_pos, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(mouse_pos)

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.center_x = 1600 // 2
        self.state = "MAIN" 
        
        self.jumlah_pemain = 0
        self.pilihan_pion = [] 

        self.bg_img = pygame.image.load("asset/menu/bg.png").convert()
        self.bg_img = pygame.transform.smoothscale(self.bg_img, (1600, 900))
        self._setup_judul()
        self._setup_buttons()

    def _setup_judul(self):
        try:
            img = pygame.image.load("asset/menu/judul.png").convert_alpha()
            w, h = img.get_size()
            self.img_judul = pygame.transform.smoothscale(img, (1000, int(1000 * (h/w))))
            self.judul_rect = self.img_judul.get_rect(midtop=(self.center_x, 10))
            self.has_judul_img = True
        except:
            self.has_judul_img = False
            
        try:
            img_sp = pygame.image.load("asset/menu/select_player.png").convert_alpha()
            w_sp, h_sp = img_sp.get_size()
            self.img_select_player = pygame.transform.smoothscale(img_sp, (500, int(500 * (h_sp/w_sp))))
            self.rect_select_player = self.img_select_player.get_rect(center=(450, 160))
            self.has_select_player_img = True
        except:
            self.has_select_player_img = False
            
        try:
            img_sp = pygame.image.load("asset/menu/select_pawn.png").convert_alpha()
            w_sp, h_sp = img_sp.get_size()
            self.img_select_pawn = pygame.transform.smoothscale(img_sp, (500, int(500 * (h_sp/w_sp))))
            self.rect_select_pawn = self.img_select_pawn.get_rect(center=(450, 160))
            self.has_select_pawn_img = True
        except:
            self.has_select_pawn_img = False
        
        try:
            img_sp = pygame.image.load("asset/menu/ready.png").convert_alpha()
            w_sp, h_sp = img_sp.get_size()
            self.img_ready = pygame.transform.smoothscale(img_sp, (700, int(700 * (h_sp/w_sp))))
            self.rect_ready = self.img_ready.get_rect(center=(self.center_x, 150))
            self.has_ready_img = True
        except:
            self.has_ready_img = False

    def _setup_buttons(self):
        self.btn_play = Button(self.center_x, 630, 300, 100, "asset/menu/play_n.png", "asset/menu/play_h.png")
        self.btn_exit = Button(self.center_x, 750, 300, 100, "asset/menu/exit_n.png", "asset/menu/exit_h.png")
        self.btn_back = Button(150, 50, 170, 60, "asset/menu/back_n.png", "asset/menu/back_h.png")
        self.btn_start = Button(1400, 800, 220, 60, "asset/menu/start_n.png", "asset/menu/start_h.png")
        
        self.btns_angka = []
        for i, num in enumerate([2, 3, 4]):
            y_pos = 300 + (i * 160)
            btn = Button(450, y_pos, 200, 70, f"asset/menu/{num}_n.png", f"asset/menu/{num}_h.png")
            self.btns_angka.append(btn)
        
        self.btns_pion = []
        pion_names = ["phoenix", "horse", "dragon", "hydra"]
        for i, name in enumerate(pion_names):
            y_pos = 250 + (i * 150)
            btn = Button(450, y_pos, 200, 70, f"asset/menu/{name}_n.png", f"asset/menu/{name}_h.png")
            self.btns_pion.append(btn)
            
    def run(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "QUIT"

            if self.state != "MAIN" and self.btn_back.is_clicked(mouse_pos, event):
                if self.state == "SELECT_PLAYER": self.state = "MAIN"
                elif self.state == "SELECT_PAWN": 
                    self.pilihan_pion = []
                    self.state = "SELECT_PLAYER"
                elif self.state == "READY":
                    self.pilihan_pion = []
                    self.state = "SELECT_PAWN"

            if self.state == "MAIN":
                if self.btn_play.is_clicked(mouse_pos, event): self.state = "SELECT_PLAYER"
                if self.btn_exit.is_clicked(mouse_pos, event): return "QUIT"
            
            elif self.state == "SELECT_PLAYER":
                for i, btn in enumerate(self.btns_angka):
                    if btn.is_clicked(mouse_pos, event):
                        self.jumlah_pemain = i + 2
                        self.state = "SELECT_PAWN"

            elif self.state == "SELECT_PAWN":
                pion_names = ["phoenix", "horse", "dragon", "hydra"]
                for i, btn in enumerate(self.btns_pion):
                    if btn.is_clicked(mouse_pos, event):
                        pilihan = pion_names[i]

                        if pilihan not in self.pilihan_pion:
                            self.pilihan_pion.append(pilihan)
                        if len(self.pilihan_pion) == self.jumlah_pemain:
                                self.state = "READY"
            
            elif self.state == "READY":
                if self.btn_start.is_clicked(mouse_pos, event):
                    return "PLAY"
                
        # --- DRAWING ---
        self.screen.blit(self.bg_img, (0, 0))
        
        if self.state != "MAIN":
            self.btn_back.draw(self.screen, mouse_pos)

        if self.state == "MAIN":
            if self.has_judul_img: self.screen.blit(self.img_judul, self.judul_rect)
            self.btn_play.draw(self.screen, mouse_pos)
            self.btn_exit.draw(self.screen, mouse_pos)
        elif self.state == "SELECT_PLAYER": 
            self._draw_select_player()
        elif self.state == "SELECT_PAWN": 
            self._draw_select_pawn()
        elif self.state == "READY":
            self._draw_ready_screen()
        
        pygame.display.flip()
        return "STAY"

    def _handle_player_selection(self, pos):
        if 400 < pos[1] < 500:
            if 325 < pos[0] < 475: self.jumlah_pemain = 2
            elif 565 < pos[0] < 715: self.jumlah_pemain = 3
            elif 805 < pos[0] < 955: self.jumlah_pemain = 4
            return self.jumlah_pemain > 0
        return False

    def _draw_select_player(self):
        if self.has_select_player_img:
            self.screen.blit(self.img_select_player, self.rect_select_player)
        else:
            self._draw_text("SELECT PLAYER", 60, (self.center_x, 150))
            
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.btns_angka:
            btn.draw(self.screen, mouse_pos)
            
    def _draw_select_pawn(self):
        if self.has_select_pawn_img:
            self.screen.blit(self.img_select_pawn, self.rect_select_pawn)
            
        p_idx = len(self.pilihan_pion) + 1
        try:
            img_player = pygame.image.load(f"asset/menu/player_{p_idx}.png").convert_alpha()
            img_player = pygame.transform.smoothscale(img_player, (200, 75)) 
            self.screen.blit(img_player, img_player.get_rect(center=(1200, 250)))
        except:
            self._draw_text(f"PLAYER {p_idx} CHOOSE", 40, (self.center_x, 250))

        mouse_pos = pygame.mouse.get_pos()
        pion_names = ["phoenix", "horse", "dragon", "hydra"]
        for i, btn in enumerate(self.btns_pion):
            if btn.rect.collidepoint(mouse_pos):
                try:
                    char_preview = pygame.image.load(f"asset/pawn/{pion_names[i]}_n.png").convert_alpha()
                    char_preview = pygame.transform.smoothscale(char_preview, (200, 300))
                    preview_rect = char_preview.get_rect(center=(1200, 450))
                    self.screen.blit(char_preview, preview_rect)
                except:
                    pass
                
        for btn in self.btns_pion:
            btn.draw(self.screen, mouse_pos)
    
    def _draw_ready_screen(self):
        if self.has_ready_img:
            self.screen.blit(self.img_ready, self.rect_ready)
        start_x = self.center_x - ((self.jumlah_pemain - 1) * 175)
        
        for i in range(self.jumlah_pemain):
            x_pos = start_x + (i * 350)
            
            try:
                img_p = pygame.image.load(f"asset/menu/player_{i+1}.png").convert_alpha()
                img_p = pygame.transform.smoothscale(img_p, (140, 55))
                self.screen.blit(img_p, img_p.get_rect(center=(x_pos, 250)))
            except:
                self._draw_text(f"PLAYER {i+1}", 30, (x_pos, 220), (255, 255, 255))
                
            pion_terpilih = self.pilihan_pion[i]
            try:
                img_pion = pygame.image.load(f"asset/pawn/{pion_terpilih}_n.png").convert_alpha()
                img_pion = pygame.transform.smoothscale(img_pion, (200, 300))
                self.screen.blit(img_pion, img_pion.get_rect(center=(x_pos, 500)))
            except:
                self._draw_text(pion_terpilih.upper(), 25, (x_pos, 380), (200, 200, 200))
                
        mouse_pos = pygame.mouse.get_pos()
        self.btn_start.draw(self.screen, mouse_pos)

    def _draw_text(self, text, size, pos, color=(0, 0, 0)):
        font = pygame.font.SysFont("Arial", size, bold=True)
        surf = font.render(text, True, color)
        self.screen.blit(surf, surf.get_rect(center=pos))