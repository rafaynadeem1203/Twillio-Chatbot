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
                    reply = "List of Products:\n"
                    # Get product data
                    products = get_products(user_phone)
                    if products:
                        # Format product data as a string
                        product_list = "\n\n".join([f"Name: {product['name']}\nDescription: {product['description']}\nQuantity: {product['quantity']}\nPrice: {product['price']}" for product in products])
                        resp.message(f"Products:\n{product_list}")
                    else:
                        resp.message("Failed to fetch product data")
                    
                    return str(resp)

                    #call the api to get all the products
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
                    
                    product_name = msg  # Assuming the message contains the name of the product to remove
                    product_id = get_product_id_by_name(product_name,user_phone)
                    if not product_id:
                        # Handle cases where product is not found or error occurred
                        reply = "Product does not exist"
                    else:
                        # Call the API or method to remove the product using product_id
                        result = delete_product(str(product_id),user_phone)
                        if result == "Product deleted successfully":
                            reply = f"Product {product_name} removed successfully"
                        else:
                            reply = f"Failed to remove product: {result}"
                    user_session['second_menu'] = None  # Reset the second menu
                    
                    session[user_phone] = user_session
                    resp.message(reply)
                    
                    return str(resp)
                elif second_menu == 'viewproduct':
                    product_name = msg  # Assuming the message contains the name of the product to remove
                    product_details = get_product_details_by_name(product_name,user_phone)
                    if not product_details:
                        # Handle cases where product is not found or error occurred
                        reply = "Product does not exist"
                    else:
                        # Format the product details into a reply message
                        reply = f"Product Details:\nName: {product_details['name']}\nBrand: {product_details['brand']}\nDescription: {product_details['description']}\nQuantity: {product_details['quantity']}\nSupplier Name: {get_supplier_name_by_id(product_details['supplier'],user_phone)}\nPrice: {product_details['price']}"
           
                    user_session['second_menu'] = None  # Reset the second menu
                    
                    session[user_phone] = user_session
                    resp.message(reply)
                    return str(resp)
                elif second_menu == 'addproduct':
                    product_details = msg
                    name, description, price, quantity, unitOfMeasure, category, brand, sku, supplierName = product_details.split(",")
                    supplier=get_supplier_id_by_name(str(supplierName),user_phone)
                    if supplier:
                        reply = add_product(name, price, category, quantity, sku, brand, unitOfMeasure, supplierName, description, user_phone)
                    else:
                        reply="Supplier does not exists."
                    user_session['second_menu'] = None  # Reset the second menu
                    session[user_phone] = user_session
                    resp.message(reply)
                    return str(resp)
                elif second_menu=="editproduct":
                    product_Name,item_name,new_value=msg.split(",")
                    product_Id = get_product_id_by_name(product_Name,user_phone)
                    if not product_Id:
                        # Handle cases where product is not found or error occurred
                        reply = "Product does not exist"
                    else:
                        edit_response = edit_product(product_Id,item_name,new_value, user_phone)
                        # Format the product details into a reply message
                        reply = edit_response
           
                    user_session['second_menu'] = None  # Reset the second menu
                    
                    session[user_phone] = user_session
                    resp.message(reply)
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
                    reply = "List of Suppliers:\n"
                    
                    # Get supplier data
                    suppliers = get_suppliers(user_phone)
                    if suppliers:
                        # Format supplier data as a string
                        supplier_list = "\n\n".join([f"Name: {supplier['name']}\nContact Person: {supplier['contactPerson']}\nPhone: {supplier['phone']}\nAddress: {supplier['address']}" for supplier in suppliers])
                        resp.message(f"Suppliers are:\n{supplier_list}")
                    else:
                        resp.message("Failed to fetch suppliers list")
                    
                    return str(resp)
                    #logic for getting the list of suppliers
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
                    supplier_name = msg  # Assuming the message contains the name of the supplier to remove
                    supplier_id = get_supplier_id_by_name(supplier_name, user_phone)
                    if not supplier_id:
                        # Handle cases where supplier is not found or error occurred
                        reply = "Supplier does not exist"
                    else:
                        # Call the API or method to remove the supplier using supplier_id
                        result = delete_supplier(str(supplier_id), user_phone)
                        if result == "Supplier deleted successfully":
                            reply = f"Supplier {supplier_name} removed successfully"
                        else:
                            reply = f"Failed to remove supplier: {result}"
                    user_session['second_menu'] = None  # Reset the second menu
                    session[user_phone] = user_session
                    resp.message(reply)
                    return str(resp)  
                elif second_menu == 'viewsupplier':
                    supplier_name = msg  # Assuming the message contains the name of the supplier to remove
                    result = get_supplier_details_by_id(get_supplier_id_by_name(supplier_name,user_phone), user_phone)
                    if result=="Supplier Not Found":
                        # Handle cases where supplier is not found or error occurred
                        reply = "Supplier does not exist"
                    else:
                            # Parse the details received in the result
                            supplier_details = result
                             # Format the Supplier details into a reply message
                            reply = f"Supplier Details:\nName: {supplier_details['name']}\nContact Person: {supplier_details['contactPerson']}\nAddress: {supplier_details['address']}\nEmail: {supplier_details['email']} \nPhone: {supplier_details['phone']}"
           
                       
                    user_session['second_menu'] = None  # Reset the second menu
                    session[user_phone] = user_session
                    resp.message(reply)
                    return str(resp)
                elif second_menu=="addsupplier":
                    supplier_details = msg
                    name,contactPerson,email,phone,address = supplier_details.split(",")
                    reply = add_supplier(name,contactPerson,email,phone,address, user_phone)
                    print(reply)
                    user_session['second_menu'] = None  # Reset the second menu
                    session[user_phone] = user_session
                    resp.message(reply)
                    return str(resp)
                elif second_menu=="editsupplier":
                    supplier_Name,item_name,new_value=msg.split(",")
                    supplier_Id = get_supplier_id_by_name(supplier_Name, user_phone)
                    if not supplier_Id:
                        # Handle cases where supplier is not found or error occurred
                        reply = "Supplier does not exist"
                    else:
                        # Parse the details received in the result
                        reply =edit_supplier(supplier_Id,item_name,new_value, user_phone)
           
                    user_session['second_menu'] = None  # Reset the second menu
                    session[user_phone] = user_session
                    resp.message(reply)
                    return str(resp)
                    
        elif first_menu == 'employeemenu':
            if not second_menu:
                
                if msg == '1':
                    user_session['second_menu'] = 'addemployee'
                    second_menu = 'addemployee'
                    reply = "Please provide details of the employee in the format:\nname,email,phone,address,position,hireDate(YYYY-MM-DDTHH:mm:ss.sssZ),salary,workingHours,status"

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
                        # Format product data as a string
                        employee_list = "\n\n".join([f"Name: {employee['name']}\nEmail: {employee['email']}\nPhone: {employee['phone']}\nAddress: {employee['address']}\nPosition: {employee['position']}\nSalary: {employee['salary']}\nWorking Hours: {employee['workingHours']}\nStatus: {'status'}\nHiredate:{employee['hireDate']}" for employee in employees])
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
                    employee_name = msg  # Assuming the message contains the name of the employee to remove
                    employee_id = get_employee_id_by_name(employee_name,user_phone)
                    if not employee_id:
                        # Handle cases where employee is not found or error occurred
                        reply = "Employee does not exist"
                    else:
                        # Call the API or method to remove the employee using employee_id
                        result = delete_employee(employee_id,user_phone)
                        if result:
                            reply = f"Employee {employee_name} removed successfully"
                        else:
                            reply = f"Operation failed: {result}"
                    user_session['second_menu'] = None  # Reset the second menu
                    session[user_phone] = user_session
                    resp.message(reply)
                    return str(resp)  
                elif second_menu == 'viewemployee':
                    employee_name = msg  # Assuming the message contains the name of the employee to remove
                    employee_details = get_employee_details_by_name(employee_name,user_phone)
                    if not employee_details:
                        # Handle cases where Employee is not found or error occurred
                        reply = "Employee does not exist"
                    else:
                        reply = f"Employee Details:\nName: {employee_details['name']}\nAddress: {employee_details['address']}\nEmail: {employee_details['email']}"
           
                    user_session['second_menu'] = None  # Reset the second menu
                    
                    session[user_phone] = user_session
                    resp.message(reply)
                    return str(resp)
                elif second_menu=="addemployee":
                    employee_details = msg
                    name,email,phone,address,position,hireDate,salary,workingHours,status = employee_details.split(",")
                    reply = add_employee(name,email,phone,address,position,hireDate,salary,workingHours,status, user_phone)
                    print(reply)
                    user_session['second_menu'] = None  # Reset the second menu
                    
                    session[user_phone] = user_session
                    resp.message(reply)
                    return str(resp)
                elif second_menu=="editemployee":
                    employee_Name,item_name,new_value=msg.split(",")
                    employee_Id = get_employee_id_by_name(employee_Name, user_phone)
                    if not employee_Id:
                        # Handle cases where employee is not found or error occurred
                        reply = "Employee does not exist"
                    else:
                        # Call the API or method to remove the employee using employee_id
                        reply =edit_employee(employee_Id,item_name,new_value, user_phone)
           
                    user_session['second_menu'] = None  # Reset the second menu
                   
                    session[user_phone] = user_session
                    resp.message(reply)
                    return str(resp)
                    
                
        
        

       
    
    
    #if the above conditions are not working
    print("Before sending the response: ",reply)
    session[user_phone] = user_session
    resp.message(reply)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
