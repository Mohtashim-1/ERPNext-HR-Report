import frappe
from frappe.utils import getdate

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
    For Security Guards: If employee joins mid-month, mark days before joining date
    as manual_absent instead of absent (so salary is not cut for those days)
    """
    if not doc.employee:
        return
    
    # Get employee designation
    designation = frappe.db.get_value("Employee", doc.employee, "designation")
    
    if designation != "Security Guard":
        return
    
    # Get employee joining date
    date_of_joining = frappe.db.get_value("Employee", doc.employee, "date_of_joining")
    
    if not date_of_joining:
        return
    
    joining_date = getdate(date_of_joining)
    
    # Initialize manual_absent if it doesn't exist
    if not hasattr(doc, 'manual_absent') or doc.manual_absent is None:
        doc.manual_absent = 0
    
    # Initialize total_absents if it doesn't exist
    if not hasattr(doc, 'total_absents') or doc.total_absents is None:
        doc.total_absents = 0
    
    # Process each row in table1
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
            # Increment manual_absent count
            doc.manual_absent = (doc.manual_absent or 0) + 1


