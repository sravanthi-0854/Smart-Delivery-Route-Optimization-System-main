from flask import Flask, render_template, request
import requests

app = Flask(__name__)

ORS_API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6Ijk4Zjg2NjZiM2QzNzQ5ZTY5Y2ViOTc3MDdhN2ZhOWViIiwiaCI6Im11cm11cjY0In0="

@app.route('/')
def login():
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/optimize')
def optimize_page():
    return render_template(
        'optimize.html',
        result=None,
        distance=0,
        time_hours=0,
        fuel_cost=0,
        start_lat=None,
        start_lon=None,
        end_lat=None,
        end_lon=None
    )


def get_coordinates(city):

    url = "https://api.openrouteservice.org/geocode/search"

    params = {
        "api_key": "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6Ijk4Zjg2NjZiM2QzNzQ5ZTY5Y2ViOTc3MDdhN2ZhOWViIiwiaCI6Im11cm11cjY0In0=",
        "text": city + ", India",
        "size": 1
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return None

    data = response.json()

    if len(data.get("features", [])) > 0:
        return data["features"][0]["geometry"]["coordinates"]

    return None


@app.route('/optimize', methods=['POST'])
def optimize():

    source = request.form['source']
    destination = request.form['destination']

    start_coords = get_coordinates(source)
    end_coords = get_coordinates(destination)

    if not start_coords or not end_coords:

        return render_template(
            'optimize.html',
            result="❌ City not found.",
            distance=0,
            time_hours=0,
            fuel_cost=0,
            start_lat=None,
            start_lon=None,
            end_lat=None,
            end_lon=None
        )

    headers = {
        "Authorization": "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6Ijk4Zjg2NjZiM2QzNzQ5ZTY5Y2ViOTc3MDdhN2ZhOWViIiwiaCI6Im11cm11cjY0In0=",
        "Content-Type": "application/json"
    }

    body = {
        "coordinates": [
            start_coords,
            end_coords
        ]
    }

    response = requests.post(
        "https://api.openrouteservice.org/v2/directions/driving-car",
        json=body,
        headers=headers
    )

    if response.status_code != 200:

        return render_template(
            'optimize.html',
            result="❌ Unable to calculate route.",
            distance=0,
            time_hours=0,
            fuel_cost=0,
            start_lat=None,
            start_lon=None,
            end_lat=None,
            end_lon=None
        )

    route_data = response.json()

    summary = route_data["routes"][0]["summary"]

    distance_km = round(summary["distance"] / 1000, 2)

    time_hours = round(summary["duration"] / 3600, 2)

    fuel_cost = round(distance_km * 5)

    result = f"{source} → {destination}"

    return render_template(
    "optimize.html",
    result=result,
    distance=distance_km,
    time_hours=time_hours,
    fuel_cost=fuel_cost,
    start_lat=start_coords[1],
    start_lon=start_coords[0],
    end_lat=end_coords[1],
    end_lon=end_coords[0]
)



if __name__ == '__main__':
    app.run(debug=True)