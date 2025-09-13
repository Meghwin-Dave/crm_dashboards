# CRM Dashboards

A comprehensive CRM dashboard application for Frappe/ERPNext that provides powerful analytics and reporting capabilities for sales teams and management.

## 🚀 Features

### 📊 **Comprehensive Dashboard**
- **CRM Master Dashboard** with 12 interactive charts
- Real-time data visualization
- Responsive design with half-width chart layout
- Public access for team collaboration

### 📈 **Advanced Reports & Analytics**

#### **Project Management**
- **Project Tracker Report** - Complete project lifecycle tracking
  - 17 detailed columns including visit dates, project stages, stakeholders
  - 3 interactive charts: Funnel, Bar, and Timeline views
  - Smart stage assignment based on completion percentage
  - Visual formatting with color-coded stages and dates

#### **Customer Analysis**
- **Customer Profile Report** - Comprehensive customer insights
  - Sales projections and historical data
  - Customer segmentation and type analysis
  - 3 charts: Sales projections, customer distribution, and sales comparison

#### **Sales Forecasting**
- **Deal Based Forecast** - Weighted deal analysis by salesperson
- **Opportunity Based Forecast** - Opportunity-driven forecasting
- **Daily Sales Report (Weekly)** - Daily sales trend analysis
- **Monthly Sales Report (Salesperson-wise)** - Monthly performance tracking

#### **Performance Analytics**
- **Deal Loss Analysis** - Lost deal categorization and analysis
- **Sales Budget** - Budget vs actual performance comparison

### 🎯 **Key Capabilities**

#### **Smart Filtering**
- Sales Person filtering
- Project Type filtering (Commercial, Residential, Industrial, Infrastructure, Mixed Use)
- Stage-based filtering with automatic percentage mapping
- Date range filtering with intelligent defaults

#### **Visual Analytics**
- **6 Bar Charts** - For comparing values across categories
- **4 Line Charts** - For showing trends over time
- **2 Pie Charts** - For showing proportions and distributions
- **1 Funnel Chart** - For showing process flow and conversion rates

#### **Data Intelligence**
- Automatic stage assignment based on project completion
- Color-coded visual indicators for status and dates
- Currency formatting with emphasis
- Date-based color coding (overdue, upcoming, future)

## 📋 **Report Details**

### **Project Tracker Report**
**Columns (17):**
- 1st Date of Visit, Project Name, Location, Sales Person
- Project Type, Developer/Client, Architect, Contractor
- QS, Consultant, Stage of Project, Project Order Value
- Order Expected Date, Decision Maker, Last Visit Date
- Current Status, Next Action Plan

**Charts (3):**
- Projects by Stage (Funnel View)
- Project Order Value by Stage (Bar Chart)
- Visit Timeline (Line Chart)

**Filters (4):**
- Sales Person, Project Type, Stage of Project, Date Range

### **Customer Profile Report**
**Charts (3):**
- Sales Projection 2025 by Sales Person (Bar Chart)
- Customers by Type (Pie Chart)
- Sales 2024 vs Projection 2025 (Line Chart)

### **Sales & Forecasting Reports**
- **Deal Based Forecast** - Salesperson-wise weighted amounts
- **Daily Sales Report** - Weekly trend analysis
- **Monthly Sales Report** - Salesperson performance tracking
- **Opportunity Based Forecast** - Opportunity-driven insights
- **Deal Loss Analysis** - Lost deal categorization
- **Sales Budget** - Budget vs actual comparison

## 🛠 **Technical Implementation**

### **Architecture**
- Built on Frappe Framework
- Compatible with ERPNext v15.76.0+
- Uses Frappe v15.78.1+
- CRM module integration

### **Database Integration**
- Custom fields for Project doctype
- Optimized SQL queries with proper indexing
- Efficient data processing and formatting
- Graceful handling of missing data

### **Chart Technology**
- Frappe's built-in charting system
- Report-based chart generation
- Real-time data binding
- Interactive dashboard integration

## 📦 **Installation**

### **Prerequisites**
- Frappe Framework v15.78.1+
- ERPNext v15.76.0+
- CRM module v1.52.9+

### **Installation Steps**

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd frappe-bench
   ```

2. **Install the app:**
   ```bash
   bench get-app crm_dashboards
   bench install-app crm_dashboards
   ```

3. **Migrate the database:**
   ```bash
   bench --site [your-site] migrate
   ```

4. **Access the dashboard:**
   - Navigate to the CRM Master Dashboard in ERPNext
   - All charts will be automatically available

## 🎨 **Customization**

### **Adding Custom Fields**
The app includes custom fields for the Project doctype. To add more:

1. Update `fixtures/custom_field.json`
2. Run `bench --site [your-site] migrate`

### **Modifying Charts**
1. Edit the respective report Python files
2. Update chart data generation functions
3. Refresh the dashboard

### **Dashboard Layout**
- Modify `crm_dashboards_dashboard/crm_master_dashboard/crm_master_dashboard.json`
- Adjust chart widths and positions
- Add or remove charts as needed

## 📊 **Dashboard Charts**

| Chart Name | Type | Report Source | Description |
|------------|------|---------------|-------------|
| Projects by Stage Funnel | Funnel | Project Tracker | Project progression through sales pipeline |
| Project Order Value by Stage | Bar | Project Tracker | Total order value for each project stage |
| Visit Timeline Chart | Line | Project Tracker | Visit frequency over time |
| Sales Projection 2025 by Sales Person | Bar | Customer Profile | Sales targets by salesperson |
| Customers by Type | Pie | Customer Profile | Customer distribution analysis |
| Sales 2024 vs Projection 2025 | Line | Customer Profile | Actual vs projected sales comparison |
| Deal Based Forecast Chart | Bar | Deal Based Forecast | Weighted deal amounts by salesperson |
| Daily Sales Weekly Trend | Line | Daily Sales Report | Daily sales trend analysis |
| Deal Loss Analysis Chart | Pie | Deal Loss | Lost deal categorization |
| Sales Budget vs Actual | Bar | Sales Budget | Budget vs actual performance |
| Monthly Sales Salesperson Wise | Line | Monthly Sales Report | Monthly sales by salesperson |
| Opportunity Based Forecast Chart | Bar | Opportunity Based Forecast | Opportunity-driven forecasting |

## 🔧 **Configuration**

### **Default Settings**
- Charts are set to "Half" width for optimal viewing
- All charts are publicly accessible
- Default date range: Last 12 months
- Auto-refresh enabled

### **Filter Configuration**
- Sales Person: Link to Sales Person doctype
- Project Type: Dropdown with predefined options
- Stage of Project: Smart mapping to completion percentage
- Date Range: Flexible from/to date selection

## 🚀 **Usage**

### **Accessing Reports**
1. Navigate to **Reports** in ERPNext
2. Select **Crm Dashboards** module
3. Choose the desired report
4. Apply filters and view results

### **Dashboard Access**
1. Go to **Dashboard** in ERPNext
2. Select **CRM Master Dashboard**
3. View all charts in a unified interface
4. Interact with charts for detailed analysis

### **Data Management**
- Reports automatically pull data from ERPNext
- Real-time updates when data changes
- Historical data preservation
- Export capabilities for all reports

## 🤝 **Contributing**

### **Development Setup**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### **Code Structure**
```
crm_dashboards/
├── crm_dashboards/
│   ├── report/
│   │   ├── project_tracker/
│   │   ├── customer_profile/
│   │   ├── deal_based_forecast/
│   │   └── ...
│   ├── crm_dashboards_dashboard/
│   └── fixtures/
├── hooks.py
└── README.md
```

## 📝 **Changelog**

### **Version 0.0.1**
- Initial release
- 8 comprehensive reports
- 12 interactive dashboard charts
- Project tracking capabilities
- Customer analysis tools
- Sales forecasting features
- Performance analytics

## 📄 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 **Support**

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔮 **Roadmap**

### **Upcoming Features**
- Advanced filtering options
- Custom chart configurations
- Export capabilities
- Mobile-responsive improvements
- Additional report types
- Real-time notifications

---

**Built with ❤️ for the Frappe/ERPNext community**