from flask import Flask, request, jsonify
import pymysql
import os
from dotenv import load_dotenv
from datetime import datetime
from flask_cors import CORS  # ✅ Import
# 
# Load environment variables from .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

app = Flask(__name__)
CORS(app)  # ✅ Enable for all routes
def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=3306,
        cursorclass=pymysql.cursors.DictCursor  # results as dict
    )

@app.route("/users", methods=["GET"])
def get_users():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM tbl_employee;")
            rows = cursor.fetchall()
        conn.close()
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@app.route("/create", methods=["POST"])
def create_user():
    data = request.json  # expects JSON input

    emp_code = data.get("emp_code")
    department_id = data.get("department_id")
    joining_date = data.get("joining_date")
    fullname = data.get("fullname")
    gender = data.get("gender")
    email = data.get("email")
    city = data.get("city")
    state = data.get("state")
    country = data.get("country")
    designationlevel = data.get("designationlevel")
    created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    updated_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    print(department_id,"department_id")

    try:
        conn = get_db_connection()
        print(data,"data")
        with conn.cursor() as cursor:
            sql = """
                    INSERT INTO tbl_employee( 
                    emp_code,
                    department_id,
                    joining_date,
                    fullname,
                    gender,
                    email,
                    city,
                    state,
                    country,
                    designationlevel,
                    created_date,
                    updated_date) VALUES ( %s, %s, %s, %s,%s,%s, %s,%s, %s,%s, %s,%s);
                    """
            #sql = "INSERT INTO tbl_employee (name, age) VALUES (%s, %s)"
            cursor.execute(sql, (emp_code, department_id,joining_date,fullname,gender,email,city,state,country,designationlevel,created_date,updated_date))
            conn.commit()
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
        
 
@app.route("/registeruser", methods=["POST"])
def register_user():
    data = request.json  # expects JSON input

    fullname = data.get("full_name")
    email = data.get("email")
    password = data.get("password")
    created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    updated_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    print(fullname,"fullname")
    print(email,"email")
    print(password,"password")
    print(created_date,"created_date")
    print(updated_date,"updated_date")

    try:
        conn = get_db_connection()
        print(data,"data")
        with conn.cursor() as cursor:
            sql = """
                    INSERT INTO tbl_user_registration( 
                    full_name,
                    email,
                    password,
                    created_date,
                    updated_date) VALUES ( %s, %s, %s, %s,%s);
                    """
            #sql = "INSERT INTO tbl_employee (name, age) VALUES (%s, %s)"
            cursor.execute(sql, (fullname, email,password,created_date,updated_date))
            conn.commit()
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
        
        

@app.route("/createDepartment", methods=["POST"])
def addDepartment():
    data = request.json  # expects JSON input

    deptname = data.get("deptname")
    deptcode = data.get("deptcode")
    emp_code = data.get("emp_code")
    created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    updated_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    print(deptname,"deptname")
    print(deptcode,"deptcode")
    print(emp_code,"emp_code")
    print(created_date,"created_date")
    print(updated_date,"updated_date")

    try:
        conn = get_db_connection()
        print(data,"data")
        with conn.cursor() as cursor:
            sql = """
                    INSERT INTO tbl_department( 
                    department_name,
                    department_code,
                    manager_emp_code,
                    created_date,
                    updated_date) VALUES ( %s, %s, %s, %s,%s);
                    """
            #sql = "INSERT INTO tbl_employee (name, age) VALUES (%s, %s)"
            cursor.execute(sql, (deptname, deptcode,emp_code,created_date,updated_date))
            conn.commit()
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


 
@app.route("/departments", methods=["GET"])
def get_departments():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM tbl_department;;")
            rows = cursor.fetchall()
        conn.close()
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
@app.route("/login", methods=["POST"])
def login_User():
    data = request.json  # expects JSON input

    email = data.get("email")
    password = data.get("password") 
    

    try:
        conn = get_db_connection()
        print(data,"data")
        with conn.cursor() as cursor:
            sql = """
                    select * from tbl_user_registration where email = %s and password = %s
                    
                    """
            #sql = "INSERT INTO tbl_employee (name, age) VALUES (%s, %s)"
            cursor.execute(sql, (email,password))
            user = cursor.fetchone()
            print(user,"user111121")
            if user:
                return jsonify({"success": True, "token": "dummyToken123",'fullname':user["full_name"]})  # You can replace with real JWT
            else:
                return jsonify({"success": False, "message": "Invalid credentials"})
 
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
        
        
@app.route("/departmentHeadByDesignationLevel", methods=["GET"])
def getDepartmentHead():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("select * from tbl_employee where designationlevel >= 7")
            rows = cursor.fetchall()
        conn.close()
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

    
@app.route("/createProject", methods=["POST"])
def addProjects():
    data = request.json  # expects JSON input

    project_name = data.get("project_name")
    project_startdate = data.get("project_startdate")
    project_enddate = data.get("project_enddate")
    project_description = data.get("project_description")
    project_code = data.get("project_code")
    client_name = data.get("client_name") 
    created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    updated_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  

    try:
        conn = get_db_connection()
        print(data,"data")
        with conn.cursor() as cursor:
            sql = """
                    INSERT INTO tbl_addproject( 
                    project_name,
                    project_startdate,
                    project_enddate,
                    project_description,
                    project_code,
                    client_name,
                    created_date,
                    updated_date) VALUES ( %s, %s, %s, %s,%s,%s,%s,%s);
                    """
            #sql = "INSERT INTO tbl_employee (name, age) VALUES (%s, %s)"
            cursor.execute(sql, (project_name, project_startdate,project_enddate,project_description,project_code,client_name,created_date,updated_date))
            conn.commit()
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
            
            
@app.route("/getprojectlist", methods=["GET"])
def get_projectlist():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM tbl_addproject;")
            rows = cursor.fetchall()
        conn.close()
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500            
             
    
@app.route("/createProjectTeam", methods=["POST"])
def addProjectTeam():
    data = request.json  # expects JSON input

    project_code = data.get("project_code")
    department_id = data.get("department_id")
    manager_emp_code = data.get("manager_emp_code") 
    created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    updated_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  

    try:
        conn = get_db_connection()
        print(data,"data")
        with conn.cursor() as cursor:
            sql = """
                    INSERT INTO tbl_project_team( 
                    project_code,
                    department_id,
                    manager_emp_code, 
                    created_date,
                    updated_date) VALUES ( %s, %s, %s, %s,%s);
                    """
            #sql = "INSERT INTO tbl_employee (name, age) VALUES (%s, %s)"
            cursor.execute(sql, (project_code, department_id,manager_emp_code,created_date,updated_date))
            conn.commit()
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
        
