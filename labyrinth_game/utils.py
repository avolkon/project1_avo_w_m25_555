# utils.py
from labyrinth_game import ROOMS, TOTAL_PUZZLES, get_input, attempt_open_treasure, back
from labyrinth_game import SIN_MULTIPLIER, STRETCH_FACTOR
import math
from typing import Union


# Модуль: описание комнаты
def describe_room(game_state):
    '''
    Выводит описание текущей комнаты из game_state.
    Args:
        game_state: {'current_room': str, ...}
    '''

    current_room = game_state['current_room']
    
    # Валидация
    if current_room not in ROOMS:
        print("❌ Неизвестная комната!")
        return
    
    room = ROOMS[current_room]

    # Интеграция счётчика решенных загадок. Инициализация puzzles_solved
    if 'puzzles_solved' not in game_state:
        game_state['puzzles_solved'] = set()
    
    # 1. Название в верхнем регистре
    print(f"\n{'═' * 50}")
    print(f"📍 {current_room.upper()}")
    
    # 2. Описание комнаты
    print(room['description'])
    
    # 3. Проверка статуса загадки в комнате
    if current_room in game_state['puzzles_solved']:
        print("✅ Загадка решена")
    elif room.get('puzzle'):
        print("🔒 Кажется, здесь есть загадка (используй команду solve/решить)")
    else:
        print("ℹ️ Загадок нет")
    
    # 4. Предметы
    if room.get('items') and room['items']:
        print(f"💎 В комнате есть артефакты: {', '.join(room['items'])}")
    
    # 5. Выходы
    print(f"🚪 Выходы: {', '.join(room['exits'].keys())}")
     
    # 6. Статистика прогресса
    # total_puzzles = len([r for r in ROOMS if ROOMS[r].get('puzzle')])
    solved_count = len(game_state['puzzles_solved'])
    print(f"🧩 Прогресс: {solved_count}/{TOTAL_PUZZLES} ({solved_count/TOTAL_PUZZLES*100:.0f}%)")
    
    print(f"{'═' * 50}")

# Модуль: решение загадок:

def solve_puzzle(game_state):
    '''
    Решает загадку в текущей комнате.
    Если загадок нет, но есть предметы - подсказывает игроку.
    '''
    current_room = game_state['current_room']

    if 'puzzles_solved' not in game_state:
        game_state['puzzles_solved'] = set()
    
    # СПЕЦИАЛЬНАЯ ЛОГИКА для treasure_room
    if current_room == 'treasure_room':
        return attempt_open_treasure(game_state)
    
    # 1. Проверка наличия загадки
    if current_room in game_state['puzzles_solved']:
        print(f"✅ Загадка в '{current_room}' уже решена!")
        print(f"🎉 Всего решено: {len(game_state['puzzles_solved'])}")
        describe_room(game_state)
        return False

    elif 'puzzle' not in ROOMS[current_room] or ROOMS[current_room]['puzzle'] is None:
        print("Загадок здесь нет.")
        
        # ПОДСКАЗКА: если есть предметы в комнате
        if ROOMS[current_room].get('items'):
            items_list = ', '.join(ROOMS[current_room]['items'])
            print(f"📌 Но в комнате есть артефакты: {items_list}")
            print("   Ты можешь взять их командой 'take' или 'взять'")
            print("   Например: 'take {0}' или 'взять {0}'".format(ROOMS[current_room]['items'][0]))
            get_input(prompt="> ")
        
        return False
    
    # 2. Получаем загадку
    puzzle = ROOMS[current_room]['puzzle']
    question, correct_answer = puzzle
    
    # 3. Выводим вопрос
    print("🧩 Загадка:")
    print(question)
    
    # 4. Получаем ответ
    user_answer = input("Твой ответ: ").strip().lower()
    
    # 5. Сравниваем ответ
    if user_answer == correct_answer.lower():
        # 6. Ответ верный
        print("✅ Правильно! Загадка решена.")

        game_state['puzzles_solved'].add(current_room)
        print(f"🎉 Всего решено: {len(game_state['puzzles_solved'])}")
   
        
        # 7. Убираем загадку
        ROOMS[current_room]['puzzle'] = None
        
        # 8. Добавляем награду
        if ROOMS[current_room]['items']:
            reward = ROOMS[current_room]['items'][0]
            if 'items' not in game_state:
                game_state['items'] = []
            game_state['items'].append(reward)
            ROOMS[current_room]['items'].remove(reward)
            print(f"🎁 Твоя награда: {reward}")
            
            # Дополнительная подсказка про использование предмета
            print(f"💡 Теперь ты можешь использовать его вводом команды: 'use {reward}' или 'применить {reward}'")
        else:
            print("🌟 Награда: опыт и знания!")
        
        return True
    else:
        # 9. Ответ неверный
        print("❌ Неверно. Попробуй снова.")
        
        # Подсказка про возвращение позже
        print("""💭 Может вернёшься позже с новыми идеями?\
              (если хочешь покинуть комнату, введи команду 'назад' или 'back'),
              чтобы продолжить, введи команду <solve> или <решить> снова""")
        get_input(prompt="> ")

        return False
    
