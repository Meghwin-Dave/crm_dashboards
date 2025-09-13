# Copyright (c) 2025, Meghwin Dave and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate, flt


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	chart = get_chart_data(data)
	
	return columns, data, None, chart


def get_columns():
	return [
		{
			"fieldname": "date_of_visit",
			"label": _("Date of Visit"),
			"fieldtype": "Date",
			"width": 120
		},
		{
			"fieldname": "sales_person",
			"label": _("Sales Person"),
			"fieldtype": "Link",
			"options": "Sales Person",
			"width": 150
		},
		{
			"fieldname": "customer",
			"label": _("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"width": 200
		},
		{
			"fieldname": "objective_of_meeting",
			"label": _("Objective of Meeting"),
			"fieldtype": "Text",
			"width": 200
		},
		{
			"fieldname": "outcome",
			"label": _("Outcome"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "estimated_order_value",
			"label": _("Estimated Order Value"),
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"fieldname": "order_lost_value",
			"label": _("Order Lost Value"),
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"fieldname": "reason",
			"label": _("Reason"),
			"fieldtype": "Text",
			"width": 200
		},
		{
			"fieldname": "next_action",
			"label": _("Next Action"),
			"fieldtype": "Text",
			"width": 200
		}
	]


def get_data(filters):
	conditions = get_conditions(filters)
	
	query = """
		SELECT 
			svl.date_of_visit,
			svl.sales_person,
			svl.customer,
			svl.objective_of_meeting,
			svl.outcome_of_meeting as outcome,
			svl.estimated_order_value,
			svl.order_lost_value,
			svl.reason_for_lost as reason,
			svl.next_action_plan as next_action,
			svl.name as sales_visit_log
		FROM `tabSales Visit Log` svl
		WHERE svl.docstatus = 1
		{conditions}
		ORDER BY svl.date_of_visit DESC, svl.sales_person
	""".format(conditions=conditions)
	
	data = frappe.db.sql(query, filters, as_dict=True)
	
	# Format currency fields
	for row in data:
		if row.get('estimated_order_value'):
			row['estimated_order_value'] = frappe.format_value(row['estimated_order_value'], {
				'fieldtype': 'Currency'
			})
		if row.get('order_lost_value'):
			row['order_lost_value'] = frappe.format_value(row['order_lost_value'], {
				'fieldtype': 'Currency'
			})
	
	return data


def get_conditions(filters):
	conditions = []
	
	if filters.get("from_date"):
		conditions.append("svl.date_of_visit >= %(from_date)s")
	
	if filters.get("to_date"):
		conditions.append("svl.date_of_visit <= %(to_date)s")
	
	if filters.get("sales_person"):
		conditions.append("svl.sales_person = %(sales_person)s")
	
	if filters.get("customer"):
		conditions.append("svl.customer = %(customer)s")
	
	if conditions:
		return "AND " + " AND ".join(conditions)
	else:
		return ""


def get_chart_data(data):
	"""Prepare chart data for Estimated Order Value grouped by Date"""
	
	# Group data by date
	date_data = {}
	
	for row in data:
		date = row.get('date_of_visit')
		estimated_value = row.get('estimated_order_value', 0)
		
		# Extract numeric value from formatted currency
		if isinstance(estimated_value, str):
			import re
			numeric_value = re.sub(r'[^\d.-]', '', str(estimated_value))
			try:
				estimated_value = float(numeric_value) if numeric_value else 0
			except ValueError:
				estimated_value = 0
		
		if date in date_data:
			date_data[date] += estimated_value
		else:
			date_data[date] = estimated_value
	
	# Sort dates for proper chart display
	sorted_dates = sorted(date_data.keys())
	values = [date_data[date] for date in sorted_dates]
	
	chart_data = {
		"data": {
			"labels": [str(date) for date in sorted_dates],
			"datasets": [{
				"name": "Estimated Order Value",
				"values": values
			}]
		},
		"type": "line",
		"colors": ["#5e64ff"]
	}
	
	return chart_data
