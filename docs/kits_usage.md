# Kit Usage Analysis

Анализ использования моделей из Kit-библиотек.

## Текущее состояние

| Kit | Всего моделей | Используется | Не используется |
|---|---|---|---|
| nature_kit | 329 | 2 | 327 |
| fantasy_town | 167 | 17 | 150 |
| **Итого** | **496** | **19** | **477** |

**Вывод:** используем ~4% возможностей Kit-ов.

## Используемые модели

### nature_kit (2 из 329)

| Модель | Где | Кол-во |
|---|---|---|
| tree_default | village.json | 2 |
| tree_oak | village.json | 2 |

### fantasy_town (17 из 167)

| Модель | Где | Кол-во |
|---|---|---|
| wall | castle, village | 71 |
| fence | village | 81 |
| road | village | 35 |
| wall-corner | castle, village | 20 |
| roof-gable | village | 13 |
| wall-window-small | castle | 12 |
| lantern | castle, village | 12 |
| roof-gable-end | village | 8 |
| hedge | village | 4 |
| hedge-large | castle | 4 |
| wall-window-stone | village | 4 |
| wall-doorway-square-wide | castle, village | 5 |
| roof-high-point | castle | 6 |
| fountain-square | castle, village | 2 |
| fountain-center | castle, village | 2 |
| cart | castle, village | 3 |
| cart-high | castle | 2 |

## Доступные, но НЕ используемые модели

### nature_kit — 327 моделей

**Деревья (60+):**
- tree_palm, tree_palmBend, tree_palmDetailedShort, tree_palmDetailedTall, tree_palmShort, tree_palmTall
- tree_pineDefaultA, tree_pineDefaultB, tree_pineGroundA, tree_pineGroundB
- tree_pineRoundA-F, tree_pineSmallA-D, tree_pineTallA-D
- tree_blocks, tree_cone, tree_detailed, tree_fat, tree_oak, tree_plateau, tree_simple, tree_small, tree_thin
- tree_default_dark, tree_oak_dark, tree_*_fall (осенние)

**Камни (30+):**
- rock_largeA-F, rock_smallA-I, rock_smallFlatA-C, rock_smallTopA-B, rock_tallA-J

**Утёсы (30):**
- cliff_block, cliff_blockCave, cliff_blockSlope, cliff_corner* (8 вариантов)
- cliff_steps, cliff_waterfall, cliff_waterfallTop, cliff_topDiagonal

**Растительность (~50):**
- plant_*, bush_*, grass_*, flower_*, mushroom_*, cactus_short, cactus_tall

**Лагерь (~15):**
- campfire_*, tent, bed, bed_floor, log_pile, stump

**Постройки (~60):**
- bridge_* (20 вариантов), fence_*, path_*, wall_*
- boat_*, raft, dock_*

### fantasy_town — 150 моделей

**Стены (30+):**
- wall-arch, wall-arch-top, wall-arch-top-detail
- wall-block, wall-block-half, wall-broken
- wall-corner-detail, wall-corner-diagonal, wall-corner-edge, wall-curved
- wall-detail-cross, wall-detail-diagonal, wall-detail-horizontal
- wall-diagonal, wall-door

**Крыши (20+):**
- roof, roof-corner, roof-corner-inner, roof-corner-round
- roof-flat, roof-gable-detail, roof-gable-top
- roof-high, roof-high-corner, roof-high-corner-round, roof-high-flat,
- roof-high-gable, roof-high-gable-detail, roof-high-gable-end, roof-high-gable-top
- roof-high-left, roof-high-point, roof-high-window, roof-window

**Двери (12):**
- wall-doorway-base, wall-doorway-round, wall-doorway-square
- wall-wood-door, wall-wood-doorway-base, wall-wood-doorway-round
- wall-wood-doorway-square, wall-wood-doorway-square-wide-curved

**Окна (12):**
- wall-window-glass, wall-window-round, wall-window-shutters
- wall-wood-window-glass, wall-wood-window-round, wall-wood-window-shutters
- wall-wood-window-small, wall-wood-window-stone

**Фонтаны (~12):**
- fountain-center, fountain-corner, fountain-corner-inner, fountain-corner-inner-square
- fountain-curved, fountain-edge, fountain-round, fountain-round-detail,
- fountain-square, fountain-square-detail

**Изгороди (8):**
- hedge, hedge-curved, hedge-gate, hedge-large, hedge-large-curved, hedge-large-gate

**Заборы (5):**
- fence, fence-broken, fence-curved, fence-gate

**Декор:**
- balcony-wall, balcony-wall-fence
- banner-green, banner-red
- chimney, chimney-base, chimney-top
- pillar-stone, pillar-wood
- planks, planks-half, planks-opening
- poles, poles-horizontal
- overhang, blade, road

## План улучшения

### Улучшить castle.json

1. **Крыши башен** — использовать разные:
   - roof-high-gable, roof-high-corner, roof-high-flat
2. **Декор стен** — добавить:
   - banner-red, banner-green (знамёна)
   - pillar-stone (колонны у входа)
   - chimney (дымоходы)
3. **Разнообразить ворота:**
   - wall-doorway-round, wall-doorway-square

### Улучшить village.json

1. **Разные дома:**
   - 3x3, 4x3, 5x5, 2x2
   - разные крыши: roof-gable, roof-high-gable, roof-flat
   - разные окна: wall-window-round, wall-window-shutters
2. **Инфраструктура:**
   - амбар, кузница, таверна
3. **Природа:**
   - палмы, сосны, толстые деревья, скалы, мосты

### Создать новые генераторы

1. **generate_dungeon.py** — подземелье с комнатами
2. **generate_market.py** — рыночная площадь
3. **generate_camp.py** — лагерь путешественников
4. **generate_harbor.py** — порт с лодками

## Как использовать этот документ

1. **Перед созданием нового генератора** — посмотреть доступные модели.
2. **Перед добавлением нового Kit-а** — проверить, не хватает ли моделей из существующих.
3. **При заказе карты** — посмотреть, какие модели можно использовать.

## Обновление документа

Запустить на PC:

    blender --background --python update_kits_usage.py

Скрипт пересчитает использование моделей и обновит этот файл.