// Copyright (c) 2025, Meghwin Dave and contributors
// For license information, please see license.txt

frappe.query_reports["Sales Budget"] = {
	"filters": [
		{
			"fieldname": "fiscal_year",
			"label": __("Fiscal Year"),
			"fieldtype": "Link",
			"options": "Fiscal Year",
			"default": frappe.defaults.get_user_default("fiscal_year"),
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
