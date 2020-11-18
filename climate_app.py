import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime
import datetime as dt

from flask import Flask, jsonify
##############################
# Reflect exhisting database
##############################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine,reflect = True)
Measurement = Base.classes.measurement
Station = Base.classes.station


##################################
# Flask Setup
##################################

climate_app = Flask(__name__)


##################################
# Flask Routes
##################################

# Home page
@climate_app.route("/")
def welcome():
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date</br>"
        f"please use date format ... YYYY-MM-DD"
    )

# Precipitation  json
@climate_app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp)
    session.close()

    prcp_data = []
    for date, data in results:
        prcp_dict = {}
        prcp_dict["precipitation(in)"] = data
        prcp_dict["date"] = date
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)

@climate_app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(Station.station, tation.name)
    session.close()

    station_data =[]
    for station, name in results:
        station_dict ={}
        station_dict["name"] = name
        station_dict["station"] = station
        station_data.append(station_dict)

    return jsonify(station_data)

@climate_app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= dt.date(2016,8,23)).filter(Measurement.station == "USC00519281").filter(Measurement.tobs).order_by(Measurement.tobs).all()
    session.close()

    tobs_data = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["temperature"] = tobs
        tobs_data.append(tobs_dict)

    return jsonify(tobs_data)

@climate_app.route("/api/v1.0/<start>")
def start(start):
    start = dt.datetime.strptime(start, "%Y-%m-%d")
    session = Session(engine)
    sel1 = [
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ]
    results = session.query(*sel1).filter(Measurement.date >= start).all()
    start_data = []
    for mini, aveg, maxi in results:
        start_dict = {}
        start_dict["TMIN"] = mini
        start_dict["TAVG"] = aveg
        start_dict["TMAX"] = maxi
        start_data.append(start_dict)

    return jsonify(start_data)

@climate_app.route("/api/v1.0/<start>/<end>")
def end(start,end):
    start = dt.datetime.strptime(start, "%Y-%m-%d")
    end = dt.datetime.strptime(end, "%Y-%m-%d")
    session = Session(engine)
    sel1 = [
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ]
    results = session.query(*sel1).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    start_end_data = []
    for mini, aveg, maxi in results:
        start_end_dict = {}
        start_end_dict["TMIN"] = mini
        start_end_dict["TAVG"] = aveg
        start_end_dict["TMAX"] = maxi
        start_end_data.append(start_end_dict)

    return jsonify(start_end_data)

if __name__ == '__main__':
    climate_app.run(debug = True)