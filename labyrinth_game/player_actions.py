# Модуль действий игрока: перемещение между комнатами

from labyrinth_game import ROOMS

# Модуль действий игрока: проверка наличия артефактов
def look_items(game_state):
    '''
    Отображает артефакты игрока.
    Args:
        game_state: {'artifacts': list, ...}
    '''
    items = game_state.get('items', [])
    
    if items:
        print(f"\n💎 Артефакты ({len(items)}): {', '.join(items)}")
    else:
        print("\n💎 Артефактов нет.")
    
    print(f"{'═' * 40}")

def get_input(prompt="> "):
    '''
    Безопасный ввод команды от пользователя.
    Args:
        prompt: Текст подсказки для ввода 
    Returns:
        str: Команда пользователя или "quit"
    '''
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def move_player(game_state, direction, silent=False):
    '''
    Перемещает игрока. Лаконично и надёжно.
    Args:
        game_state: {'current_room': str, 'steps': int}
        direction: 'north', 'south'  
        silent: без вывода
    Returns: True=успех
    '''
    current = game_state['current_room']

    # Валидация входных данных
    if current not in ROOMS:
        print(f"❌ Нет '{current}'")
        return False
    
    exits = ROOMS[current]['exits']
    if direction not in exits:
        print(f"❌ Нет выхода в направлении '{direction}' → доступные выходы {', '.join(sorted(exits))}")
        return False
    
    # Переход
    game_state['current_room'] = exits[direction]
    game_state['steps'] += 1
    
    if not silent:
        room = ROOMS[game_state['current_room']]
        print(f"\n📍 {game_state['current_room'].title()}")
        print(room['description'])
        print(f" → {', '.join(sorted(room['exits'].keys()))}")
        if room['items']: print(f"💎 {', '.join(room['items'])}")
        print(f"★ Шагов: {game_state['steps']}")
    
    return True

# Модуль действий игрока: взятие предметов

def take_item(game_state, item_name):
    '''
    Подбирает предмет из комнаты.
    
    Args:
        game_state: {'artifacts': [], 'current_room': str}
        item_name: 'torch', 'rusty_key'
    
    Returns: True=успех
    '''
    current = game_state['current_room']
    room_items = ROOMS[current].get('items', [])
    
    if item_name in room_items:
        game_state['artifacts'].append(item_name)
        room_items.remove(item_name)
        print(f"✅ Вы подняли: {item_name}")
        return True
    else:
        print("❌ Такого предмета здесь нет.")
        return False

# Модуль действий игрока: использование предметов

# Двухшаговая реализация взятия артефакта из шкатулки
def handle_bronze_box(game_state):
    items = game_state.get('items', [])
    if 'rusty_key' not in items:
        game_state['items'].append('rusty_key')
        print("✅ Теперь у тебя есть rusty_key!")
    else:
        print("✅ Шкатулка пуста.")

# Словарь обработчиков предметов
ITEM_ACTIONS = {
    'torch': lambda gs: print("🔥 Можешь освещать свой путь! Но расходуй заряд экономно."),
    'sword': lambda gs: print("⚔️ Уверенность!"),
    'bronze_box': handle_bronze_box,
    'golden_chest': lambda gs: print("🏆 ПОБЕДА!"),
    'candle': lambda gs: print("🕯️ Источник света для прочтения книги!"),
    'silver_cross': lambda gs: print("✝️ Защита от опасных артефактов!"),
    'ancient_book': lambda gs: print("📖 Теперь тебе доступны древние знания!"),
    'rotten_wood': lambda gs: print("🌲 Гнилые дрова — бесполезны."),
    'glowing_mushroom': lambda gs: print("🍄 Гриб светится, пока растёт, лучше его не брать, \nпоможет сэкономить энергию твоих источников света."),
    'water_flask': lambda gs: print("💧 Живая вода восполнила силы!"),
    'small_boat': lambda gs: print("🚤 Лодка поможет добраться до центра источника и набрать живой воды."),
}

def use_item(game_state, item_name):
    '''
    Использует предмет из набора артефактов.
    Args:
        game_state: dict с состоянием игры
        item_name: str, название предмета
    Returns:
        bool: True если предмет использован, False если нет
    '''
    # Проверяем наличие предмета в инвентаре
    items = game_state.get('items', [])
    
    if item_name not in items:
        print("❌ У вас нет такого предмета.")
        return False
    
    # Ищем обработчик в словаре
    handler = ITEM_ACTIONS.get(item_name)
    
    if handler:
        # Вызываем соответствующий обработчик
        handler(game_state)
    else:
        # Для неизвестных предметов
        print(f"❓ Не известно как пользоваться '{item_name}'.")
    
    return True
