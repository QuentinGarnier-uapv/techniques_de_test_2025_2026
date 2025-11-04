from flask import Flask, jsonify, Response
import struct
import uuid
from Triangulator import Triangulator

app = Flask(__name__)
tri = Triangulator()

@app.route("/triangulation/<pointSetId>", methods=["GET"])
def get_triangulation(pointSetId: str):
    return jsonify({"code": "", "message": pointSetId}), 0

if __name__ == "__main__":
    app.run(debug=True)
