from typing import Any, Dict

# Simple starter project to test installation and environment.
# Based on https://fastapi.tiangolo.com/tutorial/first-steps/
from fastapi import FastAPI, Response, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
# Explicitly included uvicorn to enable starting within main program.
import uvicorn

from db import DB

# Type definitions
KV = Dict[str, Any]

app = FastAPI()

db = DB(
	host="localhost",
	port=3306,
	user="username",
	password="password",
	database="s24_hw2",
)
@app.get("/")
async def healthcheck():
	return HTMLResponse(content="<h1>Heartbeat</h1>", status_code=status.HTTP_200_OK)


# function( string, [], {})
#Gets all students that satisfy the specified query parameters
@app.get("/students")
async def get_students(req: Request):
	table = 'student'
	filter = {}
	query_params = dict(req.query_params)
	fields = query_params.pop("fields", None)
	# Split fields into a list if it exists, or default to selecting all fields
	if fields:
		fields = fields.split(",")
	else:
		fields = []
	if query_params:
		filter.update(query_params)
	else:
		filter = {}
	try:
		# Assuming your DB class has a method like select(table, rows, filters) -> List[Dict]
		students = db.select(table, fields, filter)
		return students
	except Exception as e:
		return fields,filter, HTMLResponse(content="<h1>Error</h1>", status_code=status.HTTP_200_OK)

#Gets a student by ID.
@app.get("/students/{student_id}")
async def get_student(student_id: int):
	table = 'student'
	rows = []
	filters = {"student_id": student_id}
	students_id = db.select(table, rows, filters)
	response = len(students_id)
	if response == 0:
		return HTMLResponse(status_code=status.HTTP_404_NOT_FOUND)
	else:
		students_id = list(students_id)
		return students_id[0]

#Creates a student.
@app.post("/students")
async def post_student(req: Request):
	student_info = await req.json()
	enrollment_year = student_info['enrollment_year']
	if ('email' in student_info) and (2016<=enrollment_year<=2023):
		email = student_info['email']
		table = 'student'
		rows = []
		filters = {'email': email}
		students_id = db.select(table, rows, filters)
		if len(students_id) ==0:
			new_student = db.insert(table, student_info)
			return HTMLResponse(status_code=status.HTTP_201_CREATED)
		else:
			return HTMLResponse(status_code=status.HTTP_400_BAD_REQUEST)
	else:
		return HTMLResponse(status_code=status.HTTP_400_BAD_REQUEST)

#Updates a student.
@app.put("/students/{student_id}")
async def put_student(student_id: int, req: Request):
	student_update = await req.json()
	table = 'student'
	rows = []
	filters = {'student_id': student_id}
	students_search = db.select(table, rows, filters)
	if len(students_search) == 0:
		return HTMLResponse(status_code=status.HTTP_404_NOT_FOUND)
	if 'email' in student_update:
		email = student_update['email']
		if email is None:
			return HTMLResponse(status_code=status.HTTP_400_BAD_REQUEST)
		filter_email = {'email': email}
		same_email = db.select(table, rows, filter_email)
		if len(same_email) > 0:
			return HTMLResponse(status_code=status.HTTP_400_BAD_REQUEST)
	if 'enrollment_year' in student_update:
		enrollment_year = int(student_update['enrollment_year'])
		if not (2016<=enrollment_year<=2023):
			return HTMLResponse(status_code=status.HTTP_400_BAD_REQUEST)
	student_new_email = db.update(table, student_update, filters)
	return HTMLResponse(status_code=status.HTTP_200_OK)

#Deletes a student.
@app.delete("/students/{student_id}")
async def delete_student(student_id: int):
	table = 'student'
	rows = []
	filters = {'student_id': student_id}
	students_search = db.select(table, rows, filters)
	if len(students_search) == 0:
		return HTMLResponse(status_code=status.HTTP_404_NOT_FOUND)
	else:
		deleted_student = db.delete(table, filters)
		return HTMLResponse(status_code=status.HTTP_200_OK)


# --- EMPLOYEES ---
#Gets all employees that satisfy the specified query parameters.
@app.get("/employees")
async def get_employees(req: Request):
	table = 'employee'
	filter = {}
	query_params = dict(req.query_params)
	fields = query_params.pop("fields", None)
	if fields:
		fields = fields.split(",")
	else:
		fields = []
	if query_params:
		filter.update(query_params)
	else:
		filter = {}
	try:
		employees = db.select(table, fields, filter)
		return employees
	except Exception as e:
		return fields,filter, HTMLResponse(content="<h1>Error</h1>", status_code=status.HTTP_200_OK)

#Gets an employee by ID.
@app.get("/employees/{employee_id}")
async def get_employee(employee_id: int):
	table = 'employee'
	rows = []
	filters = {"employee_id": employee_id}
	employee_id = db.select(table, rows, filters)
	response = len(employee_id)
	if response == 0:
		return HTMLResponse(status_code=status.HTTP_404_NOT_FOUND)
	else:
		employee_id = list(employee_id)
		return employee_id[0]

#Creates an employee.
@app.post("/employees")
async def post_employee(req: Request):
	employee_info = await req.json()
	employee_type = employee_info['employee_type']
	valid_empoy = ['Professor', 'Lecturer', 'Staff']
	if ('email' in employee_info) and (employee_type in valid_empoy):
		email = employee_info['email']
		table = 'employee'
		rows = []
		filters = {'email': email}
		employee_id = db.select(table, rows, filters)
		if len(employee_id) ==0:
			new_employee = db.insert(table, employee_info)
			return HTMLResponse(status_code=status.HTTP_201_CREATED)
		else:
			return HTMLResponse(status_code=status.HTTP_400_BAD_REQUEST)
	else:
		return HTMLResponse(status_code=status.HTTP_400_BAD_REQUEST)

#Updates an employee.
@app.put("/employees/{employee_id}")
async def put_employee(employee_id: int, req: Request):
	employee_update = await req.json()
	table = 'employee'
	rows = []
	filters = {'employee_id': employee_id}
	valid_empoy = ['Professor', 'Lecturer', 'Staff']
	employee_search = db.select(table, rows, filters)
	if len(employee_search) == 0:
		return HTMLResponse(status_code=status.HTTP_404_NOT_FOUND)
	if 'email' in employee_update:
		email = employee_update['email']
		if email is None:
			return HTMLResponse(status_code=status.HTTP_400_BAD_REQUEST)
		filter_email = {'email': email}
		same_email = db.select(table, rows, filter_email)
		if len(same_email) > 0:
			return HTMLResponse(status_code=status.HTTP_400_BAD_REQUEST)
	if 'employee_type' in employee_update:
		employee_type = int(employee_update['employee_type'])
		if not (employee_type not in valid_empoy):
			return HTMLResponse(status_code=status.HTTP_400_BAD_REQUEST)
	employee_new_email = db.update(table, employee_update, filters)
	return HTMLResponse(status_code=status.HTTP_200_OK)

#Deletes an employee.
@app.delete("/employees/{employee_id}")
async def delete_employee(employee_id: int):
	table = 'employee'
	rows = []
	filters = {'employee_id': employee_id}
	employee_search = db.select(table, rows, filters)
	if len(employee_search) == 0:
		return HTMLResponse(status_code=status.HTTP_404_NOT_FOUND)
	else:
		deleted_employee = db.delete(table, filters)
		return HTMLResponse(status_code=status.HTTP_200_OK)


if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=8002)
