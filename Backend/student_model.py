# ============================================================
#  student_model.py  —  All DB operations for students
# ============================================================

from db_config import get_connection, get_cursor
from mysql.connector import Error


# ─────────────────────────────────────────────
#  CREATE
# ─────────────────────────────────────────────

def add_student(data: dict) -> dict:
    """
    Insert a new student.
    data keys: student_id, first_name, last_name, email, phone,
               dob, gender, department_id, year, gpa, address, status
    Returns {"success": True, "message": "...", "id": <new_id>}
    """
    sql = """
        INSERT INTO students
            (student_id, first_name, last_name, email, phone,
             dob, gender, department_id, year, gpa, address, status)
        VALUES
            (%(student_id)s, %(first_name)s, %(last_name)s, %(email)s, %(phone)s,
             %(dob)s, %(gender)s, %(department_id)s, %(year)s, %(gpa)s,
             %(address)s, %(status)s)
    """
    conn = get_connection()
    cur  = get_cursor(conn)
    try:
        cur.execute(sql, data)
        new_id = cur.lastrowid
        _log(conn, "ADD", data["student_id"], f"Added student {data['first_name']} {data['last_name']}")
        return {"success": True, "message": "Student added successfully.", "id": new_id}
    except Error as e:
        return {"success": False, "message": str(e)}
    finally:
        cur.close(); conn.close()


# ─────────────────────────────────────────────
#  READ
# ─────────────────────────────────────────────

