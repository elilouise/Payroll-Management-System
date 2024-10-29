-- SQLite
CREATE TABLE Employees (

employeeID INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
baseSalary REAL NOT NULL,
address TEXT,
role TEXT NOT NULL
);

CREATE TABLE Attendance (
attendanceID INTEGER PRIMARY KEY AUTOINCREMENT,
employeeID INTEGER, 
date DATE,
hours_worked REAL,
FOREIGN KEY (employeeID) REFERENCES Employees (employeeID)
);


