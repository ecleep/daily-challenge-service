from db import get_db
from models import get_day_key, pick_challenge

def assign_challenge(user_id, category, CHALLENGES):
    today = get_day_key()
    challenges = CHALLENGES.get(category, CHALLENGES["general"])
    challenge = pick_challenge(user_id, category, challenges, today)

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    INSERT OR IGNORE INTO assignments
    (user_id, category, date, challenge, completed)
    VALUES (?, ?, ?, ?, 0)
    """, (user_id, category, today, challenge))

    conn.commit()
    conn.close()

    return today, challenge


def complete_challenge(user_id, category):
    today = get_day_key()
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT * FROM assignments
    WHERE user_id=? AND category=? AND date=?
    """, (user_id, category, today))

    if not cur.fetchone():
        conn.close()
        return None

    cur.execute("""
    UPDATE assignments
    SET completed=1
    WHERE user_id=? AND category=? AND date=?
    """, (user_id, category, today))

    cur.execute("""
    SELECT count, last_day FROM streaks WHERE user_id=?
    """, (user_id,))

    row = cur.fetchone()

    from datetime import datetime
    today_dt = datetime.strptime(today, "%Y-%m-%d").date()

    if row is None:
        count, last_day = 1, None
    else:
        count, last_day = row["count"], row["last_day"]

    if last_day:
        last_dt = datetime.strptime(last_day, "%Y-%m-%d").date()
        diff = (today_dt - last_dt).days

        count = count + 1 if diff == 1 else 1
    else:
        count = 1

    cur.execute("""
    INSERT INTO streaks (user_id, count, last_day)
    VALUES (?, ?, ?)
    ON CONFLICT(user_id) DO UPDATE SET
        count=excluded.count,
        last_day=excluded.last_day
    """, (user_id, count, today))

    conn.commit()
    conn.close()

    return count, today


def get_streak(user_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT count FROM streaks WHERE user_id=?
    """, (user_id,))

    row = cur.fetchone()
    conn.close()

    return row["count"] if row else 0