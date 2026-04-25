from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3
import requests
import xml.etree.ElementTree as ET
from crawler import run_all_crawlers
import time

# ── 캐시 설정 ──
_cache = {"data": None, "built_at": 0}
CACHE_TTL = 300  # 5분 캐시

app = Flask(__name__)
app.json.ensure_ascii = False
CORS(app)

FLAG_MAP = {
    "Afghanistan":"🇦🇫","Albania":"🇦🇱","Algeria":"🇩🇿","Angola":"🇦🇴","Argentina":"🇦🇷",
    "Armenia":"🇦🇲","Australia":"🇦🇺","Austria":"🇦🇹","Azerbaijan":"🇦🇿","Bahrain":"🇧🇭",
    "Bangladesh":"🇧🇩","Belarus":"🇧🇾","Belgium":"🇧🇪","Bolivia":"🇧🇴",
    "Bosnia and Herzegovina":"🇧🇦","Brazil":"🇧🇷","Brunei":"🇧🇳","Bulgaria":"🇧🇬",
    "Burkina Faso":"🇧🇫","Burundi":"🇧🇮","Cambodia":"🇰🇭","Cameroon":"🇨🇲","Canada":"🇨🇦",
    "Central African Republic":"🇨🇫","Chad":"🇹🇩","Chile":"🇨🇱","China":"🇨🇳",
    "Colombia":"🇨🇴","Congo":"🇨🇬","Democratic Republic of the Congo":"🇨🇩",
    "Costa Rica":"🇨🇷","Croatia":"🇭🇷","Cuba":"🇨🇺","Cyprus":"🇨🇾","Czechia":"🇨🇿",
    "Denmark":"🇩🇰","Dominican Republic":"🇩🇴","Ecuador":"🇪🇨","Egypt":"🇪🇬",
    "El Salvador":"🇸🇻","Eritrea":"🇪🇷","Estonia":"🇪🇪","Ethiopia":"🇪🇹","Fiji":"🇫🇯",
    "Finland":"🇫🇮","France":"🇫🇷","Gabon":"🇬🇦","The Gambia":"🇬🇲","Georgia":"🇬🇪",
    "Germany":"🇩🇪","Ghana":"🇬🇭","Greece":"🇬🇷","Guatemala":"🇬🇹","Guinea":"🇬🇳",
    "Haiti":"🇭🇹","Honduras":"🇭🇳","Hong Kong":"🇭🇰","Hungary":"🇭🇺","Iceland":"🇮🇸",
    "India":"🇮🇳","Indonesia":"🇮🇩","Iran":"🇮🇷","Iraq":"🇮🇶","Ireland":"🇮🇪",
    "Israel":"🇮🇱","Italy":"🇮🇹","Jamaica":"🇯🇲","Japan":"🇯🇵","Jordan":"🇯🇴",
    "Kazakhstan":"🇰🇿","Kenya":"🇰🇪","Kosovo":"🇽🇰","Kuwait":"🇰🇼","Kyrgyzstan":"🇰🇬",
    "Laos":"🇱🇦","Latvia":"🇱🇻","Lebanon":"🇱🇧","Liberia":"🇱🇷","Libya":"🇱🇾",
    "Lithuania":"🇱🇹","Luxembourg":"🇱🇺","Madagascar":"🇲🇬","Malaysia":"🇲🇾",
    "Mali":"🇲🇱","Malta":"🇲🇹","Mauritania":"🇲🇷","Mexico":"🇲🇽","Moldova":"🇲🇩",
    "Mongolia":"🇲🇳","Montenegro":"🇲🇪","Morocco":"🇲🇦","Mozambique":"🇲🇿",
    "Myanmar (Burma)":"🇲🇲","Burma":"🇲🇲","Namibia":"🇳🇦","Nepal":"🇳🇵",
    "Netherlands":"🇳🇱","New Zealand":"🇳🇿","Nicaragua":"🇳🇮","Niger":"🇳🇪",
    "Nigeria":"🇳🇬","North Korea":"🇰🇵","North Macedonia":"🇲🇰","Norway":"🇳🇴",
    "Oman":"🇴🇲","Pakistan":"🇵🇰","Palestine":"🇵🇸","Panama":"🇵🇦","Paraguay":"🇵🇾",
    "Peru":"🇵🇪","Philippines":"🇵🇭","Poland":"🇵🇱","Portugal":"🇵🇹","Qatar":"🇶🇦",
    "Romania":"🇷🇴","Russia":"🇷🇺","Rwanda":"🇷🇼","Saudi Arabia":"🇸🇦","Senegal":"🇸🇳",
    "Serbia":"🇷🇸","Singapore":"🇸🇬","Slovakia":"🇸🇰","Slovenia":"🇸🇮","Somalia":"🇸🇴",
    "South Africa":"🇿🇦","South Korea":"🇰🇷","South Sudan":"🇸🇸","Spain":"🇪🇸",
    "Sri Lanka":"🇱🇰","Sudan":"🇸🇩","Sweden":"🇸🇪","Switzerland":"🇨🇭","Syria":"🇸🇾",
    "Taiwan":"🇹🇼","Tajikistan":"🇹🇯","Tanzania":"🇹🇿","Thailand":"🇹🇭","Togo":"🇹🇬",
    "Tunisia":"🇹🇳","Turkey":"🇹🇷","Turkmenistan":"🇹🇲","Uganda":"🇺🇬","Ukraine":"🇺🇦",
    "United Arab Emirates":"🇦🇪","Uruguay":"🇺🇾","USA":"🇺🇸","United States":"🇺🇸",
    "Uzbekistan":"🇺🇿","Venezuela":"🇻🇪","Vietnam":"🇻🇳","Yemen":"🇾🇪",
    "Zambia":"🇿🇲","Zimbabwe":"🇿🇼","Côte d'Ivoire":"🇨🇮","Mali":"🇲🇱",
    "Benin":"🇧🇯","Lesotho":"🇱🇸","Malawi":"🇲🇼","Maldives":"🇲🇻",
}

