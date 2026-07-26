"""
Church DocType (Parish level)
"""

import frappe
from frappe.model.document import Document
from frappe import _


class Church(Document):
	"""Church hierarchy: Parish/Church level"""
	
	def validate(self):
		"""Validate church data"""
		# Ensure church_code is uppercase
		if self.church_code:
			self.church_code = self.church_code.upper()
		
		# Verify parent sub-region exists
		if self.sub_region and not frappe.db.exists("Sub Region", self.sub_region):
			frappe.throw(_("Sub-Region '{0}' does not exist").format(self.sub_region))
	
	def on_update(self):
		"""Log church update"""
		frappe.msgprint(
			_("Church '{0}' updated successfully").format(self.name),
			indicator="green",
			alert=True
		)
	
	@property
	def region(self):
		"""Get parent region through sub-region"""
		if self.sub_region:
			return frappe.db.get_value("Sub Region", self.sub_region, "region")
		return None
