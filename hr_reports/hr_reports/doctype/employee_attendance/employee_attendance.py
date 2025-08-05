import frappe

def uncheck_absent_checkbox_when_mark_leave_is_checked(doc, method):
    for i in doc.table1:
        if i.mark_leave == 1:
            i.absent = 0
            doc.total_absents -= 1
        elif i.custom_adjustment_leave == 1:
            i.absent = 0
            doc.total_absents -= 1