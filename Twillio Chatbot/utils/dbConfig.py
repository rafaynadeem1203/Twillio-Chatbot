from flask import Flask
from flask import Flask, jsonify
from flask_pymongo import pymongo

def connect():
    try:
        CONNECTION_STRING = "mongodb+srv://msjbhinder:0rNbvcjqP11bAMcS@cluster0.bprya.mongodb.net/bizbot?retryWrites=true&w=majority&appName=Cluster0"
        return  pymongo.MongoClient(CONNECTION_STRING)

    except Exception as e:
        print('Something went wrong!')
        print(str(e))
        return "Failed to connect to the database."
