# Copyright (c) 2025, Meghwin Dave and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, getdate


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	chart = get_chart_data(data, filters)
	
	return columns, data, None, chart


def get_columns():
	return [
		{
			"fieldname": "sno",
			"label": _("SNO"),
			"fieldtype": "Int",
			"width": 50
		},
		{
			"fieldname": "sales_person",
			"label": _("Sales Person"),
			"fieldtype": "Link",
			"options": "Sales Person",
			"width": 150
		},
		{
			"fieldname": "customer_name",
			"label": _("Customer Name"),
			"fieldtype": "Link",
			"options": "Customer",
			"width": 200
		},
		{
			"fieldname": "location",
			"label": _("Location"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "customer_segment",
			"label": _("Customer Segment"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "business_started_year",
			"label": _("Business Started Year"),
			"fieldtype": "Int",
			"width": 120
		},
		{
			"fieldname": "sales_2024",
			"label": _("Sales in 2024"),
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"fieldname": "sales_projection_2025",
			"label": _("Sales Projection for 2025"),
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"fieldname": "customer_type",
			"label": _("Customer Type"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "company_registered",
			"label": _("Company Registered"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "taste_preference",
			"label": _("Taste Preference"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "preferred_paint_company",
			"label": _("Preferred Paint Company"),
			"fieldtype": "Data",
			"width": 180
		},
		{
			"fieldname": "projects_in_hand",
			"label": _("Projects in Hand"),
			"fieldtype": "Int",
			"width": 120
		},
		{
			"fieldname": "ongoing_projects",
			"label": _("Ongoing Projects"),
			"fieldtype": "Int",
			"width": 120
		},
		{
			"fieldname": "area_of_specialization",
			"label": _("Area of Specialization"),
			"fieldtype": "Data",
			"width": 180
		},
		{
			"fieldname": "other_business_with_us",
			"label": _("Other Business With Us"),
			"fieldtype": "Data",
			"width": 180
		},
		{
			"fieldname": "experience_rating",
			"label": _("Experience Rating"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "suggestions_for_improvement",
			"label": _("Suggestions for Improvement"),
			"fieldtype": "Text",
			"width": 200
		}
	]


def get_data(filters):
	conditions = get_conditions(filters)
	
	query = f"""
		SELECT 
			c.name as customer_name,
			c.customer_name as customer_display_name,
			c.customer_type,
			c.disabled,
			c.territory as location,
			c.market_segment as customer_segment,
			sp.name as sales_person,
			COALESCE(c.business_started_year, 0) as business_started_year,
			COALESCE(c.sales_2024, 0) as sales_2024,
			COALESCE(c.sales_projection_2025, 0) as sales_projection_2025,
			COALESCE(c.company_registered, '') as company_registered,
			COALESCE(c.taste_preference, '') as taste_preference,
			COALESCE(c.preferred_paint_company, '') as preferred_paint_company,
			COALESCE(c.projects_in_hand, 0) as projects_in_hand,
			COALESCE(c.ongoing_projects, 0) as ongoing_projects,
			COALESCE(c.area_of_specialization, '') as area_of_specialization,
			COALESCE(c.other_business_with_us, '') as other_business_with_us,
			COALESCE(c.experience_rating, '') as experience_rating,
			COALESCE(c.suggestions_for_improvement, '') as suggestions_for_improvement
		FROM `tabCustomer` c
		LEFT JOIN `tabSales Team` st ON c.name = st.parent
		LEFT JOIN `tabSales Person` sp ON st.sales_person = sp.name
		WHERE c.docstatus = 0
		{conditions}
		ORDER BY c.customer_name
	"""
	
	data = frappe.db.sql(query, as_dict=True)
	
	# Add serial numbers and format data
	for i, row in enumerate(data, 1):
		row.sno = i
		row.status = "Inactive" if row.disabled else "Active"
		row.sales_2024 = flt(row.sales_2024)
		row.sales_projection_2025 = flt(row.sales_projection_2025)
		row.business_started_year = int(row.business_started_year) if row.business_started_year else 0
		row.projects_in_hand = int(row.projects_in_hand) if row.projects_in_hand else 0
		row.ongoing_projects = int(row.ongoing_projects) if row.ongoing_projects else 0
	
	return data


def get_conditions(filters):
	conditions = []
	
	if filters.get("sales_person"):
		conditions.append("sp.name = %(sales_person)s")
	
	if filters.get("customer_segment"):
		conditions.append("c.market_segment = %(customer_segment)s")
	
	if filters.get("customer_type"):
		conditions.append("c.customer_type = %(customer_type)s")
	
	if filters.get("status"):
		if filters.get("status") == "Active":
			conditions.append("c.disabled = 0")
		elif filters.get("status") == "Inactive":
			conditions.append("c.disabled = 1")
	
	if conditions:
		return "AND " + " AND ".join(conditions)
	
	return ""


def get_chart_data(data, filters):
	charts = []
	
	# Chart 1: Bar chart of Sales Projection 2025 grouped by Sales Person
	chart1 = get_sales_projection_chart(data)
	if chart1:
		charts.append(chart1)
	
	# Chart 2: Pie chart of Customers by Type
	chart2 = get_customer_type_chart(data)
	if chart2:
		charts.append(chart2)
	
	# Chart 3: Line chart comparing Sales 2024 vs Projection 2025
	chart3 = get_sales_comparison_chart(data)
	if chart3:
		charts.append(chart3)
	
	return charts


def get_sales_projection_chart(data):
	"""Bar chart of Sales Projection 2025 grouped by Sales Person"""
	sales_person_data = {}
	
	for row in data:
		sales_person = row.sales_person or "No Sales Person"
		if sales_person not in sales_person_data:
			sales_person_data[sales_person] = 0
		sales_person_data[sales_person] += flt(row.sales_projection_2025)
	
	if not sales_person_data:
		return None
	
	return {
		"data": {
			"labels": list(sales_person_data.keys()),
			"datasets": [{
				"name": "Sales Projection 2025",
				"values": list(sales_person_data.values())
			}]
		},
		"type": "bar",
		"title": "Sales Projection 2025 by Sales Person"
	}


def get_customer_type_chart(data):
	"""Pie chart of Customers by Type"""
	customer_type_data = {}
	
	for row in data:
		customer_type = row.customer_type or "Unknown"
		if customer_type not in customer_type_data:
			customer_type_data[customer_type] = 0
		customer_type_data[customer_type] += 1
	
	if not customer_type_data:
		return None
	
	return {
		"data": {
			"labels": list(customer_type_data.keys()),
			"datasets": [{
				"name": "Customer Count",
				"values": list(customer_type_data.values())
			}]
		},
		"type": "pie",
		"title": "Customers by Type"
	}


def get_sales_comparison_chart(data):
	"""Line chart comparing Sales 2024 vs Projection 2025"""
	# Group by customer for comparison
	customer_data = {}
	
	for row in data:
		customer = row.customer_display_name
		if customer not in customer_data:
			customer_data[customer] = {
				"sales_2024": 0,
				"projection_2025": 0
			}
		customer_data[customer]["sales_2024"] += flt(row.sales_2024)
		customer_data[customer]["projection_2025"] += flt(row.sales_projection_2025)
	
	if not customer_data:
		return None
	
	# Take top 10 customers for better visualization
	sorted_customers = sorted(customer_data.items(), 
		key=lambda x: x[1]["sales_2024"] + x[1]["projection_2025"], reverse=True)[:10]
	
	labels = [item[0] for item in sorted_customers]
	sales_2024_values = [item[1]["sales_2024"] for item in sorted_customers]
	projection_2025_values = [item[1]["projection_2025"] for item in sorted_customers]
	
	return {
		"data": {
			"labels": labels,
			"datasets": [
				{
					"name": "Sales 2024",
					"values": sales_2024_values
				},
				{
					"name": "Projection 2025",
					"values": projection_2025_values
				}
			]
		},
		"type": "line",
		"title": "Sales 2024 vs Projection 2025 (Top 10 Customers)"
	}
