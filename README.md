Игра "Лабиринт сокровищ"

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