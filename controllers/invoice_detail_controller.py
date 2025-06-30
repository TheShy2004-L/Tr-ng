from Entity.InvoiceDetail import InvoiceDetail
from models.invoice_detail_model import  InvoiceDetailModel


class InvoiceDetailController:
    def __init__(self):
        """Khởi tạo Controller với đường dẫn database."""
        self.dao = InvoiceDetailModel()

    def add_invoice_detail(self, invoice_code, product_name, product_type, quantity, price, subtotal, customer_name, product_id_barcode):
        """Thêm một hóa đơn chi tiết mới."""
        invoice_detail = InvoiceDetail(
            invoice_code, product_name,
            product_type, quantity, price, subtotal, customer_name, product_id_barcode
        )
        new_id = self.dao.create_invoice_detail(invoice_detail)
        return f"Thêm thành công với ID: {new_id}" if new_id else "Thêm thất bại."

    def update_invoice_detail(self, invoice_code, product_id_barcode, quantity, price, subtotal):
        """Cập nhật một hóa đơn chi tiết."""
        update_data = {
            "quantity": quantity,
            "price": price,
            "subtotal": subtotal
        }
        rows_updated = self.dao.update_invoice_detail(invoice_code, product_id_barcode, update_data)
        return f"Cập nhật thành công {rows_updated} dòng." if rows_updated else "Không có dòng nào được cập nhật."

    def delete_invoice_detail(self, invoice_code, product_id_barcode):
        """Xóa một hóa đơn chi tiết."""
        rows_deleted = self.dao.delete_invoice_detail(invoice_code, product_id_barcode)
        return f"Đã xóa {rows_deleted} dòng." if rows_deleted else "Không tìm thấy dữ liệu để xóa."

    def get_all(self,invoice_code):
        return  self.dao.fetch_all(invoice_code)

    def get_all_by_invoice_code(self,invoice_code):
        return self.dao.fetch_all_by_invoice_code(invoice_code)