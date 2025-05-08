import frappe
import requests
from frappe.utils import nowdate
import json
from frappe import enqueue

def generate_qr_code(doc, method):
    base_url = frappe.utils.get_url()

    verify_url = f"{base_url}/verify?dn={doc.name}"

    qr_api = "https://api.qrserver.com/v1/create-qr-code/"

    response = requests.get(qr_api, params={"size": "150X150", "data": verify_url})

    doc.db_set("custom_qr_code_url", response.url)


@frappe.whitelist(allow_guest=True)
def create_stock_request():
    try:
        data = frappe.request.get_json()

        if not data:
            frappe.throw("No data reveived")

        doc = frappe.get_doc({
            "doctype": "Stock Request",
            "request_date": frappe.utils.nowdate(),
            "requested_by": data.get("user"),
            "items": [
                {
                    "item_code": d.get("item_code"),
                    "qty": d.get("qty")
                } for d in data.get("items", [])
            ]
        })

        doc.insert(ignore_permissions=True)
        frappe.db.commit()

        return {"status": "success", "name": doc.name}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), f"{e}")
        return {"error": str(e)}, 400
    


@frappe.whitelist(methods=['POST'])
def create_stock_request(**kwargs):
    requested_by = kwargs.get("requested_by")
    items = kwargs.get("items", [])

    doc = frappe.get_doc({
        "doctype": "Stock Request",
        "requested_by": requested_by,
        "request_date": nowdate(),
        "items": [
            {"item_code": item["item_code"], "qty": item["qty"]}
            for item in items
        ]
    })
    doc.insert(ignore_permissions=True)

    return "success"




@frappe.whitelist()
def enqueue_order_creation(requested_by=None, items=None):
    items = json.loads(items) if isinstance(items, str) else items

    if not requested_by:
        return "'requested_by' is required."

    if not items or not isinstance(items, list):
        return "'items' must be a non-empty list."

    for item in items:
        if not item.get("item_code") or not item.get("qty"):
            return "Each item must include 'item_code' and 'qty'."

    enqueue(
        method=create_stock_request,
        queue="default",
        requested_by=requested_by,
        items=items
    )

    return "Stock Request job queued successfully."