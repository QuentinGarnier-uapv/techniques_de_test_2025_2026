from flask import Flask, jsonify, Response
import struct
import uuid
from Triangulator import Triangulator

app = Flask(__name__)
tri = Triangulator()

@app.route("/triangulation/<pointSetId>", methods=["GET"])
def get_triangulation(pointSetId: str):
    try:
        Triangulator.triangulate(tri, pointSetId)
        return jsonify({"code": "ok", "message": pointSetId}), 200
    except Exception as e:
        return jsonify({"code": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
