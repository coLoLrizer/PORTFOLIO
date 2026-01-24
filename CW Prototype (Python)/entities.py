import pygame
import math
import random
from config import CONF, TILE_SIZE, WIDTH, HEIGHT, COLOR_PLAYER

def to_screen(x, y, z=0, cam_offset=(0,0)):
    surf = pygame.display.get_surface()
    width, height = surf.get_size()
    cx = width // 2 + cam_offset[0]
    cy = height // 2 + cam_offset[1]
    return int(cx + x * TILE_SIZE), int(cy + y * TILE_SIZE - z)

def to_world(sx, sy, cam_offset=(0,0)):
    surf = pygame.display.get_surface()
    width, height = surf.get_size()
    cx = width // 2 + cam_offset[0]
    cy = height // 2 + cam_offset[1]
    return (sx - cx) / TILE_SIZE, (sy - cy) / TILE_SIZE

# ==========================================
# --- ВИЗУАЛ УДАРА (SlashEffect) ---
# ==========================================
class SlashEffect:
    def __init__(self, target, center_angle, radius, color, swing_arc, duration, weapon_type):
        self.target = target 
        self.center_angle = center_angle
        self.radius = radius
        self.color = color
        self.duration = duration
        self.max_dur = duration
        self.swing_arc = math.radians(swing_arc)
        self.weapon_type = weapon_type
        
        self.start_angle = center_angle - (self.swing_arc / 2)
        self.end_angle = center_angle + (self.swing_arc / 2)
    
    def update(self):
        self.duration -= 1
        return self.duration > 0
    
    def draw(self, surface, cam_offset):
        pos = to_screen(self.target.x, self.target.y, 10, cam_offset)
        t = 1.0 - (self.duration / self.max_dur)
        current_angle = self.start_angle + (self.end_angle - self.start_angle) * t
        
        trail_len = 8
        for i in range(trail_len):
            trail_t = max(0, t - (i * 0.08))
            trail_ang = self.start_angle + (self.end_angle - self.start_angle) * trail_t
            tip_x = pos[0] + math.cos(trail_ang) * self.radius
            tip_y = pos[1] + math.sin(trail_ang) * self.radius
            alpha = int(150 * (1 - i/trail_len) * (self.duration/self.max_dur))
            if alpha > 0:
                width = 6 if self.weapon_type == "SWORD" else 12 
                pygame.draw.line(surface, (*self.color, alpha), pos, (tip_x, tip_y), width)

        if self.weapon_type != "HIT": 
            weapon_x = pos[0] + math.cos(current_angle) * self.radius
            weapon_y = pos[1] + math.sin(current_angle) * self.radius
            if self.weapon_type == "SWORD":
                pygame.draw.line(surface, (220, 220, 255), pos, (weapon_x, weapon_y), 4)
            elif self.weapon_type == "MACE":
                hx = pos[0] + math.cos(current_angle) * (self.radius * 0.7)
                hy = pos[1] + math.sin(current_angle) * (self.radius * 0.7)
                pygame.draw.line(surface, (50, 40, 30), pos, (hx, hy), 6)
                pygame.draw.circle(surface, (100, 100, 100), (int(weapon_x), int(weapon_y)), 10)

