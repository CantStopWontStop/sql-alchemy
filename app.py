import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask_bootstrap import Bootstrap5

from flask import Flask, jsonify, render_template, request, redirect, url_for


#################################################
# Database Setup
#################################################

precip_df = pd.read_csv('Resources/precip_df.csv')
engine    = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)

# reflect an existing database into a new model
Base      = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station     = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
bootstrap = Bootstrap5(app)


#################################################
# Flask Routes
#################################################

# 3. Define what to do when a user hits the index route
@app.route("/")
def index():
    return render_template("index.html")  

@app.route("/start", methods=['GET'])
def start():
    if request.method == "POST":
        start_date = request.form['start_date'].upper()
        return redirect(url_for('success', start_date=start_date))
    return render_template("start.html")  

# 4. Define what to do when a user hits the /about route

# @app.route("/start/<date>/", methods=["GET", "POST"])
# def specific_date(date):
#     print("\n\nDate:", date, "\n\n")
#     images = get_files_on(date)
#     print("\n\nSpecific date images:", images)
#     return default_template(date=date, image_list=images)

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    # results = session.query(measurement.date, measurement.prcp).all()
    
    precip_data = engine.execute("SELECT * FROM measurement WHERE strftime('%Y-%m-%d',date) >= '2016-09-01'").fetchall()

    session.close()

    # Convert list of tuples into normal list
   # all_precip = list(np.ravel(results))

    return render_template("precip.html", query = precip_data) 


@app.route("/api/v1.0/stations", methods=['GET'])
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(station.station, station.name, station.latitude, station.longitude).all()


    session.close()

    # Convert list of tuples into normal list
    
    #all_stations = list(np.ravel(results))
    #all_stations = list(np.ravel(results))

   # result = jsonify(all_stations)

    return render_template("station.html", query = results) 

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    precip_data = engine.execute("SELECT * FROM measurement WHERE strftime('%Y-%m-%d',date) >= '2016-09-01' AND station = 'USC00519281';").fetchall()
    
    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(measurement.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    return render_template("tobs.html", query = precip_data) 

    

@app.route("/template")
def template():
    # Create our session (link) from Python to the DB

    return render_template("template.html")  

if __name__ == "__main__":
    app.run(debug=True)
