# ============================================================
# core/recipe.py - Load and validate recipes
# Protocol 4.2.0 v2.0
# ============================================================
import json
import os

RECIPES_DIR = os.path.join(os.path.dirname(__file__), "..", "knowledge", "recipes")

VALID_ROTATIONS = [0, 90, 180, 270, -90, -180, -270, 360]


def normalize_rotation(rot):
    """Normalize rotation to 0/90/180/270."""
    rot = rot % 360
    if rot < 0:
        rot += 360
    # Round to nearest 90
    rot = round(rot / 90) * 90
    return rot % 360


def list_recipes():
    """List all recipes in knowledge/recipes/."""
    if not os.path.exists(RECIPES_DIR):
        return []
    return sorted([f[:-5] for f in os.listdir(RECIPES_DIR) if f.endswith(".json")])


def load_recipe(name):
    """Load recipe by name from knowledge/recipes/."""
    path = os.path.join(RECIPES_DIR, name + ".json")
    if not os.path.exists(path):
        return None, ["Recipe not found: " + name]
    with open(path, encoding="utf-8-sig") as f:
        try:
            data = json.load(f)
        except Exception as e:
            return None, ["JSON parse error: " + str(e)]
    return data, []


def load_recipe_file(path):
    """Load recipe from custom path."""
    if not os.path.exists(path):
        return None, ["File not found: " + path]
    with open(path, encoding="utf-8-sig") as f:
        try:
            data = json.load(f)
        except Exception as e:
            return None, ["JSON parse error: " + str(e)]
    return data, []


def validate_recipe(recipe, kit_models=None):
    """Validate recipe structure.
    
    recipe: dict
    kit_models: {kit_name: [model1, model2, ...]} - optional for model existence check
    Returns: (ok, errors, warnings)
    """
    errors = []
    warnings = []

    if not isinstance(recipe, dict):
        return False, ["Recipe must be a JSON object"], []

    name = recipe.get("name")
    if not name:
        errors.append("Missing required field: 'name'")

    # Determine type
    has_objects = "objects" in recipe
    has_generator = "generator" in recipe

    if has_objects and has_generator:
        errors.append("Recipe cannot have both 'objects' and 'generator'")
        return False, errors, warnings

    if not has_objects and not has_generator:
        errors.append("Recipe must have 'objects' (static) or 'generator' (parametric)")
        return False, errors, warnings

    if has_objects:
        # Static recipe
        objects = recipe.get("objects", [])
        if not isinstance(objects, list):
            errors.append("'objects' must be a list")
            return False, errors, warnings

        for i, obj in enumerate(objects):
            prefix = "objects[{}]".format(i)
            if not isinstance(obj, dict):
                errors.append("{} must be an object".format(prefix))
                continue

            kit = obj.get("kit")
            model = obj.get("model")
            pos = obj.get("pos")
            rot = obj.get("rot", 0)

            if not kit:
                errors.append("{}: missing 'kit'".format(prefix))
            elif kit_models and kit not in kit_models:
                errors.append("{}: unknown kit '{}'".format(prefix, kit))

            if not model:
                errors.append("{}: missing 'model'".format(prefix))
            elif kit_models and kit in kit_models and model not in kit_models[kit]:
                errors.append("{}: model '{}' not found in kit '{}'".format(prefix, model, kit))

            if not pos:
                errors.append("{}: missing 'pos'".format(prefix))
            elif not isinstance(pos, list) or len(pos) != 2:
                errors.append("{}: 'pos' must be [X, Z]".format(prefix))

            if rot not in VALID_ROTATIONS:
                errors.append("{}: rot must be one of {}, got {}".format(
                    prefix, [0, 90, 180, 270], rot))

    if has_generator:
        # Parametric recipe
        gen = recipe.get("generator")
        if not isinstance(gen, str):
            errors.append("'generator' must be a string")

    return len(errors) == 0, errors, warnings


def print_errors(name, errors):
    """Print errors in readable format."""
    if not errors:
        return
    print("")
    print("[RECIPE ERROR] Recipe '{}':".format(name))
    for e in errors:
        print("  - {}".format(e))
    print("")