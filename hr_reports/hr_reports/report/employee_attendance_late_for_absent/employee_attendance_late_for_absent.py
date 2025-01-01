# Copyright (c) 2025, mohtashim and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    # Define the order of months
    months_order = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]

    # Base query
    query = """
        SELECT 
            ea.employee AS employee,
            ea.month AS month,
            ea.year AS year,
            ea.lates_for_absent AS lates_for_absent
        FROM `tabEmployee Attendance` AS ea
        WHERE 1 = 1
    """

    # Conditions for filters
    conditions = []
    if filters.get("employee"):
        conditions.append("ea.employee = %(employee)s")
    if filters.get("month"):
        conditions.append("ea.month = %(month)s")
    if filters.get("year"):
        conditions.append("ea.year = %(year)s")

    # Add conditions to query
    if conditions:
        query += " AND " + " AND ".join(conditions)

    # Add ORDER BY clause
    query += """
        ORDER BY 
            ea.year,
            FIELD(ea.month, {months})
    """.format(months=", ".join([f"'{month}'" for month in months_order]))

    # Execute the query with filters
    data = frappe.db.sql(query, filters, as_dict=True)

    # Define columns
    columns = [
        {"label": "Employee", "fieldname": "employee", "fieldtype": "Data", "width": 250},
        {"label": "Month", "fieldname": "month", "fieldtype": "Data", "width": 100},
        {"label": "Year", "fieldname": "year", "fieldtype": "Data", "width": 200},
        {"label": "Late for Absent", "fieldname": "lates_for_absent", "fieldtype": "Data", "width": 200}
    ]

    return columns, data
