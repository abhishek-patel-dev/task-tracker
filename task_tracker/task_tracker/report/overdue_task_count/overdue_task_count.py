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
            "label": "Status",
            "fieldname": "status",
            "fieldtype": "Data",
            "width": 180,
        },
        {
            "label": "Count",
            "fieldname": "count",
            "fieldtype": "Int",
            "width": 100,
        },
    ]

    data = frappe.db.sql("""
        SELECT
            name,
            'Overdue Tasks' AS status,
            COUNT(*) AS count
        FROM `tabTask Assignment`
        WHERE
            status != 'Completed'
            AND COALESCE(revised_due_date, original_due_date) < CURDATE()
    """, as_dict=True)

    return columns, data