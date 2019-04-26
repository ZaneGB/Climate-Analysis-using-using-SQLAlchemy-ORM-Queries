
import numpy as np
import pandas as pd

import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import desc
from sqlalchemy import create_engine, inspect, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite?check_same_thread=False")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#Step 2 - Climate App

#Now that you have completed your initial analysis, design a Flask API based on the queries that you have developed.

#Use FLASK to create your routes

# import Flask

from flask import Flask, jsonify

#Hints

#You will need to join the station and measurement tables for some of the analysis queries.

#select = [Station.station, Station.name, Measurement.date, Measurement.prcp, Measurement.tob]
#station_join = session.query(*select).filter(Station.station == Measurement.station).limit(10).all()

#Use Flask jsonify to convert your API data into a valid JSON response object.

#Routes

#Create an app

app = Flask(__name__)

#Home page.

@app.route("/")

def home():
    print("Server received request for 'Home' page...")
    return "Lets go on a trip to Hawaii!"

#List all routes that are available.

@app.route("/welcome")

def welcome():
    return (
        f"Welcome to the Hawaiian Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/precipitation2<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start_end<br/>"
    )

#Query for the dates and precipitation observations from a year from the last data point.

@app.route("/api/v1.0/precipitation")

def precipitation():

    end_date = engine.execute("SELECT MAX(date) FROM measurement").fetchall()

#Calculate the start date (using dt module) 1 year ago from the last data point in the database

    end_date_str = end_date[0][0]

    year = int(end_date_str[0:4])
    month=int(end_date_str[5:7])
    day=int(end_date_str[8:10])

    start_date= dt.date(year=year, month=month, day=day) - dt.timedelta(days=364)

    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > start_date).all()
    
# """Return the precipitation data as json"""

    return jsonify(precipitation)


#Convert the query results to a Dictionary using date as the key and prcp as the value.

@app.route("/api/v1.0/precipitation2")

def precipitation2():

    end_date_2 = engine.execute("SELECT MAX(date) FROM measurement").fetchall()

#Calculate the start date (using dt module) 1 year ago from the last data point in the database

    end_date_str_2 = end_date_2[0][0]

    year_2 = int(end_date_str_2[0:4])
    month_2 = int(end_date_str_2[5:7])
    day_2 = int(end_date_str_2[8:10])

    start_date_2 = dt.date(year=year_2, month=month_2, day=day_2) - dt.timedelta(days=364)

    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= start_date_2).all()

    prcp_list = []
    
    for result in results:

        prcp_dict = {}
        prcp_dict['date'] = result[0]
        prcp_dict['prcp'] = result[1]
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)


#/api/v1.0/stations

@app.route("/api/v1.0/stations")

def stations():

# Return a JSON list of stations from the dataset.

    stations = session.query(Station.station).all()

# Convert list of tuples into normal list

    stations_list = [stations]
    
    return jsonify(stations_list)

                                                            
#/api/v1.0/tobs

@app.route("/api/v1.0/tobs")

# Query for the dates and temperature observations from a year from the last data point.

def tobs():

#Calculate the start date (using dt module) 1 year ago from the last data point in the database

    end_date = engine.execute("SELECT MAX(date) FROM measurement").fetchall()

    end_date_str = end_date[0][0]

    year = int(end_date_str[0:4])
    month=int(end_date_str[5:7])
    day=int(end_date_str[8:10])

    start_date= dt.date(year=year, month=month, day=day) - dt.timedelta(days=364)

#Return a JSON list of Temperature Observations (tobs) for the previous year.

    tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= start_date).all()

    tobs_list = [tobs]

    return jsonify(tobs_list)


#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.

@app.route("/api/v1.0/start")

def start():

#To test the app, lets use a start date of 08-16

    start_date = "2016-08-16"

    start = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
    .filter(Measurement.date >= start_date)\
    .group_by(Measurement.date).all()

#Return a JSON list of the minimum temperature, the average temp, and the max temp for dates greater than a given start date

    start_list = [start]

    return jsonify(start_list)
    

#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

@app.route("/api/v1.0/start_end")

def start_end():

    start_date = "2016-08-06"
    end_date = "2016-08-18"
    
    start_end = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
    .filter(Measurement.date >= start_date).filter(Measurement.date <= end_date)\
    .group_by(Measurement.date).all()

#Return a JSON list of the minimum temperature, the average temperature, and the max temperature 
#for a given start date or start-end range.

    start_end_list = [start_end]

    return jsonify(start_end_list)

if __name__ == "__main__":
    app.run(debug=True)

