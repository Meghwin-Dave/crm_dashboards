# Copyright (c) 2025, Meghwin Dave and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate, add_months, get_first_day, get_last_day, flt
from erpnext.accounts.utils import get_fiscal_year


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	chart = get_chart_data(data)
	
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
			"fieldname": "target_sales",
			"label": _("Target Sales"),
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
			"fieldname": "shortfall_excess",
			"label": _("Shortfall/Excess"),
			"fieldtype": "Currency",
			"width": 150
		}
	]


def get_data(filters):
	# Get fiscal year details
	fiscal_year = filters.get("fiscal_year")
	if not fiscal_year:
		fiscal_year = get_current_fiscal_year()
	
	fy_details = frappe.db.get_value("Fiscal Year", fiscal_year, 
		["year_start_date", "year_end_date"], as_dict=True)
	
	if not fy_details:
		return []
	
	# Generate month-wise data
	data = []
	month_names = ["January", "February", "March", "April", "May", "June",
				   "July", "August", "September", "October", "November", "December"]
	
	for i in range(12):
		month_start = add_months(fy_details.year_start_date, i)
		month_end = get_last_day(month_start)
		
		# Get target sales for the month
		target_sales = get_monthly_target(fiscal_year, i + 1, filters)
		
		# Get actual sales for the month
		actual_sales = get_actual_sales(month_start, month_end, filters)
		
		# Calculate shortfall/excess
		shortfall_excess = target_sales - actual_sales
		
		data.append({
			"month": month_names[i],
			"target_sales": target_sales,
			"actual_sales": actual_sales,
			"shortfall_excess": shortfall_excess
		})
	
	return data


def get_current_fiscal_year():
	"""Get current fiscal year"""
	try:
		fy = get_fiscal_year()
		return fy[0] if fy else None
	except:
		# Fallback: get the most recent fiscal year
		return frappe.db.get_value("Fiscal Year", 
			{"disabled": 0}, "name", order_by="year_start_date desc")


def get_monthly_target(fiscal_year, month_num, filters):
	"""Get monthly target based on sales person and territory filters"""
	
	# Get all sales persons based on filters
	sales_persons = get_sales_persons(filters)
	
	if not sales_persons:
		return 0
	
	total_target = 0
	month_names = ["January", "February", "March", "April", "May", "June",
				   "July", "August", "September", "October", "November", "December"]
	
	for sp in sales_persons:
		# Get target details for the sales person
		target_details = frappe.db.sql("""
			SELECT td.target_amount, td.distribution_id
			FROM `tabTarget Detail` td
			WHERE td.parent = %s AND td.fiscal_year = %s
		""", (sp.name, fiscal_year), as_dict=True)
		
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


def get_sales_persons(filters):
	"""Get sales persons based on filters"""
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


def get_actual_sales(from_date, to_date, filters):
	"""Get actual sales from Sales Invoice for the given period"""
	
	conditions = [
		"si.docstatus = 1",
		"si.posting_date >= %(from_date)s",
		"si.posting_date <= %(to_date)s"
	]
	
	# Add sales person filter if specified
	if filters.get("sales_person"):
		conditions.append("st.sales_person = %(sales_person)s")
		join_clause = "INNER JOIN `tabSales Team` st ON si.name = st.parent"
	else:
		join_clause = ""
	
	# Add territory filter if specified
	if filters.get("territory"):
		conditions.append("si.territory = %(territory)s")
	
	where_clause = " AND ".join(conditions)
	
	if join_clause:
		query = f"""
			SELECT SUM(st.allocated_amount) as total_sales
			FROM `tabSales Invoice` si
			{join_clause}
			WHERE {where_clause}
		"""
	else:
		query = f"""
			SELECT SUM(si.net_total) as total_sales
			FROM `tabSales Invoice` si
			WHERE {where_clause}
		"""
	
	result = frappe.db.sql(query, {
		"from_date": from_date,
		"to_date": to_date,
		"sales_person": filters.get("sales_person"),
		"territory": filters.get("territory")
	}, as_dict=True)
	
	return flt(result[0].total_sales) if result else 0


def get_chart_data(data=None, filters=None):
	"""Prepare chart data for Actual vs Target Sales by Month"""
	
	# If called from dashboard without parameters, get data ourselves
	if data is None:
		if filters is None:
			filters = {}
		data = get_data(filters)
	
	months = []
	actual_sales = []
	target_sales = []
	
	for row in data:
		months.append(row["month"])
		actual_sales.append(row["actual_sales"])
		target_sales.append(row["target_sales"])
	
	chart_data = {
		"data": {
			"labels": months,
			"datasets": [
				{
					"name": "Actual Sales",
					"values": actual_sales
				},
				{
					"name": "Target Sales",
					"values": target_sales
				}
			]
		},
		"type": "bar",
		"colors": ["#5e64ff", "#ff5858"]
	}
	
	return chart_data


# Whitelisted method for dashboard chart
@frappe.whitelist()
def get_sales_budget_vs_actual(filters=None):
	"""Whitelisted method for Sales Budget vs Actual chart"""
	if not filters:
		filters = {}
	
	data = get_data(filters)
	chart = get_chart_data(data)
	return chart
