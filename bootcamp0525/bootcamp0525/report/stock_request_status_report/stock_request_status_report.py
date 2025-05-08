# Copyright (c) 2025, Karani Geoffrey and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	filters = filters or {}

	conditions = ""


	if filters.get("workflow_state"):
		conditions  += " AND workflow_state = %(workflow_state)s"
	if filters.get("from_date") and filters.get("to_date"):
		conditions += " AND request_date BETWEEN %(from_date)s AND %(to_date)s"



	data = frappe.db.sql(f""" 
		SELECT 
			name, 
			requested_by,
			workflow_state,
			request_date
		FROM `tabStock Request`
		WHERE docstatus < 2 {conditions}
		ORDER BY request_date DESC

 	""", filters, as_dict=True)

	columns = [
		{
			"label": "Request ID",
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "Stock Request",
			"width": 200
		},
		{
			"label": "Requested By",
			"fieldname": "requested_by",
			"fieldtype": "Link",
			"options": "User",
			"width": 250
		},
		{
			"label": "Workflow State",
			"fieldname": "workflow_state",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"label": "Request Date",
			"fieldname": "request_date",
			"fieldtype": "Date",
			"width": 150
		},
	]


	return columns, data