# rbxgen

**Roblox Map Factory** — сборка карт из открытых CC0-библиотек.

Protocol: **4.2.0**

## Что это

rbxgen — инструмент для **автоматической сборки 3D-карт** из бесплатных
моделей (Kenney Kit) через JSON-описания.

**Одна команда — готовая карта в Roblox Studio.**

## Архитектура

Kit-библиотека -> JSON-карта -> Blender -> Studio
assets_cache/  -> maps/*.json -> build_map.py -> FBX import
(Kenney CC0)      (объекты +      (сборка +        (готово)
                   позиции)        preview)

## Что работает

| Компонент | Что делает |
|---|---|
| core/downloader.py | Скачивание CC0 Kit с OpenGameArt |
| core/importer.py | Импорт OBJ + scale + rotation + snap-to-ground |
| core/map_builder.py | Сборка карты из JSON |
| core/preview.py | 4-видовой preview (top, front, side, iso) |
| core/kit_analyzer.py | Анализ всех моделей Kit |
| build_map.py | CLI сборки |
| generate_castle.py | Генератор крепости (78 объектов) |
| generate_village.py | Генератор деревни (217 объектов) |

## Быстрый старт

### 1. Скачать Kit

    blender --background --python-expr "import sys; sys.path.insert(0,'.'); from core.downloader import get_asset; get_asset('fantasy_town')"

### 2. Сгенерировать карту

    python3 generate_castle.py
    python3 generate_village.py

### 3. Собрать в Blender

    blender --background --python build_map.py -- maps/castle.json
    blender --background --python build_map.py -- maps/village.json

### 4. Импорт в Studio

- Roblox Studio: Home -> Import 3D -> выбрать Castle_Test.fbx
- Anchored через Command Bar

## Доступные Kit

| Kit | Моделей | Источник |
|---|---|---|
| nature_kit | 329 | OpenGameArt |
| fantasy_town | 167 | OpenGameArt |

## Формат JSON-карты

    {
      "name": "Map_Name",
      "level": "FULL",
      "budget_tris": 20000,
      "ground": {
        "size": [100, 100],
        "thickness": 0.5,
        "material": "dirt"
      },
      "objects": [
        {
          "kit": "fantasy_town",
          "model": "wall",
          "pos": [X, Z],
          "scale": 4.0,
          "rotation": 0,
          "material": "stone"
        }
      ]
    }

ВАЖНО:
- pos = [X, Z] — горизонтальные координаты.
- Высота всегда 0 (объект автоматически на земле).
- rotation — в градусах вокруг вертикальной оси.

## Повороты для стен

| Сторона | rotation |
|---|---|
| Юг (-Z) | 0 |
| Север (+Z) | 180 |
| Запад (-X) | 90 |
| Восток (+X) | -90 |

## Правила стыковки

См. docs/modular_rules.md.

## Лицензия

- Модели: CC0 (Public Domain) — Kenney.nl, OpenGameArt.org
- Код: MIT
