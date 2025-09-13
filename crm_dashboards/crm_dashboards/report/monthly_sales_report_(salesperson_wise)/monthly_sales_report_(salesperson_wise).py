# Copyright (c) 2025, Meghwin Dave and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate, add_months, get_first_day, get_last_day, flt


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	chart = get_chart_data(data)
	
	return columns, data, None, chart


def get_columns():
	return [
		{
			"fieldname": "sales_person",
			"label": _("Sales Person"),
			"fieldtype": "Link",
			"options": "Sales Person",
			"width": 200
		},
		{
			"fieldname": "target_value",
			"label": _("Target Value"),
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"fieldname": "actual_sales",
			"label": _("Actual Sales"),
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"fieldname": "achievement_percentage",
			"label": _("Achievement %"),
			"fieldtype": "Percent",
			"width": 120
		}
	]


def get_data(filters):
	# Get date range for the selected month
	month = filters.get("month")
	year = getdate(month).year
	month_num = getdate(month).month
	
	from_date = get_first_day(month)
	to_date = get_last_day(month)
	
	# Get sales persons based on filters
	sales_persons = get_sales_persons(filters)
	
	data = []
	
	for sp in sales_persons:
		# Get target value for the month
		target_value = get_monthly_target(sp.name, month_num, year)
		
		# Get actual sales for the month
		actual_sales = get_actual_sales(sp.name, from_date, to_date, filters)
		
		# Calculate achievement percentage
		achievement_percentage = 0
		if target_value > 0:
			achievement_percentage = (actual_sales / target_value) * 100
		
		data.append({
			"sales_person": sp.name,
			"target_value": target_value,
			"actual_sales": actual_sales,
			"achievement_percentage": achievement_percentage
		})
	
	# Sort by actual sales descending
	data.sort(key=lambda x: x["actual_sales"], reverse=True)
	
	return data


def get_sales_persons(filters):
	conditions = ["sp.enabled = 1"]
	
	if filters.get("sales_person"):
		conditions.append("sp.name = %(sales_person)s")
	
	if filters.get("territory"):
		conditions.append("sp.territory = %(territory)s")
	
	where_clause = "WHERE " + " AND ".join(conditions)
	
	query = f"""
		SELECT DISTINCT sp.name, sp.sales_person_name
		FROM `tabSales Person` sp
		{where_clause}
		ORDER BY sp.sales_person_name
	"""
	
	return frappe.db.sql(query, filters, as_dict=True)


def get_monthly_target(sales_person, month_num, year):
	"""Get monthly target for a sales person based on their target allocation"""
	
	# Get fiscal year for the given year
	fiscal_year = frappe.db.get_value("Fiscal Year", {"year": year}, "name")
	if not fiscal_year:
		return 0
	
	# Get target details for the sales person
	target_details = frappe.db.sql("""
		SELECT td.target_amount, td.distribution_id
		FROM `tabTarget Detail` td
		WHERE td.parent = %s AND td.fiscal_year = %s
	""", (sales_person, fiscal_year), as_dict=True)
	
	if not target_details:
		return 0
	
	total_target = 0
	month_names = ["January", "February", "March", "April", "May", "June",
				   "July", "August", "September", "October", "November", "December"]
	
	for target in target_details:
		target_amount = target.target_amount or 0
		distribution_id = target.distribution_id
		
		if distribution_id:
			# Get monthly distribution percentage
			month_percentage = frappe.db.get_value(
				"Monthly Distribution Percentage",
				{"parent": distribution_id, "month": month_names[month_num - 1]},
				"percentage_allocation"
			) or 0
			
			monthly_target = target_amount * (month_percentage / 100)
		else:
			# If no distribution, divide annual target by 12
			monthly_target = target_amount / 12
		
		total_target += monthly_target
	
	return total_target


def get_actual_sales(sales_person, from_date, to_date, filters):
	"""Get actual sales for a sales person from Sales Invoice"""
	
	conditions = [
		"si.docstatus = 1",
		"si.posting_date >= %(from_date)s",
		"si.posting_date <= %(to_date)s",
		"st.sales_person = %(sales_person)s"
	]
	
	if filters.get("territory"):
		conditions.append("si.territory = %(territory)s")
	
	where_clause = " AND ".join(conditions)
	
	query = f"""
		SELECT SUM(st.allocated_amount) as total_sales
		FROM `tabSales Invoice` si
		INNER JOIN `tabSales Team` st ON si.name = st.parent
		WHERE {where_clause}
	"""
	
	result = frappe.db.sql(query, {
		"from_date": from_date,
		"to_date": to_date,
		"sales_person": sales_person,
		"territory": filters.get("territory")
	}, as_dict=True)
	
	return flt(result[0].total_sales) if result else 0


def get_chart_data(data):
	"""Prepare chart data for Actual Sales vs Target Value"""
	
	sales_persons = []
	actual_sales = []
	target_values = []
	
	for row in data:
		sales_persons.append(row["sales_person"])
		actual_sales.append(row["actual_sales"])
		target_values.append(row["target_value"])
	
	chart_data = {
		"data": {
			"labels": sales_persons,
			"datasets": [
				{
					"name": "Actual Sales",
					"values": actual_sales
				},
				{
					"name": "Target Value",
					"values": target_values
				}
			]
		},
		"type": "line",
		"colors": ["#5e64ff", "#ff5858"]
	}
	
	return chart_data
