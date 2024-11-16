# Copyright (c) 2024, mohtashim and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns, data = get_columns(filters), get_data(filters)
    return columns, data

def get_columns(filters):
    return [
        "Department:Link/Department:120",
        "Employee:Link/Employee:250",
        "Designation:Link/Designation:120",
        "Check In:Data:100",
        "Check Out:Data:100",
        "Late Coming:HTML:100",  # Changed to HTML to support highlighting
        "Early Going Hours:HTML:100",  # Changed to HTML to support highlighting
        "Late Sitting Hours:HTML:100",
        "Over Time:HTML:100",
    ]

def get_data(filters):
    cond = ""
    if filters.get("depart"):
        cond = "and emp.department='{0}' ".format(filters.get("depart"))

    if filters.get("employee"):
        cond = "and emp.employee='{0}' ".format(filters.get("employee"))

    # Fetching records with the necessary fields
    records = frappe.db.sql("""
        SELECT
            emp.department,
            emp.employee,
            emptab.date,
            emptab.check_in_1,
            emptab.check_out_1,
            emptab.late_coming_hours,
            emptab.early_going_hours,
            emptab.difference1,
            emptab.estimated_late,
            emptab.late,
            emptab.absent
        FROM `tabEmployee Attendance` AS emp
        JOIN `tabEmployee Attendance Table` AS emptab ON emptab.parent = emp.name
        JOIN `tabEmployee` emply ON emp.employee = emply.name
        WHERE emptab.date = %s {0} AND emply.status = "Active"
        ORDER BY emptab.date, emp.department
    """.format(cond), (filters.get('to'),))

    data = []
    prev_dep = None
    total_lates = 0
    total_presents = 0
    total_absents = 0

    for item in records:
        row = None
        if prev_dep != item[0]:
            prev_dep = item[0]
            row = [item[0], "", "", "", "", "", "", "", ""]
            data.append(row)
            row = [""]

        else:
            row = [""]

        # Appending data row
        row.append(item[1])  # Employee
        row.append(frappe.db.get_value("Employee", {"name": item[1]}, "designation"))  # Designation
        row.append(item[3])  # Check In
        row.append(item[4])  # Check Out

        # Highlight Late Coming Hours if not 0 or empty
        late_coming_hours = (
            f"<span style='color:red;'>{item[5]}</span>"
            if item[5] and item[5] != "00:00:00"
            else item[5]
        )
        row.append(late_coming_hours)

        # Highlight Early Going Hours if not 0 or empty
        early_going_hours = (
            f"<span style='color:orange;'>{item[6]}</span>"
            if item[6] and item[6] != "00:00:00"
            else item[6]
        )
        row.append(early_going_hours)
        
		# Highlight Overtime if not 0 or empty
        estimated_late = (
            f"<span style='color:green;'>{item[7]}</span>"
            if item[7] and item[7] != "00:00:00"
            else item[7]
        )
        row.append(estimated_late)
        
		# Highlight Overtime if not 0 or empty
        difference1 = (
            f"<span style='color:green;'>{item[8]}</span>"
            if item[8] and item[8] != "00:00:00"
            else item[8]
        )
        row.append(difference1)
        
		
        

        row.append(item[7])  # Late Sitting Hours
        row.append(item[8])  # Over Time

        # Calculating status
        status = "<span style='color:blue;'>P</span>"
        if item[9] == 1:
            status = "<span style='color:green;'>L</span>"
            total_lates += 1
        elif item[10] == 1:
            status = "<span style='color:red;'>A</span>"
            total_absents += 1
        else:
            total_presents += 1
        row.append(status)

        data.append(row)

    # Adding totals row
    data.append([
        "", "", "", "", "",
        "<b>Total Presents</b>", total_presents,
        "<b>Total Lates</b>", total_lates,
        "<b>Total Absents</b>", total_absents,
    ])
    return data