KO_NAME = {
    "Afghanistan":"아프가니스탄","Albania":"알바니아","Algeria":"알제리","Angola":"앙골라",
    "Argentina":"아르헨티나","Armenia":"아르메니아","Australia":"호주","Austria":"오스트리아",
    "Azerbaijan":"아제르바이잔","Bahrain":"바레인","Bangladesh":"방글라데시",
    "Belarus":"벨라루스","Belgium":"벨기에","Bolivia":"볼리비아",
    "Bosnia and Herzegovina":"보스니아 헤르체고비나","Brazil":"브라질","Brunei":"브루나이",
    "Bulgaria":"불가리아","Burkina Faso":"부르키나파소","Burundi":"부룬디",
    "Cambodia":"캄보디아","Cameroon":"카메룬","Canada":"캐나다",
    "Central African Republic":"중앙아프리카공화국","Chad":"차드","Chile":"칠레",
    "China":"중국","Colombia":"콜롬비아","Congo":"콩고",
    "Democratic Republic of the Congo":"콩고민주공화국","Costa Rica":"코스타리카",
    "Croatia":"크로아티아","Cuba":"쿠바","Cyprus":"키프로스","Czechia":"체코",
    "Denmark":"덴마크","Dominican Republic":"도미니카공화국","Ecuador":"에콰도르",
    "Egypt":"이집트","El Salvador":"엘살바도르","Eritrea":"에리트레아",
    "Estonia":"에스토니아","Ethiopia":"에티오피아","Fiji":"피지","Finland":"핀란드",
    "France":"프랑스","Gabon":"가봉","The Gambia":"감비아","Georgia":"조지아",
    "Germany":"독일","Ghana":"가나","Greece":"그리스","Guatemala":"과테말라",
    "Guinea":"기니","Haiti":"아이티","Honduras":"온두라스","Hong Kong":"홍콩",
    "Hungary":"헝가리","Iceland":"아이슬란드","India":"인도","Indonesia":"인도네시아",
    "Iran":"이란","Iraq":"이라크","Ireland":"아일랜드","Israel":"이스라엘",
    "Italy":"이탈리아","Jamaica":"자메이카","Japan":"일본","Jordan":"요르단",
    "Kazakhstan":"카자흐스탄","Kenya":"케냐","Kosovo":"코소보","Kuwait":"쿠웨이트",
    "Kyrgyzstan":"키르기스스탄","Laos":"라오스","Latvia":"라트비아","Lebanon":"레바논",
    "Liberia":"라이베리아","Libya":"리비아","Lithuania":"리투아니아","Luxembourg":"룩셈부르크",
    "Madagascar":"마다가스카르","Malaysia":"말레이시아","Mali":"말리","Malta":"몰타",
    "Mauritania":"모리타니","Mexico":"멕시코","Moldova":"몰도바","Mongolia":"몽골",
    "Montenegro":"몬테네그로","Morocco":"모로코","Mozambique":"모잠비크",
    "Myanmar (Burma)":"미얀마","Burma":"미얀마","Namibia":"나미비아","Nepal":"네팔",
    "Netherlands":"네덜란드","New Zealand":"뉴질랜드","Nicaragua":"니카라과",
    "Niger":"니제르","Nigeria":"나이지리아","North Korea":"북한",
    "North Macedonia":"북마케도니아","Norway":"노르웨이","Oman":"오만",
    "Pakistan":"파키스탄","Palestine":"팔레스타인","Panama":"파나마","Paraguay":"파라과이",
    "Peru":"페루","Philippines":"필리핀","Poland":"폴란드","Portugal":"포르투갈",
    "Qatar":"카타르","Romania":"루마니아","Russia":"러시아","Rwanda":"르완다",
    "Saudi Arabia":"사우디아라비아","Senegal":"세네갈","Serbia":"세르비아",
    "Singapore":"싱가포르","Slovakia":"슬로바키아","Slovenia":"슬로베니아",
    "Somalia":"소말리아","South Africa":"남아프리카공화국","South Korea":"한국",
    "South Sudan":"남수단","Spain":"스페인","Sri Lanka":"스리랑카","Sudan":"수단",
    "Sweden":"스웨덴","Switzerland":"스위스","Syria":"시리아","Taiwan":"대만",
    "Tajikistan":"타지키스탄","Tanzania":"탄자니아","Thailand":"태국","Togo":"토고",
    "Tunisia":"튀니지","Turkey":"튀르키예","Turkmenistan":"투르크메니스탄",
    "Uganda":"우간다","Ukraine":"우크라이나","United Arab Emirates":"아랍에미리트",
    "Uruguay":"우루과이","USA":"미국","United States":"미국","Uzbekistan":"우즈베키스탄",
    "Venezuela":"베네수엘라","Vietnam":"베트남","Yemen":"예멘","Zambia":"잠비아",
    "Zimbabwe":"짐바브웨","Côte d'Ivoire":"코트디부아르","Benin":"베냉",
    "Lesotho":"레소토","Malawi":"말라위","Maldives":"몰디브",
}

