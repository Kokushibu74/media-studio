import os
import json
import uuid
import subprocess
import sqlite3
from pathlib import Path
from datetime import datetime
from flask import Flask, request, render_template_string, send_from_directory, redirect, url_for, flash
from werkzeug.utils import secure_filename

ROOT = Path(__file__).resolve().parent
UPLOADS = ROOT / "uploads"
OUTPUTS = ROOT / "output"
UPLOADS.mkdir(exist_ok=True)
OUTPUTS.mkdir(exist_ok=True)

ALLOWED = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff", ".heic",
           ".mp4", ".mov", ".m4v", ".mkv", ".webm", ".avi"}
PHONE_PROFILES = {
    "none": "No phone model selected",
    "samsung_galaxy_a34_5g": "Samsung Galaxy A34 5G",
    "samsung_galaxy_a54_5g": "Samsung Galaxy A54 5G",
    "samsung_galaxy_s23": "Samsung Galaxy S23",
    "samsung_galaxy_s23_ultra": "Samsung Galaxy S23 Ultra",
    "samsung_galaxy_s24": "Samsung Galaxy S24",
    "samsung_galaxy_s24_ultra": "Samsung Galaxy S24 Ultra",
    "samsung_galaxy_s25_ultra": "Samsung Galaxy S25 Ultra",
    "iphone_13": "iPhone 13",
    "iphone_14": "iPhone 14",
    "iphone_15": "iPhone 15",
    "iphone_15_pro": "iPhone 15 Pro",
    "iphone_16_pro": "iPhone 16 Pro",
    "google_pixel_7": "Google Pixel 7",
    "google_pixel_8": "Google Pixel 8",
    "google_pixel_8_pro": "Google Pixel 8 Pro",
    "google_pixel_9_pro": "Google Pixel 9 Pro",
    "redmi_note_12": "Redmi Note 12",
    "redmi_note_13_pro": "Redmi Note 13 Pro",
    "redmi_note_13_pro_plus": "Redmi Note 13 Pro+",
    "xiaomi_13t": "Xiaomi 13T",
    "xiaomi_14": "Xiaomi 14",
    "oppo_reno_11": "OPPO Reno11",
    "oppo_reno_12": "OPPO Reno12",
    "realme_12_pro_plus": "realme 12 Pro+",
    "oneplus_12": "OnePlus 12",
    "other_model": "Other / custom model label"
}
app = Flask(__name__)
app.secret_key = os.environ.get("MEDIA_STUDIO_SECRET", "change-this-local-secret")
MAX_MB = int(os.environ.get("MEDIA_STUDIO_MAX_MB", "500"))
app.config["MAX_CONTENT_LENGTH"] = MAX_MB * 1024 * 1024

