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
			"fieldname": "opportunity_name",
			"label": _("Opportunity Name"),
			"fieldtype": "Link",
			"options": "Opportunity",
			"width": 200
		},
		{
			"fieldname": "sales_person",
			"label": _("Sales Person"),
			"fieldtype": "Link",
			"options": "User",
			"width": 150
		},
		{
			"fieldname": "contact",
			"label": _("Contact"),
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "sales_stage",
			"label": _("Sales Stage"),
			"fieldtype": "Link",
			"options": "Sales Stage",
			"width": 150
		},
		{
			"fieldname": "amount",
			"label": _("Amount"),
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"fieldname": "probability",
			"label": _("Probability"),
			"fieldtype": "Percent",
			"width": 100
		},
		{
			"fieldname": "weighted_amount",
			"label": _("Weighted Amount"),
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"fieldname": "expected_closing_date",
			"label": _("Expected Closing Date"),
			"fieldtype": "Date",
			"width": 150
		}
	]


def get_data(filters):
	conditions = get_conditions(filters)
	
	query = """
		SELECT 
			opp.name as opportunity_name,
			opp.opportunity_owner as sales_person,
			opp.contact_display as contact,
			opp.sales_stage,
			opp.opportunity_amount as amount,
			opp.probability,
			(opp.opportunity_amount * opp.probability / 100) as weighted_amount,
			opp.expected_closing as expected_closing_date,
			opp.currency
		FROM `tabOpportunity` opp
		WHERE opp.docstatus != 2
		AND opp.status IN ('Open', 'Quotation', 'Replied')
		{conditions}
		ORDER BY opp.expected_closing ASC, opp.opportunity_amount DESC
	""".format(conditions=conditions)
	
	data = frappe.db.sql(query, filters, as_dict=True)
	
	# Format currency fields
	for row in data:
		if row.get('amount'):
			row['amount'] = frappe.format_value(row['amount'], {
				'fieldtype': 'Currency',
				'currency': row.get('currency') or frappe.get_default('currency')
			})
		if row.get('weighted_amount'):
			row['weighted_amount'] = frappe.format_value(row['weighted_amount'], {
				'fieldtype': 'Currency',
				'currency': row.get('currency') or frappe.get_default('currency')
			})
	
	return data


def get_conditions(filters):
	conditions = []
	
	if filters.get("from_date"):
		conditions.append("opp.transaction_date >= %(from_date)s")
	
	if filters.get("to_date"):
		conditions.append("opp.transaction_date <= %(to_date)s")
	
	if filters.get("sales_person"):
		conditions.append("opp.opportunity_owner = %(sales_person)s")
	
	if filters.get("sales_stage"):
		conditions.append("opp.sales_stage = %(sales_stage)s")
	
	if conditions:
		return "AND " + " AND ".join(conditions)
	else:
		return ""


def get_chart_data(data=None, filters=None):
	"""Prepare chart data for Weighted Amount grouped by Sales Person"""
	
	# If called from dashboard without parameters, get data ourselves
	if data is None:
		if filters is None:
			filters = {}
		data = get_data(filters)
	
	# Group data by sales person
	sales_person_data = {}
	
	for row in data:
		sales_person = row.get('sales_person') or 'Not Assigned'
		weighted_amount = row.get('weighted_amount', 0)
		
		# Extract numeric value from formatted currency
		if isinstance(weighted_amount, str):
			import re
			numeric_value = re.sub(r'[^\d.-]', '', str(weighted_amount))
			try:
				weighted_amount = float(numeric_value) if numeric_value else 0
			except ValueError:
				weighted_amount = 0
		
		if sales_person in sales_person_data:
			sales_person_data[sales_person] += weighted_amount
		else:
			sales_person_data[sales_person] = weighted_amount
	
	# Sort by weighted amount descending
	sorted_sales_persons = sorted(sales_person_data.items(), key=lambda x: x[1], reverse=True)
	
	# Prepare chart data
	labels = [sp[0] for sp in sorted_sales_persons]
	values = [sp[1] for sp in sorted_sales_persons]
	
	chart_data = {
		"data": {
			"labels": labels,
			"datasets": [{
				"name": "Weighted Amount",
				"values": values
			}]
		},
		"type": "bar",
		"colors": ["#5e64ff", "#ff5858", "#28a745", "#ffc107", "#17a2b8", "#6f42c1", "#fd7e14", "#20c997"]
	}
	
	return chart_data


# Whitelisted method for dashboard chart
@frappe.whitelist()
def get_deal_based_forecast_chart(filters=None):
	"""Whitelisted method for Deal Based Forecast chart"""
	if not filters:
		filters = {}
	
	data = get_data(filters)
	chart = get_chart_data(data)
	return chart
