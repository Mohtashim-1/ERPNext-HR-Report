// Copyright (c) 2025, mohtashim and contributors
// For license information, please see license.txt

frappe.query_reports["Employee Attendance Late For Absent"] = {
    "filters": [
        {
            "fieldname": "employee",
            "label": "Employee",
            "fieldtype": "Link",
            "options": "Employee",
            "reqd": 0
        },
        {
            "fieldname": "month",
            "label": "Month",
            "fieldtype": "Select",
            "options": "\nJanuary\nFebruary\nMarch\nApril\nMay\nJune\nJuly\nAugust\nSeptember\nOctober\nNovember\nDecember",
            "reqd": 0
        },
        {
            "fieldname": "year",
            "label": "Year",
            "fieldtype": "Link",
			"options":"Year",
            "reqd": 0
        }
    ]
};
