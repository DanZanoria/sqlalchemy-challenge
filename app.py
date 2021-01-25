#!/usr/bin/env python
# coding: utf-8

# In[93]:


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


# In[94]:


#prepare the engine and the reflection. 

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)


# In[95]:


# View all of the classes that automap found
Base.classes.keys()


# In[96]:


# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station


# In[97]:


# so now the preparation is done. Lets create the flask server

ClimateApp = Flask(__name__)


# In[98]:


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


# In[112]:


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
    results = session.query(measurement.date,  measurement.prcp).       filter(measurement.date >= twelvemonths).order_by(measurement.date.asc()).all()

    for date, prcp in results:
        pdict = {}
        pdict[date] = prcp 
        Pdata.append(pdict)
    return jsonify(Pdata)
    # return Pdata
print(Pdata)



if __name__ == '__main__':
    ClimateApp.run(debug=True)
