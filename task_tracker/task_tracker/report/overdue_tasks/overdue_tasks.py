import frappe


def execute(filters=None):

    columns = [
        {
            "label": "Task",
            "fieldname": "name",
            "fieldtype": "Link",
            "options":"Task Assignment",
            "width": 220,
        },
        {
            "label": "Task",
            "fieldname": "task_name",
            "fieldtype": "data",
            "options":"Task Assignment",
            "width": 220,
        },
        {
            "label": "Assigned To",
            "fieldname": "assigned_to",
            "fieldtype": "Link",
            "options": "User",
            "width": 200,
        },
        {
            "label": "Due Date",
            "fieldname": "due_date",
            "fieldtype": "Date",
            "width": 120,
        },
        {
            "label": "Status",
            "fieldname": "status",
            "fieldtype": "Data",
            "width": 120,
        }
    ]

    data = frappe.db.sql("""
        SELECT
            name,
            task_name,
            assigned_to,
            COALESCE(revised_due_date, original_due_date) AS due_date,
            status
        FROM `tabTask Assignment`
        WHERE
            status != 'Completed'
            AND COALESCE(revised_due_date, original_due_date) < CURDATE()
        ORDER BY due_date ASC
    """, as_dict=True)

    return columns, data