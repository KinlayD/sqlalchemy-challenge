import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from collections import defaultdict

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
database_path = "/Users/kinlaydenning/Documents/bootcamp2022/week_10_advanced_database_storage_and_retrieval/sqlalchemy-challenge/hawaii.sqlite"
engine = create_engine(f"sqlite:///{database_path}")

# reflect an existing database into a new model
base = automap_base()
# reflect the tables
base.prepare(engine, reflect=True)

# Save reference to the table
measurement = base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def homepage():

    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(measurement.date, measurement.prcp).all()
    session.close()
    d = {}
    for date, prcp in results:
        if type(prcp) == float:
            d.setdefault(date, []).append(prcp)
    return jsonify(d)

if __name__ == '__main__':
    app.run(debug=True)
