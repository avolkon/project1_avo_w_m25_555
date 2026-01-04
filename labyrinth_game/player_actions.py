# Модуль действий игрока: перемещение между комнатами

from labyrinth_game.constants import ROOMS, TOTAL_PUZZLES
from labyrinth_game.utils import prevent_take_chest, random_event


# Модуль действий игрока: проверка наличия артефактов
def show_items(game_state):
    '''
    Отображает артефакты игрока.
    Args:
        game_state: {'artifacts': list, ...}
    '''
    # Инициализация puzzles_solved
    if 'puzzles_solved' not in game_state:
        game_state['puzzles_solved'] = set()
    
    items = game_state.get('items', [])
    
    if items:
        print(f"\n💎 Артефакты ({len(items)}): {', '.join(items)}")
    else:
        print("\n💎 Артефактов нет.")
    
    # Прогресс решённых загадок
    solved = len(game_state['puzzles_solved'])
    progress_pct = (solved / TOTAL_PUZZLES * 100) if TOTAL_PUZZLES > 0 else 0
    print(f"🧩 Загадок: {solved}/{TOTAL_PUZZLES} ({progress_pct:.0f}%)")
    
    print(f"{'═' * 50}")



# Модуль действий игрока: перемещение по комнатам

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
        print(f"Нет выхода на '{direction}' → выходы {', '.join(sorted(exits))}")
        return False
    
    # ✅ СПЕЦИАЛЬНАЯ ЛОГИКА для treasure_room:
    # ИНТЕГРАЦИЯ - проверка treasure_room и rusty_key
    target_room = exits[direction]
    if target_room == 'treasure_room':
        has_rusty_key = 'rusty_key' in game_state['items']
        
        if has_rusty_key:
            print("🔑 Ты применил rusty_key, дверь в комнату сокровищ открыта.")
            
        else:
            print("🚪 Дверь заперта. Нужен rusty_key, чтобы пройти дальше.")
            return False  # ❌ Игрок не вошёл в комнату сокровищ и вернулся в предыдущую

    # Сохраняем текущую комнату как предыдущую
    game_state['previous_room'] = current

    # Переход
    game_state['current_room'] = exits[direction]
    game_state['steps'] += 1
    
    if not silent:
        room = ROOMS[game_state['current_room']]
        print(f"\n📍 {game_state['current_room'].title()}")
        print(room['description'])
        print(f" → {', '.join(sorted(room['exits'].keys()))}")
        if room['items']:
            print(f"💎 {', '.join(room['items'])}")
            print(f"★ Шагов: {game_state['steps']}")
    
    # ИНТЕГРАЦИЯ: случайное событие после каждого успешного перемещения
    random_event(game_state)
    
    return True


# Модуль действий игрока: взятие предметов

def take_item(game_state, item_name):
    '''
    Подбирает предмет из комнаты.
    Args:
        game_state: {'items': [], 'current_room': str}
        item_name: 'torch', 'rusty_key'
    Returns: True=успех
    '''
    current = game_state['current_room']
    # СПЕЦИАЛЬНАЯ ЛОГИКА для treasure_room: БЛОКИРОВКА СУНДУКА
    if prevent_take_chest(game_state, item_name):
        return False
    
    room_items = ROOMS[current].get('items', [])

    if item_name in room_items:
        game_state['items'].append(item_name)
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
    if 'treasure_key' not in items:
        game_state['items'].append('treasure_key')
        print("🔑 Теперь у тебя есть treasure_key береги его!")
    else:
        print("Шкатулка пуста.")

# СПЕЦИАЛЬНАЯ ЛОГИКА для treasure_room
def win_treasure_key(game_state):
    current_room = game_state['current_room']
    if current_room == 'treasure_room':
        print("Ты применил ключ и замок щёлкает. Сундук открыт!")
        print("🏆 В сундуке сокровище! Это победа!")
        game_state['game_over'] = True
        if 'treasure_chest' in ROOMS[current_room]['items']:
            ROOMS[current_room]['items'].remove('treasure_chest')
        return True
    return False

    
# Словарь обработчиков предметов
ITEM_ACTIONS = {
    'torch': lambda gs: print("🔥 Можешь освещать свой путь! Расходуй заряд экономно."),
    'sword': lambda gs: print("⚔️ Уверенность!"),
    'bronze_box': handle_bronze_box,
    'treasure_key': lambda gs: print("В этой комнате ключ ничего не откроет."),
    'candle': lambda gs: print("🕯️ Свеча из часовни поможет отогнать духов!"),
    'silver_cross': lambda gs: print("✝️ Крест защитит и не раз!"),
    'ancient_book': lambda gs: print("📖 Теперь тебе доступны древние знания!"),
    'rotten_wood': lambda gs: print("🌲 Гнилые дрова может пригодятся?"),
    'glowing_mushroom': lambda gs: print("🍄Гриб светится, может пригодиться."),
    #'water_flask': lambda gs: print("💧 Живая вода восполнила силы!"),
    'small_boat': lambda gs: print("🚤 Лодка поможет найти что-то важное."),
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
    current_room = game_state['current_room']

    # СПЕЦИАЛЬНАЯ ЛОГИКА для treasure_room
    if item_name == 'treasure_key' and current_room == 'treasure_room':
        return win_treasure_key(game_state)
    
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
