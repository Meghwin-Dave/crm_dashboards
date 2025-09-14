// Copyright (c) 2025, Meghwin Dave and contributors
// For license information, please see license.txt

frappe.query_reports["Monthly Sales Report (Salesperson-wise)"] = {
	"chart": true,
	"filters": [
		{
			"fieldname": "month",
			"label": __("Month"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
		{
			"fieldname": "sales_person",
			"label": __("Sales Person"),
			"fieldtype": "Link",
			"options": "Sales Person",
			"get_query": function() {
				return {
					"filters": {
						"enabled": 1
					}
				};
			}
		},
		{
			"fieldname": "territory",
			"label": __("Territory"),
			"fieldtype": "Link",
			"options": "Territory"
		}
	]
};
