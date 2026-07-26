"""
Member DocType - Church members with portal access
"""

import frappe
from frappe.model.document import Document
from frappe import _
from datetime import date


class Member(Document):
	"""Church members with portal access"""
	
	def validate(self):
		"""Validate member data"""
		# Set email from user if not already set
		if self.user and not self.email:
			user_email = frappe.db.get_value("User", self.user, "email")
			if user_email:
				self.email = user_email
		
		# Set join_date to today if not provided
		if not self.join_date:
			self.join_date = date.today()
	
	def on_update(self):
		"""Log member update"""
		frappe.msgprint(
			_("Member '{0}' updated successfully").format(self.first_name),
			indicator="green",
			alert=True
		)
