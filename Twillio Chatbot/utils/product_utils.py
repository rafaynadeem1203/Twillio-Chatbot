from flask import jsonify
from bson import ObjectId

import requests
from utils.dbConfig import connect
def convert_phone_number(phone_number):
    return "0" + phone_number[12:]
    


def get_products(userPhone):
    try:
        connect()
        client = connect()
        transformedPhone = convert_phone_number(userPhone)
        print("transformed phone:",transformedPhone)
        db = client.get_database(transformedPhone)
        user_collection = db.products
        allProducts = list(user_collection.find({}))
        for product in allProducts:
            product['_id'] = str(product['_id'])
        print("allProducts are: ", allProducts)    
        #return jsonify({allProducts})
        client.close()
        return allProducts

    except Exception as e:
        print("Error fetching Products:", str(e))
        return "Internal Server Error", 500
        
    
def get_product_details_by_name(product_name,userPhone):
    try:
        connect()
        client = connect()
        transformedPhone = convert_phone_number(userPhone)
        print("transformed phone:",transformedPhone)
        db = client.get_database(transformedPhone)
        user_collection = db.products
        productDetails = user_collection.find_one({"name": product_name})
        productDetails["_id"]=str(productDetails["_id"])
        client.close()
        
        if productDetails:
            print("product details are: ", productDetails)
            return productDetails
        else:
            print("Product not found")
            return "Product not found"#, 404

    except Exception as e:
        print("Error fetching product details:", str(e))
        return "Internal Server Error", 500

def get_product_id_by_name(product_name, userPhone): 
    try:
        connect()
        client = connect()
        transformedPhone = convert_phone_number(userPhone)
        db = client.get_database(transformedPhone)
        user_collection = db.products  # Assuming a 'products' collection
        
        product_details = user_collection.find_one({"name": product_name})
        client.close()

        if product_details:
            print("Product Details are: ", product_details)
            return product_details['_id']
        else:
            print("Product not Found")
            return "Product not found"
    except Exception as e:
        print("Error fetching Product details:", str(e))
        return "Internal Server Error", 500


def add_product(name, price, category, quantity, sku, brand, unitOfMeasure, supplier, description, userPhone):
    try:
        transformedPhone = convert_phone_number(userPhone)
        client = connect()

        db = client.get_database(transformedPhone)
        user_collection = db.products

        product_data = {
            "name": name,
            "price": price,
            "category": category,
            "quantity": quantity,
            "sku": sku,
            "brand": brand,
            "unitOfMeasure": unitOfMeasure,
            "supplier": supplier,
            "description": description
        }

        # Insert the product data into the collection
        result = user_collection.insert_one(product_data)

        client.close()

        if result.inserted_id:
            return "Product added successfully"
        else:
            return "Failed to add product"

    except Exception as e:
        print("Error adding product:", str(e))
        return "Internal Server Error", 500
    
def delete_product(product_id, userPhone):
    try:
        connect()
        client = connect()
        transformedPhone = convert_phone_number(userPhone)
        db = client.get_database(transformedPhone)
        user_collection = db.products
        result = user_collection.delete_one({"_id": ObjectId(product_id)})
        client.close()

        if result.deleted_count > 0:
            return "Product deleted successfully"
        else:
            return "Product not found"

    except Exception as e:
        print("Error deleting product:", str(e))
        return "Error occurred while deleting the product"


def edit_product(id, item_name, new_value, userPhone):
    try:
        connect()
        client = connect()
        transformedPhone = convert_phone_number(userPhone)
        db = client.get_database(transformedPhone)
        user_collection = db.products
        
        product_id = ObjectId(id)
        result = user_collection.update_one({"_id": product_id}, {"$set": {item_name: new_value}})
        print("result in edit product api is: ", result)
        client.close()

        if result.modified_count > 0:
            return "Product edited successfully"
        else:
            return "Product not found or no changes made"

    except Exception as e:
        print("Error editing product:", str(e))
        return "Error occurred while editing the product"
