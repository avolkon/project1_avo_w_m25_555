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
        print(f"❌ Нет '{direction}' → {', '.join(sorted(exits))}")
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
def use_item(game_state, item_name):
    '''
    Использует предмет из набора артефактов.
    '''
    items = game_state.get('artifacts', [])
    
    if item_name not in items:
        print("❌ У вас нет такого предмета.")
        return False
    
    if item_name == 'torch':
        print("🔥 Можешь освещать свой путь! Но расходуй заряд экономно.")
    
    elif item_name == 'sword':
        print("⚔️ Уверенность!")
    
    elif item_name == 'bronze_box':
        if 'rusty_key' not in items:
            game_state['artifacts'].append('rusty_key')
            print("✅ + rusty_key!")
        else:
            print("✅ Шкатулка пуста.")
    
    elif item_name == 'golden_chest':
        print("🏆 ПОБЕДА!")
    
    elif item_name == 'candle':
        print("🕯️ Источник света для прочтения книги!")
    
    elif item_name == 'silver_cross':
        print("✝️ Защита от опасных артефактов!")

    elif item_name == 'ancient_book':
        print("📖 Теперь тебе доступны древние знания!")

    elif item_name == 'rotten_wood':
        print("🌲 Гнилые дрова — бесполезны.")

    elif item_name == 'glowing_mushroom':
        print("🍄 Гриб светится, пока растёт, лучше его не брать, \nпоможет сэкономить энергию твоих источников света")

    elif item_name == 'water_flask':
        print("💧 Живая вода восполнила силы и улучшила смекалку!")

    elif item_name == 'small_boat':
        print("🚤 Лодка поможет добраться до центра источника и набрать живой воды")

    else:
        print(f"❓ Не знаете '{item_name}'.")
    
    return True

# Добавьте в player_actions.py:

