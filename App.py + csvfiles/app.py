import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
station = Base.classes.station 
measurement = Base.classes.measurement

##########################################
# Flask Setup
##########################################
session = Session(engine)
app = Flask(__name__)

##########################################
# Flask Routes
##########################################


@app.route("/")
def welcome():
    """List all available api routes."""
    return ( 
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start-end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
     # Create our session (link) from Python to the DB
    session = Session(engine)

    last_12months = (dt.date(2017, 8, 23)) - (dt.timedelta(days=365))
    lastyr_precip = session.query(measurement.date, func.avg(measurement.prcp)).\
    filter(measurement.date >= last_12months).\
    group_by(measurement.date).all()
                              
    all_precip = []
    for date, prcp in lastyr_precip:
        rain_dict = {}
        rain_dict["date"] = date
        rain_dict["prcp"] = prcp
        all_precip.append(rain_dict)                        
    return jsonify(all_precip)


@app.route("/api/v1.0/stations")
def stations():
    station = Base.classes.station 
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(station.station, station.name).all()

    stations_list = []
    for station, name in results:
        stations_dict = {}
        stations_dict["station"] = station 
        stations_dict["name"] = name
        stations_list.append(stations_dict)
    return jsonify(stations_list)


@app.route("/api/v1.0/tobs")
def tobs():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    last_12months = (dt.date(2017, 8, 23)) - (dt.timedelta(days=365))
    tobs_observ = session.query(measurement.date, measurement.tobs).\
    filter(measurement.date >= last_12months).\
    group_by(measurement.date).all()

    tobs_list = []
    for date, tobs in tobs_observ:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_list.append(tobs_dict)
    return jsonify(tobs_list)


@app.route("/api/v1.0/start")
def temp (start = "2016-08-23"): 

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Given start date, to calculate all dates greater than and equal to the start date.
    start = "2016-08-23"
    temp_start = session.query(measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
    filter(measurement.date >= start).group_by(measurement.date).all()

    tempstart_list=list(temp_start)
    return jsonify(tempstart_list)

@app.route("/api/v1.0/start-end")
def tempend(start = "2016-08-23", end = "2017-08-23"):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Given start date, to calculate for dates between the start and end date inclusive.
    start = "2016-08-23"
    end = "2017-08-23"
    temp_start1 = session.query(measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
    filter(measurement.date >= start).filter(measurement.date <= end).group_by(measurement.date).all()

    tempstart_list1=list(temp_start1)
    return jsonify(tempstart_list1)

    
if __name__ == '__main__':
    app.run(debug=True)