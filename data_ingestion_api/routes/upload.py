from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import pandas as pd
import sqlite3

upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_csv():
    if "file" not in request.files:
        return jsonify({"message": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"message": "No selected file"}), 400

    try:
        df = pd.read_csv(file)

        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()

        # Drop existing table to prevent schema conflicts
        cursor.execute("DROP TABLE IF EXISTS uploaded_data")

        # Dynamically create table with flexible column types
        columns = ", ".join([f'"{col}" TEXT' for col in df.columns])
        cursor.execute(f'CREATE TABLE uploaded_data ({columns})')

        # Insert data into table
        df.to_sql("uploaded_data", conn, if_exists="append", index=False)
        conn.close()

        return jsonify({"message": "Data uploaded successfully"}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500
