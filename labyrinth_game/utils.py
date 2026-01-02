# utils.py
from labyrinth_game import ROOMS, back, describe_room, get_input


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
    
    # 1. Название в верхнем регистре
    print(f"\n{'═' * 50}")
    print(f"📍 {current_room.upper()}")
    
    # 2. Описание комнаты
    print(room['description'])
    
    # 3. Предметы
    if room.get('items') and room['items']:
        print(f"💎 В комнате есть артефакты: {', '.join(room['items'])}")
    
    # 4. Выходы
    print(f"🚪 Выходы: {', '.join(room['exits'].keys())}")
    
    # 5. Загадка
    if room.get('puzzle'):
        print("🔒 Кажется, здесь есть загадка (используй команду solve).")
    
    print(f"{'═' * 50}")

# Модуль: решение загадок, с расширенным функционалом: добавлены возможности:

def solve_puzzle(game_state):
    '''
    Решает загадку в текущей комнате.
    Если загадок нет, но есть предметы - подсказывает игроку.
    '''
    current_room = game_state['current_room']
    
    # 1. Проверка наличия загадки
    if 'puzzle' not in ROOMS[current_room] or ROOMS[current_room]['puzzle'] is None:
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
            print(f"💡 Теперь ты можешь использовать его: 'use {reward}' или 'применить {reward}'")
        else:
            print("🌟 Награда: опыт и знания!")
        
        return True
    else:
        # 9. Ответ неверный
        print("❌ Неверно. Попробуй снова.")
        
        # Подсказка про возвращение позже
        print("💭 Может вернёшься позже с новыми идеями? (если хочешь покинуть комнату, введи команду 'назад' или 'back' )")
        get_input(prompt="> ")

        return False 