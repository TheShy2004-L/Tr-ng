from datetime import datetime
from config1.config import *  # Giả sử DEFAULT_TIME là định dạng thời gian trong config1


class InvoiceDetail:
    def __init__(self, invoice_code, product_id_barcode, product_name, product_type, quantity, price, subtotal, customer_name):
        self.invoice_code = invoice_code
        self.product_name = product_name
        self.product_type = product_type
        self.quantity = quantity
        self.price = price
        self.subtotal = subtotal
        self.customer_name = customer_name
        self.product_id_barcode = product_id_barcode

    def __iter__(self):
        return dict({
            INVOICE_CODE: self.invoice_code,
            INVOICE_DETAIL_PRODUCT_NAME: self.product_name,
            INVOICE_DETAIL_PRODUCT_TYPE: self.product_type,
            INVOICE_DETAIL_QUANTITY: self.quantity,
            INVOICE_DETAIL_PRICE: self.price,
            INVOICE_DETAIL_SUBTOTAL: self.subtotal,
            INVOICE_DETAIL_CUSTOMER_NAME: self.customer_name,
            INVOICE_DETAIL_PRODUCT_ID_BARCODE: self.product_id_barcode
        })

    def __repr__(self):
        return (f"InvoiceDetail({self.invoice_code}, {self.product_id_barcode}, {self.product_name}, "
                f"{self.product_type}, {self.quantity} items, {self.price} each, "
                f"Subtotal: {self.subtotal}, Customer: {self.customer_name}")




