from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
import pandas as pd
import sqlite3

stats_bp = Blueprint("stats", __name__)

@stats_bp.route("/stats", methods=["GET"])
@jwt_required()
def get_stats():
    try:
        conn = sqlite3.connect("data.db")
        df = pd.read_sql_query("SELECT * FROM uploaded_data", conn)
        conn.close()

        if df.empty:
            return jsonify({"message": "No data available"}), 404

        # Identify numeric and categorical columns
        numerical_cols = [col for col in df.select_dtypes(include=["int64", "float64"]).columns if "phone" not in col.lower()]
        categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()

        # Compute statistics
        stats = {
            "Total Rows": len(df),
            "Total Columns": len(df.columns),
            "Missing Values (%)": (df.isnull().sum() / len(df) * 100).to_dict(),
            "Most Frequent Values": df.mode().iloc[0].dropna().to_dict()
        }

        if numerical_cols:
            numeric_summary = df[numerical_cols].describe().to_dict()
            for metric in numeric_summary:
                numeric_summary[metric] = {k: round(v, 2) for k, v in numeric_summary[metric].items()}  # Round values
            stats["Numeric Summary"] = numeric_summary

        return jsonify({"status": "success", "statistics": stats})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
