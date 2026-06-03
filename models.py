import hashlib
from datetime import datetime

def get_day_key():
    return datetime.utcnow().date().isoformat()


def pick_challenge(user_id, category, challenges, day):
    key = f"{user_id}-{category}-{day}"
    hash_val = hashlib.sha256(key.encode()).hexdigest()
    index = int(hash_val, 16) % len(challenges)
    return challenges[index]