import pygame
import random
import math
from config import WIDTH, HEIGHT, FPS, CONF, COLOR_BG, COLOR_ARENA_BORDER, TILE_SIZE
from entities import Player, PlayerProjectile, to_screen, to_world, SlashEffect, CrimsonAltar
from boss import Boss

pygame.init()
font_ui = pygame.font.SysFont("Arial", 20, bold=True)
font_big = pygame.font.SysFont("Arial", 60, bold=True)
font_desc = pygame.font.SysFont("Arial", 16)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Crimson Witch: The Altar")
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.state = "HUB"
        self.show_menu = False
        self.altar = CrimsonAltar(0, 0) 
        
        self.player = Player()
        self.boss = Boss()
        self.reset_match()
        self.debug_stats = {
            "start_ticks": 0,
            "attacks_count": 0,
            "blocks_total": 0,
            "potions_used": 0,
            "boss_potions_thrown": 0
        }

    def reset_match(self):
        # Игрок появляется чуть ниже центра
        self.player.x, self.player.y = 0, 6 
        self.player.hp = self.player.max_hp
        self.player.stamina = CONF['STAMINA_MAX']
        self.player.potion_charges = CONF['POTION_CHARGES']
        
        self.boss = Boss()
        
        self.puddles = []
        self.shadow_minions = []
        self.potion_objects = []
        self.blood_spikes = []
        self.projectiles = []
        self.player_projectiles = []
        self.visual_effects = []
        self.floaters = []
        self.shockwave_effect = None
        self.shake = 0

    def start_fight(self):
        # Применяем модификаторы (это внутри метода apply_modifiers сбросит конфиг)
        self.boss.apply_modifiers(self.altar.materials)
    
        # Сброс статистики
        self.debug_stats["start_ticks"] = pygame.time.get_ticks()
        self.debug_stats["attacks_count"] = 0
        self.debug_stats["blocks_total"] = 0
        self.debug_stats["potions_used"] = 0
        self.debug_stats["boss_potions_thrown"] = 0
        
        self.state = "PLAY"
        self.show_menu = False
        self.add_shake(5)

    def add_shake(self, amount): self.shake = min(self.shake + amount, 20)
    
    def add_floater(self, x, y, text, color):
        self.floaters.append({'x': x, 'y': y, 'z': 20, 'text': text, 'color': color, 'life': 60})

    def run(self):
        global WIDTH, HEIGHT
        while self.running:
            self.clock.tick(FPS)
            
            cam_x = random.randint(-int(self.shake), int(self.shake))
            cam_y = random.randint(-int(self.shake), int(self.shake))
            self.shake *= 0.9
            offset = (cam_x, cam_y)

            # --- EVENTS ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.running = False
                elif event.type == pygame.VIDEORESIZE:
                    WIDTH, HEIGHT = event.w, event.h
                    self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                
                elif event.type == pygame.KEYDOWN:
                    if self.state == "HUB":
                        if event.key == pygame.K_e:
                            dist = math.hypot(self.player.x, self.player.y)
                            if dist < 3.0: 
                                self.show_menu = not self.show_menu
                    
                    if event.key == pygame.K_r and self.state in ["WIN", "LOSE"]:
                        self.state = "HUB"
                        self.reset_match()

                    if self.state == "PLAY":
                        if event.key == pygame.K_1: self.player.weapon = "SWORD"; self.add_floater(self.player.x, self.player.y, "Sword", (200, 200, 200))
                        if event.key == pygame.K_2: self.player.weapon = "MACE"; self.add_floater(self.player.x, self.player.y, "Mace", (255, 100, 50))
                        if event.key == pygame.K_3: self.player.weapon = "BOW"; self.add_floater(self.player.x, self.player.y, "Bow", (100, 255, 100))
                        if event.key == pygame.K_6: self.player.use_potion(self)

                elif event.type == pygame.MOUSEBUTTONDOWN and self.show_menu:
                    self.handle_menu_click()

            self.screen.fill(COLOR_BG)
            
            pygame.draw.circle(self.screen, COLOR_ARENA_BORDER, to_screen(0, 0, 0, offset), int(10*TILE_SIZE+40), 2)
            self.altar.draw(self.screen, offset)

            if self.state == "HUB":
                self.player.move(pygame.key.get_pressed())
                self.player.draw(self.screen, offset)
                
                if not self.show_menu:
                    dist = math.hypot(self.player.x, self.player.y)
                    if dist < 3.0:
                        t = font_ui.render("[E] Offer Materials", True, (255, 255, 255))
                        self.screen.blit(t, (WIDTH//2 - t.get_width()//2, HEIGHT - 120))
                else:
                    self.draw_hub_menu()

            elif self.state == "PLAY":
                self.player.handle_input_state(pygame.mouse.get_pressed(), self, self.boss)
                self.player.move(pygame.key.get_pressed())
                self.player.update_logic(self, self.boss)
                
                self.boss.update(self.player, self)
                self.player_projectiles[:] = [p for p in self.player_projectiles if p.update(self.boss, self)]
                self.potion_objects[:] = [p for p in self.potion_objects if p.update(self.boss, self.player, self)]
                self.blood_spikes[:] = [s for s in self.blood_spikes if s.update(self.player, self.boss, self)]
                self.projectiles[:] = [p for p in self.projectiles if p.update(self.player, self)]
                self.visual_effects[:] = [v for v in self.visual_effects if v.update()]
                self.puddles[:] = [pd for pd in self.puddles if pd.update(self.player, self)]
                self.shadow_minions[:] = [m for m in self.shadow_minions if m.update(self.player, self)]
                
                if self.player.hp <= 0: self.game_over(win=False)

                for pd in self.puddles: pd.draw(self.screen, offset)
                for m in self.shadow_minions: m.draw(self.screen, offset)
                for p in self.potion_objects: p.draw(self.screen, offset)
                for s in self.blood_spikes: s.draw(self.screen, offset)
                for pr in self.projectiles: pr.draw(self.screen, offset)
                for proj in self.player_projectiles: proj.draw(self.screen, offset)
                for v in self.visual_effects: v.draw(self.screen, offset)
                
                if self.shockwave_effect:
                    wc = to_screen(self.shockwave_effect['x'], self.shockwave_effect['y'], 0, offset)
                    wr = int(4.5 * TILE_SIZE * self.shockwave_effect['progress'])
                    wa = int(200 * (1.0 - self.shockwave_effect['progress']))
                    ws = pygame.Surface((wr*2, wr*2), pygame.SRCALPHA); pygame.draw.circle(ws, (255, 200, 0, wa), (wr, wr), wr, 5); self.screen.blit(ws, (wc[0]-wr, wc[1]-wr))
                
                self.boss.draw(self.screen, offset)
                self.player.draw(self.screen, offset)
                self.draw_ui_overlay()

            for f in self.floaters[:]:
                f['life'] -= 1; f['z'] += 0.5
                sx, sy = to_screen(f['x'], f['y'], f['z'], offset)
                self.screen.blit(font_ui.render(f['text'], True, f['color']), (sx, sy))
                if f['life'] <= 0: self.floaters.remove(f)

            if self.state in ["WIN", "LOSE"]:
                self.draw_game_over()

            pygame.display.flip()
        pygame.quit()

    def handle_menu_click(self):
        mx, my = pygame.mouse.get_pos()
        start_y = HEIGHT // 2 - 100
        for i in range(1, 6):
            rect = pygame.Rect(WIDTH//2 - 200, start_y + (i-1)*60, 400, 50)
            if rect.collidepoint(mx, my):
                self.altar.toggle_material(i)
                return
        start_btn = pygame.Rect(WIDTH//2 - 100, start_y + 320, 200, 50)
        if start_btn.collidepoint(mx, my):
            self.start_fight()

    def draw_hub_menu(self):
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 230))
        self.screen.blit(s, (0,0))
        title = font_big.render("Crimson Altar", True, (255, 100, 100))
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        
        items = [
            (1, "Vile Heart", "+40% Boss HP", (255, 80, 80)),
            (2, "Strange Dust", "Mist Arena (Danger Zone)", (180, 100, 255)),
            (3, "Witch's Hair", "Fast Throwing (-10% CD)", (100, 255, 255)),
            (4, "Beast Fang", "Aggressive Minions", (100, 255, 100)),
            (5, "Golden Eye", "LEGENDARY: Cauldron Turret", (255, 215, 0))
        ]
        
        start_y = HEIGHT // 2 - 100
        mx, my = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        
        for i, (mid, name, desc, col) in enumerate(items):
            rect = pygame.Rect(WIDTH//2 - 200, start_y + i*60, 400, 50)
            is_active = mid in self.altar.materials
            if rect.collidepoint(mx, my):
                pygame.draw.rect(self.screen, (50, 50, 60), rect)
                if click:
                    self.altar.toggle_material(mid) 
                    pygame.time.delay(150)
            else:
                pygame.draw.rect(self.screen, (30, 30, 35) if not is_active else (50, 20, 20), rect)
            border_col = col if is_active else (80, 80, 80)
            pygame.draw.rect(self.screen, border_col, rect, 2 if is_active else 1)
            name_surf = font_ui.render(name, True, col if is_active else (180, 180, 180))
            desc_surf = font_desc.render(desc, True, (150, 150, 150))
            self.screen.blit(name_surf, (rect.x + 15, rect.y + 12))
            self.screen.blit(desc_surf, (rect.right - 10 - desc_surf.get_width(), rect.y + 15))
            if is_active:
                pygame.draw.circle(self.screen, col, (rect.right - 350, rect.centery), 4)

        start_btn = pygame.Rect(WIDTH//2 - 100, start_y + 320, 200, 50)
        btn_col = (100, 20, 20)
        if start_btn.collidepoint(mx, my):
            btn_col = (140, 40, 40)
            if click: self.start_fight()
        pygame.draw.rect(self.screen, btn_col, start_btn)
        pygame.draw.rect(self.screen, (255, 255, 255), start_btn, 2)
        st_txt = font_ui.render("AWAKEN WITCH", True, (255, 255, 255))
        self.screen.blit(st_txt, (start_btn.centerx - st_txt.get_width()//2, start_btn.centery - st_txt.get_height()//2))

    def draw_ui_overlay(self):
        self.draw_bar(WIDTH//2 - 300, 20, 600, 25, self.boss.hp, self.boss.max_hp, (200, 50, 50), text=f"WITCH: {int(self.boss.hp)}")
        bx, by = 20, HEIGHT - 80 
        self.draw_bar(bx, by, 250, 25, self.player.hp, self.player.max_hp, (50, 200, 50), text=f"HP: {int(self.player.hp)}")
        self.draw_bar(bx, by + 30, 250, 15, self.player.stamina, 100, (255, 200, 0), text=None)
        pot_col = (100, 255, 100) if self.player.potion_charges > 0 else (100, 100, 100)
        self.screen.blit(font_ui.render(f"[6] Heal: {self.player.potion_charges}", True, pot_col), (bx + 260, by))
        self.screen.blit(font_ui.render(f"Weapon: {self.player.weapon}", True, (200,200,200)), (bx, by-30))

    def draw_game_over(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0,0))
        txt = font_big.render("VICTORY!" if self.state == "WIN" else "YOU DIED", True, (100, 255, 100) if self.state == "WIN" else (255, 50, 50))
        self.screen.blit(txt, txt.get_rect(center=(WIDTH//2, HEIGHT//2)))
        self.screen.blit(font_ui.render("Press R to Return to Hub", True, (200,200,200)), (WIDTH//2 - 100, HEIGHT//2 + 60))

    def draw_bar(self, x, y, w, h, val, max_val, color, bg_color=(50, 50, 50), text=None):
        pygame.draw.rect(self.screen, bg_color, (x, y, w, h))
        if max_val > 0:
            fill_w = int(w * (max(0, val) / max_val))
            pygame.draw.rect(self.screen, color, (x, y, fill_w, h))
        pygame.draw.rect(self.screen, (200, 200, 200), (x, y, w, h), 2)
        if text:
            txt_surf = font_ui.render(text, True, (255, 255, 255))
            self.screen.blit(txt_surf, (x + w//2 - txt_surf.get_width()//2, y + h//2 - txt_surf.get_height()//2))

    def game_over(self, win):
        self.state = "WIN" if win else "LOSE"
        self.add_shake(20)
        if win:
            self.add_floater(self.player.x, self.player.y, "VICTORY!", (255, 215, 0))

if __name__ == "__main__": Game().run()