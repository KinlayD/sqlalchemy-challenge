from this import d
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from collections import defaultdict
import datetime as dt

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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/<start>"

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
    sq = session.query(measurement.station).\
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
    return(jsonify(date_temp_list))



if __name__ == '__main__':
    app.run(debug=True)
