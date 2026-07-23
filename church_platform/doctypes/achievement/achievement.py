"""
Achievement DocType - Member recognitions and milestones
"""

import frappe
from frappe import _


class Achievement(frappe.Model):
	"""Member achievements, recognitions, and milestones"""
	
	def validate(self):
		"""Validate achievement data"""
		# Verify member belongs to the church
		member_church = frappe.db.get_value("Member", self.member, "church")
		if member_church != self.church:
			frappe.throw(_("Member must belong to the selected church"))
	
	def on_update(self):
		"""Log achievement update"""
		member_name = frappe.db.get_value("Member", self.member, "first_name")
		frappe.msgprint(
			_("Achievement '{0}' awarded to {1}").format(self.title, member_name),
			indicator="green",
			alert=True
		)
