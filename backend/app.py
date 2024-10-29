# import `Flask` to create the web app
# import `request` to handle incoming data, and import `jsonify` to send JSON responses
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS


# import sqlite3 to connect and interact with the SQLite database
import sqlite3

# create an instance of the Flask class for the web app (i.e. initialize a new instance of the Flask app)
app = Flask(__name__)

# Enable CORS for all routes
# This will allow the frontend to make requests to the backend without being blocked by the browser's CORS policy
CORS(app)

# function to get a connection to the SQLite database
def get_db_connection():

    # create a connection to the payroll (SQLite) database
    connection = sqlite3.connect('../payroll.db')
    # configure connection to return rows as dictionaries, allowing access by column name
    connection.row_factory = sqlite3.Row 
    
    return connection

# route for the home page (the landing page of the web app)
@app.route('/')

# A 'view' function for the home route that returns a welcome message
def home():
    return "Welcome to the Payroll Management System API."

# route for adding a new employee (POST) 
@app.route('/api/employees', methods = ['POST'] )

# function for adding a new employee (POST) to the database
def add_employees():

    # Get JSON data from the request to add a new employee
    # this will allow us to extract the data sent by a client in JSON format
    data = request.get_json()

    # Extract employee details from the JSON data
    name = data.get('name')
    base_salary = data.get('baseSalary')
    address = data.get('address')
    role = data.get('role')

    # check if all required fields are not empty
    if not name or not base_salary or not role:

        # Ensure required fields are provided
        return jsonify({'error': 'Missing required fields'}), 400
     
    # Insert new employee into the Employees table in the database
    conn = get_db_connection()
        
    conn.execute(
        'INSERT INTO Employees (name, baseSalary, address, role) VALUES (?, ?, ?, ?)',
        (name, base_salary, address, role)
    )

    # Save the changes to the database
    conn.commit() 
    
    # Close the database connection
    conn.close()  

    # return success message
    return jsonify({'message': 'Employee added successfully'}), 201

# route for fetching all employees from the database (GET ALL) 
@app.route('/api/employees', methods = ['GET'])

# function to retrieve all employee records from the Employees table in the database
def get_all_employees():

    # establish a connection to the database
    conn = get_db_connection()
    
    # retrieve all records from the Employees table
    employees = conn.execute('SELECT * FROM Employees').fetchall()
    
    # close the database connection
    conn.close()

    # Convert each row from the Employees table into a dictionary for easier data handling
    employees_list = [dict(employee) for employee in employees]
    
    # return the list of employees as a JSON response with a 200 OK status code
    return jsonify(employees_list), 200

# route for fetching a specific employee from the database (GET ONE)
@app.route('/api/employees/<int:employee_id>', methods=['GET'])

# function to retrieve details of a specific employee from the database using their unique ID
def get_employee(employee_id):
      
    # establish a connection to the database
    conn = get_db_connection()

    # execute an SQL query to find the employee with the given employee_id
    employee = conn.execute(
        'SELECT * FROM Employees WHERE employeeID = ?', (employee_id,)
    ).fetchone()

    # close the database connection
    conn.close()
    
    # check if the employee was found in the database
    if employee is None:
        # if the employee with the specified ID does not exist, return a 404 error response
        return jsonify({'error': 'Employee not found'}), 404
    
    # convert sqlite3.Row object to a native Python dictionary for easier JSON serialization and data manipulation
    employee_data = dict(employee)
    
    # return the employee details as a JSON response with a 200 OK status code
    return jsonify(employee_data), 200

# route for updating a specific employee's data in the database (UPDATE ONE)
@app.route('/api/employees/<int:employee_id>', methods=['PUT'])

# function to update details for a specific employee in the Employees table, identified by employee ID
def update_employee(employee_id):

    # get the JSON data from the request body
    data = request.get_json()

    # extract employee details from the JSON data
    name = data.get('name')
    base_salary = data.get('baseSalary')
    address = data.get('address')
    role = data.get('role')

    # check if all required fields are provided (name, base salary, and role)
    if not name or not base_salary or not role:
        # return error if required fields are missing
        return jsonify({'error': 'Missing required fields'}), 400  

    # establish a connection to the database
    conn = get_db_connection()

    # execute the SQL query to update the employee's details in the Employees table
    conn.execute(
        'UPDATE Employees SET name = ?, baseSalary = ?, address = ?, role = ? WHERE employeeID = ?',
        (name, base_salary, address, role, employee_id)
    )

    # commit the changes to save the updated details in the database
    conn.commit()

    # close the database connection to free up resources
    conn.close()

    # return a success message indicating the employee was updated successfully
    return jsonify({'message': 'Employee updated successfully'}), 200


# route for deleting a specific employee from the database (DELETE request)
@app.route('/api/employees/<int:employee_id>', methods=['DELETE'])

# function to delete a specific employee from the database using their unique ID
def delete_employee(employee_id):

    # establish a connection to the database
    conn = get_db_connection()

    # retrieve the employee record by employeeID
    employee = conn.execute('SELECT * FROM Employees WHERE employeeID = ?', (employee_id,)).fetchone()

    # check if the employee record exists; return an error response if not found
    if employee is None:
        conn.close()
        return jsonify({'error': 'Employee not found'}), 404

    # delete the employee record by employeeID
    conn.execute('DELETE FROM Employees WHERE employeeID = ?', (employee_id,))
    conn.commit()  # Commit the changes to make the deletion permanent

    # close the database connection
    conn.close()

    # return a success message indicating the employee was deleted
    return jsonify({'message': 'Employee deleted successfully'}), 200


# run the app only if this file is executed directly, not when imported
if __name__ == '__main__':
    # start the Flask development server with debug mode enabled
    app.run(debug=True)