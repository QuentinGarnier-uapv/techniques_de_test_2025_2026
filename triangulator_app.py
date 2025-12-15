"""Flask application for Triangulator service."""
from flask import Flask, Response, jsonify
import urllib.error


from Triangulator import Triangulator

app = Flask(__name__)
# On instancie le service
tri = Triangulator()


@app.route("/triangulation/<pointSetId>", methods=["GET"])
def get_triangulation(pointSetId: str):
    """Handle triangulation request."""
    try:
        result = tri.triangulate(pointSetId)

        return Response(result, mimetype='application/octet-stream', status=200)

    except ValueError as e:
        # Invalid UUID or data format
        return jsonify({
             "code": "TRIANGULATION_FAILED",
             "message": "Triangulation could not be computed for the given point set."
        }), 400

    except urllib.error.HTTPError as e:
        status_code = 500
        if e.code == 404:
            status_code = 404
        elif e.code == 503:
            status_code = 503
        
        return jsonify({
            "code": "TRIANGULATION_FAILED",
            "message": "Triangulation could not be computed for the given point set."
        }), status_code

    except urllib.error.URLError as e:
        # Connection failed
        return jsonify({
            "code": "TRIANGULATION_FAILED",
            "message": "Triangulation could not be computed for the given point set."
        }), 503

    except Exception as e:
        return jsonify({
            "code": "TRIANGULATION_FAILED",
            "message": "Triangulation could not be computed for the given point set."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)