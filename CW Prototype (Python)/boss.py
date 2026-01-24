import pygame
import math
import random

from pygame import surface
from config import CONF, TILE_SIZE, COLOR_BOSS
from entities import to_screen, BloodSpike, BloodProjectile, Potion
from entities import BlinkPortal # и остальные импорты

class Boss:
    def __init__(self):
        self.x = 0; self.y = -CONF['ORBIT_RADIUS']; self.radius = 30
        self.hp = CONF['BOSS_HP']; self.max_hp = CONF['BOSS_HP']
        
        # Плавный прицел
        self.aim_x = 0; self.aim_y = 0
        
        # Таймеры
        self.blink_cd = 0; self.flash_timer = 0; self.throw_timer = 0
        self.angular_velocity = 0; self.fire_buff_stack = 0; self.assassin_timer = 0
        
        # Комбо
        self.combo_active = False; self.combo_step = 0; self.combo_timer = 0
        self.combo_cd = 0; self.combo_nearby_timer = 0
        self.damage_dealt = False 
        
        # ВАРКА
        self.brewing_active = False; self.brewing_timer = 0
        self.brewing_windup = 0 
        self.brewed_potions = []; self.potions_to_brew = []
        self.brewing_progress = 0
        
        # Статы
        self.heal_count = 0
        self.selected_potion_index = -1
        
        # Эффекты
        self.telegraph_active = False; self.auto_brew_timer = 0
        self.poison_skin = 0; self.holy_shield = 0
        self.shadow_invis = 0; self.shadow_invis_alpha = 255
        self.legendary_cauldron = False; self.cauldron_timer = 0
        
        # Модификаторы
        self.mist_enabled = False
        self.orbit_target = CONF['ORBIT_RADIUS']
        
        # Blink
        self.blink_cd = 0
        
        # --- НОВЫЕ ПЕРЕМЕННЫЕ ДЛЯ БЛИНКА ---
        self.blink_state = "IDLE" # "IDLE", "VANISH", "VOID", "APPEAR"
        self.blink_timer = 0
        self.blink_dest_x = 0
        self.blink_dest_y = 0
        self.visual_radius_scale = 1.0 # Для анимации уменьшения/увеличения

    def apply_modifiers(self, materials):
        self.max_hp = CONF['BOSS_HP']
        self.mist_enabled = False
        self.legendary_cauldron = False
        self.orbit_target = CONF['ORBIT_RADIUS']
        
        # Сброс конфига к базе
        CONF['BREWING_POTIONS_P1'] = 3
        CONF['BREWING_POTIONS_P2'] = 4
        CONF['THROW_TIMINGS'] = [2.5, 2.0, 1.5]

        # 1. Vile Heart
        if 1 in materials: self.max_hp *= 1.4 
        # 2. Strange Dust (Туман)
        if 2 in materials: 
            self.mist_enabled = True
            self.orbit_target = 7.5 
        # 3. Witch's Hair
        if 3 in materials: 
            CONF['BREWING_POTIONS_P1'] += 1; CONF['BREWING_POTIONS_P2'] += 1
            CONF['THROW_TIMINGS'] = [t * 0.9 for t in CONF['THROW_TIMINGS']]
        # 4. Beast Fang (Тени агрессивны)
        if 4 in materials:
            self.beast_fang_active = True
        # 5. Golden Eye (Котел)
        if 5 in materials: 
            self.legendary_cauldron = True; self.cauldron_timer = 300 
             
        self.hp = self.max_hp

    def update_blink_logic(self, game, player):
        if self.blink_state == "IDLE": return

        self.blink_timer -= 1
        
        # 1. ФАЗА ИСЧЕЗНОВЕНИЯ (Упрыгивает назад)
        if self.blink_state == "VANISH":
            # Уменьшаем визуальный размер (втягивается)
            self.visual_radius_scale = max(0, self.blink_timer / 15.0)
            
            # Небольшой отскок назад от игрока (визуальный)
            angle = math.atan2(self.y - player.y, self.x - player.x)
            self.x += math.cos(angle) * 0.1
            self.y += math.sin(angle) * 0.1
            
            if self.blink_timer <= 0:
                self.blink_state = "VOID"
                self.blink_timer = 10 # Время в пустоте
                
        # 2. ФАЗА ПУСТОТЫ (Мгновенный перенос)
        elif self.blink_state == "VOID":
            if self.blink_timer == 5: # На середине переносим координаты
                self.x = self.blink_dest_x
                self.y = self.blink_dest_y
                # Спавним портал выхода
                game.visual_effects.append(BlinkPortal(self.x, self.y))
                
            if self.blink_timer <= 0:
                self.blink_state = "APPEAR"
                self.blink_timer = 15 # Время появления
                
        # 3. ФАЗА ПОЯВЛЕНИЯ (Выпрыгивает)
        elif self.blink_state == "APPEAR":
            # Увеличиваемся обратно
            prog = 1.0 - (self.blink_timer / 15.0)
            self.visual_radius_scale = prog
            
            if self.blink_timer <= 0:
                self.blink_state = "IDLE"
                self.visual_radius_scale = 1.0

    def update(self, player, game):
        # --- ЛЕГЕНДАРНЫЙ КОТЕЛ (Golden Eye) ---
        self.update_blink_logic(game, player)
        if self.blink_state != "IDLE":
            return
        # --- ЛОГИКА АССАСИНА (Вставь это в начало update) ---
        if self.assassin_timer > 0:
            self.assassin_timer -= 1
            
            # Если она начала бить (комбо пошло) — фиксируем попытку
            if self.combo_active:
                self.has_attacked_in_shadow = True 
                
            # СБРОС: Если удар закончился ИЛИ время вышло
            if (self.has_attacked_in_shadow and not self.combo_active) or self.assassin_timer <= 0:
                self.assassin_timer = 0
                self.shadow_invis = 0 # Выходит из тени
                
                # Пишем результат для игрока
                msg = "STRIKE!" if self.has_attacked_in_shadow else "MISSED..."
                color = (255, 50, 50) if self.has_attacked_in_shadow else (150, 150, 150)
                game.add_floater(self.x, self.y, msg, color)
                
        if self.legendary_cauldron:
            self.cauldron_timer -= 1
            if self.cauldron_timer <= 0:
                self.cauldron_timer = 300 # Раз в 5 секунд
                from entities import Potion
                
                # Ротация 4-х стихий (без Крови, чтобы не баговало)
                p_type = random.choice(["POISON", "FIRE", "SHADOW", "HOLY"])
                
                pot = Potion(self.x, self.y, player.x, player.y, p_type)
                game.potion_objects.append(pot)
                
                if hasattr(game, 'debug_stats'): game.debug_stats["boss_potions_thrown"] += 1
                game.add_floater(self.x, self.y, "CAULDRON!", (255, 215, 0))
                game.add_shake(3)

        # --- ТУМАН (Mist) ---
        if self.mist_enabled:
            dist_to_center = math.hypot(player.x, player.y)
            if dist_to_center > 9.0:
                if pygame.time.get_ticks() % 20 == 0:
                    player.take_damage(3, game, ignore_iframes=True, can_block=False)
                    game.add_floater(player.x, player.y, "MIST BURN", (150, 0, 255))

        # 1. Прицеливание (плавное слежение)
        dist_to_player = math.hypot(self.x - player.x, self.y - player.y)
        flight_time = dist_to_player / 0.25
        wanted_x = player.x + player.vx * flight_time * 0.6
        wanted_y = player.y + player.vy * flight_time * 0.6
        self.aim_x += (wanted_x - self.aim_x) * 0.05
        self.aim_y += (wanted_y - self.aim_y) * 0.05

        # 2. Обновление таймеров
        for attr in ['flash_timer', 'blink_cd', 'combo_cd', 'poison_skin', 'holy_shield', 'assassin_timer']:
            val = getattr(self, attr); 
            if val > 0: setattr(self, attr, val - 1)
        
        if self.shadow_invis > 0: self.shadow_invis -= 1
        
        hp_pct = self.hp / self.max_hp
        phase = 2 if hp_pct < 0.3 else (1 if hp_pct < 0.6 else 0)
        
        dx, dy = self.x - player.x, self.y - player.y; dist = math.hypot(dx, dy)
        
        # 3. Логика Комбо
        if self.combo_active:
            self.telegraph_active = False; self.combo_timer -= 1
            self.handle_combo_attack(player, game, dist, dx, dy)
        else:
            if dist < CONF['COMBO_RANGE']: self.combo_nearby_timer += 1
            else: self.combo_nearby_timer = 0
            
            # Условия старта комбо: игрок рядом + прошло время + нет КД
            can_melee = (self.combo_nearby_timer >= CONF['COMBO_NEARBY_TIME'] and self.combo_cd <= 0)
            is_assassin = (self.assassin_timer > 0 and dist < 2.5 and self.combo_cd <= 0)
            
            if (can_melee or is_assassin) and not self.brewing_active and self.brewing_windup <= 0:
                self.combo_active = True; self.combo_step = 0
                self.combo_timer = CONF['COMBO_WINDUP'] + CONF['COMBO_HIT_DURATION'] + CONF['COMBO_RECOVERY']
                self.damage_dealt = False
                game.add_floater(self.x, self.y, "COMBO!", (255, 150, 0))

        self.handle_brewing(player, game, hp_pct, phase)
        
        # 4. Движение
        if not self.combo_active and not self.brewing_active and self.brewing_windup <= 0:
            if self.assassin_timer > 0:
                if dist > 1.5:
                    s = 0.10 
                    self.x -= (dx / dist) * s; self.y -= (dy / dist) * s
            else:
                if not self.combo_active and not self.brewing_active: 
                    self.handle_movement(player, game, math.hypot(self.x-player.x, self.y-player.y))

        # 5. Бросок зелий
        if not self.combo_active and not self.brewing_active and self.brewing_windup <= 0 and len(self.brewed_potions) > 0:
            if self.assassin_timer <= 0:
                self.throw_timer += 1
                req = int(CONF['THROW_TIMINGS'][phase] * 60)
                
                if self.throw_timer == req - 25:
                    self.selected_potion_index = random.randint(0, len(self.brewed_potions) - 1)
                    self.telegraph_active = True
                
                if self.throw_timer >= req:
                    self.use_potion(player, game, phase)
                    self.throw_timer = 0; self.telegraph_active = False; self.selected_potion_index = -1

    def handle_combo_attack(self, player, game, dist, dx, dy):
        windup = CONF['COMBO_WINDUP']
        hit_duration = CONF['COMBO_HIT_DURATION']
        recovery = CONF['COMBO_RECOVERY']
        
        # Фаза 1: Замах (Windup)
        if self.combo_timer > (hit_duration + recovery):
             # Медленная подводка
             if dist > 1.5: 
                 self.x -= (dx / dist) * 0.02
                 self.y -= (dy / dist) * 0.02

        # Фаза 2: УДАР (Active Hit)
        elif self.combo_timer > recovery:
             # Рывок происходит всю фазу
             if dist > 1.4: 
                 self.x -= (dx / dist) * 0.04
                 self.y -= (dy / dist) * 0.04
             
             # --- ФИКС "ФАНТОМНОЙ ТЫЧКИ" ---
             # Вычисляем, сколько кадров уже длится удар
             # self.combo_timer уменьшается, так что:
             frames_into_hit = (hit_duration + recovery) - self.combo_timer
             
             # НАНОСИМ УРОН ТОЛЬКО В ПЕРВЫЕ 5 КАДРОВ!
             # Если игрок подошел позже — палка уже пролетела.
             if frames_into_hit < 5: 
                 # Пересчитываем реальную дистанцию после рывка
                 real_dist = math.hypot(self.x - player.x, self.y - player.y)
                 
                 if not self.damage_dealt:
                    if real_dist < CONF['COMBO_RANGE'] + 0.5:
                        dmg = [15, 15, 20][self.combo_step]
                        player.take_damage(dmg, game)
                        
                        # Отталкивание
                        kb = [0.1, 0.1, 1.0][self.combo_step]
                        if real_dist > 0.01:
                             player.knockback_vx = ((player.x - self.x) / real_dist) * kb
                             player.knockback_vy = ((player.y - self.y) / real_dist) * kb
                        else: player.knockback_vx = kb
                        
                        game.add_shake(10)
                        self.damage_dealt = True # Урон прошел, больше в этом комбо не бьем
             else:

                 pass
                
        if self.combo_timer <= 0:
            self.combo_step += 1
            if self.combo_step >= 3: 
                self.combo_active = False
                self.combo_cd = 180
                self.combo_nearby_timer = 0
            else: 
                # --- [РИТМ] ДИНАМИЧЕСКИЕ ТАЙМИНГИ ---
                if self.combo_step == 2:
                    w = windup * 1.0 
                    h = hit_duration * 1.0
                    r = recovery * 1.5
                else:
                    w = windup * 0.6 
                    h = hit_duration
                    r = recovery * 0.3
                
                # Применяем новые тайминги
                self.combo_timer = w + h + r
                self.damage_dealt = False

    def handle_brewing(self, player, game, hp_pct, phase):
        # Фаза 3: Авто-варка
        if phase == 2:
            self.brewing_active = False; self.brewing_windup = 0
            if len(self.brewed_potions) < CONF['BREWING_POTIONS_P2']:
                self.auto_brew_timer -= 1
                if self.auto_brew_timer <= 0:
                    pool = ["POISON", "FIRE", "HEALING", "SHADOW", "BLOOD", "HOLY"]
                    self.brewed_potions.append(random.choice(pool))
                    self.auto_brew_timer = CONF['AUTO_BREW_TIME']
        else:
            # --- ВОТ ТУТ ОДИН ЕДИНСТВЕННЫЙ ИСПРАВЛЕННЫЙ IF ---
            if not self.brewing_active and self.brewing_windup <= 0 and \
               not self.brewed_potions and not self.potions_to_brew and \
               not self.combo_active and self.assassin_timer <= 0: # <--- ПРОВЕРКА ТУТ
                
                c = CONF['BREWING_POTIONS_P1'] if phase == 0 else CONF['BREWING_POTIONS_P2']
                pool = ["POISON", "FIRE", "HEALING", "SHADOW", "BLOOD", "HOLY"]
                self.potions_to_brew = [random.choice(pool) for _ in range(c)]
                self.brewing_windup = CONF.get('BREWING_WINDUP', 60)
                
                # Твой легендарный флоатер
                game.add_floater(self.x, self.y, "HI-HI-HA!!", (255, 255, 255))

            # --- Дальше идет просто обработка анимаций (не меняем) ---
            if self.brewing_windup > 0:
                self.brewing_windup -= 1
                if self.brewing_windup % 5 == 0:
                    w_max = CONF.get('BREWING_WINDUP', 60); prog = 1.0 - (self.brewing_windup / w_max)
                    game.add_shake(int(prog * 3))
                if self.brewing_windup <= 0:
                    self.trigger_shockwave(player, game)
                    self.brewing_active = True; self.brewing_timer = CONF['BREWING_DURATION']
            
            if self.brewing_active:
                self.brewing_timer -= 1
                self.brewing_progress = 1.0 - (self.brewing_timer / CONF['BREWING_DURATION'])
                if self.brewing_timer <= 0:
                    if self.potions_to_brew:
                        self.brewed_potions.append(self.potions_to_brew.pop(0))
                        if self.potions_to_brew: self.brewing_timer = CONF['BREWING_DURATION']
                        else: self.brewing_active = False

    def handle_movement(self, player, game, dist):
        target_r = getattr(self, 'orbit_target', CONF['ORBIT_RADIUS'])
    
        # 1. Логика движения по орбите (оставляем)
        angle_player = math.atan2(player.y, player.x)
        target_angle = angle_player + math.pi 
        curr_dist = math.hypot(self.x, self.y)

        if curr_dist > 0.01: 
            s = target_r / curr_dist
            self.x *= s; self.y *= s
        else: 
            self.x, self.y = target_r, 0
    
        curr_angle = math.atan2(self.y, self.x)
        diff = (target_angle - curr_angle + math.pi) % (2 * math.pi) - math.pi
        tv = CONF['BOSS_SPEED'] if diff > 0 else -CONF['BOSS_SPEED']
        if abs(diff) < 0.05: tv = 0
        self.angular_velocity += (tv - self.angular_velocity) * 0.05
        na = curr_angle + self.angular_velocity
        self.x = math.cos(na) * target_r
        self.y = math.sin(na) * target_r
    
        # 2. ОСТАВЛЯЕМ ТОЛЬКО ОДИН БЛОК БЛИНКА (НОВЫЙ)
        if math.hypot(self.x - player.x, self.y - player.y) < CONF['BLINK_RANGE'] and self.blink_cd <= 0:
            self.blink_cd = CONF['BLINK_CD']
        
            # ЗАПУСКАЕМ АНИМАЦИЮ (координаты X и Y здесь НЕ МЕНЯЕМ)
            self.blink_state = "VANISH"
            self.blink_timer = 20 # Сделал чуть длиннее для наглядности
            self.visual_radius_scale = 1.0
        
            # Спавним портал входа на текущем месте
            from entities import BlinkPortal
            game.visual_effects.append(BlinkPortal(self.x, self.y))
            game.add_floater(self.x, self.y, "TOO CLOSE!", (200, 100, 255))
        
            # Только вычисляем точку назначения
            na_dest = angle_player + math.pi + random.uniform(-1, 1)
            self.blink_dest_x = math.cos(na_dest) * target_r
            self.blink_dest_y = math.sin(na_dest) * target_r

    def trigger_shockwave(self, player, game):
        game.add_shake(15)
        if math.hypot(self.x - player.x, self.y - player.y) < CONF['SHOCKWAVE_RANGE']:
            player.stun_timer = max(player.stun_timer, CONF['SHOCKWAVE_STUN'])
            dx, dy = player.x - self.x, player.y - self.y
            dist = math.hypot(dx, dy)
            if dist > 0.1:
                player.knockback_vx = (dx/dist) * 2.5; player.knockback_vy = (dy/dist) * 2.5
        game.shockwave_effect = {'x': self.x, 'y': self.y, 'timer': 30, 'progress': 0}
    
    def use_potion(self, player, game, phase):
        if not self.brewed_potions: return
        
        # Выбор зелья
        if self.selected_potion_index != -1 and self.selected_potion_index < len(self.brewed_potions):
            p = self.brewed_potions.pop(self.selected_potion_index)
        else:
            p = self.brewed_potions.pop(0)
        
        emp = (self.fire_buff_stack > 0); drink = False
        
        if p == "SHADOW": drink = (phase != 2 and random.random() < 0.5)
        elif p == "HEALING": drink = (self.hp / self.max_hp < 0.6)
        elif p == "BLOOD": drink = (random.random() < 0.5)
        elif p in ["FIRE", "POISON", "HOLY"]: drink = (random.random() < 0.2)
        
        if drink: self.drink_potion(p, player, game)
        else:
            if emp: self.fire_buff_stack -= 1
            self.throw_potion(player, game, p, emp)

    def drink_potion(self, p, player, game):
        game.add_floater(self.x, self.y, f"Gulp! {p}", (200, 200, 200))
        if p == "HEALING": 
            dh = int(CONF['BOSS_DRINK_HEAL'] / (1.5 ** self.heal_count))
            self.hp = min(self.max_hp, self.hp + max(10, dh))
            game.add_floater(self.x, self.y, f"+{max(10, dh)} HP", (50, 255, 50)); self.heal_count += 1 
        elif p == "SHADOW":
            self.assassin_timer = 180 # 3 секунды на атаку
            self.shadow_invis = 180   # Полная невидимость
            self.has_attacked_in_shadow = False # Флаг: удар еще не нанесен
            game.add_floater(self.x, self.y, "ASSASSIN", (150, 0, 200))

        elif p == "FIRE": self.fire_buff_stack = 3; game.add_floater(self.x, self.y, "FIRE POWER!", (255, 100, 0))
        elif p == "POISON": self.poison_skin = 300; game.add_floater(self.x, self.y, "POISON SKIN", (50, 200, 50))
        elif p == "HOLY": self.holy_shield = 300; game.add_floater(self.x, self.y, "HOLY SHIELD", (255, 255, 200))
        elif p == "BLOOD":
            d = math.hypot(player.x - self.x, player.y - self.y)
            for i in range(8):
                a = (math.pi * 2 / 8) * i; game.blood_spikes.append(BloodSpike(self.x, self.y, a, d * 0.75))

    def throw_potion(self, player, game, p, emp):
        if p == "BLOOD": game.projectiles.append(BloodProjectile(self.x, self.y, player.x, player.y))
        else:
            pot = Potion(self.x, self.y, self.aim_x, self.aim_y, p)
            pot.radius_mult = 1.5 if emp else 1.0; game.potion_objects.append(pot)

    def take_damage(self, amount, game, player=None):
        if self.holy_shield > 0: game.add_floater(self.x, self.y, "BLOCKED", (200, 200, 255)); return
        if self.brewing_active: amount *= 0.5
        if self.poison_skin > 0 and player: player.take_damage(2, game, ignore_iframes=True)
        self.hp -= amount; self.flash_timer = 5; game.add_floater(self.x, self.y, str(int(amount)), (255, 255, 255))
        if self.hp <= 0: game.game_over(win=True)
    
    def draw(self, surface, cam_offset):
        sx, sy = to_screen(self.x, self.y, 40, cam_offset)
        
        color_map = {
            "POISON": (50, 255, 50), "FIRE": (255, 100, 0), "HEALING": (255, 50, 150),
            "SHADOW": (150, 100, 200), "BLOOD": (200, 0, 0), "HOLY": (255, 255, 200)
        }
        if self.blink_state == "VOID": return # Не рисуем, пока она в пустоте

        # Применяем масштаб
        current_radius = int(self.radius * self.visual_radius_scale)
        if current_radius <= 0: return

        sx, sy = to_screen(self.x, self.y, 40, cam_offset)
        
        # Твой код рисования круга, но используй current_radius вместо self.radius
        pygame.draw.circle(surface, (50, 0, 50), (sx, sy), current_radius) # Тело
        # Аура (кожа)
        if self.poison_skin > 0:
            for i in range(8):
                ang = (pygame.time.get_ticks() * 0.005) + (i * math.pi / 4)
                pygame.draw.circle(surface, (50, 255, 50), (int(sx + math.cos(ang)*38), int(sy + math.sin(ang)*38)), 4)
        if self.holy_shield > 0: pygame.draw.circle(surface, (255, 255, 200), (sx, sy), self.radius + 6, 2)
        

        # Индикатор варки (Шоквейв)
        if self.brewing_windup > 0:
            prog = 1.0 - (self.brewing_windup / 60.0); rs = CONF['SHOCKWAVE_RANGE'] * TILE_SIZE
            pygame.draw.circle(surface, (255, 255, 255), (sx, sy), int(rs * (1.0 - prog)), 2)
            alpha = int(prog * 150)
            w_surf = pygame.Surface((rs*2, rs*2), pygame.SRCALPHA)
            pygame.draw.circle(w_surf, (255, 200, 0, alpha), (rs, rs), int(rs * 0.8))
            surface.blit(w_surf, (sx - rs, sy - rs))

        # Телеграф броска
        if self.telegraph_active:
            c = color_map.get(self.brewed_potions[self.selected_potion_index], (255,255,255)) if self.selected_potion_index != -1 else (255,255,255)
            pygame.draw.circle(surface, c, (sx, sy), self.radius + 15, 2)
            if self.throw_timer > 0:
                ax, ay = to_screen(self.aim_x, self.aim_y, 0, cam_offset); pygame.draw.line(surface, c, (sx, sy), (ax, ay), 1)

        # Радиус комбо (предупреждение)
        if self.combo_nearby_timer > 0 and not self.combo_active:
            r = int(CONF['COMBO_RANGE'] * TILE_SIZE)
            pygame.draw.circle(surface, (100, 50, 0), (sx, sy), r, 1)
        
        # Сначала определяем актуальные тайминги для текущего шага, как в update
        c_windup = CONF['COMBO_WINDUP']
        c_hit = CONF['COMBO_HIT_DURATION']
        c_rec = CONF['COMBO_RECOVERY']

        if self.combo_step == 2: # Медленный финишер
            w = c_windup * 2.0
            h = c_hit * 1.0
            rec = c_rec * 1.5
        else: # Быстрые удары
            w = c_windup * 0.7
            h = c_hit
            rec = c_rec * 0.5

        # Теперь используем w, h, rec вместо старых CONF
        if self.combo_active and self.combo_timer > (h + rec):
            # Считаем прогресс (защита от деления на ноль)
            if w > 0:
                prog = 1.0 - (self.combo_timer - (h + rec)) / w
            else:
                prog = 1.0
            
            prog = max(0.0, min(1.0, prog)) 

            r = int(CONF['COMBO_RANGE'] * TILE_SIZE * prog)
            if r > 1:
                s = pygame.Surface((r*2+2, r*2+2), pygame.SRCALPHA)
                pygame.draw.circle(s, (255, 0, 0, 80), (r, r), r)
                surface.blit(s, (sx - r, sy - r))
                
                # Полоска зарядки (тоже используем корректный prog)
                bar_w = 60
                pygame.draw.rect(surface, (50, 0, 0), (sx - bar_w//2, sy - 65, bar_w, 4)) 
                pygame.draw.rect(surface, (255, 255, 0), (sx - bar_w//2, sy - 65, int(bar_w * prog), 4))
        
        # Котел варки
        if self.brewing_active:
            cr = int(3.0 * TILE_SIZE); cs = pygame.Surface((cr*2, cr*2), pygame.SRCALPHA)
            pygame.draw.circle(cs, (255, 165, 0, 60), (cr, cr), int(cr * self.brewing_progress))
            pygame.draw.circle(cs, (255, 140, 0, 180), (cr, cr), cr, 2); surface.blit(cs, (sx-cr, sy-cr))

        # Зелья в инвентаре
        for i, p in enumerate(self.brewed_potions):
            oy = -60 - (i * 15); c = color_map.get(p, (200,200,200))
            if i == self.selected_potion_index:
                pulse = abs(math.sin(pygame.time.get_ticks() * 0.02)) * 6
                pygame.draw.circle(surface, (255, 255, 255), (sx + 40, sy + oy), 8 + pulse, 2)
            pygame.draw.circle(surface, c, (sx + 40, sy + oy), 6)
            
        # Тело босса
        col = (220, 50, 50) if self.assassin_timer <= 0 else (80, 0, 80)
        pygame.draw.circle(surface, col, (sx, sy), self.radius)
        pygame.draw.rect(surface, (255,0,0), (sx - 30, sy - 50, 60 * (self.hp/self.max_hp), 6))