// Copyright (c) 2025, Meghwin Dave and contributors
// For license information, please see license.txt

frappe.query_reports["Customer Profile"] = {
	"filters": [
		{
			"fieldname": "sales_person",
			"label": __("Sales Person"),
			"fieldtype": "Link",
			"options": "Sales Person"
		},
		{
			"fieldname": "customer_segment",
			"label": __("Customer Segment"),
			"fieldtype": "Select",
			"options": "Contractor\nResident\nBusiness\nGovernment\nEducational\nHealthcare\nRetail\nOther"
		},
		{
			"fieldname": "customer_type",
			"label": __("Customer Type"),
			"fieldtype": "Select",
			"options": "Company\nIndividual\nPartnership"
		},
		{
			"fieldname": "status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": "Active\nInactive"
		}
	]
};
