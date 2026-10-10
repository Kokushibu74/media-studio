from pathlib import Path
import re

p = Path("app.py")
s = p.read_text(encoding="utf-8")

if "import sqlite3" not in s:
    s = s.replace("import subprocess\n", "import subprocess\nimport sqlite3\n", 1)

if 'id="history"' not in s:
    pos = s.find('<section class="card"><h2>কীভাবে AI-সম্পর্কিত প্রমাণ মূল্যায়')
    if pos < 0:
        raise SystemExit("ERROR: History panel insertion point not found. app.py was not updated.")
    panel = r'''
<section class="card" id="history">
<h2>◈ HISTORY // আগের কাজ ও ডাউনলোড</h2>
<p class="muted">রিফ্রেশ বা অ্যাপ পুনরায় চালু করলেও ইতিহাস থাকবে। সর্বশেষ ৫০টি কাজ দেখানো হয়।</p>
{% if history %}
<div class="grid">
{% for item in history %}
<div class="card" style="margin-top:0;padding:14px">
<b>{{ item.original }}</b>
<p class="muted">{{ item.created }} · {{ item.kind }}</p>
{% if item.output %}
<p><a class="btn" href="{{ url_for('download', filename=item.output) }}">⬇ আউটপুট ডাউনলোড</a></p>
{% else %}<p class="muted">আউটপুট ফাইল পাওয়া যায়নি।</p>{% endif %}
{% if item.sidecar %}
<p><a class="btn" href="{{ url_for('download', filename=item.sidecar) }}">⬇ Metadata JSON</a></p>
{% endif %}
{% if item.ai_status %}<p class="muted">AI metadata status: {{ item.ai_status }}</p>{% endif %}
</div>
{% endfor %}
</div>
{% else %}<p class="muted">এখনও কোনো ইতিহাস নেই।</p>{% endif %}
</section>
'''
    s = s[:pos] + panel + "\n" + s[pos:]

route_code = r'''
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
'''
route_pattern = re.compile(
    r'@app\.get\("/"\)\s+def index\(\):\s+return render_template_string\(HTML, profiles=PHONE_PROFILES, max_mb=MAX_MB, result=None\)\s*'
)
if "def init_history_db():" not in s:
    s, count = route_pattern.subn(route_code + "\n", s, count=1)
    if count != 1:
        raise SystemExit("ERROR: Could not safely replace index route. Restore app.py.before_history_upgrade if needed.")

old = '    return render_template_string(HTML, profiles=PHONE_PROFILES, max_mb=MAX_MB, result=result)\n\n@app.get("/download/<path:filename>")'
new = '    record_id = save_history(result, tag_path.name)\n    return redirect(url_for("index", record=record_id) + "#history")\n\n@app.get("/download/<path:filename>")'
if old in s:
    s = s.replace(old, new, 1)
elif "record_id = save_history(result, tag_path.name)" not in s:
    raise SystemExit("ERROR: Process return point not found. Restore app.py.before_history_upgrade if needed.")

p.write_text(s, encoding="utf-8")
print("History upgrade applied.")
