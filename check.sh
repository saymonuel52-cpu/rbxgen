#!/data/data/com.termux/files/usr/bin/bash
# ============================================================
# check.sh — Все проверки rbxgen + git push
# Protocol 4.2.0
# ============================================================
set -e
cd "$(dirname "$0")"

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "============================================================"
echo "  rbxgen — AUTO CHECK"
echo "============================================================"
echo ""

# ============================================================
# 1. SYNTAX CHECK — Python
# ============================================================
echo "=== [1/4] PYTHON SYNTAX ==="
PY_OK=0
PY_FAIL=0
for f in rbxgen.py core/*.py patterns/*.py; do
    if [ -f "$f" ]; then
        if python3 -c "import ast; ast.parse(open('$f').read())" 2>/dev/null; then
            echo -e "  ${GREEN}✓${NC} $f"
            PY_OK=$((PY_OK + 1))
        else
            echo -e "  ${RED}✗${NC} $f"
            PY_FAIL=$((PY_FAIL + 1))
        fi
    fi
done
echo "  Итого: $PY_OK OK, $PY_FAIL fail"
echo ""

# ============================================================
# 2. JSON CHECK — presets
# ============================================================
echo "=== [2/4] JSON VALIDATION ==="
JSON_OK=0
JSON_FAIL=0
for f in presets/*.json; do
    if [ -f "$f" ]; then
        if python3 -m json.tool "$f" > /dev/null 2>&1; then
            echo -e "  ${GREEN}✓${NC} $f"
            JSON_OK=$((JSON_OK + 1))
        else
            echo -e "  ${RED}✗${NC} $f"
            JSON_FAIL=$((JSON_FAIL + 1))
        fi
    fi
done
echo "  Итого: $JSON_OK OK, $JSON_FAIL fail"
echo ""

# ============================================================
# 3. PATTERNS COUNT — правильный подсчёт
# ============================================================
echo "=== [3/4] PATTERNS COUNT ==="
python3 << 'PYEOF'
import ast

tree = ast.parse(open('patterns/__init__.py').read())
categories = {}

for node in ast.walk(tree):
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == 'REGISTRY':
                if isinstance(node.value, ast.Dict):
                    for key, val in zip(node.value.keys, node.value.values):
                        if isinstance(key, ast.Constant) and isinstance(key.value, str):
                            if isinstance(val, ast.Dict):
                                for k, v in zip(val.keys, val.values):
                                    if (isinstance(k, ast.Constant)
                                        and k.value == 'category'
                                        and isinstance(v, ast.Constant)):
                                        cat = v.value
                                        categories[cat] = categories.get(cat, 0) + 1

total = sum(categories.values())
print(f"  Всего паттернов: {total}")
print(f"  По категориям:")
for cat in sorted(categories):
    print(f"    {cat:15s} {categories[cat]}")
PYEOF
echo ""

# ============================================================
# 4. GIT STATUS + PUSH
# ============================================================
echo "=== [4/4] GIT STATUS ==="
if [ -z "$(git status --porcelain)" ]; then
    echo -e "  ${YELLOW}Нет изменений — push не требуется${NC}"
else
    echo "  Изменения:"
    git status --short | sed 's/^/    /'
    echo ""
    echo "  Добавляю..."
    git add .
    echo "  Коммит..."
    git commit -m "auto: update $(date '+%Y-%m-%d %H:%M')" > /dev/null
    echo "  Push..."
    git push
    echo ""
    echo -e "  ${GREEN}✓ Запушено${NC}"
fi
echo ""

# ============================================================
# ИТОГ
# ============================================================
echo "============================================================"
if [ $PY_FAIL -eq 0 ] && [ $JSON_FAIL -eq 0 ]; then
    echo -e "  ${GREEN}ВСЁ ОК${NC}  |  Python: $PY_OK  |  JSON: $JSON_OK"
else
    echo -e "  ${RED}ЕСТЬ ОШИБКИ${NC}  |  Python fail: $PY_FAIL  |  JSON fail: $JSON_FAIL"
    exit 1
fi
echo "============================================================"
