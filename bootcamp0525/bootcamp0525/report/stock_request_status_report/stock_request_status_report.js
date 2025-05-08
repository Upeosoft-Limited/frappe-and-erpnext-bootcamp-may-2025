// Copyright (c) 2025, Karani Geoffrey and contributors
// For license information, please see license.txt

frappe.query_reports["Stock Request Status Report"] = {
	"filters": [
		{
			"fieldname": "requested_by",
			"label": "Requested By",
			"fieldtype": "Link",
			"options": "User"
		},
		{
			"fieldname": "workflow_state",
			"label": "Workflow State",
			"fieldtype": "Select",
			"options": ["", "Draft", "Pending Approval", "Approved"]
		},
		{
			"fieldname": "from_date",
			"label": "From Date",
			"fieldtype": "Date",
			"default": frappe.datetime.month_start(),
		},
		{
			"fieldname": "to_date",
			"label": "To Date",
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
		}
	]
};

