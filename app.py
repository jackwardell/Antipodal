from flask import Flask, render_template, request, jsonify
import os
from mapbox import Geocoder

app = Flask(__name__)

MAPBOX_API_ACCESS_TOKEN = os.getenv("MAPBOX_API_ACCESS_TOKEN")

mapbox_geocoder = Geocoder(access_token=MAPBOX_API_ACCESS_TOKEN)
location_types = ["country", "region", "district", "locality", "place", "neighborhood"]


class Config:
    name = "Antipodal Coefficient Calculator"


@app.route("/")
def hello_world():
    print(request.args)
    return render_template("index.html", config=Config)


@app.route("/api/location")
def search_dropdown():
    location = request.args.get("q")
    query = mapbox_geocoder.forward(location, types=location_types)
    results = query.json()["features"]
    return jsonify(
        [
            {"text": i["place_name"], "value": i["geometry"]["coordinates"]}
            for i in results
        ]
    )
    # return jsonify([i["place_name"] for i in results])


if __name__ == "__main__":
    app.run()
