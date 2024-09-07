from flask import Flask
from flask import Flask, jsonify
from flask_pymongo import pymongo

def connect():
    try:
        CONNECTION_STRING = "mongodb+srv://rafay:1234@cluster0.nvqyp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        return  pymongo.MongoClient(CONNECTION_STRING)

    except Exception as e:
        print('Something went wrong!')
        print(str(e))
        return "Failed to connect to the database."
