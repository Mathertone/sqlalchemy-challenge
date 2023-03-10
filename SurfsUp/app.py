from flask import Flask, jsonify
import datetime as dt
import numpy as np
import pandas as pd

# Create an instance of Flask
app = Flask(__name__)

# Define the home page
@app.route("/")
def home():
    # List all available routes
    return (
        f"Welcome to the Hawaii Weather API!<br/>"
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
        f"<a href='/api/v1.0/start_date'>/api/v1.0/start_date</a><br/>"
        f"<a href='/api/v1.0/start_date/end_date'>/api/v1.0/start_date/end_date</a><br/>"
    )

# Define the precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query the precipitation data for the last 12 months
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= last_year).all()

    # Create a dictionary using date as the key and prcp as the value
    precipitation = {}
    for result in results:
        precipitation[result[0]] = result[1]

    # Return the JSON representation of the dictionary
    return jsonify(precipitation)

# Define the stations route
@app.route("/api/v1.0/stations")
def stations():
    # Query the stations
    results = session.query(Station.station).all()

    # Convert list of tuples into normal list
    stations = list(np.ravel(results))

    # Return the JSON list of stations
    return jsonify(stations)

# Define the tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    # Query the temperature observations for the most active station in the last year of data
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(measurement.date, measurement.tobs).filter(measurement.station == 'USC00519281').filter(measurement.date >= last_year).all()

    # Create a list of temperature observations
    temperatures = list(np.ravel(results))

    # Return the JSON list of temperature observations
    return jsonify(temperatures)

# Define the start and end date route
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end=None):
    # Query the minimum, average, and maximum temperature for a given start or start-end range
    if end:
        results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
            filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    else:
        results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
            filter(measurement.date >= start).all()

    # Create a list of dictionaries with the minimum, average, and maximum temperature
    temperatures = []
    for result in results:
        temperature = {}