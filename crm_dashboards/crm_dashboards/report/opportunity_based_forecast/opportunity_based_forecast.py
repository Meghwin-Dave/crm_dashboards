# Copyright (c) 2025, Meghwin Dave and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate, add_days, today


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
			opp.sales_stage,
			opp.opportunity_amount as amount,
			opp.probability,
			(opp.opportunity_amount * opp.probability / 100) as weighted_amount,
			opp.expected_closing as expected_closing_date,
			opp.currency
		FROM `tabOpportunity` opp
		WHERE opp.docstatus != 2
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
	
	if filters.get("territory"):
		conditions.append("opp.territory = %(territory)s")
	
	if conditions:
		return " AND " + " AND ".join(conditions)
	else:
		return ""


def get_chart_data(data):
	# Group data by sales stage for the chart
	sales_stage_data = {}
	
	for row in data:
		stage = row.get('sales_stage') or 'Not Set'
		weighted_amount = row.get('weighted_amount', 0)
		
		# Extract numeric value from formatted currency
		if isinstance(weighted_amount, str):
			# Remove currency symbols and formatting
			import re
			numeric_value = re.sub(r'[^\d.-]', '', str(weighted_amount))
			try:
				weighted_amount = float(numeric_value) if numeric_value else 0
			except ValueError:
				weighted_amount = 0
		
		if stage in sales_stage_data:
			sales_stage_data[stage] += weighted_amount
		else:
			sales_stage_data[stage] = weighted_amount
	
	# Prepare chart data
	chart_data = {
		"data": {
			"labels": list(sales_stage_data.keys()),
			"datasets": [{
				"name": "Weighted Amount",
				"values": list(sales_stage_data.values())
			}]
		},
		"type": "bar",
		"colors": ["#5e64ff", "#ff5858", "#28a745", "#ffc107", "#17a2b8", "#6f42c1", "#fd7e14", "#20c997"]
	}
	
	return chart_data
