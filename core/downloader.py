# ============================================================
# core/downloader.py - Free 3D assets (OpenGameArt only)
# Protocol 4.2.0
# ============================================================
import os
import urllib.request
import zipfile

CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "assets_cache")


def ensure_cache():
    os.makedirs(CACHE_DIR, exist_ok=True)
    return CACHE_DIR


def download_and_extract(name, url, subdir):
    cache = ensure_cache()
    extract_path = os.path.join(cache, subdir)

    if os.path.exists(extract_path):
        print("[CACHE] {} already exists".format(name))
        return extract_path

    zip_path = os.path.join(cache, name + ".zip")

    try:
        print("[DOWNLOAD] {}".format(url))
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=120) as r:
            with open(zip_path, 'wb') as f:
                f.write(r.read())
        with zipfile.ZipFile(zip_path, 'r') as z:
            z.extractall(extract_path)
        os.remove(zip_path)
        print("[OK] -> {}".format(extract_path))
        return extract_path
    except Exception as e:
        print("[ERROR] {}".format(e))
        return None


# OpenGameArt direct URLs (verified)
OGA_ASSETS = {
    "nature_kit": {
        "url": "https://opengameart.org/sites/default/files/Nature%20Kit%20%282.1%29.zip",
        "subdir": "nature_kit",
    },
    "fantasy_town": {
        "url": "https://opengameart.org/sites/default/files/kenney_fantasy-town-kit_2.0.zip",
        "subdir": "fantasy_town",
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