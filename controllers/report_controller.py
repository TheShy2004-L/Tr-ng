import calendar

from models.invoice_model import InvoiceModel
from models.report_model import *

class ReportController:
    def get_reports(self):
        """Lấy danh sách tất cả báo cáo"""
        try:
            return get_list_reports()
        except Exception as e:
            print(f"Lỗi khi lấy danh sách báo cáo: {e}")
            return []

    def add_report(self,month,year):

        try:
            self.invoice_model = InvoiceModel()
            list_invoice_in_month = self.invoice_model.get_invoice_by_month(month,year)
            drink_qty = 0
            drink_price = 0
            food_qty = 0
            food_price = 0

            for item in list_invoice_in_month:
                drink_qty += item[4]
                food_qty += item[5]
                drink_price += item[6]
                food_price += item[7]

            total_sold = drink_qty + food_qty
            total_price = drink_price + food_price

            return create_report(drink_qty, drink_price, food_qty, food_price, total_sold, total_price)
        except Exception as e:
            print(f"Lỗi khi thêm báo cáo: {e}")
            return None

    def get_id_now(self):
        return get_id_time_now()
    def update_all_report(self):
        if self.get_id_now() is None:
            self.add_report(datetime.now().month,datetime.now().year)
            return
        try:
            self.invoice_model = InvoiceModel()
            list_invoice_in_month = self.invoice_model.get_invoice_by_month(datetime.now().month,datetime.now().year)
            drink_qty = 0
            drink_price = 0
            food_qty = 0
            food_price = 0

            for item in list_invoice_in_month:
                drink_qty += item[4]
                food_qty += item[5]
                drink_price += item[6]
                food_price += item[7]

            total_sold = drink_qty + food_qty
            total_price = drink_price + food_price
            return update_report(self.get_id_now(), drink_qty, drink_price, food_qty, food_price, total_sold, total_price)
        except Exception as e:
            print(f"Lỗi khi cập nhật báo cáo thang {datetime.now().month}: {e}")
            return None

    def delete_report(self, report_id):
        """Xóa báo cáo theo ID"""
        try:
            return remove_report(report_id)
        except Exception as e:
            print(f"Lỗi khi xóa báo cáo {report_id}: {e}")
            return None

    def get_report_by_month(self, month, year):
        """Lấy danh sách báo cáo theo tháng"""
        try:
            return list(get_list_report_by_month(month, year))
        except Exception as e:
            print(f"Lỗi khi lấy báo cáo tháng {month}-{year}: {e}")
            return []

    def get_data_quarter(self,quarter,year):
        list_data =[]
        quarters = {"1":(1,2,3),
                    "2": (3,4,5),
                    "3": (7,8,9),
                    "4": (10,11,12),
        }
        for i in quarters:
            if quarter == int(i):
                for month in quarters[i]:
                    list_data.append(self.get_report_by_month(int(month), int(year)))
                break
        return list_data
