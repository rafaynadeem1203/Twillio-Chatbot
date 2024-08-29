from flask import jsonify
import requests
from bson import ObjectId
from utils.dbConfig import connect

from utils.dbConfig import connect
def convert_phone_number(phone_number):
    return "0" + phone_number[12:]

def get_employees(userPhone):
    try:
        connect()
        client = connect()
        transformedPhone = convert_phone_number(userPhone)
        db = client.get_database(transformedPhone)
        user_collection = db.employees
        allEmployees = list(user_collection.find({}))
        for employee in allEmployees:
            employee['_id'] = str(employee['_id'])
        print("allEmployee are: ", allEmployees)    
        #return jsonify({allEmployees})
        return allEmployees

    except Exception as e:
        print("Error fetching Employees:", str(e))
        return "Internal Server Error", 500       


def get_employee_id_by_name(employee_name,userPhone):
    try:
        connect()
        client = connect()
        transformedPhone = convert_phone_number(userPhone)
        print("transformed phone:",transformedPhone)
        db = client.get_database(transformedPhone)
        user_collection = db.employees
        employeeDetails = user_collection.find_one({"name": employee_name})
        client.close()

        if employeeDetails:
            print("employee details are: ", employeeDetails)
            return employeeDetails['_id']
        else:
            print("Employee not found")
            return "Employee not found"#, 404

    except Exception as e:
        print("Error fetching Employee details:", str(e))
        return "Internal Server Error", 500


    
def delete_employee(employee_id, userPhone):
    try:
        connect()
        client = connect()
        transformedPhone = convert_phone_number(userPhone)
        db = client.get_database(transformedPhone)
        user_collection = db.employees
        result = user_collection.delete_one({"_id": ObjectId(employee_id)})
        client.close()

        if result.deleted_count > 0:
            return "Employee deleted successfully"
        else:
            return "Employee not found"

    except Exception as e:
        print("Error deleting employee:", str(e))
        return "Error occurred while deleting the employee"

   
def get_employee_details_by_id(employee_id, userPhone):
    if not employee_id:
        return "Employee ID is required"

    try:
        connect()
        client = connect()
        transformedPhone = convert_phone_number(userPhone)
        db = client.get_database(transformedPhone)
        user_collection = db.employees  # Adjust collection name as per your database
        
        employee_details = user_collection.find_one({"_id": ObjectId(employee_id)})
        client.close()

        if employee_details:
            print("Employee Details are: ", employee_details)
            return employee_details
        else:
            print("Employee not found")
            return "Employee not found"

    except Exception as e:
        print("Error fetching employee details:", str(e))
        return "Internal Server Error", 500
    

def  add_employee(name, email, phone, address, position, hireDate, salary, workingHours, status, userPhone):
    try:
        transformedPhone = convert_phone_number(userPhone)
        client = connect()

        db = client.get_database(transformedPhone)
        user_collection = db.employees

        employee_data = {
            "name": name,
            "email": email,
            "phone": phone,
            "address": address,
            "position": position,
            "hireDate": hireDate,
            "salary": salary,
            "workingHours": workingHours,
            "status": status
        }

        # Insert the employee data into the collection
        result = user_collection.insert_one(employee_data)

        client.close()

        if result.inserted_id:
            return "Employee added successfully"
        else:
            return "Failed to add employee"

    except Exception as e:
        print("Error adding employee:", str(e))
        return "Internal Server Error", 500
    
def edit_employee(id, item_name,new_value, userPhone):
    try:
        connect()
        client = connect()
        transformedPhone = convert_phone_number(userPhone)
        db = client.get_database(transformedPhone)
        user_collection = db.employees
        
        employee_id = ObjectId(id)
        result = user_collection.update_one({"_id": employee_id}, {"$set": {item_name: new_value}})

        client.close()

        if result.modified_count > 0:
            return "Employee edited successfully"
        else:
            return "Employee not found or no changes made"

    except Exception as e:
        print("Error editing employee:", str(e))
        return "Error occurred while editing the employee"

def get_employee_details_by_name(employee_name, userPhone):
    if not employee_name:
        return "Employee name is required"

    try:
        connect()
        client = connect()
        transformedPhone = convert_phone_number(userPhone)
        db = client.get_database(transformedPhone)
        user_collection = db.employees  # Adjust collection name based on your database schema
        
        employee_details = user_collection.find_one({"name": employee_name})
        employee_details["_id"]=str(employee_details["_id"])
        client.close()

        if employee_details:
            print("Employee Details are: ", employee_details)
            return employee_details
        else:
            print("Employee not found")
            return "Employee not found"  # Or any specific message for employee not found

    except Exception as e:
        print("Error fetching employee details:", str(e))
        return "Internal Server Error", 500
