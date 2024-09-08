from flask import Flask, request,session
from twilio.twiml.messaging_response import MessagingResponse
import os

from utils.product_utils import get_products, get_product_details_by_name, add_product, delete_product, edit_product, get_product_id_by_name
from utils.supplier_utils import get_suppliers, get_supplier_id_by_name, delete_supplier, add_supplier, edit_supplier, get_supplier_details_by_id, get_supplier_name_by_id
from utils.employee_utils import get_employees, delete_employee , get_employee_details_by_id, add_employee, edit_employee, get_employee_details_by_name, get_employee_id_by_name




app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'defaultsecretkey')


    
@app.route("/")
def hello():
    return "Welcome to the Inventory Management Website"

@app.route("/sms", methods=['POST'])
def sms_reply():
    
    reply = "Welcome"  # Initializing with a default value
    msg = request.form.get('Body')
    if msg.lower()=="reset":
        session.clear()
    user_phone = request.form.get('From')
    
    user_session = session.get(user_phone, {'first_time': True})
    resp = MessagingResponse()

    if user_session['first_time']:
        reply = "Welcome to the Inventory Management Website\n1. Information regarding Products\n2. Information regarding Suppliers\n3. Information regarding Employees\n4. Type reset to reset\n5. General information about the whole system"
        print("reply in first_ti1me",reply)
        user_session['first_time'] = False
        session[user_phone] = user_session
        resp.message(reply)
        return str(resp)
        
    else:
        first_menu = user_session.get('first_menu')
        second_menu = user_session.get('second_menu')
        
        if not first_menu:
            if msg == '1':
                
                user_session['first_menu'] = 'productmenu'
                first_menu = 'productmenu'
                reply = "1. Add a product\n2. Remove a product\n3. Edit a product\n4. Show all the products\n5. Get product by name\n6. Return to the main menu"

            elif msg == '2':
                user_session['first_menu'] = 'suppliermenu'
                first_menu = 'suppliermenu'
                reply = "1. Add a supplier\n2. Remove a supplier\n3. Edit a supplier\n4. Show all the suppliers\n5. Get supplier by name\n6. Return to the main menu"

            elif msg == '3':
                user_session['first_menu'] = 'employeemenu'
                first_menu = 'employeemenu'
                reply = "1. Add an employee\n2. Remove an employee\n3. Edit an employee\n4. Show all the employees\n5. Get employee by name\n6. Return to the main menu"

            elif msg == '5':
                user_session['first_menu'] = 'general'
                first_menu = 'general'
                reply = "What's your question? Free feel to ask any question related to Inventory Management System"

     
            else:
                reply = "Invalid option selected"
            session[user_phone] = user_session
            resp.message(reply)
            return str(resp)
           

        if first_menu == 'productmenu':
            if not second_menu:
                # Handle product menu options
                if msg == '1': 
                    user_session['second_menu'] = 'addproduct'
                    second_menu = 'addproduct'
                    reply = "Please provide details of the product in the format:\nname,description,price,quantity,unitOfMeasure,category,brand,sku,supplierName(which exists)"
                elif msg == '2':
                    user_session['second_menu'] = 'removeproduct'
                    second_menu = 'removeproduct'
                    reply = "Please provide the name of the product you want to delete"
                    # Handle removing a product
                elif msg == '3':
                    user_session['second_menu'] = 'editproduct'
                    second_menu = 'editproduct'
                    reply = "Please provide the name of the product followed by item name:value you want to change in the below format\nProduct Name,item name,new value"
                    # Handle editing a product
                elif msg == '5':
                    user_session['second_menu'] = 'viewproduct'
                    second_menu = 'viewproduct'
                    reply = "Please provide the name of the product you want to see details of"
                    # Handle editing a product    
                elif msg == '4':
                    try:
                        reply = "List of Products:\n"

                        # Get product data
                        products = get_products(user_phone)

                        if products:
                            # Ensure products is a list of dictionaries
                            if not isinstance(products, list):
                                raise TypeError("Products data should be a list.")

                            # Format product data as a string
                            product_list = "\n\n".join(
                                [f"Name: {product.get('name', 'N/A')}\n"
                                f"Description: {product.get('description', 'N/A')}\n"
                                f"Quantity: {product.get('quantity', 'N/A')}\n"
                                f"Price: {product.get('price', 'N/A')}"
                                for product in products]
                            )
                            resp.message(f"Products:\n{product_list}")
                        else:
                            resp.message("Failed to fetch product data")

                        return str(resp)

                    except TypeError as te:
                        # Handle TypeError for incorrect data type issues
                        error_message = f"TypeError: {te}"
                        print(error_message)
                        resp.message(error_message)
                        return str(resp)

                    except Exception as e:
                        # Handle any unexpected errors
                        error_message = f"An error occurred: {e}"
                        print(error_message)
                        resp.message(error_message)
                        return str(resp)



                elif msg == '6':
                    session.clear()
                    user_session['second_menu'] = None  # Reset the second menu
                    user_session['first_menu'] = None  # Reset the first menu
    
                    reply = "Returning to the main menu\n1. Information regarding Products\n2. Information regarding Suppliers\n3. Information regarding Employees\n4. General information about the whole system"
                    #delete all the first_menu, secon_menu and first_Time if necessary
                else:
                    reply = "Invalid option. Please choose a valid option."           

            else:
                if second_menu == 'removeproduct':
                    try:
                        # Assume the message contains the name of the product to remove
                        product_name = msg

                        # Retrieve the product ID based on the product name
                        product_id = get_product_id_by_name(product_name, user_phone)

                        if not product_id:
                            # Handle cases where the product is not found
                            raise Exception(f"{product_name} does not exits.")
                        else:
                            # Call the API or method to remove the product using the product_id
                            result = delete_product(str(product_id), user_phone)

                            if result == "Product deleted successfully":
                                reply = f"Product {product_name} removed successfully"
                            else:
                                reply = f"Failed to remove product: {result}"

                        # Reset the second menu and update the session
                        user_session['second_menu'] = None
                        session[user_phone] = user_session

                        # Send the response message
                        resp.message(reply)
                        return str(resp)
                
                    except Exception as e:
                        # Handle any unexpected errors
                        error_message = f"An error occurred: {e}"
                        print(error_message)
                        resp.message(error_message)
                        return str(resp)

                elif second_menu == 'viewproduct':
                    try:
                        # Assume the message contains the name of the product to view
                        product_name = msg

                        # Retrieve product details based on the product name
                        product_details = get_product_details_by_name(product_name, user_phone)

                        if not product_details:
                            # Handle cases where the product is not found
                           raise Exception(f"{product_name} is not a valid product.")
                        else:
                            # Retrieve the supplier name using the supplier ID from product details
                            supplier_name = get_supplier_name_by_id(product_details.get('supplier', ''), user_phone)
                            if not supplier_name:
                                supplier_name = "Supplier information not available"

                            # Format the product details into a reply message
                            reply = (f"Product Details:\n"
                                    f"Name: {product_details.get('name', 'N/A')}\n"
                                    f"Brand: {product_details.get('brand', 'N/A')}\n"
                                    f"Description: {product_details.get('description', 'N/A')}\n"
                                    f"Quantity: {product_details.get('quantity', 'N/A')}\n"
                                    f"Supplier Name: {supplier_name}\n"
                                    f"Price: {product_details.get('price', 'N/A')}")

                        # Reset the second menu and update the session
                        user_session['second_menu'] = None
                        session[user_phone] = user_session

                        # Send the response message
                        resp.message(reply)
                        return str(resp)
                    
                   
                    except Exception as e:
                        # Handle any unexpected errors
                        error_message = f"An error occurred: {e}"
                        print(error_message)
                        resp.message(error_message)
                        return str(resp)

                elif second_menu == 'addproduct':
                    try:
                        # Check if the message contains the correct number of product details
                        product_details = msg.split(",")
                        if len(product_details) != 9:
                            raise ValueError("Incorrect number of product details provided. Expected 9 values.")

                        # Unpack product details
                        name, description, price, quantity, unitOfMeasure, category, brand, sku, supplierName = product_details

                        # Retrieve supplier ID
                        supplier = get_supplier_id_by_name(str(supplierName), user_phone)

                        if supplier:
                            # Call the API or method to add the product
                            reply = add_product(name, price, category, quantity, sku, brand, unitOfMeasure, supplierName, description, user_phone)
                        else:
                            raise ValueError(f"{supplierName} is not a supplier. Please enter correcct supplier")

                        # Reset the second menu and update the session
                        user_session['second_menu'] = None
                        session[user_phone] = user_session

                        # Send the response message
                        resp.message(reply)
                        return str(resp)

                    except ValueError as ve:
                        # Handle ValueError for incorrect number of details or other value-related issues
                        error_message = f"ValueError: {ve}"
                        print(error_message)
                        resp.message(error_message)
                        return str(resp)

                    except Exception as e:
                        # Handle any unexpected errors
                        error_message = f"An error occurred: {e}"
                        print(error_message)
                        resp.message(error_message)
                        return str(resp)

                elif second_menu=="editproduct":
                    try:
                        # Split the input message to get product details
                        product_Name, item_name, new_value = msg.split(",")

                        # Validate item_name
                        valid_item_names = ["name", "description", "price", "quantity", "unitOfMeasure", "category", "brand", "sku", "supplierName"]
                        if item_name not in valid_item_names:
                            raise ValueError(f"Invalid item_name: {item_name}. Must be one of {', '.join(valid_item_names)}.")
                        if item_name=="supplierName":
                            supplier_exists=get_supplier_id_by_name(item_name,user_phone)
                            if not supplier_exists:
                                raise ValueError(f"Invalid supplier name. Please enter a name which exists in database")
                        # Retrieve the product ID based on the product name
                        product_Id = get_product_id_by_name(product_Name, user_phone)

                        if not product_Id:
                            # Handle cases where the product is not found
                            raise ValueError(f"Invalid Product Name. Please enter correct name.")
                        else:
                            # Call the API or method to edit the product details
                            edit_response = edit_product(product_Id, item_name, new_value, user_phone)
                            reply = edit_response

                        # Reset the second menu and update the session
                        user_session['second_menu'] = None
                        session[user_phone] = user_session

                        # Send the response message
                        resp.message(reply)
                        return str(resp)

                    except ValueError as ve:
                        # Handle ValueError for invalid item_name or other value-related issues
                        error_message = f"ValueError: {ve}"
                        print(error_message)
                        resp.message(error_message)
                        return str(resp)

                    except Exception as e:
                        # Handle any unexpected errors
                        error_message = f"An error occurred: {e}"
                        print(error_message)
                        resp.message(error_message)
                        return str(resp)

          

        elif first_menu == 'suppliermenu':
            if not second_menu:
                # Handle supplier menu options
                if msg == '1':
                    user_session['second_menu'] = 'addsupplier'
                    second_menu = 'addsupplier'
                    reply = "Please provide details of the supplier in the format:\nname,contactPerson,email,phone,address"
                elif msg == '2':
                    user_session['second_menu'] = 'removesupplier'
                    second_menu = 'removesupplier'
                    reply = "Please provide the name of the supplier you want to delete"
                    # Handle removing a supplier
                elif msg == '3':
                    user_session['second_menu'] = 'editsupplier'
                    second_menu = 'editsupplier'
                    reply = "Please provide the name of the supplier followed by item name:value you want to change in the below format\nSupplier Name,item name,new value"
                    # Handle editing a supplier
                elif msg == '4':
                    try:
                        reply = "List of Suppliers:\n"
                        
                        # Get supplier data
                        suppliers = get_suppliers(user_phone)

                        if suppliers:
                            # Ensure suppliers is a list of dictionaries
                            if not isinstance(suppliers, list):
                                raise TypeError("Suppliers data should be a list.")

                            # Format supplier data as a string
                            supplier_list = "\n\n".join(
                                [f"Name: {supplier.get('name', 'N/A')}\n"
                                f"Contact Person: {supplier.get('contactPerson', 'N/A')}\n"
                                f"Phone: {supplier.get('phone', 'N/A')}\n"
                                f"Address: {supplier.get('address', 'N/A')}"
                                for supplier in suppliers]
                            )
                            resp.message(f"Suppliers are:\n{supplier_list}")
                        else:
                            resp.message("Failed to fetch suppliers list")

                        return str(resp)

                    except TypeError as te:
                        # Handle TypeError for incorrect data type issues
                        error_message = f"TypeError: {te}"
                        print(error_message)
                        resp.message(error_message)
                        return str(resp)

                    except Exception as e:
                        # Handle any other unexpected errors
                        error_message = f"An error occurred: {e}"
                        print(error_message)
                        resp.message(error_message)
                        return str(resp)

                                        
                elif msg == '5':
                    user_session['second_menu'] = 'viewsupplier'
                    second_menu = 'viewsupplier'
                    reply = "Please provide the name of the supplier you want to see details of"
                     
                elif msg == '6':
                    session.clear()
                    user_session['second_menu'] = None  # Reset the second menu
                    user_session['first_menu'] = None  # Reset the first menu
                    reply = "Returning to the main menu\n1. Information regarding Products\n2. Information regarding Suppliers\n3. Information regarding Employees\n4. General information about the whole system"
                    #logic for going back
                else:
                    reply = "Invalid option. Please choose a valid option."
                session[user_phone] = user_session
                resp.message(reply)
                return str(resp)
            else:
                if second_menu == 'removesupplier':
                    try:
                        # Assume the message contains the name of the supplier to remove
                        supplier_name = msg

                        # Retrieve the supplier ID based on the supplier name
                        supplier_id = get_supplier_id_by_name(supplier_name, user_phone)

                        if not supplier_id:
                            # Handle cases where the supplier is not found
                            reply = "Supplier does not exist"
                        else:
                            # Call the API or method to remove the supplier using the supplier_id
                            result = delete_supplier(str(supplier_id), user_phone)

                            if result == "Supplier deleted successfully":
                                reply = f"Supplier {supplier_name} removed successfully"
                            else:
                                reply = f"Failed to remove supplier: {result}"

                        # Reset the second menu and update the session
                        user_session['second_menu'] = None
                        session[user_phone] = user_session

                        # Send the response message
                        resp.message(reply)
                        return str(resp)

                    except Exception as e:
                        # Handle any unexpected errors
                        error_message = f"An error occurred: {e}"
                        print(error_message)
                        resp.message(error_message)
                        return str(resp)
 
                elif second_menu == 'viewsupplier':
                    try:
                        # Assume the message contains the name of the supplier to retrieve
                        supplier_name = msg

                        # Retrieve the supplier ID based on the supplier name
                        supplier_id = get_supplier_id_by_name(supplier_name, user_phone)
                        if not supplier_id:
                            raise ValueError("Supplier not found.")

                        # Retrieve supplier details based on the supplier ID
                        result = get_supplier_details_by_id(supplier_id, user_phone)

                        
                        # Format the supplier details into a reply message
                        supplier_details = result
                        reply = (f"Supplier Details:\n"
                                f"Name: {supplier_details.get('name', 'N/A')}\n"
                                f"Contact Person: {supplier_details.get('contactPerson', 'N/A')}\n"
                                f"Address: {supplier_details.get('address', 'N/A')}\n"
                                f"Email: {supplier_details.get('email', 'N/A')}\n"
                                f"Phone: {supplier_details.get('phone', 'N/A')}")

                        # Reset the second menu and update the session
                        user_session['second_menu'] = None
                        session[user_phone] = user_session

                        # Send the response message
                        resp.message(reply)
                        return str(resp)

                    except ValueError as ve:
                        # Handle ValueError for invalid supplier ID or other value-related issues
                        error_message = f"ValueError: {ve}"
                        print(error_message)
                        resp.message(error_message)
                        return str(resp)

                    except Exception as e:
                        # Handle any unexpected errors
                        error_message = f"An error occurred: {e}"
                        print(error_message)
                        resp.message(error_message)
                        return str(resp)

                elif second_menu=="addsupplier":
                    try:
                        # Split the input message to get supplier details
                        supplier_details = msg.split(",")

                        if len(supplier_details) != 5:
                            raise ValueError("Incorrect number of supplier details provided. Expected 5 values.")

                        name, contactPerson, email, phone, address = supplier_details

                        # Call the API or method to add the supplier
                        reply = add_supplier(name, contactPerson, email, phone, address, user_phone)
                        print(reply)

                        # Reset the second menu and update the session
                        user_session['second_menu'] = None
                        session[user_phone] = user_session

                        # Send the response message
                        resp.message(reply)
                        return str(resp)

                    except ValueError as ve:
                        # Handle ValueError for incorrect input format or other value-related issues
                        error_message = f"ValueError: {ve}"
                        print(error_message)
                        resp.message(error_message)
                        return str(resp)

                    except Exception as e:
                        # Handle any unexpected errors
                        error_message = f"An error occurred: {e}"
                        print(error_message)
                        resp.message(error_message)
                        return str(resp)

                elif second_menu=="editsupplier":
                    try:
                        # Split the input message to get supplier details
                        supplier_Name, item_name, new_value = msg.split(",")

                        # Validate the item_name
                        valid_item_names = ["name", "contactPerson", "email", "phone", "address"]
                        if item_name not in valid_item_names:
                            raise ValueError(f"Invalid item_name: {item_name}. Must be one of {', '.join(valid_item_names)}.")

                        # Retrieve the supplier ID based on the supplier name
                        supplier_Id = get_supplier_id_by_name(supplier_Name, user_phone)

                        if not supplier_Id:
                            # Handle cases where the supplier is not found
                            reply = "Supplier does not exist"
                        else:
                            # Call the API or method to edit the supplier details
                            reply = edit_supplier(supplier_Id, item_name, new_value, user_phone)

                        # Reset the second menu and update the session
                        user_session['second_menu'] = None
                        session[user_phone] = user_session

                        # Send the response message
                        resp.message(reply)
                        return str(resp)

                    except ValueError as ve:
                        # Handle ValueError for invalid item_name or other value-related issues
                        error_message = f"ValueError: {ve}"
                        print(error_message)
                        resp.message(error_message)
                        return str(resp)

                    except Exception as e:
                        # Handle any unexpected errors
                        error_message = f"An error occurred: {e}"
                        print(error_message)
                        resp.message(error_message)
                        return str(resp)

                    
        elif first_menu == 'employeemenu':
            if not second_menu:
                
                if msg == '1':
                    user_session['second_menu'] = 'addemployee'
                    second_menu = 'addemployee'
                    reply = "Please provide details of the employee in the format:\nname,email,phone,address,position,hireDate(YYYY-MM-DDTHH:mm:ss.sssZ),salary,workingHours,status(Active, On Leave, Terminated)"

                elif msg == '2':
                    user_session['second_menu'] = 'removeemployee'
                    second_menu = 'removeemployee'
                    reply = "Please provide the name of the employee you want to delete"
            
                elif msg == '3':
                    user_session['second_menu'] = 'editemployee'
                    second_menu = 'editemployee'
                    reply = "Please provide the name of the employee followed by item name:value you want to change in the below format\nEmployee Name,item name,new value"
                    # Handle editing an employee
                elif msg == '4':
                    reply = "List of Employees:\n"
                    # Get employees data
                    employees = get_employees(user_phone)
                    if employees:
                       employee_list = "\n\n".join( [f"Name: {employee.get('name', 'N/A')}\nEmail: {employee.get('email', 'N/A')}\nPhone: {employee.get('phone', 'N/A')}" for employee in employees])
                       resp.message(f"Employees are:\n{employee_list}")
                    else:
                        resp.message("Failed to fetch employees list")
                    
                    return str(resp)
                elif msg == '5':
                    user_session['second_menu'] = 'viewemployee'
                    second_menu = 'viewemployee'
                    reply = "Please provide the name of the employee you want to see details of"
                   
                elif msg == '6':
                    session.clear()
                    user_session['second_menu'] = None  # Reset the second menu
                    user_session['first_menu'] = None  # Reset the first menu
                    reply = "Returning to the main menu\n1. Information regarding Products\n2. Information regarding Suppliers\n3. Information regarding Employees\n4. General information about the whole system"

                else:
                    reply = "Invalid option. Please choose a valid option."
                session[user_phone] = user_session
                resp.message(reply)
                return str(resp)    
            else:
                if second_menu == 'removeemployee':
                    try:
                        # Assume the message contains the name of the employee to remove
                        employee_name = msg

                        # Retrieve the employee ID based on the name
                        employee_id = get_employee_id_by_name(employee_name, user_phone)

                        if not employee_id:
                            # Handle cases where the employee is not found
                            reply = "Employee does not exist"
                        else:
                            # Attempt to delete the employee using the retrieved employee_id
                            result = delete_employee(employee_id, user_phone)

                            if result:
                                reply = f"Employee {employee_name} removed successfully"
                            else:
                                reply = f"Operation failed: {result}"

                        # Reset the second menu and update the session
                        user_session['second_menu'] = None
                        session[user_phone] = user_session

                        # Send the response message
                        resp.message(reply)
                        return str(resp)

                    except Exception as e:
                        # Handle any unexpected errors
                        error_message = f"An error occurred: {e}"
                        print(error_message)
                        resp.message(error_message)
                        return str(resp)

                elif second_menu == 'viewemployee':
                        try:
                            # Assume the message contains the name of the employee to retrieve
                            employee_name = msg

                            # Retrieve the employee details based on the name
                            employee_details = get_employee_details_by_name(employee_name, user_phone)

                            if not employee_details:
                                # Handle cases where employee is not found
                                reply = "Employee does not exist"
                            else:
                                # Format the employee details for the response
                                reply = (f"Employee Details:\n"
                                        f"Name: {employee_details.get('name', 'N/A')}\n"
                                        f"Address: {employee_details.get('address', 'N/A')}\n"
                                        f"Email: {employee_details.get('email', 'N/A')}\n"
                                        f"Position: {employee_details.get('position', 'N/A')}\n"
                                        f"Salary: {employee_details.get('salary', 'N/A')}\n"
                                        f"Working Hours: {employee_details.get('workingHours', 'N/A')}\n"
                                        f"Status: {employee_details.get('status', 'N/A')}\n"
                                        f"Hire Date: {employee_details.get('hireDate', 'N/A')}")

                            # Reset the second menu and update the session
                            user_session['second_menu'] = None
                            session[user_phone] = user_session

                            # Send the response message
                            resp.message(reply)
                            return str(resp)

                        except Exception as e:
                            # Handle any unexpected errors
                            error_message = f"An error occurred: {e}"
                            print(error_message)
                            resp.message(error_message)
                            return str(resp)

                elif second_menu=="addemployee":
                    try:
                        # Split employee details from the input message
                        employee_details = msg.split(",")
                        if len(employee_details) != 9:
                            raise ValueError("Incorrect number of employee details provided.")

                        name, email, phone, address, position, hireDate, salary, workingHours, status = employee_details
                        valid_statuses = ["Active", "Terminated", "On leave"]
                        
                        if status not in valid_statuses:
                            raise ValueError(f"Invalid status value: {status}. Must be one of {', '.join(valid_statuses)}.")

                        # Add employee information
                        reply = add_employee(name, email, phone, address, position, hireDate, salary, workingHours, status, user_phone)

                        # Reset the second menu and update session
                        user_session['second_menu'] = None
                        session[user_phone] = user_session

                        # Send response message
                        resp.message(reply)
                        return str(resp)

                    except ValueError as ve:
                        # Handle ValueError and send the message to the client
                        error_message = f"Error: {ve}"
                        print(error_message)
                        resp.message(error_message)
                        return str(resp)

                    except Exception as e:
                        # Handle any other exceptions and send the message to the client
                        error_message = f"An error occurred: {e}"
                        print(error_message)
                        resp.message(error_message)
                        return str(resp)

                elif second_menu=="editemployee":
                    try:
                        # Split the input message to get employee details
                        employee_Name, item_name, new_value = msg.split(",")

                        # Validate the item_name
                        valid_item_names = ["name", "email", "phone", "address", "position", "hireDate", "salary", "workingHours", "status"]
                        if item_name not in valid_item_names:
                            raise ValueError(f"Invalid item_name: {item_name}. Must be one of {', '.join(valid_item_names)}.")

                        # Retrieve the employee ID based on the name
                        employee_Id = get_employee_id_by_name(employee_Name, user_phone)

                        if not employee_Id:
                            # Handle cases where employee is not found
                            reply = "Employee does not exist"
                        else:
                            # Call the API or method to edit the employee details
                            reply = edit_employee(employee_Id, item_name, new_value, user_phone)

                        # Reset the second menu and update the session
                        user_session['second_menu'] = None
                        session[user_phone] = user_session

                        # Send the response message
                        resp.message(reply)
                        return str(resp)

                    except ValueError as ve:
                        # Handle ValueError, including invalid item_name or any other value-related issues
                        error_message = f"ValueError: {ve}"
                        print(error_message)
                        resp.message(error_message)
                        return str(resp)

                    except Exception as e:
                        # Handle any other unexpected errors
                        error_message = f"An error occurred: {e}"
                        print(error_message)
                        resp.message(error_message)
                        return str(resp)

    #if the above conditions are not working
    print("Before sending the response: ",reply)
    session[user_phone] = user_session
    resp.message(reply)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
