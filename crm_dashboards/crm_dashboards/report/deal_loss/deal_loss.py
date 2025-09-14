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
			"fieldname": "customer",
			"label": _("Customer"),
			"fieldtype": "Data",
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
			"fieldname": "lost_reason",
			"label": _("Lost Reason"),
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "lost_amount",
			"label": _("Lost Amount"),
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"fieldname": "closing_date",
			"label": _("Closing Date"),
			"fieldtype": "Date",
			"width": 150
		}
	]


def get_data(filters):
	conditions = get_conditions(filters)
	
	query = """
		SELECT 
			opp.name as opportunity_name,
			opp.customer_name as customer,
			opp.opportunity_owner as sales_person,
			GROUP_CONCAT(DISTINCT olr.lost_reason SEPARATOR ', ') as lost_reason,
			opp.opportunity_amount as lost_amount,
			opp.modified as closing_date,
			opp.currency
		FROM `tabOpportunity` opp
		LEFT JOIN `tabOpportunity Lost Reason Detail` olr ON opp.name = olr.parent
		WHERE opp.status = 'Lost'
		AND opp.docstatus != 2
		{conditions}
		GROUP BY opp.name
		ORDER BY opp.modified DESC
	""".format(conditions=conditions)
	
	data = frappe.db.sql(query, filters, as_dict=True)
	
	# Format currency fields
	for row in data:
		if row.get('lost_amount'):
			row['lost_amount'] = frappe.format_value(row['lost_amount'], {
				'fieldtype': 'Currency',
				'currency': row.get('currency') or frappe.get_default('currency')
			})
	
	return data


def get_conditions(filters):
	conditions = []
	
	if filters.get("from_date"):
		conditions.append("DATE(opp.modified) >= %(from_date)s")
	
	if filters.get("to_date"):
		conditions.append("DATE(opp.modified) <= %(to_date)s")
	
	if filters.get("sales_person"):
		conditions.append("opp.opportunity_owner = %(sales_person)s")
	
	if filters.get("lost_reason"):
		conditions.append("olr.lost_reason = %(lost_reason)s")
	
	if conditions:
		return "AND " + " AND ".join(conditions)
	else:
		return ""


def get_chart_data(data=None, filters=None):
	"""Prepare chart data for Count of Lost Deals by Reason"""
	
	# If called from dashboard without parameters, get data ourselves
	if data is None:
		if filters is None:
			filters = {}
		data = get_data(filters)
	
	# Count lost deals by reason
	reason_counts = {}
	
	for row in data:
		lost_reasons = row.get('lost_reason', 'Not Specified')
		if lost_reasons and lost_reasons != 'Not Specified':
			# Split multiple reasons and count each
			reasons = [reason.strip() for reason in lost_reasons.split(',')]
			for reason in reasons:
				if reason:
					reason_counts[reason] = reason_counts.get(reason, 0) + 1
		else:
			reason_counts['Not Specified'] = reason_counts.get('Not Specified', 0) + 1
	
	# Prepare chart data
	labels = list(reason_counts.keys())
	values = list(reason_counts.values())
	
	chart_data = {
		"data": {
			"labels": labels,
			"datasets": [{
				"name": "Lost Deals",
				"values": values
			}]
		},
		"type": "pie",
		"colors": ["#ff5858", "#ffc107", "#28a745", "#17a2b8", "#6f42c1", "#fd7e14", "#20c997", "#dc3545"]
	}
	
	return chart_data


# Whitelisted method for dashboard chart
@frappe.whitelist()
def get_deal_loss_analysis_chart(filters=None):
	"""Whitelisted method for Deal Loss Analysis chart"""
	if not filters:
		filters = {}
	
	data = get_data(filters)
	chart = get_chart_data(data)
	return chart
