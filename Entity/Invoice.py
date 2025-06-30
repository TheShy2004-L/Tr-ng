from datetime import datetime

from config1.config import DEFAULT_TIME


class Invoice:
    def __init__(self,  employee_code, customer_name,total_quantity_drink,
                 total_quantity_food,total_price_drink,total_price_food,total_price,invoice_code):
        self.employee_code = employee_code
        self.customer_name = customer_name
        self.date_created = datetime.now().strftime(DEFAULT_TIME)
        self.total_quantity_drink = total_quantity_drink
        self.total_quantity_food = total_quantity_food
        self.total_price_drink = total_price_drink
        self.total_price_food = total_price_food
        self.total_price =  total_price
        self.invoice_code = invoice_code

    def __iter__(self):
        return iter([
            self.employee_code,
            self.customer_name,
            self.date_created,
            self.total_quantity_drink ,
            self.total_quantity_food ,
            self.total_price_drink ,
            self.total_price_food ,
            self.total_price,
            self.invoice_code
        ])

    def __repr__(self):
        return (f"Invoice({self.employee_code}, {self.customer_name}, "
                f"{self.date_created}, Total Price: {self.total_price}, Total Quantity: "
                f"{self.total_quantity_drink} drinks, {self.total_quantity_food} foods,code: {self.invoice_code})")

