# dependecies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# database setup
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# flask setup
app = Flask(__name__)

# flask routes
@app.route("/")
def welcome():
    """List all avaiable api routes."""
    return(
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start_end"
    )

# precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    # session (link) from python to the DB
    session = Session(engine)
    
    # query the results
    results = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()
    
    #closing the session
    session.close()
    
    # create a dictionary and append the data
    precipitation_data = []
    for data, prcp in results:
        dict = {}
        dict["date"] = data
        dict["prcp"] = prcp
        precipitation_data.append(dict)
         
    return jsonify(precipitation_data)

# stations
@app.route("/api/v1.0/stations")
def stations():
    # session from python to the DB
    session = Session(engine)
    
    # query all the station names
    results = session.query(Station.station, Station.name).all()
    
    # close the session
    session.close()
    
    # dictionary with all data appended
    all_stations=[]
    for station, name in results:
        dict={}
        dict['station'] = station
        dict['name'] = name
        all_stations.append(dict)
        
    #return the results
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)
    
    most_active_station = 'USC00519281'
    from_date = '2016-08-23'
    to_date = '2017-08-23'
    
    # Query the dates and temperature observations of the 
    # most-active station for the previous year of data.
    results = session.query(Measurement.date, Measurement.tobs).\
                                        filter(Measurement.station == most_active_station).\
                                        filter(Measurement.date <= to_date).\
                                        filter(Measurement.date >= from_date).all()
    
    # close the session
    session.close()
        
    #get results
    tobs_results = []
    for date, temp in results:
        active_dict = {}
        active_dict[date] = temp
        tobs_results.append(active_dict)

    # return results
    return jsonify(tobs_results)
    
    
@app.route("/api/v1.0/<start>")
def start_def(start):
    from_date = '2016-08-23'
    to_date = '2017-08-23'
    # start the session - python to DB
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs),
                            func.avg(Measurement.tobs), 
                            func.max(Measurement.tobs)).\
                                filter(Measurement.date >= from_date).all()
    
    # close the session
    session.close()
    
    # to hold the data/results
    start_final = []
    
    # gather the data
    for min, avg, max in results:
        info_dict = {}
        info_dict["TMIN"] = min
        info_dict["TAVG"] = avg
        info_dict["TMAX"] = max
    
        start_final.append(info_dict)
     
    #return
    return jsonify(start_final)
    
    
@app.route("/api/v1.0/<start>/<end>")
def end_def(start,end):
    
    from_date = '2016-08-23'
    to_date = '2017-08-23'
    
    session = Session(engine)
    
    results = session.query(func.min(Measurement.tobs),
                            func.avg(Measurement.tobs), 
                            func.max(Measurement.tobs)).\
                                filter(Measurement.date >= from_date).\
                                filter(Measurement.date <= to_date).all()

    # close the session
    session.close()        

    # to hold the data/results
    end_final = []    

    # gather the data
    for min, avg, max in results:
        info_dict = {}
        info_dict["TMIN"] = min
        info_dict["TAVG"] = avg
        info_dict["TMAX"] = max
        end_final.append(info_dict)

    # return
    return jsonify(end_final)

if __name__ == '__main__':
    app.run(debug=True)