#populate team according to department head  select * from tbl_employee  where manager_emp_code = 'E365'

@app.route("/getTeamMembersByDeptId", methods=["GET"])
def getTeamMembersByDeptHead():
    data = request.json
    department_id = data.get("department_id")
    print(department_id,"department_id")
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """
                    SELECT te.fullname as fullname ,te.emp_code as emp_code,td.manager_emp_code as manager_emp_code,td.department_name as department_name
                    FROM tbl_employee te INNER JOIN tbl_department td
                    ON te.department_id = td.department_id where te.department_id = %s
                    
                  """
            cursor.execute(sql,(department_id)) 
            rows = cursor.fetchall()
        conn.close()
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500      



#pass project code from dashboard and resolve dashboard errors

@app.route("/getProjectByProjectcode", methods=["GET"])
def getProjectByProjectcode():
    #data = request.json 
    project_code = "AIDS001"
    print(project_code,"project_code")
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """ 
                    SELECT *, pr.project_name as project_name
                    FROM tbl_project_team 
                    INNER JOIN tbl_employee 
                    ON tbl_project_team.department_id = tbl_employee.department_id                     
                    INNER JOIN tbl_addproject pr
                    ON tbl_project_team.project_code = pr.project_code
                    where tbl_project_team.project_code = %s
                    
                  """
            cursor.execute(sql,(project_code)) 
            rows = cursor.fetchall()
        conn.close()
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500     
    

 
@app.route("/getProjectandTeamDetails", methods=["POST"])
def getProjectandTeamDetails():
    data = request.json  # expects JSON input 
    project_code = data.get("project_code")  
    try:
        conn = get_db_connection()
        print(data,"data")
        with conn.cursor() as cursor:
            sql = """
                  SELECT * FROM tbl_project_team tp
                    INNER JOIN tbl_employee te
                    ON tp.department_id = te.department_id
                    INNER JOIN tbl_addproject pj
                    ON pj.project_code = tp.project_code
                    where tp.project_code = %s
                    
                 """
            #sql = "INSERT INTO tbl_employee (name, age) VALUES (%s, %s)"
            cursor.execute(sql, (project_code))
            rows = cursor.fetchall()
        conn.close()
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500 
        
        

@app.route("/createTaskTicket", methods=["POST"])
def addTaskTicket():
    data = request.json  # expects JSON input

    title = data.get("tasktitle")
    description = data.get("description")
    time_required = data.get("time_required") 
    project_id = data.get("project_id") 
    ticket_progress_status = data.get("ticket_progress_status") 
    emp_code = data.get("emp_code")
    created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    updated_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")   
    

    try:
        conn = get_db_connection()
        print(data,"data")
        with conn.cursor() as cursor:
            sql = """
                  INSERT INTO tbl_task_ticket
                    (
                    title,
                    description,
                    time_required,
                    project_id,
                    ticket_progress_status,
                    emp_code,
                    created_date,
                    updated_date
                    )
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s);
                    """
            #sql = "INSERT INTO tbl_employee (name, age) VALUES (%s, %s)"
            cursor.execute(sql, (title, description,time_required,project_id,ticket_progress_status,emp_code,created_date,updated_date))
            conn.commit()
        return jsonify({"message": "Task created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
        

@app.route("/getTaskDetailsByEmployeeID", methods=["GET"])
def getTaskDetailsByEmployeeID(): 
    emp_code = request.args.get('emp_code')
    
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """ 
                    select * from tbl_task_ticket tt
                    INNER JOIN tbl_addproject ap on ap.project_id = tt.project_id where tt.emp_code = %s
                    
                  """
            cursor.execute(sql,(emp_code)) 
            rows = cursor.fetchall()
        conn.close()
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500     
    

if __name__ == "__main__":
    app.run(debug=True, port=5000)



#check API calls getProjectandTeamDetails project code required to creat taks API call,alignment,report charts

 #based on getProjectandTeamDetails create API for create ticket per user while create ticket pass selected project code to populate getProjectandTeamDetails
 # correct UI
