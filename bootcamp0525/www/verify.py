import frappe

def get_context(context):
    dn = frappe.form_dict.get("dn")
    
    if dn:
        dn = dn.strip() 

    frappe.logger().info(f"Received DN: {dn}")

    if not dn:
        context.valid = False
        return context

    try:
        doc = frappe.get_doc("Delivery Note", dn)
        frappe.logger().info(f"Fetched Delivery Note: {doc.name} with docstatus {doc.docstatus}")

        if doc.docstatus != 1:
            context.valid = False
        else:
            context.valid = True

            # Pass the main Delivery Note
            context.delivery = doc

            # Pass the Delivery Note number
            context.delivery_number = doc.name

            # Pass items list: each with item name and quantity
            items = []
            for item in doc.items:
                items.append({
                    "item_name": item.item_name,
                    "qty": item.qty
                })
            context.delivery_items = items
    except frappe.DoesNotExistError:
        context.valid = False

    return context
