"""
import_github_sources.py - Safe GitHub Source Quarantine & Review
Strictly imports code for isolated review.
Never executes imported code automatically.
"""

import os
import json
import hashlib
import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("GitHubImporter")

def calculate_sha256(filepath: str) -> str:
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def quarantine_source_file(filename: str, content: str, target_dir: str = "staging") -> Dict[str, Any]:
    os.makedirs(target_dir, exist_ok=True)
    clean_name = os.path.basename(filename)
    dest_path = os.path.join(target_dir, clean_name)
    
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    os.chmod(dest_path, 0o644)
    file_hash = calculate_sha256(dest_path)
    manifest = {
        "file": clean_name,
        "path": dest_path,
        "sha256": file_hash,
        "quarantined": True,
        "executable": False
    }
    manifest_path = os.path.join(target_dir, f"{clean_name}.manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as mf:
        json.dump(manifest, mf, indent=2)
    logger.info("Quarantined %s (SHA256: %s)", clean_name, file_hash[:12])
    return manifest
