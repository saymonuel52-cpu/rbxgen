# ============================================================
# core/downloader.py - Free 3D assets
# Protocol 4.2.0 | OpenGameArt.org (CC0)
# ============================================================
import os
import urllib.request
import zipfile

CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "assets_cache")


def ensure_cache():
    os.makedirs(CACHE_DIR, exist_ok=True)
    return CACHE_DIR


def download_file(url, dest_path):
    try:
        print("[DOWNLOAD] {}".format(url))
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=120) as response:
            with open(dest_path, 'wb') as f:
                f.write(response.read())
        print("[OK] -> {}".format(dest_path))
        return True
    except Exception as e:
        print("[ERROR] {}".format(e))
        return False


def download_and_extract(name, url, extract_subdir=None):
    cache = ensure_cache()
    extract_path = os.path.join(cache, extract_subdir or name)

    if os.path.exists(extract_path):
        print("[CACHE] {} already exists".format(name))
        return extract_path

    zip_path = os.path.join(cache, name + ".zip")

    if download_file(url, zip_path):
        try:
            with zipfile.ZipFile(zip_path, 'r') as z:
                z.extractall(extract_path)
            print("[EXTRACT] {} -> {}".format(zip_path, extract_path))
            os.remove(zip_path)
            return extract_path
        except Exception as e:
            print("[ERROR] extract: {}".format(e))
            return None
    return None


# OpenGameArt.org assets (CC0)
OGA_ASSETS = {
    "nature_kit": {
        "url": "https://opengameart.org/sites/default/files/Nature%20Kit%20%282.1%29.zip",
        "subdir": "nature_kit",
    },
    "nature_pack_extended": {
        "url": "https://opengameart.org/sites/default/files/naturePack_extended.zip",
        "subdir": "nature_pack_extended",
    },
    "castle_kit": {
        "url": "https://opengameart.org/sites/default/files/Castle%20Kit.zip",
        "subdir": "castle_kit",
    },
    "fantasy_town": {
        "url": "https://opengameart.org/sites/default/files/Fantasy%20Town%20Base.zip",
        "subdir": "fantasy_town",
    },
    "survival_kit": {
        "url": "https://opengameart.org/sites/default/files/Survival%20Kit.zip",
        "subdir": "survival_kit",
    },
    "platformer_kit": {
        "url": "https://opengameart.org/sites/default/files/Platformer%20Kit.zip",
        "subdir": "platformer_kit",
    },
    "graveyard_kit": {
        "url": "https://opengameart.org/sites/default/files/Graveyard%20Kit.zip",
        "subdir": "graveyard_kit",
    },
    "pirate_kit": {
        "url": "https://opengameart.org/sites/default/files/Pirate%20Kit.zip",
        "subdir": "pirate_kit",
    },
}


def get_asset(asset_name):
    if asset_name not in OGA_ASSETS:
        print("[ERROR] Unknown asset: {}".format(asset_name))
        print("[INFO] Available: {}".format(list(OGA_ASSETS.keys())))
        return None
    info = OGA_ASSETS[asset_name]
    return download_and_extract(asset_name, info["url"], info["subdir"])


def list_assets():
    return list(OGA_ASSETS.keys())


def download_all():
    """Download all available assets."""
    results = {}
    for name in OGA_ASSETS:
        print("")
        print("=== {} ===".format(name))
        results[name] = get_asset(name)
    return results