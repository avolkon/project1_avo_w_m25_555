from constants import ROOMS, START_ROOM, WIN_ROOM
print(f"Комнаты: {len(ROOMS)}")  # 9
print(f"Старт: {ROOMS[START_ROOM]['exits']}")  # {'north': 'hall', 'east': 'trap_room'}
print(f"Победа: {WIN_ROOM in ROOMS}")  # True

# Проверка всех exits
all_exits_valid = all(
    all(to_room in ROOMS for to_room in room_data['exits'].values())
    for room_data in ROOMS.values()
)
print(f"Все выходы валидны: {all_exits_valid}")  # True
