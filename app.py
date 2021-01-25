#!/usr/bin/env python
# coding: utf-8

#Creating the app.py through jupyter. For my benefit. Will convert later

#import Flask, jsonify from the module flask
from flask import Flask, jsonify

#import every module and funtions i may need to accomplish this
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from dateutil.relativedelta import relativedelta

#prepare the engine and the reflection. 

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# View all of the classes that automap found
Base.classes.keys()

# Save references to each table
measurement = Base.classes.measurement
statoin = Base.classes.station

#I dont know why but when i originally have the variable as station and not statoin, the variable caused an error when it was time to make the station page


# Lets create the flask server. 

ClimateApp = Flask(__name__)



# Creating the routes. Lets create the first route
@ClimateApp.route("/")
def welcome():
    """List all routes that are available"""
    return (
        f"Welcome to the Giant Robot Climate App<br/>"
        f"Giant Robots protects these routes</br>"
        f"/api/v1.0/precipitation</br>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/<start></br>"
        f"/api/v1.0/<end></br>"
    )


#create the precipation route
# start a session. 
session = Session(engine)
# Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
# Return the JSON representation of your dictionary.
   


Pdata = []
@ClimateApp.route("/api/v1.0/precipitation")
def precipitation():
   #Copying what i did from the starter
    twelvemonths = dt.date(2017, 8, 23) - relativedelta(years=1)
    results = session.query(measurement.date,  measurement.prcp).filter(measurement.date >= twelvemonths).order_by(measurement.date.asc()).all()

    for date, prcp in results:
        pdict = {}
        pdict[date] = prcp 
        Pdata.append(pdict)
    return jsonify(Pdata)
    # return Pdata
print(Pdata)
session.close()

session = Session(engine)
statcap = []
@ClimateApp.route("/api/v1.0/stations")
def stations():
    stion = session.query(statoin.station, statoin.name, statoin.latitude, statoin.longitude, statoin.elevation).all()

    for station_name, latitude, longitude, elevation, station  in stion:
        ScapD = {}
        ScapD["station"] = station
        ScapD["name"] = station_name
        ScapD["latitude"] = latitude
        ScapD["elevation"] = elevation
        ScapD["longitude"] = longitude
        statcap.append(ScapD)
    return jsonify(statcap)
    # return statcap

session.close()

if __name__ == '__main__':
    ClimateApp.run(debug=True)
