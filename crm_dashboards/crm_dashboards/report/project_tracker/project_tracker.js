// Copyright (c) 2025, Meghwin Dave and contributors
// For license information, please see license.txt

frappe.query_reports["Project Tracker"] = {
	"chart": true,
	"filters": [
		// Sales Person filter disabled until custom fields are installed
		// {
		// 	"fieldname": "sales_person",
		// 	"label": __("Sales Person"),
		// 	"fieldtype": "Link",
		// 	"options": "Sales Person",
		// 	"width": "100%"
		// },
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
	},
	
	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		
		// Color code the stage of project column
		if (column.fieldname === "stage_of_project") {
			const stage = data.stage_of_project;
			let color = "";
			
			switch(stage) {
				case "Initial Discussion":
					color = "#ff6b6b";
					break;
				case "Proposal Sent":
					color = "#4ecdc4";
					break;
				case "Negotiation":
					color = "#45b7d1";
					break;
				case "Final Discussion":
					color = "#96ceb4";
					break;
				case "Order Pending":
					color = "#feca57";
					break;
				case "Order Received":
					color = "#48dbfb";
					break;
				default:
					color = "#ddd";
			}
			
			value = `<span style="background-color: ${color}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 500;">${stage}</span>`;
		}
		
		// Format currency values
		if (column.fieldname === "project_order_value") {
			if (value && value !== "0.00") {
				value = `<span style="font-weight: 600; color: #2e7d32;">${value}</span>`;
			}
		}
		
		// Format dates
		if (column.fieldname === "first_visit_date" || column.fieldname === "last_visit_date" || column.fieldname === "order_expected_date") {
			if (value) {
				const date = new Date(value);
				const today = new Date();
				const diffTime = date - today;
				const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
				
				if (diffDays < 0) {
					value = `<span style="color: #d32f2f;">${value}</span>`;
				} else if (diffDays <= 30) {
					value = `<span style="color: #f57c00;">${value}</span>`;
				} else {
					value = `<span style="color: #2e7d32;">${value}</span>`;
				}
			}
		}
		
		return value;
	}
};
