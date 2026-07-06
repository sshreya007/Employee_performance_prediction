import json
from database.database import get_db


def save_prediction(username: str, employee_name: str, department: str,
                    job_role: str, input_data: dict,
                    prediction: int, confidence: float):
    db = get_db()
    db.execute(
        """INSERT INTO predictions
           (username, employee_name, department, job_role, input_data, prediction, confidence)
           VALUES (?,?,?,?,?,?,?)""",
        (username, employee_name, department, job_role,
         json.dumps(input_data), prediction, confidence),
    )
    db.commit()


def get_predictions(username: str, limit: int = 50) -> list[dict]:
    db = get_db()
    rows = db.execute(
        """SELECT * FROM predictions WHERE username=?
           ORDER BY created_at DESC LIMIT ?""",
        (username, limit),
    ).fetchall()
    result = []
    for row in rows:
        d = dict(row)
        d["input_data"] = json.loads(d["input_data"])
        result.append(d)
    return result


def delete_prediction(pred_id: int, username: str):
    db = get_db()
    db.execute(
        "DELETE FROM predictions WHERE id=? AND username=?",
        (pred_id, username),
    )
    db.commit()


def get_stats(username: str) -> dict:
    db = get_db()
    row = db.execute(
        """SELECT COUNT(*) as total,
                  AVG(prediction) as avg_rating,
                  SUM(CASE WHEN prediction=1 THEN 1 ELSE 0 END) as low,
                  SUM(CASE WHEN prediction=4 THEN 1 ELSE 0 END) as outstanding
           FROM predictions WHERE username=?""",
        (username,),
    ).fetchone()
    return dict(row)