EN_NAME = {v: k for k, v in KO_NAME.items()}  # 한글→영어 역매핑

SOURCE_FLAG = {"한국":"🇰🇷","미국":"🇺🇸","영국":"🇬🇧","독일":"🇩🇪","프랑스":"🇫🇷","일본":"🇯🇵"}
ALL_SOURCES = [
    {"name":"영국","flag":"🇬🇧"},{"name":"한국","flag":"🇰🇷"},{"name":"미국","flag":"🇺🇸"},
    {"name":"일본","flag":"🇯🇵"},{"name":"독일","flag":"🇩🇪"},{"name":"프랑스","flag":"🇫🇷"},
]

def get_db():
    conn = sqlite3.connect("embassy.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_history_table():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS status_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            country_name TEXT,
            source_country TEXT,
            old_status TEXT,
            new_status TEXT,
            changed_at TEXT
        )
    """)
    conn.commit()
    conn.close()

init_history_table()

def get_all_data():
    try:
        conn = get_db()
        rows = conn.execute("SELECT * FROM embassy_status ORDER BY updated_at DESC").fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except:
        return []

def build_summary(data):
    country_map = {}
    ord_s = {"red":0,"yellow":1,"green":2}
    for row in data:
        en = row["country_name"]
        if en not in country_map:
            country_map[en] = {
                "country_name": KO_NAME.get(en, en),
                "country_name_en": en,
                "flag": FLAG_MAP.get(en, "🏳️"),
                "embassies": {},
                "updated_at": row["updated_at"]
            }
        src = row["source_country"]
        ex = country_map[en]["embassies"].get(src)
        if not ex or ord_s[row["status"]] < ord_s[ex["status"]]:
            country_map[en]["embassies"][src] = {
                "flag": SOURCE_FLAG.get(src,"🏳️"),
                "name": src,
                "status": row["status"],
                "label": row["status_label"]
            }

    result = []
    for en, info in country_map.items():
        # 데이터 없는 출처는 "운영"으로 채우기
        for src in ALL_SOURCES:
            if src["name"] not in info["embassies"]:
                info["embassies"][src["name"]] = {
                    "flag": src["flag"], "name": src["name"],
                    "status": "green", "label": "운영"
                }
        emb = list(info["embassies"].values())
        red = sum(1 for e in emb if e["status"]=="red")
        yellow = sum(1 for e in emb if e["status"]=="yellow")
        if red >= 2: level = "위험"
        elif red == 1 or yellow >= 2: level = "주의요망"
        else: level = "안전"
        result.append({
            "country_name": info["country_name"],
            "country_name_en": en,
            "flag": info["flag"],
            "embassies": emb,
            "level": level,
            "red_count": red,
            "yellow_count": yellow,
            "updated_at": info["updated_at"]
        })
    ord_l = {"위험":0,"주의요망":1,"안전":2}
    result.sort(key=lambda x: (ord_l[x["level"]], -x["red_count"]))
    return result

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/api/countries")
def get_countries():
    global _cache
    now = time.time()
    # 캐시가 있고 TTL 안 지났으면 캐시 반환
    if _cache["data"] and (now - _cache["built_at"]) < CACHE_TTL:
        return jsonify({"success": True, "data": _cache["data"], "cached": True})
    # 캐시 갱신
    data = build_summary(get_all_data())
    _cache = {"data": data, "built_at": now}
    return jsonify({"success": True, "data": data, "cached": False})

@app.route("/api/stats")
def get_stats():
    s = build_summary(get_all_data())
    return jsonify({"success":True,"data":{
        "위험":sum(1 for c in s if c["level"]=="위험"),
        "주의요망":sum(1 for c in s if c["level"]=="주의요망"),
        "안전":sum(1 for c in s if c["level"]=="안전"),
        "total":len(s)
    }})

@app.route("/api/news/<country_name>")
def get_news(country_name):
    try:
        # 한글 이름이면 영어로 변환
        en_name = EN_NAME.get(country_name, country_name)
        query = f"{en_name} embassy evacuation travel warning"
        url = f"https://news.google.com/rss/search?q={requests.utils.quote(query)}&hl=en&gl=US&ceid=US:en"
        res = requests.get(url, timeout=10, headers={"User-Agent":"Mozilla/5.0"})
        root = ET.fromstring(res.content)
        items = []
        for item in root.findall(".//item")[:5]:
            title = item.findtext("title","")
            link = item.findtext("link","")
            pub_date = item.findtext("pubDate","")
            source = item.findtext("source","")
            items.append({"title":title,"link":link,"pub_date":pub_date,"source":source})
        return jsonify({"success":True,"data":items})
    except Exception as e:
        return jsonify({"success":False,"data":[],"error":str(e)})

@app.route("/api/history/<country_name>")
def get_history(country_name):
    try:
        en_name = EN_NAME.get(country_name, country_name)
        conn = get_db()
        rows = conn.execute("""
            SELECT * FROM status_history
            WHERE country_name = ?
            ORDER BY changed_at DESC LIMIT 20
        """, (en_name,)).fetchall()
        conn.close()
        return jsonify({"success":True,"data":[dict(r) for r in rows]})
    except Exception as e:
        return jsonify({"success":False,"data":[]})

@app.route("/api/crawl")
def manual_crawl():
    global _cache
    run_all_crawlers()
    # 크롤링 후 캐시 초기화
    _cache = {"data": None, "built_at": 0}
    return jsonify({"success":True,"message":"크롤링 완료! 캐시 초기화됨"})

@app.route("/api/cache/clear")
def clear_cache():
    global _cache
    _cache = {"data": None, "built_at": 0}
    return jsonify({"success":True,"message":"캐시 초기화 완료"})

scheduler = BackgroundScheduler()
scheduler.add_job(run_all_crawlers,"interval",hours=6)
scheduler.start()

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 서버 시작! http://localhost:{port}")
    print("⏰ 크롤러는 6시간마다 자동 실행됩니다")
    app.run(debug=False, host="0.0.0.0", port=port)