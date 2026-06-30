import frappe
from frappe.model.document import Document
from frappe.utils import getdate

class TaskAssignment(Document):

    def validate(self):
        self.update_extension_count()
        self.calculate_score()
        self.update_status()
        self.send_extension_email()

    def update_extension_count(self):
  

        if self.is_new():
            self.extension_count = 0
            return

        old_doc = self.get_doc_before_save()

        if not old_doc:
            return

        if old_doc.revised_due_date != self.revised_due_date:

            if not old_doc.revised_due_date:

                if (
                    self.revised_due_date
                    and self.original_due_date
                    and self.revised_due_date > self.original_due_date
                ):
                    self.extension_count = 1
                else:
                    self.extension_count = old_doc.extension_count or 0

            else:

                if (
                    self.revised_due_date
                    and getdate(self.revised_due_date) > getdate(old_doc.revised_due_date)
                ):
                    self.extension_count = (old_doc.extension_count or 0) + 1
                else:
                    self.extension_count = old_doc.extension_count or 0

        else:
            self.extension_count = old_doc.extension_count or 0

    def calculate_score(self):

        score_map = {
            0: 100,
            1: 75,
            2: 50,
            3: 25
        }

        self.score = score_map.get(self.extension_count or 0, 0)

    def update_status(self):

        if self.status == "Completed":
            return

        if (self.extension_count or 0) >= 4:
            self.status = "Failed"

        elif not self.status:
            self.status = "Open"
		
              		
    def send_extension_email(self):
        if (self.extension_count or 0) <= 2:
            return

        if not self.assigned_to:
            return

        user_email = frappe.db.get_value("User", self.assigned_to, "email")

        if not user_email:
            return

        flag = f"email_sent_for_{self.name}_{self.extension_count}"

        if frappe.cache().get_value(flag):
            return

        frappe.sendmail(
            recipients=[user_email],
            subject=f"Task '{self.task_name}' Extended {self.extension_count} Times",
            message=f"""
                <p>Hello,</p>

                <p>Your task <b>{self.task_name}</b> has been extended 
                <b>{self.extension_count}</b> times.</p>

                <p>Please complete it as soon as possible.</p>

                <br>
                <p>Thanks,<br>Task Tracker System</p>
            """
        )

        frappe.cache().set_value(flag, True)