import json

from models.invoice_model import InvoiceModel

class InvoiceController:
    def __init__(self):
        self.invoice_model = InvoiceModel()

    def create_invoice_scan(self):
            self.invoice_model.create_invoice()

    def update_invoice_scan(self,invoice):
            self.invoice_model.update_invoice(invoice)

    def return_invoice_code(self):
            return self.invoice_model.return_product_code()

    def delete_invoice_by_code(self,invoice_code):
           self.invoice_model.delete_invoice(invoice_code)

    def fetch_invoice(self):
            self.invoice_model.fetch_all_invoices()

    def get_all_invoice(self):
        return self.invoice_model.fetch_all_invoices()
    def get_invoice_by_day(self,day,month,year):
        return self.invoice_model.get_invoice_by_day(day,month,year)