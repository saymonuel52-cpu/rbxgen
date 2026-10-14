# ============================================================
# core/downloader.py - Download free 3D assets
# Protocol 4.2.0 | Source: OpenGameArt.org (CC0)
# ============================================================
import os
import urllib.request
import zipfile
import json

CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "assets_cache")


def ensure_cache():
    """Ensure cache directory exists."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    return CACHE_DIR


def download_file(url, dest_path):
    """Download file from URL to dest_path."""
    try:
        print("[DOWNLOAD] {}".format(url))
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=60) as response:
            with open(dest_path, 'wb') as f:
                f.write(response.read())
        print("[OK] -> {}".format(dest_path))
        return True
    except Exception as e:
        print("[ERROR] {}".format(e))
        return False


def download_and_extract(name, url, extract_subdir=None):
    """Download ZIP and extract."""
    cache = ensure_cache()
    if extract_subdir:
        extract_path = os.path.join(cache, extract_subdir)
    else:
        extract_path = os.path.join(cache, name)

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


# ============================================================
# OpenGameArt.org assets (CC0, stable)
# ============================================================
OGA_ASSETS = {
    "nature_kit": {
        "url": "https://opengameart.org/sites/default/files/Nature%20Kit%20%282.1%29.zip",
        "subdir": "nature_kit",
    },
    "nature_pack_extended": {
        "url": "https://opengameart.org/sites/default/files/naturePack_extended.zip",
        "subdir": "nature_pack_extended",
    },
}


def get_asset(asset_name):
    """Download OGA asset by name."""
    if asset_name not in OGA_ASSETS:
        print("[ERROR] Unknown asset: {}".format(asset_name))
        print("[INFO] Available: {}".format(list(OGA_ASSETS.keys())))
        return None
    info = OGA_ASSETS[asset_name]
    return download_and_extract(asset_name, info["url"], info["subdir"])


def list_assets():
    """List available assets."""
    return list(OGA_ASSETS.keys())