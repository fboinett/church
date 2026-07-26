"""
Blog Comment DocType - Moderated comments on blog posts
"""

import frappe
from frappe.model.document import Document
from frappe import _
from datetime import datetime


class BlogComment(Document):
	"""Comments on blog posts with moderation workflow"""
	
	def validate(self):
		"""Validate blog comment data"""
		# Set submitted_date to now if not provided
		if not self.submitted_date:
			self.submitted_date = datetime.now()
		
		# Default status to Pending
		if not self.status:
			self.status = "Pending"
	
	def on_update(self):
		"""Log comment update and send notifications"""
		if self.status == "Approved":
			# Send notification to blog subscribers (future feature)
			frappe.msgprint(
				_("Comment approved and is now visible"),
				indicator="green",
				alert=True
			)
		elif self.status == "Rejected":
			frappe.msgprint(
				_("Comment rejected"),
				indicator="red",
				alert=True
			)
	
	def approve_comment(self, approved_by):
		"""Approve a pending comment"""
		if self.status != "Pending":
			frappe.throw(_("Only pending comments can be approved"))
		
		self.status = "Approved"
		self.approved_by = approved_by
		self.approved_date = datetime.now()
		self.save()
		
		frappe.msgprint(_("Comment approved successfully"), indicator="green")
	
	def reject_comment(self, approved_by, notes=""):
		"""Reject a pending comment"""
		if self.status != "Pending":
			frappe.throw(_("Only pending comments can be rejected"))
		
		self.status = "Rejected"
		self.approved_by = approved_by
		self.approved_date = datetime.now()
		self.approval_notes = notes
		self.save()
		
		frappe.msgprint(_("Comment rejected"), indicator="red")
