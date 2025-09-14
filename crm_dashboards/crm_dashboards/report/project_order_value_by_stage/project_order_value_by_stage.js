// Copyright (c) 2025, Meghwin Dave and contributors
// For license information, please see license.txt

frappe.query_reports["Project Order Value by Stage"] = {
	"chart": true,
	"filters": [
		{
			"fieldname": "project_type",
			"label": __("Project Type"),
			"fieldtype": "Select",
			"options": [
				"",
				"Commercial",
				"Residential", 
				"Industrial",
				"Infrastructure",
				"Mixed Use"
			],
			"width": "100%"
		},
		{
			"fieldname": "stage_of_project",
			"label": __("Stage of Project"),
			"fieldtype": "Select",
			"options": [
				"",
				"Initial Discussion",
				"Proposal Sent",
				"Negotiation",
				"Final Discussion",
				"Order Pending",
				"Order Received"
			],
			"width": "100%"
		},
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "100%",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -12)
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "100%",
			"default": frappe.datetime.get_today()
		}
	],
	
	"onload": function(report) {
		// Set default date range to last 12 months
		report.set_filter_value("from_date", frappe.datetime.add_months(frappe.datetime.get_today(), -12));
		report.set_filter_value("to_date", frappe.datetime.get_today());
	}
};
