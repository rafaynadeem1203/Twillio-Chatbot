from flask import Flask, request,session
from twilio.twiml.messaging_response import MessagingResponse

from utils.product_utils import get_products, get_product_details_by_name, add_product, delete_product, edit_product, get_product_id_by_name
from utils.supplier_utils import get_suppliers, get_supplier_id_by_name, delete_supplier, add_supplier, edit_supplier, get_supplier_details_by_name
from utils.employee_utils import get_employees, delete_employee , get_employee_details_by_id, add_employee, edit_employee, get_employee_details_by_name
from utils.workorders_utils import get_workorders, get_workorder_by_id




app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkeyjuni'

    
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
                user_session['first_menu']='workordermenu'
                first_menu='workordermenu'
                reply="1. Show Workorders based on Wo#\n2. Show All workorders\n3. Return to main menu"

            elif msg == '6':
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
                        product_list = "\n\n".join([f"Name: {product['name']}\nDescription: {product['description']}\nPrice: {product['price']}" for product in products])
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
                    if product_id=="Product not found":
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
                    result = get_product_details_by_name(product_name,user_phone)
                    if result=="Product not found":
                        # Handle cases where product is not found or error occurred
                        reply = "Product does not exist"
                    else:
                        # Call the API or method to remove the product using product_id
                        
                        if result == "Product not found":
                            reply = "Product not found"
                        elif result=="Product details not found":
                            reply = "Product details not found"
                        elif result=="Product ID is required":
                            reply="Product ID is required"
                        else:
                             # Parse the details received in the result
                            product_details = result

                             # Format the product details into a reply message
                            reply = f"Product Details:\nName: {product_details['name']}\nDescription: {product_details['description']}\nPrice: {product_details['price']}"
           
                    user_session['second_menu'] = None  # Reset the second menu
                    
                    session[user_phone] = user_session
                    resp.message(reply)
                    return str(resp)
                elif second_menu == 'addproduct':
                    product_details = msg
                    name, description, price, quantity, unitOfMeasure, category, brand, sku, supplierName = product_details.split(",")
                    supplier=get_product_details_by_name(str(supplierName),user_phone);
                    print(name, description, price, quantity, unitOfMeasure, category, brand, sku, supplierName)
                    reply = add_product(name, price, category, quantity, sku, brand, unitOfMeasure, supplier, description, user_phone)
                    print(reply)
                    user_session['second_menu'] = None  # Reset the second menu
                    
                    session[user_phone] = user_session
                    resp.message(reply)
                    return str(resp)
                elif second_menu=="editproduct":
                    product_Name,item_name,new_value=msg.split(",")
                    product_Id = get_product_id_by_name(product_Name,user_phone)
                    if product_Id=="Product not found":
                        # Handle cases where product is not found or error occurred
                        reply = "Product does not exist"
                    else:
                        # Call the API or method to remove the product using product_id
                        result = get_product_details_by_name(product_Name, user_phone)
                        if result == "Product not found":
                            reply = "Product not found"
                        elif result=="Product details not found":
                            reply = "Product details not found"
                        elif result=="Product ID is required":
                            reply="Product ID is required"
                        else:
                             # Parse the details received in the result
                            product_details = result
                            product_details[item_name]=new_value
                            print("product details from edit product are",product_details)
                            edit_response = edit_product(product_details['_id'],item_name,new_value, user_phone)
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
                        supplier_list = "\n\n".join([f"Name: {supplier['name']}\nPhone: {supplier['phone']}\nAddress: {supplier['address']}" for supplier in suppliers])
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
                    if supplier_id=="Supplier not found":
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
                    result = get_supplier_id_by_name(supplier_name, user_phone)
                    if result=="Supplier not found":
                        # Handle cases where supplier is not found or error occurred
                        reply = "Supplier does not exist"
                    else:
                        # Call the API or method to remove the supplier using supplier_id
                        if result == "Supplier not found":
                            reply = "Supplier not found"
                        elif result=="Supplier details not found":
                            reply = "Supplier details not found"
                        elif result=="Supplier ID is required":
                            reply="Supplier ID is required"
                        else:
                             # Parse the details received in the result
                            supplier_details = result

                             # Format the Supplier details into a reply message
                            reply = f"Supplier Details:\nName: {supplier_details['name']}\nAddress: {supplier_details['address']}\nEmail: {supplier_details['email']}"
           
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
                    supplier_Id = get_supplier_details_by_name(supplier_Name, user_phone)
                    if supplier_Id=="Supplier not found":
                        # Handle cases where supplier is not found or error occurred
                        reply = "Supplier does not exist"
                    else:
                        # Call the API or method to remove the supplier using supplier_id
                        result = get_supplier_details_by_name(supplier_Name, user_phone)
                        if result == "Supplier not found":
                            reply = "Supplier not found"
                        elif result=="Supplier details not found":
                            reply = "Supplier details not found"
                        elif result=="Supplier ID is required":
                            reply="Supplier ID is required"
                        else:
                             # Parse the details received in the result
                            supplier_details = result
                            supplier_details[item_name]=new_value
                            reply =edit_supplier(supplier_details['_id'],item_name,new_value, user_phone)
           
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
                        employee_list = "\n\n".join([f"Name: {employee['name']}\nEmail: {employee['email']}\nPhone: {employee['phone']}" for employee in employees])
                        resp.message(f"employees are:\n{employee_list}")
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
                    employee_id = get_employee_details_by_id(employee_name,user_phone)
                    if employee_id=="Employee not found":
                        # Handle cases where employee is not found or error occurred
                        reply = "Employee does not exist"
                    else:
                        # Call the API or method to remove the employee using employee_id
                        result = delete_employee(str(employee_id))
                        if result == "Employee deleted successfully":
                            reply = f"Employee {employee_name} removed successfully"
                        else:
                            reply = f"Operation failed: {result}"
                    user_session['second_menu'] = None  # Reset the second menu
                    
                    session[user_phone] = user_session
                    resp.message(reply)
                    return str(resp)  
                elif second_menu == 'viewemployee':
                    employee_name = msg  # Assuming the message contains the name of the employee to remove
                    result = get_employee_details_by_name(employee_name,user_phone)
                    if result=="Employee not found":
                        # Handle cases where Employee is not found or error occurred
                        reply = "Employee does not exist"
                    else:
                        # Call the API or method to remove the Employee using Employee_id
                        if result == "Employee not found":
                            reply = "Employee not found"
                        elif result=="Employee details not found":
                            reply = "Employee details not found"
                        elif result=="Employee ID is required":
                            reply="Employee ID is required"
                        else:
                             # Parse the details received in the result
                            employee_details = result

                             # Format the Supplier details into a reply message
                            reply = f"Supplier Details:\nName: {employee_details['name']}\nAddress: {employee_details['address']}\nEmail: {employee_details['email']}"
           
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
                    employee_Id = get_employee_details_by_name(employee_Name, user_phone)
                    if employee_Id=="Employeer not found":
                        # Handle cases where employee is not found or error occurred
                        reply = "Employee does not exist"
                    else:
                        # Call the API or method to remove the employee using employee_id
                        result = get_employee_details_by_id(str(employee_Id), user_phone)
                        if result == "Employee not found":
                            reply = "Employee not found"
                        elif result=="Employee details not found":
                            reply = "Employee details not found"
                        elif result=="Employee ID is required":
                            reply="Employee ID is required"
                        else:
                             # Parse the details received in the result
                            employee_details = result
                            employee_details[item_name]=new_value
                            reply =edit_employee(employee_details['_id'],item_name,new_value, user_phone)
           
                    user_session['second_menu'] = None  # Reset the second menu
                   
                    session[user_phone] = user_session
                    resp.message(reply)
                    return str(resp)
        elif first_menu=='workordermenu':
            if not second_menu:
                if msg== '1':
                    user_session['second_menu']='viewworkorder'
                    second_menu = 'viewworkorder'
                    reply = "Please provide the WO # of the workorder you want to see details of"
                elif msg=='2':
                    reply = "List of Workorders:\n"
                    workorders = get_workorders('workorder')
                    print(workorders)
                    if workorders:
                        workorder_list = "\n\n".join([
                        f"WO #: {workorder['woID']}\n"
                        f"Date: {workorder['date']}\n"
                        f"Start Date: {workorder['startDate'] if workorder['startDate'] else 'Not specified'}\n"
                        f"End Date: {workorder['endDate'] if workorder['endDate'] else 'Not specified'}\n"
                        f"Description: {workorder['description']}\n"
                        f"Site Name: {workorder['siteName']}\n"
                        f"Status: {'Completed' if workorder['status'] else 'Pending'}"
                        for workorder in workorders
                    ])            
                        resp.message(f"Products:\n{workorder_list}")
                    else:
                        resp.message("Failed to fetch product data")
                    session[user_phone] = user_session
                    return str(resp)
                elif msg=='3':
                    session.clear()
                    user_session['second_menu'] = None  # Reset the second menu
                    user_session['first_menu'] = None  # Reset the first menu
                    reply="1. Show Workorders based on Wo#\n2. Show All workorders\n3. Return to main menu"

                else:
                    reply = "Invalid option. Please choose a valid option."
                session[user_phone] = user_session
                resp.message(reply)
                return str(resp)    
            else:
                if second_menu == 'viewworkorder':
                    workorderID = msg  # Assuming the message contains the id of the workorder to view
                    workorder_details = get_workorder_by_id(workorderID,'workorder')
                    if employee_id=="Workorder not found":
                        # Handle cases where workorder is not found or error occurred
                        reply = "Workorder does not exist"
                    else:
                        reply = f"Workorder Details:\nWorkorder ID: {workorder_details['woID']}\nDate: {workorder_details['date']}\nStart Date & Time: {workorder_details['startDate']}\nEnd Date & Time: {workorder_details['endDate']}\nDescription: {workorder_details['description']}\nSite Name: {workorder_details['siteName']}\nStatus: {'Completed' if workorder_details['status'] else 'Pending'}"
                        
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
