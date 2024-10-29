
// Wait for the HTML document (DOM) to be fully loaded before executing the code in this block
document.addEventListener('DOMContentLoaded', () => {

    

    // Handle form submission for adding an employee
    document.getElementById('employeeForm').addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent the default form submission behavior
        addEmployee(); // Call the function to add a new employee to the backend
    });



    // Load all employees when the "Load Employees" button is clicked
    document.getElementById('loadEmployees').addEventListener('click', loadEmployees);



    // Handle form submission for getting a specific employee
    document.getElementById('getEmployeeForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent default form submission behavior
    getEmployee();  // Call function to get an employee by ID
    });




    

});



// Function to add a new employee
function addEmployee() {

    // Extract values entered by the user in the form fields (name, baseSalary, address, role)
    const name = document.getElementById('name').value;
    const baseSalary = document.getElementById('baseSalary').value;
    const address = document.getElementById('address').value;
    const role = document.getElementById('role').value;
    
    // Create an object containing the employee data to be sent to the backend
    const employeeData = {
        name: name,
        baseSalary: parseFloat(baseSalary), // Convert base salary from string to a number
        address: address,
        role: role
    };

    // Use the fetch API to send a POST request to the backend API to add the new employee
    fetch('http://127.0.0.1:5000/api/employees', {
        method: 'POST', // HTTP method to indicate adding a new resource (employee)
        headers: {
            'Content-Type': 'application/json' // Specify the content type as JSON
        },
         // Convert the employeeData object to a JSON string to send in the request body
        body: JSON.stringify(employeeData)  
    })
    .then(response => response.json()) // Convert the server response to JSON format
    .then(data => {
        // Display success or error message 
        // i.e. We are getting the message div element to display feedback to the user
        const messageDiv = document.getElementById('message');

        // If the response contains an error, display an error message
        if (data.error) {
            messageDiv.textContent = `Error: ${data.error}`; // Show error message from the response
            messageDiv.style.color = 'red'; // Set the message color to red to indicate an error
        } else {
            // If no error, display a success message
            messageDiv.textContent = 'Employee added successfully!';
            messageDiv.style.color = 'green'; // Set the message color to green to indicate success
        }
    }) 
    // If there is an error during the fetch operation, catch it and handle it here
    .catch(error => {
        
        // Log the error to the console for debugging
        console.error('Error adding employee:', error); 

        // Display a generic error message to the user
        const messageDiv = document.getElementById('message'); 
        messageDiv.textContent = 'An error occurred while adding the employee.';
        
        // Set the message color to red to indicate an error
        messageDiv.style.color = 'red';
    });
}



// Function to load all employees
function loadEmployees() {
    // Send a GET request to the server to fetch all employee records
    fetch('http://127.0.0.1:5000/api/employees')
     // Parse the response from JSON
    .then(response => response.json()) 
    .then(data => {
        // Get the HTML element with the ID 'employeesList' to display employees data
        const employeesListDiv = document.getElementById('employeesList');
        // Clear any existing content in the employees list
        employeesListDiv.innerHTML = '';  
        data.forEach(employee => {
            // Create a new div for each employee and display their details
            const employeeDiv = document.createElement('div');
            employeeDiv.textContent = `ID: ${employee.employeeID}, Name: ${employee.name}, Role: ${employee.role}, Salary: ${employee.baseSalary}`;
            employeesListDiv.appendChild(employeeDiv);  // Append the employee information to the list
            });
        });
}
