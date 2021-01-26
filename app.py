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
        f"/api/v1.0/start</br>"
        f"/api/v1.0/end</br>"
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

#create a new session, create the tobs route
#Like the precipitation route, this is mostly copy and paste from the starter. If done correctly.

session = Session(engine)
Tempcap = []
@ClimateApp.route("/api/v1.0/tobs")
def tobs():
    #Get a count for all the stations activity
    ACstation = session.query(measurement.station, func.count(measurement.station)).\
        group_by(measurement.station).order_by( func.count(measurement.station).desc()).all()
    
    #Whats the most active and Least Active Station
    MactiveS = ACstation[0][0]
    LactiveS = ACstation[8][0]
    print(f"The most active station is " + MactiveS + ". ")
    print(f"The least active station is " + LactiveS + ". ")

    #Do a query to get the temperature Data of the most active station
    twelvemonths = dt.date(2017, 8, 23) - relativedelta(years=1)
    #Im just redoing twelvemonths. Because i got an error it the variable didnt exist. I think I made twelvemeonths only available for PRCP.
    twelvemtemp = session.query(measurement.date,  measurement.tobs).filter(measurement.date >= twelvemonths).order_by(measurement.date.asc()).all()
    #my code in starter for twelvemtemp didnt work so i just resuse the prcp code. And it works. I think the code i had in starter had too many functions.

    #Capture the data
    for date, temperature in twelvemtemp:
        TdCap = {}
        TdCap[date] = temperature
        Tempcap.append(TdCap)
    return jsonify(Tempcap)
    # return Pdata
session.close()

#setting up the start page
@ClimateApp.route("/api/v1.0/start")

def alpha(alpha = 0):
   
    #Return the minimun, maximum, and average temperature
    STDStats = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date > alpha).all()
    
    #jsonify the result
    return jsonify(STDStats)
    
session.close()

@ClimateApp.route("/api/v1.0/end")
def alphaomega (alpha = 0, omega = 0):

    #this is a copy and past of the prevvious line. But I dont know what im doing.

  
    alpha = session.query(measurement.date).order_by(measurement.date).first()
    omega = session.query(measurement.date).order_by(measurement.date.desc()).first()
    # print(alpha, omega)   

    #I cannot figure this out. If i copy with what i on start, i would get null, and do anything else i get errors thats not consistent.
    #The only constency is that its somewhere in the STDA variable. Which is the crux of the homework
    #I tried creating a variable for alpha and omega, I tried making them = 0, only overrite them.
    # No matter what I do i cannot get anything

    STDA = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date < omega).\
        filter(measurement.date > alpha).all()    
    return jsonify(STDA)
    
session.close()


if __name__ == '__main__':
    ClimateApp.run(debug=True)
