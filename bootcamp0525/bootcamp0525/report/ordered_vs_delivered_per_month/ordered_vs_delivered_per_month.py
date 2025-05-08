# Copyright (c) 2025, Karani Geoffrey and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import getdate, nowdate, add_months
import calendar

def execute(filters=None):
    labels = []
    ordered = []
    delivered = []
    tabular_data = []

    today = getdate(nowdate())

    for i in range(11, -1, -1): 
        month_start = add_months(today.replace(day=1), -i)
        month_end_day = calendar.monthrange(month_start.year, month_start.month)[1]
        month_end = month_start.replace(day=month_end_day)
        label = month_start.strftime('%b %Y')

        # Get all created stock requests (Draft + Submitted + Cancelled)
        total_requests = frappe.db.count("Stock Request", {
            "request_date": ["between", [month_start, month_end]]
        })

        # Get only those with workflow_state = Delivered
        delivered_count = frappe.db.count("Stock Request", {
            "workflow_state": "Delivered",
            "request_date": ["between", [month_start, month_end]]
        })

        labels.append(label)
        ordered.append(total_requests)
        delivered.append(delivered_count)
        tabular_data.append([label, total_requests, delivered_count])

    if frappe.flags.in_chart:
        return {
            "labels": labels,
            "datasets": [
                {"name": "Ordered", "values": ordered},
                {"name": "Delivered", "values": delivered}
            ]
        }

    columns = [
        {"label": "Month", "fieldname": "month", "fieldtype": "Data", "width": 120},
        {"label": "Ordered", "fieldname": "ordered", "fieldtype": "Int", "width": 100},
        {"label": "Delivered", "fieldname": "delivered", "fieldtype": "Int", "width": 100}
    ]
    return columns, tabular_data