HTML = r"""
<!doctype html>
<html lang="bn">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Anime Action · Media Metadata Studio</title>
<style>
:root{color-scheme:dark;--bg:#10131a;--panel:#191e29;--line:#30394b;--text:#f3f5fa;--muted:#aab4c5;--accent:#83aaff}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:16px system-ui,-apple-system,sans-serif}
main{max-width:900px;margin:auto;padding:22px 15px 50px}.hero{padding:22px;border:1px solid var(--line);border-radius:18px;background:linear-gradient(135deg,#202b40,#171b25)}
h1{font-size:clamp(25px,5vw,38px);margin:0 0 8px}.muted{color:var(--muted);line-height:1.55}.card{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:18px;margin-top:16px}
label{display:block;font-weight:650;margin:12px 0 7px}input,select,textarea{width:100%;padding:12px;border:1px solid var(--line);border-radius:10px;background:#10141d;color:var(--text);font:inherit}
input[type=file]{padding:10px}button,.btn{display:inline-block;background:var(--accent);color:#101827;border:0;border-radius:10px;padding:12px 16px;font-weight:750;font-size:15px;text-decoration:none;cursor:pointer;margin-top:14px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}.flash{padding:11px;border-radius:10px;background:#342b1c;margin:10px 0}.result{overflow-wrap:anywhere;white-space:pre-wrap;background:#10141d;border:1px solid var(--line);padding:12px;border-radius:10px;font-size:13px}
.tag{display:inline-block;border:1px solid var(--line);padding:5px 9px;border-radius:999px;color:var(--muted);font-size:13px;margin:3px 4px 3px 0}
hr{border:0;border-top:1px solid var(--line);margin:18px 0}footer{margin-top:22px;font-size:13px;color:var(--muted)}
body{background:radial-gradient(ellipse at 10% 0%,#25205b 0,transparent 42%),radial-gradient(ellipse at 95% 20%,#092e45 0,transparent 38%),var(--bg);overflow-x:hidden}
.hero{position:relative;overflow:hidden;background:linear-gradient(125deg,#1c2450,#10192b 60%,#321447);border-color:#3c5e91;box-shadow:0 0 28px #4a50ff33;animation:heroPulse 5s ease-in-out infinite}
.hero:after{content:"";position:absolute;left:-30%;right:-30%;height:2px;top:0;background:linear-gradient(90deg,transparent,#69f5ff,white,#ff4fd8,transparent);animation:scan 5s linear infinite}
.card{background:linear-gradient(145deg,#151d33,#0e1424);border-color:#2c3c63;box-shadow:0 12px 35px #0003;animation:riseIn .4s ease both}
button,.btn{background:linear-gradient(100deg,#69f5ff,#9bb6ff 55%,#e58bff);color:#080d1c;box-shadow:0 0 20px #69f5ff20;transition:transform .18s,filter .18s}
button:hover,.btn:hover{transform:translateY(-2px);filter:brightness(1.12);box-shadow:0 0 25px #69f5ff55}
.tag{border-color:#3a527f;background:#141d35aa;color:#b8faff}
@keyframes scan{0%{transform:translateY(0)}100%{transform:translateY(240px)}}
@keyframes heroPulse{0%,100%{box-shadow:0 0 22px #4a50ff22}50%{box-shadow:0 0 38px #4a50ff55,0 0 18px #ff4fd833}}
@keyframes riseIn{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
body{background:radial-gradient(ellipse at 10% 0%,#25205b 0,transparent 42%),radial-gradient(ellipse at 95% 20%,#092e45 0,transparent 38%),var(--bg);overflow-x:hidden}
.hero{position:relative;overflow:hidden;background:linear-gradient(125deg,#1c2450,#10192b 60%,#321447);border-color:#3c5e91;box-shadow:0 0 28px #4a50ff33;animation:heroPulse 5s ease-in-out infinite}
.hero:after{content:"";position:absolute;left:-30%;right:-30%;height:2px;top:0;background:linear-gradient(90deg,transparent,#69f5ff,white,#ff4fd8,transparent);animation:scan 5s linear infinite}
.card{background:linear-gradient(145deg,#151d33,#0e1424);border-color:#2c3c63;box-shadow:0 12px 35px #0003;animation:riseIn .4s ease both}
button,.btn{background:linear-gradient(100deg,#69f5ff,#9bb6ff 55%,#e58bff);color:#080d1c;box-shadow:0 0 20px #69f5ff20;transition:transform .18s,filter .18s}
button:hover,.btn:hover{transform:translateY(-2px);filter:brightness(1.12);box-shadow:0 0 25px #69f5ff55}
.tag{border-color:#3a527f;background:#141d35aa;color:#b8faff}
@keyframes scan{0%{transform:translateY(0)}100%{transform:translateY(240px)}}
@keyframes heroPulse{0%,100%{box-shadow:0 0 22px #4a50ff22}50%{box-shadow:0 0 38px #4a50ff55,0 0 18px #ff4fd833}}
@keyframes riseIn{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
</style></head><body><main>
<div class="hero"><h1>⚡ ANIME ACTION <span style="color:#69f5ff">MEDIA STUDIO</span></h1><div class="muted">LOCAL SCAN // METADATA ANALYSIS // PRIVACY CLEANING</div>
<p class="muted">এই অ্যাপটি আপনার Termux ডিভাইসেই চলে। ফাইলগুলো কোনো ক্লাউড সার্ভারে পাঠানো হয় না।</p>
<span class="tag">Images</span><span class="tag">Videos</span><span class="tag">ExifTool</span><span class="tag">FFprobe</span></div>
{% with messages = get_flashed_messages() %}{% for m in messages %}<div class="flash">{{m}}</div>{% endfor %}{% endwith %}
<section class="card"><h2>১. ফাইল আপলোড ও পরীক্ষা</h2><p class="muted">সর্বোচ্চ ফাইল সাইজ: {{max_mb}} MB। সমর্থিত ছবি ও ভিডিও ফরম্যাট।</p>
<form method="post" action="/process" enctype="multipart/form-data">
<label>ফাইল নির্বাচন করুন</label><input type="file" name="media" accept="image/*,video/*" required>
<div class="grid"><div><label>ফোনের মডেল নির্বাচন (model preset)</label><select name="profile">{% for k,v in profiles.items() %}<option value="{{k}}">{{v}}</option>{% endfor %}</select></div>
<div><label>প্রজেক্ট / ক্যাটাগরি</label><input name="category" maxlength="100" placeholder="যেমন: Travel / Portfolio"></div></div>
<label>নিজস্ব ট্যাগ / বিবরণ</label><input name="custom_comment" maxlength="500" placeholder="নিজের নোট বা বিবরণ">
<label><input type="checkbox" name="clean" value="yes" checked style="width:auto"> আউটপুট কপিতে সমর্থিত মেটাডাটা পরিষ্কার করার চেষ্টা করুন</label>
<button type="submit" id="processBtn">⚡ SCAN &amp; PROCESS</button><p id="scanStatus" class="muted" style="display:none">◈ SCANNING FILE · ANALYZING METADATA · PLEASE WAIT...</p>
</form></section>
{% if result %}
<section class="card"><h2>২. বিশ্লেষণের ফলাফল</h2>
<p><b>ফাইল:</b> {{result.original}}</p><p><b>ধরন:</b> {{result.kind}}</p>
<p><b>AI-সম্পর্কিত প্রমাণ:</b> {{result.ai_status}}</p><p class="muted">{{result.ai_explanation}}</p>
<p><b>প্রসেসিং:</b> {{result.processing}}</p>
{% if result.output %}<p><a class="btn" href="{{url_for('download', filename=result.output)}}">আউটপুট ডাউনলোড</a></p>{% endif %}
<h3>মেটাডাটা (সংক্ষিপ্ত রিপোর্ট)</h3><div class="result">{{result.metadata}}</div>
{% if result.tags %}<h3>অ্যাপের কাস্টম ট্যাগ</h3><div class="result">{{result.tags}}</div>{% endif %}
<p class="muted">কাস্টম প্রোফাইলটি আলাদা sidecar JSON ফাইলে রাখা হয়; এটি প্রকৃত ক্যামেরা মডেল বা ক্যাপচার-ইতিহাস হিসেবে ফাইলে জাল করা হয় না।</p>
</section>{% endif %}



<section class="card"><h2>কীভাবে AI-সম্পর্কিত প্রমাণ মূল্যায়ন হয়?</h2>
<ul class="muted"><li>Content Credentials / C2PA বা AI-সম্পর্কিত মেটাডাটা পাওয়া গেলে সেটি রিপোর্ট করা হয়।</li><li>প্রমাণ না পাওয়া মানে AI ব্যবহার হয়নি—এমন নিশ্চয়তা নয়। মেটাডাটা মুছে যেতে পারে বা কোনো ফাইলে শুরু থেকেই নাও থাকতে পারে।</li><li>এটি কোনো নির্ভুল AI-ডিটেক্টর নয়; দৃশ্যমান/পিক্সেলভিত্তিক AI সনাক্তকরণ করে না।</li></ul>
</section>
<footer>লোকাল-অনলি ব্যবহারের জন্য। সার্ভার 127.0.0.1-এ bind করা হয়, তাই একই ফোনের ব্রাউজার থেকে খুলুন। অপরিচিত নেটওয়ার্কে public bind করবেন না।</footer>
{% if result %}<div id="aiDetectionPopup" style="position:fixed;inset:0;background:#0009;z-index:9999;display:flex;align-items:center;justify-content:center;padding:18px"><div style="background:white;color:#222;max-width:520px;padding:22px;border-radius:14px"><h2>AI Content Check</h2><p><b>Status:</b> {{ result.ai_status }}</p><p>{{ result.ai_explanation }}</p><p>এই ফলাফল metadata-ভিত্তিক; নিশ্চিত AI শনাক্তকরণ নয়।</p><button onclick="this.parentElement.parentElement.remove()">বন্ধ করুন</button></div></div>{% endif %}
<script>const f=document.forms[0];if(f){f.addEventListener("submit",()=>{const b=document.getElementById("processBtn"),t=document.getElementById("scanStatus");if(b){b.disabled=true;b.textContent="◌ PROCESSING...";}if(t)t.style.display="block";});}</script><script>const f=document.forms[0];if(f){f.addEventListener("submit",()=>{const b=document.getElementById("processBtn"),t=document.getElementById("scanStatus");if(b){b.disabled=true;b.textContent="◌ PROCESSING...";}if(t)t.style.display="block";});}</script></main></body></html>
"""

