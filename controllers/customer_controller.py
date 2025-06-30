from models.customer_model import CustomerModel

class CustomerController:
    def __init__(self):
        self.model = CustomerModel()

    def add_customer(self, name, phone, address):
        return self.model.add_customer(name, phone, address)

    def update_customer(self, id_kh, name, phone, address):
        return self.model.update_customer(id_kh, name, phone, address)

    def delete_customer(self, id_kh):
        return self.model.delete_customer(id_kh)

    def search_customer(self, keyword):
        return self.model.search_customer(keyword)

    def get_all_customers(self):
        return self.model.get_all_customers()

    def close(self):
        self.model.close()