# TREASURE ROOM финальная игровая логика

def attempt_open_treasure(game_state):
    '''
    Пытается открыть treasure_chest в treasure_room.
    '''
    current_room = game_state['current_room']
    
    # Проверка наличия ключа
    if 'treasure_key' in game_state.get('items', []):
        print("🔑 Чтобы открыть сундук примени treasure_key")
        print("💡 Команда: use treasure_key или применить treasure_key")
        return False  # Игрок должен использовать ключ
    
    # Нет ключа → Выбор: Загадка или отказ
    else:
        choice = input("Попробовать ввести код? (да/нет): ").strip().lower()
    
        if choice not in ['да', 'yes', 'y']:
            print("Ты отступаешь от сундука.")
            return False
        else:    
            print("""Сундук заперт. На сундуке надпись:
                  В печали молчит, а в счастье поёт,
                  Без неё — тело есть, а человек не живёт.
                  Она не стареет, не рвётся, не тлеет,
                  А лишь растёт, если сердце умеет.""")
    
    
    # 3 попытки загадки
    correct_answer = 'душа'
    for attempt in range(3):
        user_answer = input("Твой ответ: \n> ").strip().lower()
        
        if user_answer == correct_answer:
            # Победа!
            if 'treasure_chest' in ROOMS[current_room]['items']:
                ROOMS[current_room]['items'].remove('treasure_chest')
            print("Ты применил верный код и замок щёлкает. Сундук открыт!")
            print("🏆 В сундуке сокровище! Это победа!")
            game_state['game_over'] = True
            return True
        
        print(f"❌ Неверный код. Осталось попыток: {2 - attempt}")
    
    # Завершение игры после 3 неудачных попыток
    print("Игра окончена. Сокровище добыть не удалось.")
    print("🔄 Запусти игру заново: введи в терминале команду make run")
    game_state['game_over'] = True
    return True

def prevent_take_chest(game_state, item_name):
    '''Блокирует взятие treasure_chest'''
    if item_name == 'treasure_chest':
        print("❌ Вы не можете поднять сундук, он слишком тяжелый.")
        return True
    return False

# Модуль: генерация псевдослучайных чисел

# Импорты для данной функции (перенесены в начало)
# from labyrinth_game import SIN_MULTIPLIER, STRETCH_FACTOR
# import math
# from typing import Union

# Создание генератора
def pseudo_random(seed: int, modulo: int) -> int:
    """
    Высокопроизводительный генератор псевдослучайных чисел [0, modulo).
    Алгоритм (математически предсказуемый):
    1. sin(seed × SIN_MULTIPLIER) → [-1, 1]
    2. × STRETCH_FACTOR → "размазывание"
    3. {x} = x % 1 → [0, 1) (дробная часть)
    4. × modulo → [0, modulo)
    5. int() → целое число в диапазоне [0, modulo)

    Args:
        seed: Последовательное значение (например, game_state['steps'])
        modulo: Верхняя граница диапазона (должно быть > 0)
    Returns:
        int: Число в диапазоне [0, modulo)
    Raises:
        ValueError: если modulo <= 0
        TypeError: если seed не является int
    """
    
    # Валидация входных данных
    if not isinstance(seed, int):
        raise TypeError(f"seed должен быть int, получено: {type(seed)}")
    if modulo <= 0:
        raise ValueError(f"modulo должно быть > 0, получено: {modulo}")

    # Основной расчёт
    sin_value = math.sin(seed * SIN_MULTIPLIER) # синус от seed,
    # умноженный на большое число с дробной частью (константа)
    stretched = sin_value * STRETCH_FACTOR # соответствует задаче:
    # Результат умножьте на другое большое число с дробной частью
    # чтобы "размазать" значения
    fractional = stretched % 1 # получение дробной части от результата вычислений
    result = int(fractional * modulo) # реализована задача отбросить дробную часть
    # и получить целое число через встроенную функцию int()

    return result