def run_cmd(args, timeout=35):
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout.strip(), p.stderr.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        return 127, "", str(e)

def file_kind(path):
    ext = path.suffix.lower()
    if ext in {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff", ".heic"}:
        return "Image"
    if ext in {".mp4", ".mov", ".m4v", ".mkv", ".webm", ".avi"}:
        return "Video"
    return "Unknown"

def metadata_report(path):
    code, out, err = run_cmd(["exiftool", "-j", "-G1", "-s", str(path)])
    if code == 0 and out:
        try:
            data = json.loads(out)[0]
            # Avoid excessively long reports in the web page.
            safe = {k: v for k, v in data.items()
                    if k not in {"SourceFile", "File:Directory", "File:FileName"}}
            return json.dumps(safe, ensure_ascii=False, indent=2)[:12000], safe
        except Exception:
            pass
    if file_kind(path) == "Video":
        code, out, err = run_cmd(["ffprobe", "-v", "quiet", "-show_format", "-show_streams",
                                  "-of", "json", str(path)])
        if code == 0:
            try:
                data = json.loads(out)
                return json.dumps(data, ensure_ascii=False, indent=2)[:12000], data
            except Exception:
                pass
    return "Metadata could not be read. Install ExifTool; for video also install FFmpeg.", {}

def assess_ai(metadata, path):
    flat = json.dumps(metadata, ensure_ascii=False).lower()

    ai_indicators = [
        "comfyui", "stable diffusion", "stablediffusion",
        "midjourney", "dall-e", "dalle", "generative ai",
        "generated by ai", "adobe firefly", "novelai",
        "trainedalgorithmicmedia"
    ]

    found = [word for word in ai_indicators if word in flat]

    c2pa_found = any(
        word in flat
        for word in ("c2pa", "contentcredentials", "content credentials")
    )

    if found:
        return (
            "AI-সম্পর্কিত metadata সংকেত পাওয়া গেছে",
            "পরিচিত সংকেত: " + ", ".join(found)
            + "। এটি metadata-ভিত্তিক ইঙ্গিত; একে এককভাবে চূড়ান্ত প্রমাণ ধরা যাবে না।"
        )

    if c2pa_found:
        return (
            "Content Credentials-সম্পর্কিত তথ্য পাওয়া গেছে",
            "এই তথ্যের উপস্থিতি একা AI দিয়ে তৈরি হওয়ার প্রমাণ নয়। "
            "Credential-এর বিস্তারিত ও সত্যতা আলাদাভাবে যাচাই প্রয়োজন।"
        )

    return (
        "অনির্ধারিত — AI ব্যবহারের প্রমাণ পাওয়া যায়নি",
        "সমর্থিত metadata-তে পরিচিত AI-generator সংকেত পাওয়া যায়নি। "
        "এটি AI-মুক্ত হওয়ার প্রমাণ নয়। এই অ্যাপে বর্তমানে pixel-based "
        "AI detection model সংযুক্ত নেই।"
    )


DB_PATH = ROOT / "history.sqlite3"

def db_connect():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def init_history_db():
    with db_connect() as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created TEXT NOT NULL,
            original TEXT NOT NULL,
            kind TEXT NOT NULL DEFAULT 'Media file',
            ai_status TEXT NOT NULL DEFAULT '',
            ai_explanation TEXT NOT NULL DEFAULT '',
            processing TEXT NOT NULL DEFAULT '',
            metadata TEXT NOT NULL DEFAULT '',
            tags TEXT NOT NULL DEFAULT '',
            output TEXT,
            sidecar TEXT UNIQUE
        )""")
        known = {r[0] for r in con.execute(
            "SELECT sidecar FROM history WHERE sidecar IS NOT NULL"
        )}
        for sidecar in OUTPUTS.glob("*.metadata.json"):
            if sidecar.name in known:
                continue
            try:
                tags = json.loads(sidecar.read_text(encoding="utf-8"))
                base = sidecar.name[:-len(".metadata.json")]
                matches = list(OUTPUTS.glob(base + "_clean.*"))
                created = tags.get("processed_at") or datetime.fromtimestamp(
                    sidecar.stat().st_mtime
                ).astimezone().isoformat(timespec="seconds")
                con.execute("""
                INSERT OR IGNORE INTO history
                (created, original, kind, ai_status, ai_explanation,
                 processing, metadata, tags, output, sidecar)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    str(created),
                    str(tags.get("original_filename") or base),
                    "পুরোনো ফাইল",
                    "আগের রেকর্ডে সংরক্ষিত নয়",
                    "পুরোনো রেকর্ড থেকে AI ফলাফল পুনরুদ্ধার করা যায়নি।",
                    "পুরোনো প্রসেসিং বিবরণ সংরক্ষিত ছিল না।",
                    "পুরোনো পূর্ণ রিপোর্ট পাওয়া যায়নি।",
                    json.dumps(tags, ensure_ascii=False, indent=2),
                    matches[0].name if matches else None,
                    sidecar.name
                ))
            except (OSError, ValueError, TypeError):
                continue

