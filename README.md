# Odoo tutorials

## Results Achieved:
•	Successfully developed the “estate” module with full real estate management capabilities, including creating, editing, deleting, and viewing property details.
•	Ensured security compliance and smooth integration with other Odoo components.

  1.	**Architecture Overview**:
	•	Studied Odoo’s three-tier architecture: presentation layer, logic layer (Python), and data layer (PostgreSQL).
  2.	**Creating a New Application**:
	•	Initialized the “estate” module for real estate management, setting up the required directory structure and files.
	3.	**Basic Models and Fields**:
	•	Defined the estate.property model with fields such as name, description, expected_price, bedrooms, living_area, etc.
	4.	**Security and permission**:
	•	Configured user access rights using security/estate_security.xml and security/ir.model.access.csv to manage permissions for different user groups.
	5.	**Menu**:
	•	Created menus and actions in views/estate_menu.xml to allow users to navigate through module functionalities.
	6.	**Basic Views**:
	•	Designed list (tree), form, and search views in views/estate_property_views.xml for displaying and managing real estate data.
	7.	**Model Relationships**:
	•	Established relationships such as Many2one, One2many, and Many2many to link estate.property with models like res.users (sellers) and estate.property.type.
	8.	**Computed Fields and Onchange Methods**:
	•	Used computed fields to update values dynamically based on business logic and applied the @api.onchange decorator to respond to user input changes.
	9.	**Actions**:
	•	Created server actions to implement features like changing property states or sending notifications.
	10.	**Constraints**:
	•	Added SQL and Python constraints to ensure data integrity, such as preventing the sale price from being lower than the expected price.
	11.	**Additional Features**:
	•	Improved user interface with widgets, including integer sliders and status buttons.
	12.	**Inheritance**:
	•	Used Odoo’s inheritance system to extend or modify existing models and views without altering the original files.
	13.	**Integration with Other Modules**:
	•	Integrated the “estate” module with account to generate invoices when a property is sold.