# ==========================================
# --- ИГРОК ---
# ==========================================
class Player:
    def __init__(self):
        self.x = 0; self.y = 4; self.radius = 15
        self.hp = CONF['PLAYER_HP']; self.max_hp = CONF['PLAYER_HP']
        self.iframes = 0; self.temp_hp = 0; self.stun_timer = 0
        self.vx = 0; self.vy = 0; self.knockback_vx = 0; self.knockback_vy = 0
        self.sword_dash_active = 0; self.stamina = CONF['STAMINA_MAX']
        self.weapon = "SWORD"; self.attack_cd = 0
        self.is_charging = False; self.charge_timer = 0; self.is_blocking = False; self.last_mouse_state = False
        
        # [NEW] Горение
        self.burn_timer = 0
        self.burn_tick = 0
        
        # [NEW] Блок (Hytale Style - Charges)
        self.shield_max_charges = 3
        self.shield_charges = 3
        self.shield_regen_timer = 0
        self.block_cooldown = 0
        
        # Механики
        self.windup_timer = 0; self.pending_attack_data = None
        self.potion_charges = CONF['POTION_CHARGES']; self.regen_timer = 0
        self.potion_active_timer = 0

    def use_potion(self, game):
        if self.potion_charges > 0:
            self.potion_charges -= 1
            heal = self.max_hp * CONF['POTION_INSTANT_PCT']
            self.hp = min(self.max_hp, self.hp + heal)
            game.add_floater(self.x, self.y, f"+{int(heal)} HP", (50, 255, 50))
            self.regen_timer = CONF['POTION_DURATION']
        else:
            game.add_floater(self.x, self.y, "No Potions!", (150, 150, 150))

    def take_damage(self, amount, game, ignore_iframes=False, can_block=True):
        # 1. Блок (ПО ЗАРЯДАМ)
        blocked = False
        if self.is_blocking and not ignore_iframes and can_block:
            if self.shield_charges > 0:
                # Успешный блок
                self.shield_charges -= 1
                self.shield_regen_timer = 180 # 3 сек КД регена
                game.add_floater(self.x, self.y, "BLOCKED!", (100, 200, 255))
                game.add_shake(2)
                if hasattr(game, 'debug_stats'): game.debug_stats["blocks_total"] += 1
                blocked = True
            else:
                # Пробитие
                game.add_floater(self.x, self.y, "GUARD BREAK!", (255, 50, 0))
                self.is_blocking = False
                self.stun_timer = 30
                game.add_shake(5)

        # 2. Получение урона
        if not blocked:
            if amount > 0:
                if self.iframes <= 0 or ignore_iframes:
                    if self.temp_hp > 0:
                        if amount <= self.temp_hp: self.temp_hp -= amount; amount = 0
                        else: amount -= self.temp_hp; self.temp_hp = 0
                    
                    if amount > 0:
                        self.hp -= amount
                        if not ignore_iframes: self.iframes = CONF['IFRAMES']
                        game.add_shake(5 if not ignore_iframes else 2)
                        game.add_floater(self.x, self.y, f"-{int(amount)}", (255, 50, 50))

    def move(self, keys):
        if self.sword_dash_active > 0:
            self.x += self.vx; self.y += self.vy; self.sword_dash_active -= 1; return

        ix, iy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: ix -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: ix += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]: iy -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: iy += 1
        if ix != 0 or iy != 0: l = math.hypot(ix, iy); ix /= l; iy /= l
        
        spd = CONF['WALK_SPEED']
        if keys[pygame.K_LSHIFT] and self.stamina > 0 and (ix!=0 or iy!=0) and not self.is_blocking:
            spd = CONF['RUN_SPEED']; self.stamina = max(0, self.stamina - CONF['STAMINA_RUN_COST'])
        else:
            reg = CONF['STAMINA_REGEN_IDLE'] if (ix==0 and iy==0) else CONF['STAMINA_REGEN_WALK']
            if not self.is_charging and not self.is_blocking: self.stamina = min(CONF['STAMINA_MAX'], self.stamina + reg)

        if self.is_charging:
             if self.weapon == "MACE": spd *= CONF['WEAPONS']['MACE'].get('MOVE_SPEED_WHILE_CHARGING', 0.4)
             else: spd *= 0.4
        
        if self.windup_timer > 0: spd *= 0.2
        if self.is_blocking: spd *= CONF['BLOCK_SPEED_PENALTY']
        if self.attack_cd > 0: spd *= CONF['WEAPONS'][self.weapon].get('SPEED_PENALTY', 1.0)
        if self.stun_timer > 0: spd = 0

        tvx, tvy = ix * (spd / TILE_SIZE), iy * (spd / TILE_SIZE)
        acc = CONF['ACCELERATION'] if not self.is_blocking else 0.5
        if ix != 0 or iy != 0: self.vx += (tvx - self.vx) * acc; self.vy += (tvy - self.vy) * acc
        else: self.vx += (0 - self.vx) * CONF['FRICTION']; self.vy += (0 - self.vy) * CONF['FRICTION']

        self.x += self.vx; self.y += self.vy
        self.x += self.knockback_vx; self.y += self.knockback_vy
        self.knockback_vx *= 0.85; self.knockback_vy *= 0.85
        if self.stun_timer > 0: self.stun_timer -= 1

    def handle_input_state(self, mouse, game, boss):
        self.is_blocking = mouse[2]
        curr_lmb = mouse[0]
        
        if self.weapon == "BOW":
            if curr_lmb: 
                self.is_charging = True; self.charge_timer = min(self.charge_timer + 1, CONF['WEAPONS']['BOW']['CHARGE_TIME'])
            elif self.last_mouse_state and not curr_lmb:
                self.fire_bow(game); self.is_charging = False; self.charge_timer = 0
        else:
            if curr_lmb and not self.is_blocking:
                self.is_charging = True
                max_charge = CONF['WEAPONS'][self.weapon]['CHARGE_TIME']
                self.charge_timer = min(self.charge_timer + 1, max_charge)
            elif self.last_mouse_state and not curr_lmb and not self.is_blocking:
                if self.charge_timer >= CONF['WEAPONS'][self.weapon]['CHARGE_TIME']: self.heavy_attack(game, boss)
                else: self.light_attack(game, boss)
                self.is_charging = False; self.charge_timer = 0
        self.last_mouse_state = curr_lmb

    def light_attack(self, game, boss):
        if self.attack_cd > 0 or self.windup_timer > 0: return
        cfg = CONF['WEAPONS'][self.weapon]
        if self.stamina < cfg['STAMINA']: game.add_floater(self.x, self.y, "No Stamina", (150, 150, 150)); return
        self.stamina -= cfg['STAMINA']; self.attack_cd = cfg['CD']
        mx, my = pygame.mouse.get_pos(); px, py = to_screen(self.x, self.y)
        ang = math.atan2(my - py, mx - px)
        
        if self.weapon == "MACE":
            self.windup_timer = cfg.get('WINDUP', 30)
            self.pending_attack_data = {'angle': ang, 'boss': boss, 'cfg': cfg}
        else:
            self._execute_visuals_and_hit(game, boss, cfg, ang, "SWORD")

    def _execute_visuals_and_hit(self, game, boss, cfg, angle, w_type):
        arc, time = cfg.get('SWING_ARC', 90), cfg.get('SWING_TIME', 15)
        color = (100, 200, 255) if w_type == "SWORD" else (255, 150, 50)
        game.visual_effects.append(SlashEffect(self, angle, int(cfg['RANGE']*TILE_SIZE), color, arc, time, w_type))
        self._check_melee_hit(boss, game, cfg['RANGE'], cfg['DMG']); game.add_shake(2)

    def heavy_attack(self, game, boss):
        cfg = CONF['WEAPONS'][self.weapon]
        if self.stamina < cfg['STAMINA_CHARGE']: game.add_floater(self.x, self.y, "No Stamina!", (200, 200, 200)); return
        self.stamina -= cfg['STAMINA_CHARGE']
        mx, my = pygame.mouse.get_pos(); px, py = to_screen(self.x, self.y)
        ang = math.atan2(my - py, mx - px)
        
        if self.weapon == "SWORD":
            ds = cfg['DASH_FORCE'] / TILE_SIZE; self.vx, self.vy = math.cos(ang) * ds, math.sin(ang) * ds
            self.sword_dash_active = 15; self.iframes = 20; game.add_shake(10)
            game.visual_effects.append(SlashEffect(self, ang, 60, (0, 255, 255), 30, 10, "SWORD"))
        elif self.weapon == "MACE":
            game.add_shake(20); game.visual_effects.append(SlashEffect(self, ang, 120, (255, 50, 0), 180, 40, "MACE"))
            if self._check_melee_hit(boss, game, cfg['RANGE'] * 1.5, cfg['CHARGED_DMG']):
                kb = cfg['KNOCKBACK']; boss.x += math.cos(ang) * kb; boss.y += math.sin(ang) * kb

    def fire_bow(self, game):
        mx, my = pygame.mouse.get_pos()
        px, py = to_screen(self.x, self.y)
        ang = math.atan2(my - py, mx - px)
        cfg = CONF['WEAPONS']['BOW']
        
        # p - это процент зарядки (от 0.0 до 1.0)
        p = self.charge_timer / cfg['CHARGE_TIME']
        
        # Считаем урон строго по конфигу:
        # Урон = Минимум + (Разница между Максом и Минимумом) * Процент зарядки
        dmg = cfg['DMG_MIN'] + (cfg['DMG_MAX'] - cfg['DMG_MIN']) * p
        
        # Скорость стрелы тоже берем из конфига
        spd = cfg['ARROW_SPEED'] * (0.5 + 0.5 * p) # Стрела летит быстрее, если заряжена
        
        game.player_projectiles.append(PlayerProjectile(
            self.x, self.y, 
            self.x + math.cos(ang), self.y + math.sin(ang), 
            spd / TILE_SIZE, 
            dmg
        ))
        game.add_shake(int(5 * p))

    def _check_melee_hit(self, boss, game, r, dmg):
        h = False
        if math.hypot(boss.x - self.x, boss.y - self.y) < (r + boss.radius / TILE_SIZE): boss.take_damage(dmg, game, self); h = True
        for m in game.shadow_minions:
            if math.hypot(m.x - self.x, m.y - self.y) < (r + 1.0): m.hp -= dmg; game.add_floater(m.x, m.y, str(int(dmg)), (200, 200, 200)); h = True
        return h

    def update_logic(self, game, boss):
        # [NEW] Логика BURN (Горение)
        if self.burn_timer > 0:
            self.burn_timer -= 1
            self.burn_tick += 1
            if self.burn_tick >= 25: # Урон раз в 0.4 сек
                self.hp -= 1
                self.burn_tick = 0
                game.add_floater(self.x, self.y, "BURN", (255, 100, 0))

        # [NEW] Реген щита
        if self.shield_regen_timer > 0:
            self.shield_regen_timer -= 1
        elif self.shield_charges < self.shield_max_charges:
            if pygame.time.get_ticks() % 120 == 0: # Раз в 2 сек
                self.shield_charges += 1
                game.add_floater(self.x, self.y, "+SHIELD", (100, 200, 255))

        if self.iframes > 0: self.iframes -= 1
        if self.attack_cd > 0: self.attack_cd -= 1
        if self.windup_timer > 0:
            self.windup_timer -= 1
            if self.windup_timer == 0 and self.pending_attack_data:
                d = self.pending_attack_data; self._execute_visuals_and_hit(game, d['boss'], d['cfg'], d['angle'], "MACE"); self.pending_attack_data = None
        
        if self.sword_dash_active > 0:
            if self._check_melee_hit(boss, game, 1.5, CONF['WEAPONS']['SWORD']['CHARGED_DMG']):
                self.sword_dash_active = 0; self.vx *= -0.5; self.vy *= -0.5; game.add_shake(5)
                
        if self.regen_timer > 0:
            self.regen_timer -= 1
            heal = (self.max_hp * CONF['POTION_REGEN_PCT']) / CONF['POTION_DURATION']
            self.hp = min(self.max_hp, self.hp + heal)

    def _draw_windup(self, surface, px, py):
        mx, my = pygame.mouse.get_pos(); ang = math.atan2(my - py, mx - px)
        shake = math.sin(pygame.time.get_ticks() * 0.05) * 0.15 
        back_ang = ang - math.pi * 0.7 + shake
        hx, hy = px + math.cos(back_ang) * 45, py + math.sin(back_ang) * 45
        pygame.draw.line(surface, (60, 45, 35), (px, py), (hx, hy), 6)
        pygame.draw.circle(surface, (120, 120, 120), (int(hx), int(hy)), 10)

    def draw(self, surface, cam_offset):
        if self.iframes > 0 and (self.iframes // 4) % 2 == 0: return 
        sx, sy = to_screen(self.x, self.y, 0, cam_offset)
        px, py = to_screen(self.x, self.y, 10, cam_offset)
        pygame.draw.circle(surface, (0,0,0,100), (sx, sy), self.radius, 2)
        
        if self.windup_timer > 0: self._draw_windup(surface, px, py)
        
        col = (100, 200, 255)
        if self.weapon == "MACE": col = (255, 150, 100)
        if self.weapon == "BOW": col = (150, 255, 150)
        
        # Индикация щита (синяя аура)
        if self.is_blocking: pygame.draw.circle(surface, (100, 100, 255), (px, py), self.radius + 5, 2)
        
        pygame.draw.circle(surface, col, (px, py), self.radius)
        if self.temp_hp > 0: pygame.draw.circle(surface, (100, 255, 100), (px, py), self.radius + 2, 2)
        
        if self.regen_timer > 0:
            pulse = (math.sin(pygame.time.get_ticks() * 0.01) + 1) * 2
            pygame.draw.circle(surface, (50, 255, 50), (px, py), self.radius + 6 + pulse, 1)

        # [NEW] Отрисовка зарядов щита (шарики)
        if self.shield_charges > 0:
            for i in range(self.shield_charges):
                angle = (pygame.time.get_ticks() * 0.005) + (i * (6.28 / 3))
                bx = px + math.cos(angle) * 35
                by = py + math.sin(angle) * 35
                pygame.draw.circle(surface, (100, 200, 255), (int(bx), int(by)), 6)
                pygame.draw.circle(surface, (255, 255, 255), (int(bx), int(by)), 3)

        if self.is_charging:
            p = min(1.0, self.charge_timer / CONF['WEAPONS'][self.weapon].get('CHARGE_TIME', 60))
            if self.weapon == "BOW":
                mx, my = pygame.mouse.get_pos(); ang = math.atan2(my - py, mx - px); bd = 20
                bx, by = px + math.cos(ang) * bd, py + math.sin(ang) * bd; bend = 1.0 - (p * 0.5)
                tx, ty = px + math.cos(ang - 0.5 * bend) * (bd + 15), py + math.sin(ang - 0.5 * bend) * (bd + 15)
                btx, bty = px + math.cos(ang + 0.5 * bend) * (bd + 15), py + math.sin(ang + 0.5 * bend) * (bd + 15)
                pygame.draw.line(surface, (139, 69, 19), (bx, by), (tx, ty), 3); pygame.draw.line(surface, (139, 69, 19), (bx, by), (btx, bty), 3)
                sc = (200, 200, 200) if p < 1.0 else (255, 50, 50)
                hx, hy = px + math.cos(ang) * (bd - p * 10), py + math.sin(ang) * (bd - p * 10)
                pygame.draw.line(surface, sc, (tx, ty), (hx, hy), 1); pygame.draw.line(surface, sc, (btx, bty), (hx, hy), 1)
            bc = (255, 255, 0) if p < 1.0 else (255, 0, 0)
            pygame.draw.rect(surface, bc, (px - 25, py - 40, 50 * p, 8)); pygame.draw.rect(surface, (255,255,255), (px - 25, py - 40, 50, 8), 1)

# ==========================================
# --- ЛУЖИ И ПРОЖЕКТАЙЛЫ ---
# ==========================================
class PlayerProjectile:
    def __init__(self, x, y, tx, ty, speed, damage):
        self.x, self.y = x, y; a = math.atan2(ty - y, tx - x); self.vx, self.vy = math.cos(a) * speed, math.sin(a) * speed
        self.damage, self.life = damage, CONF['ARROW_LIFETIME']
    def update(self, boss, game):
        self.x += self.vx; self.y += self.vy; self.life -= 1
        if math.hypot(boss.x - self.x, boss.y - self.y) < 1.5:
            boss.take_damage(self.damage, game)
            game.visual_effects.append(SlashEffect(boss, 0, 10, (255, 255, 0), 360, 5, "HIT"))
            return False 
        for m in game.shadow_minions:
            if math.hypot(m.x - self.x, m.y - self.y) < 1.5:
                m.hp -= self.damage; game.add_floater(m.x, m.y, str(int(self.damage)), (200, 200, 255)); return False
        return self.life > 0
    def draw(self, s, c): px, py = to_screen(self.x, self.y, 10, c); pygame.draw.line(s, (255, 255, 200), (px, py), (px - self.vx * 1.5, py - self.vy * 1.5), 3)

class BloodProjectile:
    def __init__(self, x, y, tx, ty):
        self.x, self.y = x, y
        angle = math.atan2(ty - y, tx - x)
        speed = CONF['BLOOD_PROJ_SPEED'] * 0.7 
        
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = 200
    def update(self, player, game):
        self.x += self.vx; self.y += self.vy; self.life -= 1
        
        # Проверка попадания
        if math.hypot(player.x - self.x, player.y - self.y) < 1.2: # Чуть увеличил хитбокс (1.0 -> 1.2) для честности
            player.take_damage(20, game, can_block=True)
            game.visual_effects.append(SlashEffect(player, 0, 15, (255, 50, 50), 360, 5, "HIT"))
            if not player.is_blocking: # Если игрок НЕ заблочил
                game.boss.hp = min(game.boss.max_hp, game.boss.hp + 50) # ХИЛ!
                game.add_floater(game.boss.x, game.boss.y, "DRAIN!", (200, 0, 0))
            return False
            
        return self.life > 0

    def draw(self, surface, cam_offset):
        pos = to_screen(self.x, self.y, 10, cam_offset)
        # Рисуем "хвост"
        end_x = pos[0] - self.vx * 4 * TILE_SIZE 
        end_y = pos[1] - self.vy * 4 * TILE_SIZE
        pygame.draw.line(surface, (150, 0, 0), pos, (end_x, end_y), 6)
        # Ядро снаряда
        pygame.draw.circle(surface, (255, 50, 50), pos, 7)

class BloodSpike:
    def __init__(self, x, y, angle, max_dist): self.x, self.y, self.angle, self.max_dist = x, y, angle, max_dist; self.dist_traveled, self.active, self.radius = 0, True, 10 
    def update(self, player, boss, game):
        if not self.active: return False
        ta = math.atan2(player.y - self.y, player.x - self.x); diff = (ta - self.angle + math.pi) % (2 * math.pi) - math.pi
        self.angle += max(min(diff, CONF['SPIKE_TURN_SPEED']), -CONF['SPIKE_TURN_SPEED'])
        self.x += math.cos(self.angle) * CONF['SPIKE_SPEED']; self.y += math.sin(self.angle) * CONF['SPIKE_SPEED']; self.dist_traveled += CONF['SPIKE_SPEED']
        if math.hypot(player.x - self.x, player.y - self.y) < (self.radius/TILE_SIZE + player.radius/TILE_SIZE): player.take_damage(15, game); self.active = False; return False
        return self.dist_traveled < self.max_dist
    def draw(self, s, c): p = to_screen(self.x, self.y, 0, c); pygame.draw.line(s, (200, 0, 0), p, (p[0] + math.cos(self.angle)*20, p[1] + math.sin(self.angle)*20), 4)

# --- В entities.py замени класс ShadowMinion ---

class ShadowMinion:
    def __init__(self, x, y, px, py, aggressive=False):
        self.x, self.y = x, y
        self.hp = CONF['SHADOW_MINION_HP']
        self.radius = 12
        self.aggressive = aggressive
        # Если Beast Fang активен: Скорость x1.7
        self.speed = CONF['SHADOW_MINIONS_SPEED'] * (1.7 if aggressive else 1.0)
        self.state = "FOLLOW"
        self.timer = 0
        self.lunge_vx, self.lunge_vy = 0, 0
        
        # Начальный толчок при спавне
        dx, dy = self.x - px, self.y - py; dist = math.hypot(dx, dy)
        if dist < 1.5: 
            push = 2.0
            self.x += (dx/dist if dist > 0 else 1) * push
            self.y += (dy/dist if dist > 0 else 0) * push

    def update(self, player, game):
        dx, dy = player.x - self.x, player.y - self.y
        dist = math.hypot(dx, dy)
        
        if self.state == "FOLLOW":
            # Агрессивные лучше преследуют
            if dist > 0.8:
                self.x += (dx/dist) * self.speed
                self.y += (dy/dist) * self.speed
            else:
                self.state = "PREPARE"
                # Агрессивные атакуют почти мгновенно (12 кадров вместо 35)
                self.timer = 20 if self.aggressive else 35
                if self.aggressive:
                    # Рассчитываем вектор резкого рывка (Lunge)
                    self.lunge_vx = (dx/dist) * 0.18
                    self.lunge_vy = (dy/dist) * 0.18
        
        elif self.state == "PREPARE":
            self.timer -= 1
            if self.aggressive:
                # Скользим к игроку во время замаха (Рывок)
                self.x += self.lunge_vx
                self.y += self.lunge_vy
            
            if self.timer <= 0:
                # Увеличенный радиус попадания для агрессивных
                hit_radius = 1.8 if self.aggressive else 1.6
                if dist < hit_radius: 
                    player.take_damage(CONF['DMG_SHADOW'], game)
                    game.visual_effects.append(SlashEffect(self, 0, 15, (150, 0, 200), 360, 10, "HIT"))
                self.state = "COOLDOWN"
                self.timer = 20 if self.aggressive else 45 
        
        elif self.state == "COOLDOWN":
            self.timer -= 1
            if self.timer <= 0: self.state = "FOLLOW"
        return self.hp > 0

    def draw(self, surface, cam_offset):
        sx, sy = to_screen(self.x, self.y, 0, cam_offset); px, py = to_screen(self.x, self.y, 10, cam_offset)
        
        # Цвет меняется если агрессивный
        color = (100, 50, 150)
        if self.aggressive: color = (100, 0, 0) # Темно-красный корпус
        
        z_bounce = 0
        if self.state == "PREPARE":
            if (pygame.time.get_ticks() // 100) % 2 == 0: color = (255, 50, 50)
            z_bounce = math.sin(self.timer * 0.2) * 5
            
        pygame.draw.circle(surface, (0, 0, 0, 80), (sx, sy), self.radius, 2)
        pygame.draw.circle(surface, color, (px, py - z_bounce), self.radius)
        
        # Глаза: Желтые если злые, Белые если обычные
        eye_c = (255, 255, 255)
        if self.aggressive: eye_c = (255, 200, 0)
        if self.state == "PREPARE": eye_c = (255, 0, 0) # Красные при атаке
        
        pygame.draw.circle(surface, eye_c, (px - 4, py - 4 - z_bounce), 3)
        pygame.draw.circle(surface, eye_c, (px + 4, py - 4 - z_bounce), 3)
        if self.aggressive:
             # Злые брови
             pygame.draw.line(surface, (0,0,0), (px - 7, py - 8 - z_bounce), (px - 2, py - 5 - z_bounce), 1)
             pygame.draw.line(surface, (0,0,0), (px + 7, py - 8 - z_bounce), (px + 2, py - 5 - z_bounce), 1)

class PuddleBase:
    def __init__(self, x, y, radius, color, life):
        self.x = x; self.y = y; self.max_radius = radius; self.radius = 0
        self.life = life; self.color = color
        self.points = [random.uniform(0, 6.28) for _ in range(12)]
        self.time = 0; self.tick_timer = 0; self.tick_rate = 20 # Дефолт

    def update(self, player, game):
        if self.radius < self.max_radius: self.radius += 0.5
        self.life -= 1; self.time += 0.1
        if self.tick_timer > 0: self.tick_timer -= 1
        
        if math.hypot(player.x - self.x, player.y - self.y) < (self.radius / TILE_SIZE): 
            if self.tick_timer <= 0: 
                self.on_collision(player, game)
                self.tick_timer = self.tick_rate # Используем индивидуальный темп
        return self.life > 0

    def on_collision(self, player, game): pass

    def draw(self, s, cam):
        if self.radius < 1: return
        surf = pygame.Surface((int(self.max_radius*2+20), int(self.max_radius*2+20)), pygame.SRCALPHA)
        poly = []
        for i in range(12):
            ang = (math.pi*2/12)*i; r = self.radius + math.sin(self.time + self.points[i])*2
            poly.append((surf.get_width()//2 + math.cos(ang)*r, surf.get_height()//2 + math.sin(ang)*r*0.6))
        alpha = int(min(255, (self.life/60.0 if self.life < 60 else 1.0) * 180))
        pygame.draw.polygon(surf, (*self.color, alpha), poly)
        pygame.draw.polygon(surf, (255, 255, 255, alpha), poly, 2)
        p = to_screen(self.x, self.y, 0, cam)
        s.blit(surf, (p[0]-surf.get_width()//2, p[1]-surf.get_height()//2))

class PoisonPuddle(PuddleBase):
    def __init__(self, x, y, radius=45, delay=0):
        # Передаем всё в базу (цвет зеленый, время жизни из конфига)
        super().__init__(x, y, radius, (50, 200, 50), CONF['TIME_POISON'])
        self.tick_rate = 45 
        self.spawn_delay = delay # Задержка перед активацией лужи
    def update(self, player, game):
        if self.spawn_delay > 0:
            self.spawn_delay -= 1
            return True
        return super().update(player, game)
    def draw(self, s, cam):
        if self.spawn_delay > 0:
            return
        super().draw(s, cam)

    def on_collision(self, player, game):
        player.take_damage(CONF['DMG_POISON'], game, ignore_iframes=True)

class FirePuddle(PuddleBase):
    def __init__(self, x, y, radius=55):
        super().__init__(x, y, radius, (255, 100, 0), CONF['TIME_FIRE'])
        self.tick_rate = 6 
    def on_collision(self, player, game):
        player.take_damage(CONF['DMG_FIRE'], game, ignore_iframes=True)
        player.burn_timer = 180 

class HolyPuddle:
    def __init__(self, x, y, player): self.x, self.y, self.life, self.active = x, y, 180, False
    def update(self, player, game):
        self.life -= 1
        if self.life > 80:
            dx, dy = player.x - self.x, player.y - self.y; d = math.hypot(dx, dy)
            if d > 0.1: self.x += (dx/d) * 0.06; self.y += (dy/d) * 0.06
        if self.life < 40:
            self.active = True
            if math.hypot(player.x - self.x, player.y - self.y) < 1.5: player.take_damage(CONF['DMG_HOLY'], game)
        return self.life > 0
    def draw(self, s, cam):
        p = to_screen(self.x, self.y, 0, cam); alpha = random.randint(150, 255) if (self.life < 80 and not self.active) else 100
        surf = pygame.Surface((120, 120), pygame.SRCALPHA); pygame.draw.ellipse(surf, (255, 255, 200, alpha), (10, 35, 100, 50)); s.blit(surf, (p[0]-60, p[1]-60))
        if self.active: sb = pygame.Surface((60, 800), pygame.SRCALPHA); pygame.draw.rect(sb, (255, 255, 200, 200), (10, 0, 40, 800)); s.blit(sb, (p[0]-30, p[1]-800+20))

class Potion:
    def __init__(self, sx, sy, tx, ty, pt):
        self.start_x, self.start_y = sx, sy; self.tx, self.ty = tx, ty; self.type = pt; self.x, self.y = sx, sy; self.radius_mult = 1.0
        dist = math.hypot(tx - sx, ty - sy); self.total_dur = max(40, int(dist / 0.25)); self.life = self.total_dur
        self.max_height = 50 + dist * 10 
        self.color = {"POISON": (50, 255, 50), "FIRE": (255, 100, 0), "HEALING": (255, 50, 150),
                      "SHADOW": (150, 100, 200), "BLOOD": (200, 0, 0), "HOLY": (255, 255, 200)}.get(pt, (255, 255, 150))

    def update(self, boss, player, game):
        self.life -= 1; t = 1.0 - (self.life / self.total_dur)
        self.x = self.start_x + (self.tx - self.start_x) * t; self.y = self.start_y + (self.ty - self.start_y) * t
        if self.life <= 0: self.on_impact(player, game); return False 
        return True 

    def on_impact(self, p, g):
        g.add_shake(5 * self.radius_mult)

        if self.type == "POISON": 
            main_r = 45 * self.radius_mult
            g.puddles.append(PoisonPuddle(self.x, self.y, radius=main_r, delay=0))
            
            # 3 капли по 60% размера (small_r)
            small_r = main_r * 0.6
            
            # Берем случайный начальный поворот, чтобы "трилистник" каждый раз был под разным углом
            start_angle = random.uniform(0, math.pi * 2)
            
            for i in range(3):
                # Равномерно распределяем: 0, 120 и 240 градусов + небольшой разброс (jitter)
                # (i * 2 * pi / 3) — это жесткое разделение на 3 части
                a = start_angle + (i * (math.pi * 2 / 3)) + random.uniform(-0.4, 0.4)
                
                dist = random.uniform(1.0, 1.5) * self.radius_mult
                
                # Координаты капли
                drop_x = self.x + math.cos(a) * dist
                drop_y = self.y + math.sin(a) * dist
                
                # Последовательный прилет (15, 30, 45 кадров задержки)
                g.puddles.append(PoisonPuddle(drop_x, drop_y, radius=small_r, delay=(i+1)*15))
        elif self.type == "FIRE": g.puddles.append(FirePuddle(self.x, self.y, radius=55 * self.radius_mult))
        elif self.type == "HOLY": g.puddles.append(HolyPuddle(self.x, self.y, p))
        elif self.type == "HEALING":
            check_radius = CONF['HEALING_EXPLOSION_RADIUS'] * self.radius_mult
            if math.hypot(self.x - p.x, self.y - p.y) < check_radius:
                c = int(p.hp * CONF['HEALING_PLAYER_CONVERSION']); p.hp -= c; p.temp_hp += c
                g.add_floater(p.x, p.y, f"CONVERTED! +{c}", (100, 255, 100))
        elif self.type == "SHADOW":
            # Проверяем флаг Beast Fang
            is_aggro = getattr(g.boss, 'beast_fang_active', False)
            c = 3 + (2 if self.radius_mult > 1 else 0)
            
            for i in range(c):
                a = (i/c)*math.pi*2; dist = 1.5 * self.radius_mult
                # Передаем aggressive=is_aggro
                g.shadow_minions.append(ShadowMinion(self.x+math.cos(a)*dist, self.y+math.sin(a)*dist, p.x, p.y, aggressive=is_aggro))
        elif self.type == "BLOOD":
            check_radius = 2.5 * self.radius_mult
            if math.hypot(self.x - p.x, self.y - p.y) < check_radius: p.take_damage(CONF['DMG_BLOOD'] * self.radius_mult, g)

    def draw(self, surface, cam_offset):
        t = 1.0 - (self.life / self.total_dur); arc_height = self.max_height * 4 * t * (1 - t)
        ground_pos = to_screen(self.x, self.y, 0, cam_offset); potion_pos = to_screen(self.x, self.y, arc_height, cam_offset)
        vis_size = 10 * self.radius_mult 
        shadow_scale = 1.0 - (arc_height / 300.0); shadow_w = int(14 * shadow_scale * self.radius_mult)
        if shadow_w > 2:
            s = pygame.Surface((shadow_w*2, shadow_w), pygame.SRCALPHA)
            pygame.draw.ellipse(s, (0, 0, 0, 100), (0, 0, shadow_w*2, shadow_w))
            surface.blit(s, (ground_pos[0]-shadow_w, ground_pos[1]-shadow_w//2))
        if self.type == "HEALING":
             r_px = int(CONF['HEALING_EXPLOSION_RADIUS'] * self.radius_mult * TILE_SIZE)
             pygame.draw.circle(surface, (0, 255, 0), ground_pos, r_px, 1)
        pygame.draw.circle(surface, self.color, potion_pos, int(vis_size))
        pygame.draw.circle(surface, (255, 255, 255), potion_pos, int(vis_size)+2, 2)

class CrimsonAltar:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.materials = [] # Список ID предметов (1-5)
        # Радиусы колец
        self.ring_radii = [2.0, 4.0, 6.0, 8.0, 10.0]

    def toggle_material(self, mat_id):
        if mat_id in self.materials: self.materials.remove(mat_id)
        else: self.materials.append(mat_id); self.materials.sort()

    def draw(self, surface, cam_offset):
        pos = to_screen(self.x, self.y, 0, cam_offset)
        pygame.draw.circle(surface, (30, 20, 30), pos, int(1.2 * TILE_SIZE))
        color_map = {1: (220, 50, 50), 2: (150, 50, 255), 3: (0, 255, 255), 4: (50, 255, 50), 5: (255, 200, 0)}
        mist_active = (2 in self.materials)

        for i, radius in enumerate(self.ring_radii):
            r_px = int(radius * TILE_SIZE)
            
            if i == 4 and mist_active:
                for j in range(24): 
                    ang = (j / 24) * 6.28 + pygame.time.get_ticks() * 0.0008
                    pulse_r = r_px + math.sin(pygame.time.get_ticks() * 0.002 + j) * 15
                    mx = pos[0] + math.cos(ang) * pulse_r
                    my = pos[1] + math.sin(ang) * pulse_r
                    s = pygame.Surface((80, 80), pygame.SRCALPHA)
                    pygame.draw.circle(s, (80, 0, 120, 60), (40, 40), 40)
                    pygame.draw.circle(s, (150, 50, 255, 30), (40, 40), 25)
                    surface.blit(s, (mx-40, my-40))
            
            stone_col = (60, 60, 70) if not (i == 4 and mist_active) else (40, 0, 60)
            pygame.draw.circle(surface, stone_col, pos, r_px, 8)
            
            if i < len(self.materials):
                mat_id = self.materials[i]
                glow = color_map.get(mat_id, (255, 255, 255))
                p = (math.sin(pygame.time.get_ticks() * 0.005 + i) + 1) * 0.5
                c = [int(x * (0.5 + 0.5 * p)) for x in glow]
                pygame.draw.circle(surface, c, pos, r_px, 2)

        for i, radius in enumerate(self.ring_radii):
            r_px = int(radius * TILE_SIZE)
            pygame.draw.circle(surface, (70, 72, 75), pos, r_px, 12)
            pygame.draw.circle(surface, (30, 32, 35), pos, r_px + 6, 2)
            pygame.draw.circle(surface, (30, 32, 35), pos, r_px - 6, 2)
            if i < len(self.materials):
                mat_id = self.materials[i] 
                glow = color_map.get(mat_id, (255, 255, 255))
                pulse = (math.sin(pygame.time.get_ticks() * 0.005 + i) + 1) * 0.5
                cur_glow = [int(c * (0.5 + 0.5 * pulse)) for c in glow]
                pygame.draw.circle(surface, cur_glow, pos, r_px, 3)

        y_off = math.sin(pygame.time.get_ticks() * 0.004) * 5
        pygame.draw.ellipse(surface, (120, 0, 30), (pos[0]-15, pos[1]-20+y_off, 30, 40))

class BlinkPortal:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.life = 40 # Живет пока идет анимация
        self.angle = 0

    def update(self):
        self.life -= 1
        self.angle += 10
        return self.life > 0

    def draw(self, surface, cam_offset):
        sx, sy = to_screen(self.x, self.y, 20, cam_offset) # Z=20 (под боссом)
        
        # Эффект пульсации и вращения
        radius = 40 if self.life > 10 else int(40 * (self.life / 10))
        
        # Рисуем овал (портал)
        portal_surf = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(portal_surf, (50, 0, 50), (radius, radius), radius) # Темная дыра
        pygame.draw.circle(portal_surf, (150, 0, 150), (radius, radius), radius, 4) # Ободок
        
        surface.blit(portal_surf, (sx - radius, sy - radius))