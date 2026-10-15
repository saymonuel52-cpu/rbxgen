# JSON Reference — формат карт rbxgen

Шпаргалка по созданию карт.

## Структура карты

    {
      "name": "Map_Name",
      "level": "FULL",
      "budget_tris": 20000,
      "ground": { ... },
      "objects": [ ... ]
    }

| Поле | Тип | Описание |
|---|---|---|
| name | string | Имя модели в Studio |
| level | string | BASE / EXTENDED / FULL |
| budget_tris | int | Лимит треугольников |
| ground | object | Земляная площадка |
| objects | array | Список объектов |

## Ground

    {
      "size": [100, 100],
      "pos": [0, 0, 0],
      "thickness": 0.5,
      "material": "dirt"
    }

| Поле | Тип | Описание |
|---|---|---|
| size | [X, Z] | Размер в studs |
| pos | [X, Y, Z] | Центр площадки |
| thickness | float | Толщина |
| material | string | Материал |

## Object

    {
      "kit": "fantasy_town",
      "model": "wall",
      "pos": [X, Z],
      "scale": 4.0,
      "rotation": 0,
      "material": "stone"
    }

| Поле | Тип | Описание |
|---|---|---|
| kit | string | Имя набора |
| model | string | Имя модели (без .obj) |
| pos | [X, Z] | Позиция (высота = 0) |
| scale | float | Масштаб (1 модуль = scale studs) |
| rotation | int | Поворот в градусах |
| material | string | Имя материала |

## ВАЖНО

- **pos = [X, Z]** — только 2 координаты.
- **Высота всегда 0** — объект автоматически на земле.
- **rotation** — вокруг вертикальной оси.
- **1 модуль** = размер модели × scale.

## Повороты для стен

| Сторона | rotation | Направление |
|---|---|---|
| Юг | 0 | -Z |
| Север | 180 | +Z |
| Запад | 90 | -X |
| Восток | -90 | +X |

## Повороты для углов

| Угол | rotation | Позиция |
|---|---|---|
| Юго-запад (SW) | 0 | (-X, -Z) |
| Юго-восток (SE) | -90 | (+X, -Z) |
| Северо-восток (NE) | 180 | (+X, +Z) |
| Северо-запад (NW) | 90 | (-X, +Z) |

## Материалы

| Материал | Описание |
|---|---|
| wood_old | Тёмное дерево |
| wood_new | Светлое дерево |
| stone | Камень |
| iron | Железо |
| gold | Золото |
| glass | Стекло |
| fabric | Ткань |
| leather | Кожа |
| vine | Лоза |
| leaf | Листва |
| dirt | Земля |
| straw | Солома |
| galvanized | Оцинковка |

## Доступные Kit

| Kit | Моделей | Тип |
|---|---|---|
| nature_kit | 329 | Природа |
| fantasy_town | 167 | Средневековый город |

## Пример — дом 3x3

    {
      "name": "House_01",
      "objects": [
        {"kit": "fantasy_town", "model": "wall",
         "pos": [-4, -6], "scale": 4.0, "rotation": 0, "material": "wood_old"},
        {"kit": "fantasy_town", "model": "wall-doorway-square-wide",
         "pos": [0, -6], "scale": 4.0, "rotation": 0, "material": "wood_old"},
        {"kit": "fantasy_town", "model": "wall",
         "pos": [4, -6], "scale": 4.0, "rotation": 0, "material": "wood_old"},
        {"kit": "fantasy_town", "model": "wall-corner",
         "pos": [-6, -6], "scale": 4.0, "rotation": 0, "material": "wood_old"}
      ]
    }

## Полезные команды

    # Скачать Kit
    blender --background --python-expr "import sys; sys.path.insert(0,'.'); from core.downloader import get_asset; get_asset('fantasy_town')"

    # Список моделей в Kit
    blender --background --python -c "import sys; sys.path.insert(0,'.'); from core.importer import list_models; print(list_models('fantasy_town'))"

    # Собрать карту
    blender --background --python build_map.py -- maps/castle.json
