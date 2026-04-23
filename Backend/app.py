# ============================================================
#  app.py  —  Flask REST API  (run this to start the backend)
# ============================================================

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys, os

# Make sure the backend package is on the path
sys.path.insert(0, os.path.dirname(__file__))

from student_model import (
    add_student, get_all_students, get_student_by_id,
    update_student, delete_student,
    get_departments, get_dashboard_stats, get_activity_log,
)

app = Flask(__name__)
CORS(app)   # allow the frontend (different port) to call the API


# ─── Health ──────────────────────────────────────────────────
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "Student Management API"})


# ─── Dashboard ───────────────────────────────────────────────
@app.route("/api/dashboard", methods=["GET"])
def dashboard():
    return jsonify(get_dashboard_stats())


# ─── Students ────────────────────────────────────────────────
@app.route("/api/students", methods=["GET"])
def list_students():
    search      = request.args.get("search", "")
    dept_id     = request.args.get("department_id", type=int)
    status      = request.args.get("status")
    page        = request.args.get("page", 1, type=int)
    per_page    = request.args.get("per_page", 10, type=int)
    return jsonify(get_all_students(search, dept_id, status, page, per_page))


@app.route("/api/students", methods=["POST"])
def create_student():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided."}), 400
    result = add_student(data)
    code   = 201 if result["success"] else 400
    return jsonify(result), code


@app.route("/api/students/<student_id>", methods=["GET"])
def read_student(student_id):
    result = get_student_by_id(student_id)
    code   = 200 if result["success"] else 404
    return jsonify(result), code


@app.route("/api/students/<student_id>", methods=["PUT"])
def edit_student(student_id):
    data   = request.get_json()
    result = update_student(student_id, data)
    code   = 200 if result["success"] else 400
    return jsonify(result), code


@app.route("/api/students/<student_id>", methods=["DELETE"])
def remove_student(student_id):
    result = delete_student(student_id)
    code   = 200 if result["success"] else 404
    return jsonify(result), code


# ─── Departments ─────────────────────────────────────────────
@app.route("/api/departments", methods=["GET"])
def list_departments():
    return jsonify(get_departments())


# ─── Activity Log ────────────────────────────────────────────
@app.route("/api/logs", methods=["GET"])
def activity_logs():
    limit = request.args.get("limit", 20, type=int)
    return jsonify(get_activity_log(limit))


# ─── Run ─────────────────────────────────────────────────────


if __name__ == "__main__":
    print("\n🎓  Student Management API  running on  http://localhost:5000\n")
    app.run(debug=True, port=5000)