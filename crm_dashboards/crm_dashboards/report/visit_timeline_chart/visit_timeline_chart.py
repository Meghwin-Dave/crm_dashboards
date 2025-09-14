# Copyright (c) 2025, Meghwin Dave and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, getdate, today, add_days


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	chart = get_chart_data(data, filters)
	return columns, data, None, chart


def get_columns():
	return [
		{
			"fieldname": "month",
			"label": _("Month"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "first_visits",
			"label": _("First Visits"),
			"fieldtype": "Int",
			"width": 100
		},
		{
			"fieldname": "last_visits",
			"label": _("Last Visits"),
			"fieldtype": "Int",
			"width": 100
		}
	]


def get_data(filters):
	# Check if there are any projects first
	project_count = frappe.db.sql("SELECT COUNT(*) as count FROM `tabProject` WHERE docstatus = 0", as_dict=True)
	
	if project_count[0].count == 0:
		return []
	
	# Build conditions using string formatting for now
	conditions = get_conditions_simple(filters)
	
	query = f"""
		SELECT 
			p.name as project_name,
			p.project_name as project_display_name,
			p.status as current_status,
			p.expected_start_date as first_visit_date,
			p.expected_end_date as order_expected_date,
			p.project_type,
			COALESCE(c.territory, '') as location,
			p.notes as next_action_plan,
			p.percent_complete,
			c.customer_name as developer_client,
			'' as sales_person,
			'' as architect,
			'' as contractor,
			'' as qs,
			'' as consultant,
			'' as stage_of_project,
			0 as project_order_value,
			'' as decision_maker,
			p.expected_start_date as last_visit_date
		FROM `tabProject` p
		LEFT JOIN `tabCustomer` c ON p.customer = c.name
		WHERE p.docstatus = 0
		{conditions}
		ORDER BY p.expected_start_date DESC, p.name
	"""
	
	data = frappe.db.sql(query, as_dict=True)
	
	# Add serial numbers and format data
	for i, row in enumerate(data, 1):
		row.sno = i
		row.project_order_value = flt(row.project_order_value)
		row.percent_complete = flt(row.percent_complete)
		
		# Set stage based on percent complete
		if row.percent_complete == 0:
			row.stage_of_project = "Initial Discussion"
		elif row.percent_complete < 25:
			row.stage_of_project = "Proposal Sent"
		elif row.percent_complete < 50:
			row.stage_of_project = "Negotiation"
		elif row.percent_complete < 75:
			row.stage_of_project = "Final Discussion"
		elif row.percent_complete < 100:
			row.stage_of_project = "Order Pending"
		else:
			row.stage_of_project = "Order Received"
		
		# Set default values for custom fields that don't exist yet
		row.architect = row.architect or ""
		row.contractor = row.contractor or ""
		row.qs = row.qs or ""
		row.consultant = row.consultant or ""
		row.decision_maker = row.decision_maker or ""
		row.location = row.location or ""
		row.next_action_plan = row.next_action_plan or ""
	
	return data


def get_conditions_simple(filters):
	conditions = []
	
	if not filters:
		filters = {}
	
	if filters.get("project_type"):
		conditions.append(f"p.project_type = '{filters.get('project_type')}'")
	
	if filters.get("stage_of_project"):
		# Since custom field doesn't exist yet, we'll filter based on percent_complete
		stage_mapping = {
			"Initial Discussion": (0, 0),
			"Proposal Sent": (1, 24),
			"Negotiation": (25, 49),
			"Final Discussion": (50, 74),
			"Order Pending": (75, 99),
			"Order Received": (100, 100)
		}
		if filters.get("stage_of_project") in stage_mapping:
			min_pct, max_pct = stage_mapping[filters.get("stage_of_project")]
			conditions.append(f"p.percent_complete BETWEEN {min_pct} AND {max_pct}")
	
	# Handle date filters more carefully
	if filters.get("from_date") and filters.get("to_date"):
		conditions.append(f"p.expected_start_date BETWEEN '{filters.get('from_date')}' AND '{filters.get('to_date')}'")
	elif filters.get("from_date"):
		conditions.append(f"p.expected_start_date >= '{filters.get('from_date')}'")
	elif filters.get("to_date"):
		conditions.append(f"p.expected_start_date <= '{filters.get('to_date')}'")
	
	if conditions:
		return "AND " + " AND ".join(conditions)
	
	return ""


def get_chart_data(data, filters):
	"""Timeline chart of visits (1st Visit vs Last Visit)"""
	# Group by month for better visualization
	monthly_data = {}
	
	for row in data:
		first_visit = getdate(row.first_visit_date)
		last_visit = getdate(row.last_visit_date)
		
		# Create month key
		first_month = first_visit.strftime("%Y-%m") if first_visit else None
		last_month = last_visit.strftime("%Y-%m") if last_visit else None
		
		if first_month:
			if first_month not in monthly_data:
				monthly_data[first_month] = {"first_visits": 0, "last_visits": 0}
			monthly_data[first_month]["first_visits"] += 1
		
		if last_month:
			if last_month not in monthly_data:
				monthly_data[last_month] = {"first_visits": 0, "last_visits": 0}
			monthly_data[last_month]["last_visits"] += 1
	
	if not monthly_data:
		return None
	
	# Sort by month
	sorted_months = sorted(monthly_data.keys())
	
	first_visit_values = [monthly_data[month]["first_visits"] for month in sorted_months]
	last_visit_values = [monthly_data[month]["last_visits"] for month in sorted_months]
	
	return {
		"data": {
			"labels": sorted_months,
			"datasets": [
				{
					"name": "First Visits",
					"values": first_visit_values
				},
				{
					"name": "Last Visits",
					"values": last_visit_values
				}
			]
		},
		"type": "line"
	}
