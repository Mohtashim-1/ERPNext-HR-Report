import frappe
from frappe.utils import getdate
from datetime import date as dt
import calendar

def uncheck_absent_checkbox_when_mark_leave_is_checked(doc, method):
    for i in doc.table1:
        if i.mark_leave == 1:
            i.absent = 0
            doc.total_absents -= 1
        elif i.custom_adjustment_leave == 1:
            i.absent = 0
            doc.total_absents -= 1


def handle_security_guard_joining_date(doc, method):
    """
    For Security Guards and Gate Keepers: If employee joins mid-month, mark days before joining date
    as manual_absent instead of absent (so salary is not cut for those days)
    """
    if not doc.employee:
        return
    
    # Get employee designation
    designation = frappe.db.get_value("Employee", doc.employee, "designation")
    
    if designation not in ["Security Guard", "GATE KEEPER"]:
        return
    
    # Get employee joining date
    date_of_joining = frappe.db.get_value("Employee", doc.employee, "date_of_joining")
    
    if not date_of_joining:
        return
    
    joining_date = getdate(date_of_joining)
    
    # Get period start date (first_day) from the attendance period
    if not hasattr(doc, 'month') or not hasattr(doc, 'year'):
        return
    
    # Get HR Settings for period configuration
    hr_settings = frappe.get_single('V HR Settings')
    
    # Calculate first_day based on month/year and HR settings
    def get_month_no(month_name):
        months = {
            'January': 1, 'February': 2, 'March': 3, 'April': 4,
            'May': 5, 'June': 6, 'July': 7, 'August': 8,
            'September': 9, 'October': 10, 'November': 11, 'December': 12
        }
        return months.get(month_name, 1)
    
    month = get_month_no(doc.month)
    year = int(doc.year)
    _, num_days = calendar.monthrange(year, month)
    first_day = dt(year, month, 1)
    
    # Adjust first_day if HR settings have custom period
    if hr_settings.period_from != 1:
        if month == 1:
            temp_month = 12
        else:
            temp_month = month - 1
        first_day = dt(year, temp_month, int(hr_settings.period_from))
    
    first_day = getdate(first_day)
    
    # Calculate number of days between first_day and joining_date
    # Only count if joining_date is after first_day
    if joining_date > first_day:
        # Calculate days difference
        days_diff = (joining_date - first_day).days
        # Set manual_absent to the number of days before joining
        doc.manual_absent = days_diff
    else:
        # If joining_date is on or before first_day, no manual absent days
        doc.manual_absent = 0
    
    # Initialize total_absents if it doesn't exist
    if not hasattr(doc, 'total_absents') or doc.total_absents is None:
        doc.total_absents = 0
    
    # Process each row in table1 to unmark absent for days before joining
    for row in doc.table1:
        if not row.date:
            continue
        
        row_date = getdate(row.date)
        
        # If the date is before joining date and marked as absent
        if row_date < joining_date and row.absent == 1:
            # Unmark as absent
            row.absent = 0
            # Reduce total_absents count (only if it's greater than 0)
            if doc.total_absents > 0:
                doc.total_absents -= 1


