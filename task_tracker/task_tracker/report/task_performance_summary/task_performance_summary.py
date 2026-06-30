import frappe


def execute(filters=None):
    columns = get_columns()
    data = get_data()

    return columns, data


def get_columns():
    return [
        {
            "label": "Task Assignment",
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Task Assignment",
            "width": 220,
        },
        {
            "label": "Assigned To",
            "fieldname": "assigned_to",
            "fieldtype": "Link",
            "options": "User",
            "width": 220,
        },
        {
            "label": "Average Score",
            "fieldname": "average_score",
            "fieldtype": "Float",
            "width": 150,
        },
        {
            "label": "Total Tasks",
            "fieldname": "total_tasks",
            "fieldtype": "Int",
            "width": 120,
        },
    ]


def get_data():
    return frappe.db.sql("""
        SELECT
            MIN(name) AS name,
            assigned_to,
            ROUND(AVG(score), 2) AS average_score,
            COUNT(name) AS total_tasks
        FROM `tabTask Assignment`
        GROUP BY assigned_to
        ORDER BY average_score DESC
    """, as_dict=True)