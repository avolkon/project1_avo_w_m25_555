Как выглядит современный pyproject.toml (PEP 621)
toml

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[project]
name = "my-project"
version = "0.1.0"
description = "My awesome project"
readme = "README.md"
requires-python = ">=3.8"
authors = [
    {name = "Your Name", email = "you@example.com"},
]
dependencies = [
    "requests>=2.25.0",
    "click>=8.0.0",
]

[project.scripts]
my-cli = "my_project.cli:main"


Как выглядел старый формат (Poetry‑specific)
toml

[tool.poetry]
name = "my-project"
version = "0.1.0"
description = "My awesome project"
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.8"
requests = "^2.25"
click = "^8.0"


[tool.poetry.scripts]
my-cli = "my_project.cli:main"


[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"


Разница между [tool.poetry] и [project] в pyproject.toml — это эволюция стандарта конфигурации Python‑проектов и совместимость разных версий Poetry.

Почему так происходит
Исторический контекст

Раньше Poetry использовал секцию [tool.poetry] как единственный способ описания проекта.

Это было нестандартным решением: официальный PEP 621 (2021 г.) предписывает использовать [project].

Переход на стандарт PEP 621

С версии Poetry 1.2+ (2022 г.) инструмент начал поддерживать [project] для совместимости со стандартом.

Но сохранил [tool.poetry] для обратной совместимости с старыми проектами.

Двойная поддержка

Современные версии Poetry читают обе секции:

Если есть [project] — используют его.

Если нет — fallback к [tool.poetry].

При создании нового проекта через poetry init сейчас чаще генерируется [project].

Проблема в вашем pyproject.toml — ошибка синтаксиса и некорректные настройки. Разберём по пунктам.

Ошибки в текущем файле
Лишний пробел перед packages
В строке  packages = [...] есть невидимый пробел в начале. TOML‑парсер игнорирует такую строку, поэтому Poetry не видит секцию packages.

Некорректный путь к пакету
Вы указали { include = "labyrinth_game" }, но Poetry не знает, где искать эту папку (нет параметра from).

Неверное имя скрипта
project = "labyrinth_game.main:main" — если в main.py нет функции main(), запуск через poetry run project не сработает.

[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"

[project]
name = "project1_avo_m25_555"
version = "0.1.0"
description = "ДЗ1 Игра Лабиринт сокровищ Анастасия Волконская НИЯУ МИФИ Python"
authors = [
    {name = "avo", email = "aavolkon@mail.ru"}
]
readme = "README.md"
requires-python = ">=3.11"
dependencies = []

# Указываем пакет и его расположение
packages = [
    { include = "labyrinth_game", from = "." },  # "." означает текущую папку
]

[project.scripts]
# Если в main.py есть функция main():
labyrinth = "labyrinth_game.main:main"
# Или просто укажите модуль (если хотите запускать как `python -m ...`):
# labyrinth = "labyrinth_game.main"

