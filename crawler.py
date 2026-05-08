import requests
from bs4 import BeautifulSoup
import os
import psycopg2
import sqlite3
from datetime import datetime

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
DATABASE_URL = os.environ.get("DATABASE_URL", "")

def get_conn():
    if DATABASE_URL:
        return psycopg2.connect(DATABASE_URL), True
    else:
        conn = sqlite3.connect("embassy.db")
        return conn, False

def init_db():
    conn, is_pg = get_conn()
    cur = conn.cursor()
    if is_pg:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS embassy_status (
                id SERIAL PRIMARY KEY,
                country_name TEXT,
                source_country TEXT,
                status TEXT,
                status_label TEXT,
                detail TEXT,
                updated_at TEXT
            )
        """)
    else:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS embassy_status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                country_name TEXT,
                source_country TEXT,
                status TEXT,
                status_label TEXT,
                detail TEXT,
                updated_at TEXT
            )
        """)
    conn.commit()
    cur.close()
    conn.close()
    print("✅ DB 초기화 완료")

def clear_source(source_country):
    conn, is_pg = get_conn()
    cur = conn.cursor()
    q = "DELETE FROM embassy_status WHERE source_country = %s" if is_pg else "DELETE FROM embassy_status WHERE source_country = ?"
    cur.execute(q, (source_country,))
    conn.commit()
    cur.close()
    conn.close()

def save_to_db(results):
    if not results:
        return
    conn, is_pg = get_conn()
    cur = conn.cursor()
    ph = "%s" if is_pg else "?"
    for r in results:
        cur.execute(f"""
            INSERT INTO embassy_status
                (country_name, source_country, status, status_label, detail, updated_at)
            VALUES ({ph},{ph},{ph},{ph},{ph},{ph})
        """, (r["country_name"], r["source_country"], r["status"],
              r["status_label"], r["detail"], r["updated_at"]))
    conn.commit()
    cur.close()
    conn.close()
    print(f"  ✅ {len(results)}개 저장")

def crawl_us_state():
    print("🇺🇸 미국 국무부 크롤링...")
    results = []
    try:
        url = "https://travel.state.gov/content/travel/en/traveladvisories/traveladvisories.html/"
        res = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(res.text, "html.parser")
        for row in soup.select("table tr"):
            cols = row.select("td")
            if len(cols) < 2: continue
            country = cols[0].get_text(strip=True)
            level_text = cols[1].get_text(strip=True)
            if not country or country.startswith("Level"): continue
            if "Level 4" in level_text: status, label = "red", "철수"
            elif "Level 3" in level_text: status, label = "yellow", "대기"
            elif "Level 2" in level_text: status, label = "yellow", "대기"
            else: status, label = "green", "운영"
            results.append({"country_name":country,"source_country":"미국","status":status,"status_label":label,"detail":f"미국 국무부: {level_text}","updated_at":datetime.now().isoformat()})
        print(f"  → {len(results)}개 수집")
    except Exception as e:
        print(f"  ❌ 실패: {e}")
    return results

def crawl_uk_fcdo():
    print("🇬🇧 영국 외무부 크롤링...")
    high_risk = ["ukraine","russia","sudan","haiti","myanmar","burma","afghanistan","syria","iraq","yemen","somalia","libya","mali","niger","south-sudan","ethiopia","pakistan","north-korea","iran","venezuela","belarus","israel","lebanon","palestine","gaza"]
    results = []
    try:
        res = requests.get("https://www.gov.uk/foreign-travel-advice", headers=HEADERS, timeout=15)
        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.select(".govuk-list li a")
        print(f"  → {len(items)}개 국가 확인 중...")
        for item in items:
            country_name = item.get_text(strip=True)
            href = item.get("href","")
            is_high_risk = any(k in href.lower() for k in high_risk)
            if is_high_risk:
                try:
                    dr = requests.get("https://www.gov.uk"+href, headers=HEADERS, timeout=10)
                    pt = dr.text.lower()
                    if "advise against all travel" in pt or "do not travel" in pt:
                        status,label,detail = "red","철수","영국 외무부: 전면 여행 금지"
                    elif "essential travel only" in pt or "advise against all but essential" in pt:
                        status,label,detail = "yellow","대기","영국 외무부: 필수 여행 외 자제"
                    else:
                        status,label,detail = "yellow","대기","영국 외무부: 주의 필요"
                except:
                    status,label,detail = "yellow","대기","영국 외무부: 주의 필요"
            else:
                status,label,detail = "green","운영","영국 외무부: 정상"
            results.append({"country_name":country_name,"source_country":"영국","status":status,"status_label":label,"detail":detail,"updated_at":datetime.now().isoformat()})
        print(f"  → {len(results)}개 수집")
    except Exception as e:
        print(f"  ❌ 실패: {e}")
    return results

def run_all_crawlers():
    print(f"\n{'='*40}\n크롤링 시작: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{'='*40}")
    init_db()
    uk = crawl_uk_fcdo()
    if len(uk) > 0:
        clear_source("영국")
        save_to_db(uk)
    us = crawl_us_state()
    if len(us) > 0:
        clear_source("미국")
        save_to_db(us)
    print(f"✅ 크롤링 완료! 영국:{len(uk)} 미국:{len(us)}\n{'='*40}\n")

if __name__ == "__main__":
    run_all_crawlers()