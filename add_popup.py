from pathlib import Path

p = Path("app.py")
s = p.read_text()
marker = "</main></body></html>"

if marker not in s:
print("ERROR: HTML marker পাওয়া যায়নি; app.py অপরিবর্তিত।")
elif 'id="aiDetectionPopup"' in s:
print("Popup আগে থেকেই আছে।")
else:
popup = """
{% if result %}

<div id="aiDetectionPopup" style="position:fixed;inset:0;background:#0009;z-index:9999;display:flex;align-items:center;justify-content:center;padding:18px">
<div style="background:white;color:#222;max-width:520px;padding:22px;border-radius:14px">
<h2>AI Content Check</h2>
<p><b>Status:</b> {{ result.ai_status }}</p>
<p>{{ result.ai_explanation }}</p>
<p style="font-size:13px">এই পরীক্ষা ফাইলের metadata-নির্ভর; এটি AI তৈরির নিশ্চিত প্রমাণ নয়।</p>
<button onclick="document.getElementById('aiDetectionPopup').remove()">বন্ধ করুন</button>
</div>
</div>
{% endif %}
"""
    p.write_text(s.replace(marker, popup + "\n" + marker, 1))
    print("Popup যোগ হয়েছে।")