# utils.py
def trigger_trap(game_state: dict) -> None:
    """
    ЛОВУШКА v15: ✅ Количество артефактов ДО потери + упрощенная проверка ПОСЛЕ
    """
    print("Ловушка активирована! Пол стал дрожать…")
    
    # Инициализация
    if 'items' not in game_state:
        game_state['items'] = []
    if 'steps' not in game_state:
        game_state['steps'] = 0
    if 'current_room' not in game_state:
        game_state['current_room'] = 'start'
        
    items = game_state['items']
    current_room = game_state['current_room']
    lost_item = None
    
    # Инициализация структуры комнаты
    if 'rooms' not in game_state:
        game_state['rooms'] = {}
    if current_room not in game_state['rooms']:
        game_state['rooms'][current_room] = {'items': [], 'charmed_item': None}
    
    # ✅ 1. ПРОВЕРКА АРТЕФАКТОВ ДО потери (КОЛИЧЕСТВО + ПЕРЕЧЕНЬ)
    artifacts_before = [item for item in items if item in ['candle', 'silver_cross']]
    artifacts_count = len(artifacts_before)
    
    if artifacts_count > 0:
        print(f"У тебя {artifacts_count} артефактов(а): {', '.join(artifacts_before)}")
    
    # 2. ПОТЕРЯ СЛУЧАЙНОГО ПРЕДМЕТА → в комнату как charmed_item
    if items:
        item_index = pseudo_random(game_state['steps'], len(items))
        lost_item = items.pop(item_index)
        print(f"Ты потерял предмет: {lost_item}")
        
        # ✅ ПЕРЕМЕЩАЕМ в комнату как заколдованный артефакт
        game_state['rooms'][current_room]['charmed_item'] = lost_item
        print(f"📦 {lost_item} теперь заколдованный артефакт в комнате!")
        
    else:
        print("У тебя нет предметов для потери.")
        lost_item = None
    
    # ✅ 3. ПРОВЕРКА АРТЕФАКТОВ ПОСЛЕ ПОТЕРИ (упрощенная)
    has_candle = 'candle' in items
    has_silver_cross = 'silver_cross' in items
    
    # ЛОГИКА: если БЫЛ хотя бы 1 артефакт ДО потери
    if artifacts_count > 0:
        print("Ты можешь отпугнуть духов и вернуть потерянный предмет: ")
        print("примени 1 из артефактов, полученных в часовне ")
        print("(для этого введи команду 'use ' или 'применить' и название нужного артефакта).")
        
        # Возможность посмотреть артефакты
        while True:
            try:
                cmd = get_input(prompt="> ").strip().lower()
                
                # ✅ ПОКАЗ АРТЕФАКТОВ
                if cmd in ['items', 'артефакты']:
                    current_artifacts = [item for item in items if item in ['candle', 'silver_cross']]
                    if current_artifacts:
                        print(f"Твои артефакты: {', '.join(current_artifacts)}")
                    else:
                        print("У тебя нет артефактов.")
                    continue
                
                # ✅ СТРОГАЯ ПРОВЕРКА 4 КОМАНД
                valid_commands = [
                    "use candle",
                    "применить candle", 
                    "use silver_cross",
                    "применить silver_cross"
                ]
                
                if cmd in valid_commands and lost_item:
                    # ✅ ПРОВЕРКА ТЕКУЩЕГО состояния (упрощенная)
                    if (cmd in ["use candle", "применить candle"] and has_candle) or \
                       (cmd in ["use silver_cross", "применить silver_cross"] and has_silver_cross):
                        
                        # ✅ ВОЗВРАТ ПОТЕРЯННОГО ПРЕДМЕТА
                        items.append(lost_item)
                        game_state['rooms'][current_room]['charmed_item'] = None
                        print(f"✅ Артефакт сработал! {lost_item} возвращен в инвентарь!")
                        print(f"📦 Инвентарь: {', '.join(items)}")
                        print("Игра продолжается!")
                        return
                    else:
                        print("❌ У тебя нет этого артефакта!")
                        break
                else:
                    print("Ты не применил артефакт. Предмет остался заколдованным в комнате.")
                    print("В комнате присутствует заколдованный артефакт, ты можешь взять его, ")
                    print("применив один из артефактов, найденных в часовне.")
                    break
                    
            except (KeyboardInterrupt, EOFError):
                print("\nПрерывание... игра окончена.")
                game_state['game_over'] = True
                return
    
    # 4. НЕТ АРТЕФАКТОВ → УРОН 0-13
    else:
        damage = pseudo_random(game_state['steps'], 14)
        print(f"Нанесён урон: {damage}")
        
        if damage in [0, 4, 13]:
            print("Игра окончена. Сокровище добыть не удалось.")
            print("🔄 Запусти игру заново: введи в терминале команду make run")
            game_state['game_over'] = True
        else:
            print("Нанесён урон, но он не смертельный, ты можешь продолжить игру")
            print("В комнате присутствует заколдованный артефакт, ты можешь взять его, ")
            print("применив один из артефактов, найденных в часовне.")
            back(game_state)
