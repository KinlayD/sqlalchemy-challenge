import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# database setup
database_path = "/Users/kinlaydenning/Documents/bootcamp2022/week_10_advanced_database_storage_and_retrieval/sqlalchemy-challenge/hawaii.sqlite"
engine = create_engine(f"sqlite:///{database_path}")

# reflect an existing database into a new model
base = automap_base()
# reflect the tables
base.prepare(engine, reflect=True)

# Save reference to the table
measurement = base.classes.measurement
station = base.classes.station

# flask setup
app = Flask(__name__)

# flask routes
@app.route("/")
def homepage():

    return (
        f"Available Routes:<br/>"
        f"-----------------------<br/>"
        f"                        <br/>"
        f"-----------------------<br/>"
        f"Precipitation (In Inches) by date:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"-----------------------<br/>"
        f"                        <br/>"
        f"-----------------------<br/>"
        f"List of stations: <br/>"
        f"/api/v1.0/stations<br/>"
        f"-----------------------<br/>"
        f"                        <br/>"
        f"-----------------------<br/>"
        f"Provide a start date, find avg, max, and min temperature<br/>" 
        f"for all dates greater than or equal to start date (In Fahrenheit):<br/>"
        f"format: YY-M-D<br/>" 
        f"/api/v1.0/<start><br/>"
        f"-----------------------<br/>"
        f"                        <br/>"
        f"-----------------------<br/>"
        f"Provide a start date and an end date, find avg, max and<br/>"
        f"min temperature within the the given interval: <br/>"
        f"format: YY-M-D/YY-M-D<br/>" 
        f"/api/v1.0/<start>/<end><br/>"
        f"-----------------------"

    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(measurement.date, measurement.prcp).all()
    session.close()

    precipitation = {}
    for date, prcp in results:
        if type(prcp) == float:
            precipitation.setdefault(date, []).append(prcp)
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    sq = session.query(station.name).\
    filter(measurement.station == station.station).distinct().all()
    session.close()
    
    sd_list = list(np.ravel(sq))
    return jsonify(sd_list)

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    func_dt = [func.avg(measurement.tobs),
                    func.max(measurement.tobs),
                    func.min(measurement.tobs)]
    start = session.query(*func_dt).\
    filter(func.strftime("%Y-%m-%d", measurement.date) >= start).all()
    session.close()
    date_temp_list = list(np.ravel(start))
    return (jsonify(date_temp_list))

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)
    func_dt = [func.avg(measurement.tobs),
                    func.max(measurement.tobs),
                    func.min(measurement.tobs)]
    start_end = session.query(*func_dt).\
    filter(func.strftime("%Y-%m-%d", measurement.date) >= start).\
    filter(func.strftime("%Y-%m-%d", measurement.date) <= end).all()
    session.close()
    date_temp_range_list = list(np.ravel(start_end))
    return jsonify(date_temp_range_list)

if __name__ == '__main__':
    app.run(debug=True)
