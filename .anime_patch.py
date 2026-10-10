from pathlib import Path
p=Path("app.py")
s=p.read_text(encoding="utf-8")
s=s.replace('}PHONE_PROFILES = {','}\nPHONE_PROFILES = {')
a=s.find("PHONE_PROFILES = {")
b=s.find("\napp = Flask(__name__)",a)
if a<0 or b<0: raise SystemExit("PATCH_ERROR: PHONE_PROFILES block not found")
profiles="""PHONE_PROFILES = {
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
}"""
s=s[:a]+profiles+s[b:]
s=s.replace("<title>Media Metadata Studio</title>","<title>Anime Action · Media Metadata Studio</title>")
css="""body{background:radial-gradient(ellipse at 10% 0%,#25205b 0,transparent 42%),radial-gradient(ellipse at 95% 20%,#092e45 0,transparent 38%),var(--bg);overflow-x:hidden}
.hero{position:relative;overflow:hidden;background:linear-gradient(125deg,#1c2450,#10192b 60%,#321447);border-color:#3c5e91;box-shadow:0 0 28px #4a50ff33;animation:heroPulse 5s ease-in-out infinite}
.hero:after{content:"";position:absolute;left:-30%;right:-30%;height:2px;top:0;background:linear-gradient(90deg,transparent,#69f5ff,white,#ff4fd8,transparent);animation:scan 5s linear infinite}
.card{background:linear-gradient(145deg,#151d33,#0e1424);border-color:#2c3c63;box-shadow:0 12px 35px #0003;animation:riseIn .4s ease both}
button,.btn{background:linear-gradient(100deg,#69f5ff,#9bb6ff 55%,#e58bff);color:#080d1c;box-shadow:0 0 20px #69f5ff20;transition:transform .18s,filter .18s}
button:hover,.btn:hover{transform:translateY(-2px);filter:brightness(1.12);box-shadow:0 0 25px #69f5ff55}
.tag{border-color:#3a527f;background:#141d35aa;color:#b8faff}
@keyframes scan{0%{transform:translateY(0)}100%{transform:translateY(240px)}}
@keyframes heroPulse{0%,100%{box-shadow:0 0 22px #4a50ff22}50%{box-shadow:0 0 38px #4a50ff55,0 0 18px #ff4fd833}}
@keyframes riseIn{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}"""
s=s.replace("</style>",css+"\n</style>",1)
s=s.replace('<div class="hero"><h1>Media Metadata Studio</h1><div class="muted">লোকাল ফাইল পরীক্ষা · প্রাইভেসি ক্লিনিং · কাস্টম ট্যাগ</div>','<div class="hero"><h1>⚡ ANIME ACTION <span style="color:#69f5ff">MEDIA STUDIO</span></h1><div class="muted">LOCAL SCAN // METADATA ANALYSIS // PRIVACY CLEANING</div>')
s=s.replace('<label>প্রোফাইল (শুধু কাস্টম লেবেল)</label>','<label>ফোনের মডেল নির্বাচন (model preset)</label>')
s=s.replace('<button type="submit">বিশ্লেষণ ও প্রসেস করুন</button>','<button type="submit" id="processBtn">⚡ SCAN &amp; PROCESS</button><p id="scanStatus" class="muted" style="display:none">◈ SCANNING FILE · ANALYZING METADATA · PLEASE WAIT...</p>')
s=s.replace('</main></body></html>','<script>const f=document.forms[0];if(f){f.addEventListener("submit",()=>{const b=document.getElementById("processBtn"),t=document.getElementById("scanStatus");if(b){b.disabled=true;b.textContent="◌ PROCESSING...";}if(t)t.style.display="block";});}</script></main></body></html>')
p.write_text(s,encoding="utf-8")
compile(s,"app.py","exec")
print("PATCH_OK: phone model list + anime action UI; syntax validated")
