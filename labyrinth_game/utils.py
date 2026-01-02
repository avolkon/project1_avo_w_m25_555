# utils.py
from constants import ROOMS

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

