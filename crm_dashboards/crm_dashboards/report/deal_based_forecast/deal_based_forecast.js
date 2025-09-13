// Copyright (c) 2025, Meghwin Dave and contributors
// For license information, please see license.txt

frappe.query_reports["Deal Based Forecast"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_days(frappe.datetime.get_today(), -30),
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
		{
			"fieldname": "sales_person",
			"label": __("Sales Person"),
			"fieldtype": "Link",
			"options": "User",
			"get_query": function() {
				return {
					"filters": {
						"enabled": 1,
						"user_type": "System User"
					}
				};
			}
		},
		{
			"fieldname": "sales_stage",
			"label": __("Sales Stage"),
			"fieldtype": "Link",
			"options": "Sales Stage"
		}
	]
};
