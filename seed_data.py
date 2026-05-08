import os
import psycopg2
import sqlite3
from datetime import datetime

DATABASE_URL = os.environ.get("DATABASE_URL", "")

def get_conn():
    if DATABASE_URL:
        return psycopg2.connect(DATABASE_URL), True
    else:
        conn = sqlite3.connect("embassy.db")
        return conn, False

def save_to_db(results):
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

SEED = [
    {"country_name":"Ukraine","source_country":"한국","status":"red","status_label":"철수","detail":"한국 외교부 4단계"},
    {"country_name":"Ukraine","source_country":"미국","status":"red","status_label":"철수","detail":"미국 국무부 Level 4"},
    {"country_name":"Ukraine","source_country":"일본","status":"red","status_label":"철수","detail":"일본 외무성 레벨4"},
    {"country_name":"Ukraine","source_country":"독일","status":"red","status_label":"철수","detail":"독일 외무부 Reisewarnung"},
    {"country_name":"Ukraine","source_country":"프랑스","status":"red","status_label":"철수","detail":"프랑스 외무부: 여행 금지"},
    {"country_name":"Russia","source_country":"한국","status":"yellow","status_label":"대기","detail":"한국 외교부 2단계"},
    {"country_name":"Russia","source_country":"미국","status":"red","status_label":"철수","detail":"미국 국무부 Level 4"},
    {"country_name":"Russia","source_country":"일본","status":"yellow","status_label":"대기","detail":"일본 외무성 레벨2"},
    {"country_name":"Russia","source_country":"독일","status":"yellow","status_label":"대기","detail":"독일 외무부: 부분 경보"},
    {"country_name":"Russia","source_country":"프랑스","status":"yellow","status_label":"대기","detail":"프랑스 외무부: 주의"},
    {"country_name":"Sudan","source_country":"한국","status":"red","status_label":"철수","detail":"한국 외교부 4단계"},
    {"country_name":"Sudan","source_country":"미국","status":"red","status_label":"철수","detail":"미국 국무부 Level 4"},
    {"country_name":"Sudan","source_country":"일본","status":"red","status_label":"철수","detail":"일본 외무성 레벨4"},
    {"country_name":"Sudan","source_country":"독일","status":"red","status_label":"철수","detail":"독일 외무부 Reisewarnung"},
    {"country_name":"Sudan","source_country":"프랑스","status":"red","status_label":"철수","detail":"프랑스 외무부: 여행 금지"},
    {"country_name":"Haiti","source_country":"한국","status":"red","status_label":"철수","detail":"한국 외교부 4단계"},
    {"country_name":"Haiti","source_country":"미국","status":"red","status_label":"철수","detail":"미국 국무부 Level 4"},
    {"country_name":"Haiti","source_country":"일본","status":"yellow","status_label":"대기","detail":"일본 외무성 레벨3"},
    {"country_name":"Haiti","source_country":"독일","status":"red","status_label":"철수","detail":"독일 외무부 Reisewarnung"},
    {"country_name":"Haiti","source_country":"프랑스","status":"yellow","status_label":"대기","detail":"프랑스 외무부: 주의"},
    {"country_name":"Afghanistan","source_country":"한국","status":"red","status_label":"철수","detail":"한국 외교부 4단계"},
    {"country_name":"Afghanistan","source_country":"미국","status":"red","status_label":"철수","detail":"미국 국무부 Level 4"},
    {"country_name":"Afghanistan","source_country":"일본","status":"red","status_label":"철수","detail":"일본 외무성 레벨4"},
    {"country_name":"Afghanistan","source_country":"독일","status":"red","status_label":"철수","detail":"독일 외무부 Reisewarnung"},
    {"country_name":"Afghanistan","source_country":"프랑스","status":"red","status_label":"철수","detail":"프랑스 외무부: 여행 금지"},
    {"country_name":"Syria","source_country":"한국","status":"red","status_label":"철수","detail":"한국 외교부 4단계"},
    {"country_name":"Syria","source_country":"미국","status":"red","status_label":"철수","detail":"미국 국무부 Level 4"},
    {"country_name":"Syria","source_country":"일본","status":"red","status_label":"철수","detail":"일본 외무성 레벨4"},
    {"country_name":"Syria","source_country":"독일","status":"red","status_label":"철수","detail":"독일 외무부 Reisewarnung"},
    {"country_name":"Syria","source_country":"프랑스","status":"red","status_label":"철수","detail":"프랑스 외무부: 여행 금지"},
    {"country_name":"Yemen","source_country":"한국","status":"red","status_label":"철수","detail":"한국 외교부 4단계"},
    {"country_name":"Yemen","source_country":"미국","status":"red","status_label":"철수","detail":"미국 국무부 Level 4"},
    {"country_name":"Yemen","source_country":"일본","status":"red","status_label":"철수","detail":"일본 외무성 레벨4"},
    {"country_name":"Yemen","source_country":"독일","status":"red","status_label":"철수","detail":"독일 외무부 Reisewarnung"},
    {"country_name":"Yemen","source_country":"프랑스","status":"red","status_label":"철수","detail":"프랑스 외무부: 여행 금지"},
    {"country_name":"Somalia","source_country":"한국","status":"red","status_label":"철수","detail":"한국 외교부 4단계"},
    {"country_name":"Somalia","source_country":"미국","status":"red","status_label":"철수","detail":"미국 국무부 Level 4"},
    {"country_name":"Somalia","source_country":"일본","status":"red","status_label":"철수","detail":"일본 외무성 레벨4"},
    {"country_name":"Somalia","source_country":"독일","status":"red","status_label":"철수","detail":"독일 외무부 Reisewarnung"},
    {"country_name":"Somalia","source_country":"프랑스","status":"red","status_label":"철수","detail":"프랑스 외무부: 여행 금지"},
    {"country_name":"Libya","source_country":"한국","status":"red","status_label":"철수","detail":"한국 외교부 4단계"},
    {"country_name":"Libya","source_country":"미국","status":"red","status_label":"철수","detail":"미국 국무부 Level 4"},
    {"country_name":"Libya","source_country":"일본","status":"yellow","status_label":"대기","detail":"일본 외무성 레벨3"},
    {"country_name":"Libya","source_country":"독일","status":"red","status_label":"철수","detail":"독일 외무부 Reisewarnung"},
    {"country_name":"Libya","source_country":"프랑스","status":"red","status_label":"철수","detail":"프랑스 외무부: 여행 금지"},
    {"country_name":"Myanmar (Burma)","source_country":"한국","status":"yellow","status_label":"대기","detail":"한국 외교부 3단계"},
    {"country_name":"Myanmar (Burma)","source_country":"미국","status":"red","status_label":"철수","detail":"미국 국무부 Level 4"},
    {"country_name":"Myanmar (Burma)","source_country":"일본","status":"yellow","status_label":"대기","detail":"일본 외무성 레벨3"},
    {"country_name":"Myanmar (Burma)","source_country":"독일","status":"yellow","status_label":"대기","detail":"독일 외무부: 부분 경보"},
    {"country_name":"Myanmar (Burma)","source_country":"프랑스","status":"yellow","status_label":"대기","detail":"프랑스 외무부: 주의"},
    {"country_name":"Iraq","source_country":"한국","status":"red","status_label":"철수","detail":"한국 외교부 4단계"},
    {"country_name":"Iraq","source_country":"미국","status":"red","status_label":"철수","detail":"미국 국무부 Level 4"},
    {"country_name":"Iraq","source_country":"일본","status":"red","status_label":"철수","detail":"일본 외무성 레벨4"},
    {"country_name":"Iraq","source_country":"독일","status":"red","status_label":"철수","detail":"독일 외무부 Reisewarnung"},
    {"country_name":"Iraq","source_country":"프랑스","status":"red","status_label":"철수","detail":"프랑스 외무부: 여행 금지"},
    {"country_name":"Israel","source_country":"한국","status":"yellow","status_label":"대기","detail":"한국 외교부 2단계"},
    {"country_name":"Israel","source_country":"미국","status":"yellow","status_label":"대기","detail":"미국 국무부 Level 3"},
    {"country_name":"Israel","source_country":"일본","status":"yellow","status_label":"대기","detail":"일본 외무성 레벨2"},
    {"country_name":"Israel","source_country":"독일","status":"yellow","status_label":"대기","detail":"독일 외무부: 부분 경보"},
    {"country_name":"Israel","source_country":"프랑스","status":"yellow","status_label":"대기","detail":"프랑스 외무부: 주의"},
    {"country_name":"North Korea","source_country":"한국","status":"red","status_label":"철수","detail":"한국 외교부 4단계"},
    {"country_name":"North Korea","source_country":"미국","status":"red","status_label":"철수","detail":"미국 국무부 Level 4"},
    {"country_name":"North Korea","source_country":"일본","status":"red","status_label":"철수","detail":"일본 외무성 레벨4"},
    {"country_name":"North Korea","source_country":"독일","status":"red","status_label":"철수","detail":"독일 외무부 Reisewarnung"},
    {"country_name":"North Korea","source_country":"프랑스","status":"red","status_label":"철수","detail":"프랑스 외무부: 여행 금지"},
    {"country_name":"Iran","source_country":"한국","status":"yellow","status_label":"대기","detail":"한국 외교부 2단계"},
    {"country_name":"Iran","source_country":"미국","status":"red","status_label":"철수","detail":"미국 국무부 Level 4"},
    {"country_name":"Iran","source_country":"일본","status":"yellow","status_label":"대기","detail":"일본 외무성 레벨3"},
    {"country_name":"Iran","source_country":"독일","status":"yellow","status_label":"대기","detail":"독일 외무부: 주의"},
    {"country_name":"Iran","source_country":"프랑스","status":"yellow","status_label":"대기","detail":"프랑스 외무부: 주의"},
    {"country_name":"South Sudan","source_country":"한국","status":"red","status_label":"철수","detail":"한국 외교부 4단계"},
    {"country_name":"South Sudan","source_country":"미국","status":"red","status_label":"철수","detail":"미국 국무부 Level 4"},
    {"country_name":"South Sudan","source_country":"일본","status":"red","status_label":"철수","detail":"일본 외무성 레벨4"},
    {"country_name":"South Sudan","source_country":"독일","status":"red","status_label":"철수","detail":"독일 외무부 Reisewarnung"},
    {"country_name":"South Sudan","source_country":"프랑스","status":"red","status_label":"철수","detail":"프랑스 외무부: 여행 금지"},
    {"country_name":"Mali","source_country":"한국","status":"yellow","status_label":"대기","detail":"한국 외교부 3단계"},
    {"country_name":"Mali","source_country":"미국","status":"red","status_label":"철수","detail":"미국 국무부 Level 4"},
    {"country_name":"Mali","source_country":"일본","status":"yellow","status_label":"대기","detail":"일본 외무성 레벨3"},
    {"country_name":"Mali","source_country":"독일","status":"red","status_label":"철수","detail":"독일 외무부 Reisewarnung"},
    {"country_name":"Mali","source_country":"프랑스","status":"red","status_label":"철수","detail":"프랑스 외무부: 여행 금지"},
    {"country_name":"Venezuela","source_country":"한국","status":"yellow","status_label":"대기","detail":"한국 외교부 2단계"},
    {"country_name":"Venezuela","source_country":"미국","status":"red","status_label":"철수","detail":"미국 국무부 Level 4"},
    {"country_name":"Venezuela","source_country":"일본","status":"yellow","status_label":"대기","detail":"일본 외무성 레벨3"},
    {"country_name":"Venezuela","source_country":"독일","status":"yellow","status_label":"대기","detail":"독일 외무부: 부분 경보"},
    {"country_name":"Venezuela","source_country":"프랑스","status":"yellow","status_label":"대기","detail":"프랑스 외무부: 주의"},
    {"country_name":"Belarus","source_country":"한국","status":"yellow","status_label":"대기","detail":"한국 외교부 2단계"},
    {"country_name":"Belarus","source_country":"미국","status":"yellow","status_label":"대기","detail":"미국 국무부 Level 3"},
    {"country_name":"Belarus","source_country":"일본","status":"yellow","status_label":"대기","detail":"일본 외무성 레벨2"},
    {"country_name":"Belarus","source_country":"독일","status":"red","status_label":"철수","detail":"독일 외무부 Reisewarnung"},
    {"country_name":"Belarus","source_country":"프랑스","status":"yellow","status_label":"대기","detail":"프랑스 외무부: 주의"},
]

def run_seed():
    print("🌱 시드 데이터 주입 중...")
    conn, is_pg = get_conn()
    cur = conn.cursor()
    ph = "%s" if is_pg else "?"
    seed_sources = ["한국","미국","일본","독일","프랑스"]
    for src in seed_sources:
        cur.execute(f"DELETE FROM embassy_status WHERE source_country = {ph}", (src,))
    conn.commit()
    cur.close()
    conn.close()
    now = datetime.now().isoformat()
    data = [{**d, "updated_at": now} for d in SEED]
    save_to_db(data)
    print(f"✅ {len(data)}개 시드 데이터 주입 완료!")

if __name__ == "__main__":
    run_seed()