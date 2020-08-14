import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()
# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

measurement = Base.classes.measurement
station = Base.classes.station


# 3. Define static routes
@app.route("/")
def welcome():
    return (
        f"Welcome to Hawaii API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/startdateYYYYMMDD<br/>"
        f"/api/v1.0/start/start/endYYYYMMDD/YYYYMMDD"
    )

@app.route("/api/v1.0/precipitation")
def index():
    session = Session(engine)
    results = session.query(measurement.date, measurement.prcp).all()
    session.close()

    # prcp_dictionary = []
    # prcp_dict = {}
    # for r in results:
    #     prcp_dict["date"] = r[0]
    #     prcp_dict["prcp"] = r[1]
    #     prcp_dictionary.append(prcp_dict)
    
    return jsonify(results)
#look into jsonify function
#print(prcp_dict)


@app.route("/api/v1.0/stations")
def station_names():
    session = Session(engine)
    results_stat = session.query(station.station).all()
    session.close() 
    station_list = list(np.ravel(results_stat))
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def temperature():
    session = Session(engine)
    results_temp = session.query(measurement.station, measurement.date, measurement.tobs).filter(measurement.date > '2016-08-23', measurement.station == 'USC00519523')
    session.close()
    station_temp = list(results_temp)
    return jsonify(station_temp)

@app.route("/api/v1.0/<start>")
def max_min_avg(start):
    session = Session(engine)
    max_temp = session.query(func.max(measurement.tobs).filter(measurement.date > start)).scalar()
    min_temp = session.query(func.min(measurement.tobs).filter(measurement.date > start)).scalar()
    avg_temp = session.query(func.avg(measurement.tobs).filter(measurement.date > start)).scalar()
    session.close()
    station_mma = [max_temp, min_temp, avg_temp]
    return jsonify(station_mma)

@app.route("/api/v1.0/start/<start>/<end>")
def max_mins_avgs(start,end):
    session = Session(engine)
    max_temps = session.query(func.max(measurement.tobs).filter(measurement.date > start, measurement.date < end)).scalar()
    min_temps = session.query(func.min(measurement.tobs).filter(measurement.date > start, measurement.date < end)).scalar()
    avg_temps = session.query(func.avg(measurement.tobs).filter(measurement.date > start, measurement.date < end)).scalar()
    session.close()
    station_mmas = [max_temps, min_temps, avg_temps]
    return jsonify(station_mmas)


if __name__ == '__main__':
    app.run(debug=True)


