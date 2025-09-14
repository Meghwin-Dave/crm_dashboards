// Copyright (c) 2025, Meghwin Dave and contributors
// For license information, please see license.txt

frappe.ui.form.on("Sales Visit Log", {
	refresh(frm) {
		// Set default date to today
		if (!frm.doc.date_of_visit) {
			frm.set_value("date_of_visit", frappe.datetime.get_today());
		}
		
		// Set default sales person to current user
		if (!frm.doc.sales_person) {
			frm.set_value("sales_person", frappe.user.name);
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