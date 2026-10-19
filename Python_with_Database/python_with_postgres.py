import psycopg2
import psycopg2.extras

class DBHelper:
    def __init__(self):
        self.con = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres",
            password="ZenDhwani",
            database="Employee"
        )

        query = """
        CREATE TABLE IF NOT EXISTS employee (
            id INT PRIMARY KEY,
            name VARCHAR(40) NOT NULL,
            salary INT,
            dept_id VARCHAR(30)
        )
        """

        cursor = self.con.cursor()
        try:
            cursor.execute(query)
            self.con.commit()
            print("Table Created")
        except Exception:
            self.con.rollback()
            raise
        finally:
            cursor.close()

    def insert_employee(self, empId, name, salary, deptId):
        query = """
        INSERT INTO employee (id, name, salary, dept_id)
        VALUES (%s, %s, %s, %s)
        """

        cursor = self.con.cursor()
        try:
            cursor.execute(query, (empId, name, salary, deptId))
            self.con.commit()
            print("Employee saved to DB")
        except Exception as error:
            self.con.rollback()
            print(error)
        finally:
            cursor.close()

    def fetch_all(self):
        query = "SELECT * FROM employee"

        cursor = self.con.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        )
        try:
            cursor.execute(query)

            for row in cursor.fetchall():
                print("ID:", row["id"])
                print("Name:", row["name"])
                print("Salary:", row["salary"])
                print("Department:", row["dept_id"])
                print("----------------------------")
        finally:
            cursor.close()

    def fetch_specific_employee(self, empId):
        query = "SELECT * FROM employee WHERE id = %s"

        cursor = self.con.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        )
        try:
            cursor.execute(query, (empId,))
            row = cursor.fetchone()

            if row:
                print("ID:", row["id"])
                print("Name:", row["name"])
                print("Salary:", row["salary"])
                print("Department:", row["dept_id"])
            else:
                print("Employee not found")
        finally:
            cursor.close()

    def delete_employee(self, empId):
        query = "DELETE FROM employee WHERE id = %s"

        cursor = self.con.cursor()
        try:
            cursor.execute(query, (empId,))
            self.con.commit()

            if cursor.rowcount > 0:
                print("Deleted Employee Successfully")
            else:
                print("Employee not found")
        except Exception as error:
            self.con.rollback()
            print(error)
        finally:
            cursor.close()

    def update_employee(self, empId, newName, newSalary, newDeptId):
        query = """
        UPDATE employee
        SET name = %s, salary = %s, dept_id = %s
        WHERE id = %s
        """

        cursor = self.con.cursor()
        try:
            cursor.execute(
                query,
                (newName, newSalary, newDeptId, empId)
            )
            self.con.commit()

            if cursor.rowcount > 0:
                print("Employee Updated Successfully")
            else:
                print("Employee not found")
        except Exception as error:
            self.con.rollback()
            print(error)
        finally:
            cursor.close()

    def close_connection(self):
        self.con.close()


helper = None

try:
    helper = DBHelper()

    # Insert employee
    # helper.insert_employee(1, "Dhwani", 40000, "D1")
    # helper.insert_employee(2, "Dhyey", 50000, "D2")
    # helper.insert_employee(3, "Shlok", 35000, "D1")

    # Fetch all employees
    # helper.fetch_all()

    # Fetch specific employee
    # helper.fetch_specific_employee(1)

    # Update employee
    # helper.update_employee(1, "Dhvani", 60000, "D2")

    # Delete employee
    # helper.delete_employee(3)

    # Display all employees after changes
    helper.fetch_all()

except Exception as error:
    print(error)

finally:
    if helper is not None:
        helper.close_connection()
