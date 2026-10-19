import mysql.connector as connector

class DBHelper:
  def __init__(self):
    self.con = connector.connect(host='localhost', port='3306', user='root', password='Zig11Dhw@ni', database='pythontest')

    # Table will create only if it is not exist
    query ='create table if not exists user(userId int primary key, userName varchar(200), phone varchar(12))'
    cursor = self.con.cursor()
    cursor.execute(query)

    print("Table Created")

  # Insert
  def insert_user(self, userid, username, phone):
    query="insert into user(userId, userName, phone) values({}, '{}', '{}')".format(userid, username, phone)
    print(query)

    cursor = self.con.cursor()
    cursor.execute(query)
    self.con.commit() #save in database
    print("User saved to DB")

  # Fetching all
  def fetch_all(self):
    query = "Select * from user"
    cursor = self.con.cursor()
    cursor.execute(query)

    for row in cursor:
      # print(row)
      print("UserId : ", row[0])
      print("UserName : ", row[1])
      print("Phone : ", row[2])
      print("----------------------------")

  # Fetching specific user
  def fetch_specific_user(self, userId):
      query = "Select * from user where userId = {}".format(userId)
      cursor = self.con.cursor()
      cursor.execute(query)
  
      for row in cursor:
        # print(row)
        print("UserId : ", row[0])
        print("UserName : ", row[1])
        print("Phone : ", row[2])
        print("----------------------------")

  # Delete user
  def delete_user(self, userId):
    query = "Delete from user where userId = {}".format(userId)
    print(query)
    cursor = self.con.cursor()
    cursor.execute(query)
    self.con.commit()   # permanent delete from DB
    print("Deleted User Successfully")

  # Update User
  def update_user(self, userId, newName, newPhone):
    query = "Update user set userName = '{}', phone = '{}' where userId = {}".format(newName, newPhone, userId)
    print(query)
    cursor = self.con.cursor()
    cursor.execute(query)
    self.con.commit()
    print("User Updated Successfully")


# ------------ main coding -----------------

# --class object
helper = DBHelper()

# --insert into database with the help of python code
# helper.insert_user(101, "Dhwani", "9876543210")
# helper.insert_user(102, "Dhyey", "9876543220")
# helper.insert_user(103, "Shlok", "9876543230")
# helper.insert_user(104, "Pooja", "9876543240")

# --Fetching all record
# helper.fetch_all()

# --Fetching specific user record
# helper.fetch_specific_user(101)

# --Delete User
# helper.delete_user(104)
# helper.fetch_all()

# --Update user
# helper.update_user(101, 'Dhvani', '9876543231')
# helper.fetch_all()
