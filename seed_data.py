import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("embassy.db")
    cur = conn.cursor()
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
    conn.close()

def save_to_db(results):
    conn = sqlite3.connect("embassy.db")
    cur = conn.cursor()
    for r in results:
        cur.execute("""
            INSERT INTO embassy_status
                (country_name, source_country, status, status_label, detail, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["country_name"], r["source_country"], r["status"],
              r["status_label"], r["detail"], r["updated_at"]))
    conn.commit()
    conn.close()

SEED = [
    # 우크라이나
    {"country_name":"Ukraine","source_country":"한국","status":"red","status_label":"철수","detail":"한국 외교부 4단계: 여행금지"},
    {"country_name":"Ukraine","source_country":"미국","status":"red","status_label":"철수","detail":"미국 국무부 Level 4"},
    {"country_name":"Ukraine","source_country":"일본","status":"red","status_label":"철수","detail":"일본 외무성 레벨4"},
    {"country_name":"Ukraine","source_country":"독일","status":"red","status_label":"철수","detail":"독일 외무부 Reisewarnung"},
    {"country_name":"Ukraine","source_country":"프랑스","status":"red","status_label":"철수","detail":"프랑스 외무부: 여행 금지"},
    # 러시아
    {"country_name":"Russia","source_country":"한국","status":"yellow","status_label":"대기","detail":"한국 외교부 2단계: 여행자제"},
    {"country_name":"Russia","source_country":"미국","status":"red","status_label":"철수","detail":"미국 국무부 Level 4"},
    {"country_name":"Russia","source_country":"일본","status":"yellow","status_label":"대기","detail":"일본 외무성 레벨2"},
    {"country_name":"Russia","source_country":"독일","status":"yellow","status_label":"대기","detail":"독일 외무부: 부분 경보"},
    {"country_name":"Russia","source_country":"프랑스","status":"yellow","status_label":"대기","detail":"프랑스 외무부: 주의"},
    # 수단
    {"country_name":"Sudan","source_country":"한국","status":"red","status_label":"철수","detail":"한국 외교부 4단계"},
    {"country_name":"Sudan","source_country":"미국","status":"red","status_label":"철수","detail":"미국 국무부 Level 4"},
    {"country_name":"Sudan","source_country":"일본","status":"red","status_label":"철수","detail":"일본 외무성 레벨4"},
    {"country_name":"Sudan","source_country":"독일","status":"red","status_label":"철수","detail":"독일 외무부 Reisewarnung"},
    {"country_name":"Sudan","source_country":"프랑스","status":"red","status_label":"철수","detail":"프랑스 외무부: 여행 금지"},
    # 아이티
    {"country_name":"Haiti","source_country":"한국","status":"red","status_label":"철수","detail":"한국 외교부 4단계"},
    {"country_name":"Haiti","source_country":"미국","status":"red","status_label":"철수","detail":"미국 국무부 Level 4"},
    {"country_name":"Haiti","source_country":"일본","status":"yellow","status_label":"대기","detail":"일본 외무성 레벨3"},
    {"country_name":"Haiti","source_country":"독일","status":"red","status_label":"철수","detail":"독일 외무부 Reisewarnung"},
    {"country_name":"Haiti","source_country":"프랑스","status":"yellow","status_label":"대기","detail":"프랑스 외무부: 주의"},
    # 아프가니스탄
    {"country_name":"Afghanistan","source_country":"한국","status":"red","status_label":"철수","detail":"한국 외교부 4단계"},
    {"country_name":"Afghanistan","source_country":"미국","status":"red","status_label":"철수","detail":"미국 국무부 Level 4"},
    {"country_name":"Afghanistan","source_country":"일본","status":"red","status_label":"철수","detail":"일본 외무성 레벨4"},
    {"country_name":"Afghanistan","source_country":"독일","status":"red","status_label":"철수","detail":"독일 외무부 Reisewarnung"},
    {"country_name":"Afghanistan","source_country":"프랑스","status":"red","status_label":"철수","detail":"프랑스 외무부: 여행 금지"},
    # 시리아
    {"country_name":"Syria","source_country":"한국","status":"red","status_label":"철수","detail":"한국 외교부 4단계"},
    {"country_name":"Syria","source_country":"미국","status":"red","status_label":"철수","detail":"미국 국무부 Level 4"},
    {"country_name":"Syria","source_country":"일본","status":"red","status_label":"철수","detail":"일본 외무성 레벨4"},
    {"country_name":"Syria","source_country":"독일","status":"red","status_label":"철수","detail":"독일 외무부 Reisewarnung"},
    {"country_name":"Syria","source_country":"프랑스","status":"red","status_label":"철수","detail":"프랑스 외무부: 여행 금지"},
    # 예멘
    {"country_name":"Yemen","source_country":"한국","status":"red","status_label":"철수","detail":"한국 외교부 4단계"},
    {"country_name":"Yemen","source_country":"미국","status":"red","status_label":"철수","detail":"미국 국무부 Level 4"},
    {"country_name":"Yemen","source_country":"일본","status":"red","status_label":"철수","detail":"일본 외무성 레벨4"},
    {"country_name":"Yemen","source_country":"독일","status":"red","status_label":"철수","detail":"독일 외무부 Reisewarnung"},
    {"country_name":"Yemen","source_country":"프랑스","status":"red","status_label":"철수","detail":"프랑스 외무부: 여행 금지"},
    # 소말리아
    {"country_name":"Somalia","source_country":"한국","status":"red","status_label":"철수","detail":"한국 외교부 4단계"},
    {"country_name":"Somalia","source_country":"미국","status":"red","status_label":"철수","detail":"미국 국무부 Level 4"},
    {"country_name":"Somalia","source_country":"일본","status":"red","status_label":"철수","detail":"일본 외무성 레벨4"},
    {"country_name":"Somalia","source_country":"독일","status":"red","status_label":"철수","detail":"독일 외무부 Reisewarnung"},
    {"country_name":"Somalia","source_country":"프랑스","status":"red","status_label":"철수","detail":"프랑스 외무부: 여행 금지"},
    # 리비아
    {"country_name":"Libya","source_country":"한국","status":"red","status_label":"철수","detail":"한국 외교부 4단계"},
    {"country_name":"Libya","source_country":"미국","status":"red","status_label":"철수","detail":"미국 국무부 Level 4"},
    {"country_name":"Libya","source_country":"일본","status":"yellow","status_label":"대기","detail":"일본 외무성 레벨3"},
    {"country_name":"Libya","source_country":"독일","status":"red","status_label":"철수","detail":"독일 외무부 Reisewarnung"},
    {"country_name":"Libya","source_country":"프랑스","status":"red","status_label":"철수","detail":"프랑스 외무부: 여행 금지"},
    # 미얀마
    {"country_name":"Myanmar (Burma)","source_country":"한국","status":"yellow","status_label":"대기","detail":"한국 외교부 3단계"},
    {"country_name":"Myanmar (Burma)","source_country":"미국","status":"red","status_label":"철수","detail":"미국 국무부 Level 4"},
    {"country_name":"Myanmar (Burma)","source_country":"일본","status":"yellow","status_label":"대기","detail":"일본 외무성 레벨3"},
    {"country_name":"Myanmar (Burma)","source_country":"독일","status":"yellow","status_label":"대기","detail":"독일 외무부: 부분 경보"},
    {"country_name":"Myanmar (Burma)","source_country":"프랑스","status":"yellow","status_label":"대기","detail":"프랑스 외무부: 주의"},
    # 이라크
    {"country_name":"Iraq","source_country":"한국","status":"red","status_label":"철수","detail":"한국 외교부 4단계"},
    {"country_name":"Iraq","source_country":"미국","status":"red","status_label":"철수","detail":"미국 국무부 Level 4"},
    {"country_name":"Iraq","source_country":"일본","status":"red","status_label":"철수","detail":"일본 외무성 레벨4"},
    {"country_name":"Iraq","source_country":"독일","status":"red","status_label":"철수","detail":"독일 외무부 Reisewarnung"},
    {"country_name":"Iraq","source_country":"프랑스","status":"red","status_label":"철수","detail":"프랑스 외무부: 여행 금지"},
    # 이스라엘
    {"country_name":"Israel","source_country":"한국","status":"yellow","status_label":"대기","detail":"한국 외교부 2단계"},
    {"country_name":"Israel","source_country":"미국","status":"yellow","status_label":"대기","detail":"미국 국무부 Level 3"},
    {"country_name":"Israel","source_country":"일본","status":"yellow","status_label":"대기","detail":"일본 외무성 레벨2"},
    {"country_name":"Israel","source_country":"독일","status":"yellow","status_label":"대기","detail":"독일 외무부: 부분 경보"},
    {"country_name":"Israel","source_country":"프랑스","status":"yellow","status_label":"대기","detail":"프랑스 외무부: 주의"},
    # 북한
    {"country_name":"North Korea","source_country":"한국","status":"red","status_label":"철수","detail":"한국 외교부 4단계"},
    {"country_name":"North Korea","source_country":"미국","status":"red","status_label":"철수","detail":"미국 국무부 Level 4"},
    {"country_name":"North Korea","source_country":"일본","status":"red","status_label":"철수","detail":"일본 외무성 레벨4"},
    {"country_name":"North Korea","source_country":"독일","status":"red","status_label":"철수","detail":"독일 외무부 Reisewarnung"},
    {"country_name":"North Korea","source_country":"프랑스","status":"red","status_label":"철수","detail":"프랑스 외무부: 여행 금지"},
    # 이란
    {"country_name":"Iran","source_country":"한국","status":"yellow","status_label":"대기","detail":"한국 외교부 2단계"},
    {"country_name":"Iran","source_country":"미국","status":"red","status_label":"철수","detail":"미국 국무부 Level 4"},
    {"country_name":"Iran","source_country":"일본","status":"yellow","status_label":"대기","detail":"일본 외무성 레벨3"},
    {"country_name":"Iran","source_country":"독일","status":"yellow","status_label":"대기","detail":"독일 외무부: 주의"},
    {"country_name":"Iran","source_country":"프랑스","status":"yellow","status_label":"대기","detail":"프랑스 외무부: 주의"},
    # 남수단
    {"country_name":"South Sudan","source_country":"한국","status":"red","status_label":"철수","detail":"한국 외교부 4단계"},
    {"country_name":"South Sudan","source_country":"미국","status":"red","status_label":"철수","detail":"미국 국무부 Level 4"},
    {"country_name":"South Sudan","source_country":"일본","status":"red","status_label":"철수","detail":"일본 외무성 레벨4"},
    {"country_name":"South Sudan","source_country":"독일","status":"red","status_label":"철수","detail":"독일 외무부 Reisewarnung"},
    {"country_name":"South Sudan","source_country":"프랑스","status":"red","status_label":"철수","detail":"프랑스 외무부: 여행 금지"},
    # 말리
    {"country_name":"Mali","source_country":"한국","status":"yellow","status_label":"대기","detail":"한국 외교부 3단계"},
    {"country_name":"Mali","source_country":"미국","status":"red","status_label":"철수","detail":"미국 국무부 Level 4"},
    {"country_name":"Mali","source_country":"일본","status":"yellow","status_label":"대기","detail":"일본 외무성 레벨3"},
    {"country_name":"Mali","source_country":"독일","status":"red","status_label":"철수","detail":"독일 외무부 Reisewarnung"},
    {"country_name":"Mali","source_country":"프랑스","status":"red","status_label":"철수","detail":"프랑스 외무부: 여행 금지"},
    # 베네수엘라
    {"country_name":"Venezuela","source_country":"한국","status":"yellow","status_label":"대기","detail":"한국 외교부 2단계"},
    {"country_name":"Venezuela","source_country":"미국","status":"red","status_label":"철수","detail":"미국 국무부 Level 4"},
    {"country_name":"Venezuela","source_country":"일본","status":"yellow","status_label":"대기","detail":"일본 외무성 레벨3"},
    {"country_name":"Venezuela","source_country":"독일","status":"yellow","status_label":"대기","detail":"독일 외무부: 부분 경보"},
    {"country_name":"Venezuela","source_country":"프랑스","status":"yellow","status_label":"대기","detail":"프랑스 외무부: 주의"},
    # 벨라루스
    {"country_name":"Belarus","source_country":"한국","status":"yellow","status_label":"대기","detail":"한국 외교부 2단계"},
    {"country_name":"Belarus","source_country":"미국","status":"yellow","status_label":"대기","detail":"미국 국무부 Level 3"},
    {"country_name":"Belarus","source_country":"일본","status":"yellow","status_label":"대기","detail":"일본 외무성 레벨2"},
    {"country_name":"Belarus","source_country":"독일","status":"red","status_label":"철수","detail":"독일 외무부 Reisewarnung"},
    {"country_name":"Belarus","source_country":"프랑스","status":"yellow","status_label":"대기","detail":"프랑스 외무부: 주의"},
]

def run_seed():
    print("🌱 시드 데이터 입력 중...")
    # 시드 대상 나라들의 기존 시드 데이터 삭제 (영국 제외)
    seed_sources = ["한국", "미국", "일본", "독일", "프랑스"]
    conn = sqlite3.connect("embassy.db")
    cur = conn.cursor()
    for src in seed_sources:
        cur.execute("DELETE FROM embassy_status WHERE source_country = ?", (src,))
    conn.commit()
    conn.close()

    now = datetime.now().isoformat()
    data = [{**d, "updated_at": now} for d in SEED]
    save_to_db(data)
    print(f"✅ {len(data)}개 시드 데이터 입력 완료!")
    print("  (영국·미국은 크롤러가 자동 업데이트)")

if __name__ == "__main__":
    init_db()
    run_seed()
    print("\n✅ 완료! 이제 app.py 실행하세요.")