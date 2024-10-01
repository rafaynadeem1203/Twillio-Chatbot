from flask import jsonify
from bson import ObjectId
from datetime import datetime
from dateutil import parser

import requests
from utils.dbConfig import connect

def format_date(iso_date):
    if iso_date is None:
        return iso_date
    # Parse ISO date string to datetime object
    date_obj = parser.isoparse(iso_date)
    # Format to include date and time,"August 27, 2024, 07:00 PM"
    return date_obj.strftime("%B %d, %Y, %I:%M %p") 

def get_workorders(dbname):
    try:
        connect()
        client = connect()
        db = client.get_database(dbname)
        user_collection = db.workorders
        allWorkorders = list(user_collection.find({}))
        for item in allWorkorders:
            item['_id'] = str(item['_id'])
            item['date']=format_date(item['date'])
            item['startDate']=format_date(item['startDate'])
            item['endDate']=format_date(item['endDate'])

        print("All workorders are: ", allWorkorders)    
        #return jsonify({allWorkorders})
        client.close()
        return allWorkorders

    except Exception as e:
        print("Error fetching Workorders:", str(e))
        return "Internal Server Error", 500
        
        

def get_workorder_by_id(id,dbname):
    try:
        connect()
        client = connect()
        db = client.get_database(dbname)
        user_collection = db.workorders
        workorder_details = user_collection.find_one({"woID": id})
        workorder_details["_id"]=str(workorder_details["_id"])
        workorder_details['date']=format_date(workorder_details['date'])
        workorder_details['startDate']=format_date(workorder_details['date'])
        workorder_details['endDate']=format_date(workorder_details['date'])
        client.close()
        
        if workorder_details:
            print("Workorder details are: ", workorder_details)
            return workorder_details
        else:
            print("Workorder not found")
            return "Workorder not found"

    except Exception as e:
        print("Error fetching Workorder details:", str(e))
        return "Internal Server Error", 500

