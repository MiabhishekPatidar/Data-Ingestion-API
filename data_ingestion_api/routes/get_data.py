import sqlite3
from flask import Blueprint, jsonify

get_data_bp = Blueprint("get_data", __name__)

@get_data_bp.route("/get_data", methods=["GET"])
def get_data():
    try:
        conn = sqlite3.connect("data.db")  # New connection per request
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM uploaded_data")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        data = [dict(zip(columns, row)) for row in rows]
        conn.close()  # Close connection after fetching data
        return jsonify({"data": data, "status": "success"})
    except sqlite3.OperationalError as e:
        return jsonify({"error": str(e), "status": "failed"}), 500
