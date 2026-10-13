# rbxgen

**Roblox Object Factory** — генератор детализированных 3D-объектов для Roblox через Blender.

Версия протокола: **4.2.0**

## Что это

`rbxgen` — система из **паттернов** (Blender-функций), которые собираются в объекты по **JSON-пресетам**.

## Ключевые возможности

- 135 паттернов в 15 категориях
- CLI-генератор: `blender --background --python rbxgen.py -- <preset>`
- Валидатор геометрии (BASE / EXTENDED / FULL)
- JSON-отчёты на каждый объект
- FBX-экспорт с пресетом Roblox
- Luau-генератор (Phase 2)

## Структура



## Установка

Требуется Blender 3.6+ (LTS) и Python 3.10+ (встроен в Blender).

## Использование

```bash
blender --background --python rbxgen.py -- list
blender --background --python rbxgen.py -- tree
blender --background --python rbxgen.py -- house_detailed

---

## ШАГ 2 — .gitignore

```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/

# Blender
*.blend1
*.blend2

# OS
.DS_Store
Thumbs.db
desktop.ini

# IDE
.vscode/
.idea/
*.swp

# Project
reports/*.json
!reports/.gitkeep
assets_cache/
.env
