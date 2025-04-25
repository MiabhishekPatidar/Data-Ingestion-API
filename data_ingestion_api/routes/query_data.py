import sqlite3
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from db import get_db_connection  # ✅ Ensure correct import

query_data_bp = Blueprint("query_data", __name__)

@query_data_bp.route("/query_data", methods=["GET"])
@jwt_required()
def query_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # ✅ Fetch all column names dynamically
        cursor.execute("PRAGMA table_info(uploaded_data)")
        columns_info = cursor.fetchall()
        valid_columns = {col[1] for col in columns_info}  # Extract column names

        # ✅ Extract query parameters dynamically
        query_params = {key: value for key, value in request.args.items() if key in valid_columns}

        if not query_params:
            return jsonify({"error": "No valid query parameters provided", "status": "failed"}), 400

        # ✅ Construct dynamic SQL query
        query = "SELECT * FROM uploaded_data WHERE 1=1"
        params = []

        for column, value in query_params.items():
            query += f" AND {column} = ?"
            params.append(value)

        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        if not rows:
            return jsonify({"error": "No matching records found", "status": "failed"}), 404

        data = [dict(zip(columns, row)) for row in rows]
        return jsonify({"data": data, "status": "success"})

    except sqlite3.OperationalError as e:
        return jsonify({"error": str(e), "status": "failed"}), 500

    finally:
        conn.close()  # ✅ Close connection
