from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in crm_dashboards/__init__.py
from crm_dashboards import __version__ as version

setup(
	name="crm_dashboards",
	version=version,
	description="Comprehensive CRM dashboard application for Frappe/ERPNext",
	author="Meghwin Dave",
	author_email="meghwindave04@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