def get_all_students(search: str = "", department_id: int = None,
                     status: str = None, page: int = 1, per_page: int = 10) -> dict:
    """Return paginated list of students with optional filters."""
    where_clauses, params = [], {}

    if search:
        where_clauses.append(
            "(s.first_name LIKE %(search)s OR s.last_name LIKE %(search)s "
            " OR s.student_id LIKE %(search)s OR s.email LIKE %(search)s)"
        )
        params["search"] = f"%{search}%"

    if department_id:
        where_clauses.append("s.department_id = %(dept)s")
        params["dept"] = department_id

    if status:
        where_clauses.append("s.status = %(status)s")
        params["status"] = status

    where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

    count_sql = f"SELECT COUNT(*) AS total FROM students s {where_sql}"
    data_sql  = f"""
        SELECT s.*, d.name AS department_name, d.code AS department_code
        FROM students s
        LEFT JOIN departments d ON s.department_id = d.id
        {where_sql}
        ORDER BY s.created_at DESC
        LIMIT %(limit)s OFFSET %(offset)s
    """
    params["limit"]  = per_page
    params["offset"] = (page - 1) * per_page

    conn = get_connection()
    cur  = get_cursor(conn)
    try:
        cur.execute(count_sql, params)
        total = cur.fetchone()["total"]
        cur.execute(data_sql, params)
        students = cur.fetchall()
        # Convert date / decimal objects to JSON-safe types
        for s in students:
            if s.get("dob"):        s["dob"]  = str(s["dob"])
            if s.get("gpa") is not None: s["gpa"] = float(s["gpa"])
            if s.get("created_at"): s["created_at"] = str(s["created_at"])
            if s.get("updated_at"): s["updated_at"] = str(s["updated_at"])
        return {"success": True, "students": students, "total": total,
                "page": page, "per_page": per_page,
                "total_pages": -(-total // per_page)}   # ceiling division
    except Error as e:
        return {"success": False, "message": str(e)}
    finally:
        cur.close(); conn.close()


def get_student_by_id(student_id: str) -> dict:
    """Fetch a single student by their student_id string."""
    sql = """
        SELECT s.*, d.name AS department_name, d.code AS department_code
        FROM students s
        LEFT JOIN departments d ON s.department_id = d.id
        WHERE s.student_id = %s
    """
    conn = get_connection()
    cur  = get_cursor(conn)
    try:
        cur.execute(sql, (student_id,))
        row = cur.fetchone()
        if row:
            if row.get("dob"):        row["dob"]  = str(row["dob"])
            if row.get("gpa") is not None: row["gpa"] = float(row["gpa"])
            if row.get("created_at"): row["created_at"] = str(row["created_at"])
            if row.get("updated_at"): row["updated_at"] = str(row["updated_at"])
            return {"success": True, "student": row}
        return {"success": False, "message": "Student not found."}
    except Error as e:
        return {"success": False, "message": str(e)}
    finally:
        cur.close(); conn.close()


def get_dashboard_stats() -> dict:
    """Return counts for the dashboard cards."""
    conn = get_connection()
    cur  = get_cursor(conn)
    try:
        cur.execute("SELECT COUNT(*) AS c FROM students WHERE status='Active'")
        active = cur.fetchone()["c"]

        cur.execute("SELECT COUNT(*) AS c FROM students")
        total = cur.fetchone()["c"]

        cur.execute("SELECT COUNT(*) AS c FROM departments")
        depts = cur.fetchone()["c"]

        cur.execute("SELECT AVG(gpa) AS avg_gpa FROM students WHERE gpa IS NOT NULL")
        avg_gpa = cur.fetchone()["avg_gpa"] or 0

        cur.execute("""
            SELECT d.name AS dept, COUNT(s.id) AS cnt
            FROM students s
            JOIN departments d ON s.department_id = d.id
            GROUP BY d.name ORDER BY cnt DESC LIMIT 6
        """)
        dept_dist = cur.fetchall()

        cur.execute("""
            SELECT DATE_FORMAT(created_at,'%Y-%m') AS month, COUNT(*) AS cnt
            FROM students
            GROUP BY month ORDER BY month DESC LIMIT 6
        """)
        monthly = cur.fetchall()

        return {
            "success": True,
            "active_students": active,
            "total_students":  total,
            "departments":     depts,
            "avg_gpa":         round(float(avg_gpa), 2),
            "dept_distribution": dept_dist,
            "monthly_enrollments": monthly,
        }
    except Error as e:
        return {"success": False, "message": str(e)}
    finally:
        cur.close(); conn.close()


# ─────────────────────────────────────────────
#  UPDATE
# ─────────────────────────────────────────────

def update_student(student_id: str, data: dict) -> dict:
    """Update fields for an existing student."""
    allowed = ["first_name", "last_name", "email", "phone", "dob",
               "gender", "department_id", "year", "gpa", "address", "status"]
    updates = {k: v for k, v in data.items() if k in allowed}
    if not updates:
        return {"success": False, "message": "No valid fields to update."}

    set_clause = ", ".join(f"{k} = %({k})s" for k in updates)
    updates["_sid"] = student_id
    sql = f"UPDATE students SET {set_clause} WHERE student_id = %(_sid)s"

    conn = get_connection()
    cur  = get_cursor(conn)
    try:
        cur.execute(sql, updates)
        if cur.rowcount == 0:
            return {"success": False, "message": "Student not found."}
        _log(conn, "UPDATE", student_id, f"Updated fields: {list(updates.keys())}")
        return {"success": True, "message": "Student updated successfully."}
    except Error as e:
        return {"success": False, "message": str(e)}
    finally:
        cur.close(); conn.close()


# ─────────────────────────────────────────────
#  DELETE
# ─────────────────────────────────────────────

def delete_student(student_id: str) -> dict:
    """Delete a student by student_id."""
    conn = get_connection()
    cur  = get_cursor(conn)
    try:
        cur.execute("SELECT first_name, last_name FROM students WHERE student_id=%s", (student_id,))
        row = cur.fetchone()
        if not row:
            return {"success": False, "message": "Student not found."}
        cur.execute("DELETE FROM students WHERE student_id=%s", (student_id,))
        _log(conn, "DELETE", student_id, f"Deleted {row['first_name']} {row['last_name']}")
        return {"success": True, "message": "Student deleted successfully."}
    except Error as e:
        return {"success": False, "message": str(e)}
    finally:
        cur.close(); conn.close()


# ─────────────────────────────────────────────
#  DEPARTMENTS
# ─────────────────────────────────────────────

def get_departments() -> dict:
    conn = get_connection()
    cur  = get_cursor(conn)
    try:
        cur.execute("SELECT * FROM departments ORDER BY name")
        return {"success": True, "departments": cur.fetchall()}
    except Error as e:
        return {"success": False, "message": str(e)}
    finally:
        cur.close(); conn.close()


# ─────────────────────────────────────────────
#  ACTIVITY LOG
# ─────────────────────────────────────────────

def get_activity_log(limit: int = 20) -> dict:
    conn = get_connection()
    cur  = get_cursor(conn)
    try:
        cur.execute(
            "SELECT * FROM activity_log ORDER BY created_at DESC LIMIT %s", (limit,)
        )
        rows = cur.fetchall()
        for r in rows:
            r["created_at"] = str(r["created_at"])
        return {"success": True, "logs": rows}
    except Error as e:
        return {"success": False, "message": str(e)}
    finally:
        cur.close(); conn.close()


# ─────────────────────────────────────────────
#  INTERNAL HELPER
# ─────────────────────────────────────────────

def _log(conn, action: str, student_id: str, details: str):
    try:
        cur = get_cursor(conn)
        cur.execute(
            "INSERT INTO activity_log (action, student_id, details) VALUES (%s,%s,%s)",
            (action, student_id, details)
        )
        cur.close()
    except Exception:
        pass   # logging should never break main flow
