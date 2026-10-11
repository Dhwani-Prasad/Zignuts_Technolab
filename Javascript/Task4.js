class University {
  constructor(name) {
    this.name = name;
    this.departments = [];
  }

  addDepartment(department) {
    this.departments.push(department);
  }

  removeDepartment(department) {
    let index = this.departments.indexOf(department);

    if (index !== -1) {
      this.departments.splice(index, 1);
    }
  }

  displayDepartments() {
    console.log(this.name);
    console.log(this.departments);
  }
}

let u = new University("ABC University");

u.addDepartment("Computer Science");
u.addDepartment("Mechanical");
u.addDepartment("Civil");

u.displayDepartments();

u.removeDepartment("Mechanical");

u.displayDepartments();