import pygame

CONF = {
    # --- ИГРОК ---
    'PLAYER_HP': 150,
    'WALK_SPEED': 4,
    'RUN_SPEED': 7,
    'ACCELERATION': 0.2,
    'FRICTION': 0.15,
    'IFRAMES': 60,
    
    # СТАМИНА
    'STAMINA_MAX': 100,
    'STAMINA_RUN_COST': 0.5,
    'STAMINA_REGEN_IDLE': 0.6,
    'STAMINA_REGEN_WALK': 0.3,
    
    # БЛОК
    'BLOCK_DMG_REDUCTION': 0.7,
    'BLOCK_SPEED_PENALTY': 0.3,
    # ХИЛКА
    'POTION_CHARGES': 2,
    'POTION_INSTANT_PCT': 0.15,  # 15% сразу
    'POTION_REGEN_PCT': 0.30,    # 30% потом
    'POTION_DURATION': 900,      # 15 секунд (60 * 15)
    
    # --- ОРУЖИЕ ---
    'WEAPONS': {
        'SWORD': {
            'DMG': 17,              # Быстрый урон
            'CD': 15,               # Кулдаун 0.33с
            'RANGE': 2.1,
            'SWING_ARC': 70,
            'SWING_TIME': 7,
            'SPEED_PENALTY': 0.9, 
            'STAMINA': 1,
            
            # Рывок (Dash)
            'CHARGED_DMG': 35,      # Урон от столкновения
            'CHARGE_TIME': 40,      # Зарядка 0.6с
            'DASH_FORCE': 20,       # Скорость полета
            'STAMINA_CHARGE': 35
        },
        'MACE': {
            'DMG': 35,              # Тяжелый удар
            'CD': 50,               
            'WINDUP': 30,           # 0.5с ЗАДЕРЖКА ПЕРЕД УДАРОМ
            'RANGE': 2.6,
            'SWING_ARC': 100,
            'SWING_TIME': 20,
            'SPEED_PENALTY': 0.7,   # Сильное замедление при замахе
            'STAMINA': 15,
            
            # Заряженная (Smash)
            'CHARGED_DMG': 150,
            'CHARGE_TIME': 100,     # 2 секунды заряжать
            'STAMINA_CHARGE': 40,
            'KNOCKBACK': 1.0,
            'MOVE_SPEED_WHILE_CHARGING': 0.4 
        },
        'BOW': {
            'DMG_MIN': 5, 
            'DMG_MAX': 25,
            'CHARGE_TIME': 70,   
            'SPEED_PENALTY': 0.2,
            'ARROW_SPEED': 25
        }
    },
    
    'ARROW_LIFETIME': 80,

    # --- БОСС ---
    'BOSS_HP': 1500,
    'ORBIT_RADIUS': 10,
    'BOSS_SPEED': 0.006,
    'BLINK_RANGE': 3.5,
    'BLINK_CD': 1800,
    'BOSS_DRINK_HEAL': 400,
    
    # Комбо
    'COMBO_RANGE': 3.5,
    'COMBO_NEARBY_TIME': 150,
    'COMBO_CD': 300,
    'COMBO_WINDUP': 35,
    'COMBO_HIT_DURATION': 10,
    'COMBO_RECOVERY': 20,
    
    # Варка
    'BREWING_DURATION': 60,
    'BREWING_WINDUP': 50,
    'BREWING_POTIONS_P1': 3,
    'BREWING_POTIONS_P2': 4,
    'BREWING_CAULDRON_RADIUS': 3.0,
    'AUTO_BREW_TIME': 40,
    
    'SHOCKWAVE_STUN': 60,
    'SHOCKWAVE_RANGE': 4.5,
    'THROW_TIMINGS': [2.5, 2.0, 1.5],
    
    'DMG_POISON': 6, 'DMG_FIRE': 1, 'DMG_HOLY': 25, 'DMG_BLOOD': 15, 'DMG_SHADOW': 5,
    'PUDDLE_TICK_RATE': 5,
    'TIME_POISON': 900, 'TIME_FIRE': 420,
    
    'SPIKE_COUNT': 8, 'SPIKE_TURN_SPEED': 0.04, 'SPIKE_SPEED': 0.15, 'BLOOD_PROJ_SPEED': 0.20,
    'FIRE_BUFF_USES': 4, 'FIRE_BUFF_MULT': 1.3,
    'ASSASSIN_TIME': 180, 'ASSASSIN_SPEED_MULT': 1.4,
    'HEALING_PLAYER_CONVERSION': 0.2, 'HEALING_TEMP_HP_DECAY': 0.02, 'HEALING_EXPLOSION_RADIUS': 1.5,
    'SHADOW_INVIS_ALPHA': 50, 'SHADOW_MINIONS_COUNT': 3, 'SHADOW_MINIONS_SPEED': 0.08, 'SHADOW_MINION_HP': 40,
    'POISON_SKIN_DMG': 1,
    'PHASE_2_THRESHOLD': 0.6, 'PHASE_3_THRESHOLD': 0.3,
}

WIDTH, HEIGHT = 1000, 700
FPS = 60
TILE_SIZE = 40 
COLOR_PLAYER = (100, 200, 255)
COLOR_BOSS = (220, 50, 50)
COLOR_BG = (20, 24, 30)
COLOR_ARENA_BORDER = (60, 60, 70)