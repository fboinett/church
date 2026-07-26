"""
Sub Region DocType (Archdeaconry level)
"""

import frappe
from frappe.model.document import Document
from frappe import _


class SubRegion(Document):
	"""Church hierarchy: Archdeaconry/Sub-Region level"""
	
	def validate(self):
		"""Validate sub-region data"""
		# Ensure sub_region_code is uppercase
		if self.sub_region_code:
			self.sub_region_code = self.sub_region_code.upper()
		
		# Verify parent region exists
		if self.region and not frappe.db.exists("Region", self.region):
			frappe.throw(_("Region '{0}' does not exist").format(self.region))
	
	def on_update(self):
		"""Log sub-region update"""
		frappe.msgprint(
			_("Sub-Region '{0}' updated successfully").format(self.name),
			indicator="green",
			alert=True
		)
