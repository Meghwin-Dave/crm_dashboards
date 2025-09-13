// Copyright (c) 2025, Meghwin Dave and contributors
// For license information, please see license.txt

frappe.ui.form.on("Sales Visit Log", {
	refresh(frm) {
		// Add custom buttons
		if (frm.doc.docstatus === 1) {
			frm.add_custom_button(__("Create Follow-up Task"), function() {
				frm.call("create_follow_up_task");
			});
		}
		
		// Set default date to today
		if (!frm.doc.date_of_visit) {
			frm.set_value("date_of_visit", frappe.datetime.get_today());
		}
		
		// Set default sales person to current user
		if (!frm.doc.sales_person) {
			frm.set_value("sales_person", frappe.user.name);
		}
	},

	customer(frm) {
		// Fetch customer details when customer is selected
		if (frm.doc.customer) {
			frm.call("get_customer_details").then(r => {
				if (r.message) {
					frm.set_value("customer_type", r.message.customer_type);
					frm.set_value("customer_segment", r.message.market_segment);
				}
			});
		}
	},

	outcome_of_meeting(frm) {
		// Show/hide reason for lost field based on outcome
		if (frm.doc.outcome_of_meeting === "Unsuccessful") {
			frm.set_df_property("reason_for_lost", "reqd", 1);
		} else {
			frm.set_df_property("reason_for_lost", "reqd", 0);
		}
	},

	estimated_order_value(frm) {
		// Clear order lost value if estimated order value is entered
		if (frm.doc.estimated_order_value && frm.doc.order_lost_value) {
			frm.set_value("order_lost_value", 0);
		}
	},

	order_lost_value(frm) {
		// Clear estimated order value if order lost value is entered
		if (frm.doc.order_lost_value && frm.doc.estimated_order_value) {
			frm.set_value("estimated_order_value", 0);
		}
	}
});

// Custom function to create follow-up task
frappe.ui.form.on("Sales Visit Log", "create_follow_up_task", function(frm) {
	frm.call("create_follow_up_task").then(r => {
		if (r.message) {
			frappe.msgprint(__("Follow-up task created successfully"));
		}
	});
});