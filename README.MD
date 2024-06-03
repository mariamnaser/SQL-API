# SQL API Project

### Overview
The project sets up a web server using FastAPI and defines endpoints to perform CRUD (Create, Read, Update, Delete) operations on two tables in the database: `student` and `employee`. The database connection details are specified in the `db` module.

### Main Components

1. **FastAPI Application Setup:**
   - The main application is initialized with FastAPI.
   - The database connection is established using the `DB` class, with credentials provided directly in the code (though it's noted this should be handled securely in production).

2. **Health Check Endpoint:**
   - `GET /` returns a simple heartbeat message to indicate the server is running.

3. **Student Endpoints:**
   - `GET /students`: Retrieves all students or students matching specific query parameters. Supports a `fields` parameter to return only specified attributes.
   - `GET /students/{student_id}`: Retrieves a student by their unique ID.
   - `POST /students`: Creates a new student. The request body must include the student's details in JSON format. Ensures email uniqueness and validates the enrollment year.
   - `PUT /students/{student_id}`: Updates the details of an existing student identified by their ID. Validates the email and enrollment year.
   - `DELETE /students/{student_id}`: Deletes a student identified by their ID from the database.

4. **Employee Endpoints:**
   - `GET /employees`: Retrieves all employees or employees matching specific query parameters. Supports a `fields` parameter to return only specified attributes.
   - `GET /employees/{employee_id}`: Retrieves an employee by their unique ID.
   - `POST /employees`: Creates a new employee. The request body must include the employee's details in JSON format. Ensures email uniqueness and validates the employee type.
   - `PUT /employees/{employee_id}`: Updates the details of an existing employee identified by their ID. Validates the email and employee type.
   - `DELETE /employees/{employee_id}`: Deletes an employee identified by their ID from the database.

### Database Operations
The `DB` class (imported from the `db` module) is used to interact with the database. It includes methods like `select`, `insert`, `update`, and `delete` to perform the necessary operations based on the requests received by the API.

### Example Usage
- **Retrieve All Students:**
  ```sh
  GET /students
  ```
  This will return a list of all students.

- **Retrieve Specific Students with Filters:**
  ```sh
  GET /students?first_name=John&last_name=Doe
  ```
  This will return students whose first name is John and last name is Doe.

- **Create a New Student:**
  ```json
  POST /students
  {
      "first_name": "John",
      "last_name": "Doe",
      "email": "john.doe@example.com",
      "enrollment_year": 2020
  }
  ```
  This will create a new student with the specified details.

- **Update a Student:**
  ```json
  PUT /students/1
  {
      "first_name": "Johnny"
  }
  ```
  This will update the first name of the student with ID 1 to Johnny.

- **Delete a Student:**
  ```sh
  DELETE /students/1
  ```
  This will delete the student with ID 1 from the database.

### Error Handling
The API includes basic error handling to return appropriate HTTP status codes:
- `404 Not Found` if the requested student or employee does not exist.
- `400 Bad Request` if the request body is invalid, such as missing required fields or containing invalid data.
- `200 OK` for successful operations.

By providing these endpoints, the application allows users to manage students and employees in the database through simple HTTP requests, making it easy to integrate with other systems or front-end applications.
