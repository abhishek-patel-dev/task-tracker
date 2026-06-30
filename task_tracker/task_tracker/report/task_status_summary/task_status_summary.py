import frappe


def execute(filters=None):
    columns = [
        {
            "label": "Task Assignment",
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Task Assignment",
            "width": 220,
        },
        {
            "label": "Status",
            "fieldname": "status",
            "fieldtype": "Data",
            "width": 150,
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
            MIN(name) AS name,
            status,
            COUNT(*) AS count
        FROM `tabTask Assignment`
        WHERE status IN ('Completed', 'Failed')
        GROUP BY status
    """, as_dict=True)

    return columns, data