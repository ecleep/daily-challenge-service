# Daily Challenge Assignment Service

## Overview

The Daily Challenge Assignment Service is a Python Flask microservice that assigns users a daily challenge based on their selected activity category and tracks completion streaks.

The service ensures:

* Consistent daily challenge assignment per user and category
* Deterministic challenge selection per day
* Persistent streak tracking using SQLite

---

## Features

### 1. Daily Challenge Assignment

* Assigns a challenge based on:

  * user_id
  * category
  * current date

* Ensures:

  * Same user + category + same day = same challenge
  * A new challenge will be issued every day.

---

### 2. Streak Tracking

* Tracks consecutive days of completed challenges
* Increments streak if challenges are completed on consecutive days
* Resets streak if a day is missed

---

## Project Structure

```text
daily-challenge-service/
│
├── app.py              # Flask API layer
├── services.py         # Business logic
├── db.py               # SQLite database layer
├── models.py           # Challenge selection logic
├── config.py           # Configuration constants
├── challenges.json     # Challenge data
├── challenges.db       # SQLite database file
└── README.md
```

## Architecture

The system is split into layers:

* **app.py** → API endpoints (HTTP interface only)
* **services.py** → Core business logic (assignment, completion, streaks)
* **db.py** → Database connection and schema initialization
* **models.py** → Deterministic challenge selection logic
* **config.py** → Configuration values

This separation improves maintainability and testability.

---

## Installation

### 1. Clone repository

```bash
git clone https://github.com/ecleep/daily-challenge-service.git
cd daily-challenge-service
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Service

Start the Flask server:

```bash
python app.py
```

Service runs at:

```
http://localhost:6000
```

---

## API Endpoints

### 1. Daily Challenge Assignment

Returns the assigned challenge for a user and category.

#### Request

```http
GET /daily-challenge?user_id=123&category=study
```

#### Response

```json
{
  "user_id": "123",
  "category": "study",
  "date": "2026-06-04",
  "challenge": "Solve 5 algebra problems"
}
```

---

### 2. Complete Challenge

Marks today’s challenge as completed and updates streak.

#### Request

```http
POST /complete-challenge
Content-Type: application/json
```

```json
{
  "user_id": "123",
  "category": "study"
}
```

#### Response

```json
{
  "message": "Challenge completed",
  "streak": 3,
  "date": "2026-06-04"
}
```

---

### 3. Get Streak

Returns current streak count.

#### Request

```http
GET /streak?user_id=123
```

#### Response

```json
{
  "user_id": "123",
  "streak": 3
}
```

---

## Data Storage

The service currently uses SQLite for persistence.

### Tables

#### assignments

Stores daily assigned challenges.

| Column    | Type    | Description        |
| --------- | ------- | ------------------ |
| user_id   | TEXT    | User identifier    |
| category  | TEXT    | Challenge category |
| date      | TEXT    | Assignment date    |
| challenge | TEXT    | Assigned challenge |
| completed | INTEGER | Completion status  |

---

#### streaks

Stores user streak data.

| Column   | Type    | Description          |
| -------- | ------- | -------------------- |
| user_id  | TEXT    | User identifier      |
| count    | INTEGER | Current streak count |
| last_day | TEXT    | Last completion date |

---

## Challenge Data

Stored in `challenges.json`.

Example:

```json
{
  "categories": {
    "study": [
      "Solve 5 algebra problems",
      "Read 10 pages of a textbook"
    ],
    "fitness": [
      "Run 2 kilometers",
      "Do 20 push-ups"
    ]
  }
}
```

New challenges can be added without modifying code.

---

## Design Logic

### Daily Challenge Selection

A deterministic hash-based algorithm ensures consistency:

```
user_id + category + date → SHA-256 → index → challenge
```

This guarantees:

* Repeatable results within a day
* Automatic rotation across days
* No database lookup required for selection

---

### Streak Calculation

Rules:

* +1 if completed on consecutive days
* Reset to 1 if a day is missed
* Based on date difference between last completion and current day

---

## Dependencies

* Flask
* SQLite (built-in with Python)

Install:

```bash
pip install Flask
```

---

## Future Improvements

* Replace SQLite with an actual database for scaling
* Add authentication
* Add rate limiting
* Add caching for performance
