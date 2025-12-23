from flask import Flask, render_template, abort, send_file, request
from pathlib import Path
import json
import os
import mimetypes

BASE_DIR = Path(__file__).resolve().parent

app = Flask(
    __name__,
    template_folder=BASE_DIR / "templates",
    static_folder=BASE_DIR / "static"
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RESULT_PATH = PROJECT_ROOT / "result.json"

def load_results():
    if RESULT_PATH.exists():
        with open(RESULT_PATH, "r", encoding = "utf-8") as f:
            return json.load(f)
    
    return []

@app.route("/")
def index():
    results = load_results()

    grouped = {
        "exact_duplicates": [],
        "similar_photos": [],
        "burst_photos": [],
        "blurry_photo": [],
        "dark_photo": [],
        "large_photo": [],
        "screenshots": [],
    }
    
    for item in results:
        t = item.get("type")
        if t in grouped:
            grouped[t].append(item)
        else:
            grouped.setdefault("other", []).append(item)

    
    freed_bytes = 0.0

    for t in ("exact_duplicates", "similar_photos", "burst_photo"):
        for g in grouped.get(t, []):
            for p in g.get("suggest_delete", []):
                try:
                    freed_bytes += os.path.getsize(p)
                except OSError:
                    pass
    
    return render_template(
        "index.html",
        grouped = grouped,
        freed_mb = freed_bytes / (1024 * 1024),
        total_groups = len(grouped.get("exact_duplicates", []))
        + len(grouped.get("similar_photos", []))
        + len(grouped.get("burst_photos", [])),
    )
    
@app.route("/img")
def img():
    path = request.args.get("path")
    
    if not path:
        abort(400)

    p = Path(path)

    photos_dir = (PROJECT_ROOT / "photos").resolve()
    
    try:
        p_resolved = p.resolve()
    except:
        abort(400)

    if photos_dir not in p_resolved.parents and p_resolved != photos_dir:
        abort(403)

    if not p_resolved.exists() or not p_resolved.is_file():
        abort(404)

    mime, _ = mimetypes.guess_type(str(p_resolved))

    return send_file(str(p_resolved), mimetype = mime or "image/jpg")

if __name__ == "__main__":
    app.run(debug = True)