def save_history(result, sidecar_name):
    with db_connect() as con:
        cur = con.execute("""
        INSERT INTO history
        (created, original, kind, ai_status, ai_explanation, processing,
         metadata, tags, output, sidecar)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().astimezone().isoformat(timespec="seconds"),
            result["original"], result["kind"], result["ai_status"],
            result["ai_explanation"], result["processing"],
            result["metadata"], result["tags"], result["output"],
            sidecar_name
        ))
        return cur.lastrowid

init_history_db()

@app.get("/")
def index():
    with db_connect() as con:
        rows = con.execute(
            "SELECT * FROM history ORDER BY id DESC LIMIT 50"
        ).fetchall()
        history = [dict(r) for r in rows]
        selected = request.args.get("record", type=int)
        row = (
            con.execute("SELECT * FROM history WHERE id=?", (selected,)).fetchone()
            if selected else (rows[0] if rows else None)
        )
        result = dict(row) if row else None
    return render_template_string(
        HTML, profiles=PHONE_PROFILES, max_mb=MAX_MB,
        result=result, history=history
    )

@app.post("/process")
def process():
    f = request.files.get("media")
    if not f or not f.filename:
        flash("আগে একটি ফাইল নির্বাচন করুন।")
        return redirect(url_for("index"))
    original = secure_filename(f.filename)
    ext = Path(original).suffix.lower()
    if ext not in ALLOWED:
        flash("এই ফাইল ফরম্যাট সমর্থিত নয়।")
        return redirect(url_for("index"))
    stem = Path(original).stem[:70] or "media"
    uid = uuid.uuid4().hex[:8]
    saved = UPLOADS / f"{stem}_{uid}{ext}"
    f.save(saved)
    if saved.stat().st_size == 0:
        saved.unlink(missing_ok=True)
        flash("ফাইলটি খালি। অন্য ফাইল চেষ্টা করুন।")
        return redirect(url_for("index"))

    report, meta = metadata_report(saved)
    ai_status, ai_explanation = assess_ai(meta, saved)
    profile = request.form.get("profile", "none")
    if profile not in PHONE_PROFILES:
        profile = "none"
    category = request.form.get("category", "").strip()[:100]
    comment = request.form.get("custom_comment", "").strip()[:500]
    tags = {
        "profile_label": PHONE_PROFILES[profile],
        "category": category,
        "comment": comment,
        "original_filename": original,
        "created_by_this_tool": "Media Metadata Studio",
        "note": "These are user-supplied labels, not verified capture-device metadata.",
        "processed_at": datetime.now().astimezone().isoformat(timespec="seconds")
    }
    tag_path = OUTPUTS / f"{stem}_{uid}.metadata.json"
    tag_path.write_text(json.dumps(tags, ensure_ascii=False, indent=2), encoding="utf-8")

    out_name = f"{stem}_{uid}_clean{ext}"
    out_path = OUTPUTS / out_name
    processing = "মূল ফাইল অপরিবর্তিত রাখা হয়েছে; আউটপুট কপি তৈরি করা হয়েছে।"
    clean = request.form.get("clean") == "yes"
    if clean:
        code, out, err = run_cmd(["exiftool", "-all=", "-o", str(out_path), str(saved)], timeout=60)
        if code == 0 and out_path.exists():
            processing = "ExifTool দিয়ে সমর্থিত এমবেডেড মেটাডাটা পরিষ্কার করা হয়েছে।"
        else:
            # Do not silently return the original with a misleading clean label.
            processing = "মেটাডাটা পরিষ্কার করা যায়নি (ExifTool অনুপস্থিত বা ফরম্যাট সমর্থিত নয়)। রিপোর্ট/ট্যাগ JSON তৈরি হয়েছে।"
            out_name = None
    else:
        processing = "মেটাডাটা অপরিবর্তিত রাখা হয়েছে; কাস্টম ট্যাগ JSON তৈরি হয়েছে।"
        # Make an output copy without altering the source.
        try:
            import shutil
            shutil.copy2(saved, out_path)
        except Exception:
            out_name = None

    # Do not reveal absolute local paths in the UI.
    result = {
        "original": original,
        "kind": file_kind(saved),
        "ai_status": ai_status,
        "ai_explanation": ai_explanation,
        "processing": processing,
        "metadata": report,
        "tags": json.dumps(tags, ensure_ascii=False, indent=2),
        "output": out_name
    }
    record_id = save_history(result, tag_path.name)
    return redirect(url_for("index", record=record_id) + "#history")

@app.get("/download/<path:filename>")
def download(filename):
    # Only serve files within output folder, never uploaded source files.
    return send_from_directory(OUTPUTS, filename, as_attachment=True)

@app.errorhandler(413)
def too_large(_):
    flash(f"ফাইলের সাইজ {MAX_MB} MB-এর বেশি। ছোট ফাইল ব্যবহার করুন।")
    return redirect(url_for("index"))

if __name__ == "__main__":
    print("Media Metadata Studio: http://127.0.0.1:5000")
    print("Local-only server. Stop with Ctrl+C.")
    app.run(host="127.0.0.1", port=5000, debug=False)
