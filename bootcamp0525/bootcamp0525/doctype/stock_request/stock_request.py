# Copyright (c) 2025, Karani Geoffrey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname


class StockRequest(Document):
	def validate(self):
		for item in self.items:
			stock = frappe.db.get_value("Bin", {"item_code": item.item_code}, "actual_qty") or 0

			item.available_stock = stock

			if self.workflow_state == "Pending Approval" and item.qty > stock:
				frappe.throw(f"Insufficient stock for {item.item_name}. Requested: {item.qty}, Available: {stock}")


	def autoname(self):
		self.name = make_autoname("KAR-.YYYY.-.MM.-.###")


	
	def on_update(self):
		if self.workflow_state == "Approved" and not self.material_request_created():
			self.create_material_request()




	def material_request_created(self):
		return frappe.db.exists("Material Request", {"custom_stock_request": self.name})
	


	def create_material_request(self):
		mr = frappe.new_doc("Material Request")
		mr.material_request_type = "Material Issue"
		mr.transaction_date = self.request_date or frappe.utils.nowdate()
		mr.custom_stock_request = self.name

		for item in self.items:
			mr.append("items", {
			 "item_code": item.item_code,
			 "qty": item.qty,
			 "schedule_date": self.request_date or frappe.utils.nowdate()
			 }
			)

		mr.insert(ignore_permissions=True)
		mr.submit()