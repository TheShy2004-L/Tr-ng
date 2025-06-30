import json
import os
import threading

import cv2
import time
from pyzbar.pyzbar import decode

from Entity.InvoiceDetail import InvoiceDetail
from config1.config import INVOICE_DETAIL_PRODUCT_ID_BARCODE, INVOICE_DETAIL_QUANTITY, PATH_CART, PATH_RECOGNIZE
from controllers.invoice_controller import InvoiceController
from models.product_model import ProductModel


def update_from_file():
    last_modified_time = os.path.getmtime(PATH_CART)

    def watch_file():
        nonlocal last_modified_time
        while True:
            new_modified_time = os.path.getmtime(PATH_CART)

            if new_modified_time != last_modified_time:
                last_modified_time = new_modified_time
                with open(PATH_RECOGNIZE, "w") as file:
                    file.write("True")
            else:
                with open(PATH_RECOGNIZE, "w") as file:
                    file.write("False")
            time.sleep(0.2)  # Kiểm tra mỗi giây


    thread = threading.Thread(target=watch_file, daemon=True)
    thread.start()


class ScanBarcode:
    def __init__(self):
        self.invoice_controller = None
        self.total_list = []
        self.modelProduct = None
        self.info_product = None
        self.cap = cv2.VideoCapture(0)
        self.last_scanned = ""
        self.running = True
    def start_add_scanning(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            barcodes = decode(frame)
            for barcode in barcodes:
                raw_data = barcode.data.decode("utf-8")

                # Kiểm tra nếu mã vạch đã quét rồi thì bỏ qua
                if raw_data == self.last_scanned:
                    continue

                self.last_scanned = raw_data  # Lưu mã vạch đã quét
                print(f"📌 Đã quét: {raw_data}")

                try:
                    self.info_product = json.loads(raw_data)  # Chuyển JSON string → dictionary
                    # for key, value in info_product.items():
                    #     print(f"{key}: {value}")

                    product_id = int(self.info_product["product_id_barcode"])
                    product_name = self.info_product["product_name"]
                    price = self.info_product["price"]
                    product_type = self.info_product["product_type"]
                    points = self.info_product["points"]
                    self.modelProduct = ProductModel()
                    self.modelProduct.add_product(product_name, price, None, product_type, points, product_id)

                except json.JSONDecodeError:
                    print("❌ Mã vạch không chứa dữ liệu JSON hợp lệ")

                # Hiển thị lên ảnh
                x, y, w, h = barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, raw_data, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                cv2.imshow("Barcode Scanner", frame)

                # Chờ 2 giây trước khi tiếp tục quét
                time.sleep(0.5)

            cv2.imshow("Barcode Scanner", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def start_order_scanning(self):
        self.total_list=[]
        if self.cap is None or not self.cap.isOpened():  # Nếu camera chưa được mở
            self.cap = cv2.VideoCapture(0)  # Mở lại camera
            if not self.cap.isOpened():
                print("❌ Không thể mở lại camera!")
                return
        self.invoice_controller = InvoiceController()
        self.invoice_controller.create_invoice_scan()
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                break

            barcodes = decode(frame)
            for barcode in barcodes:
                raw_data = barcode.data.decode("utf-8")
                exist = True
                for i in self.total_list:
                    print(i)
                try:
                    info_product = json.loads(raw_data)
                    invoice_code = self.invoice_controller.return_invoice_code()
                    product_id_barcode = int(info_product["product_id_barcode"])
                    for items in self.total_list:
                        # print(items[INVOICE_DETAIL_PRODUCT_ID_BARCODE])
                        if items[INVOICE_DETAIL_PRODUCT_ID_BARCODE] == product_id_barcode:
                            # print(items[INVOICE_DETAIL_QUANTITY])
                            # print(type(items[INVOICE_DETAIL_QUANTITY]))
                            items[INVOICE_DETAIL_QUANTITY] +=1  # Tăng số lượng sản phẩm
                            exist = False
                            break

                    if exist :
                        product_name = info_product["product_name"]
                        product_type = info_product["product_type"]
                        quantity = 1
                        price = info_product["price"]
                        subtotal = 0
                        customer = "customer"

                        list_info = []
                        list_info.extend([invoice_code, product_id_barcode, product_name, product_type, quantity, price, subtotal,customer])
                        a = InvoiceDetail(*list_info).__iter__()
                        self.total_list.append(a)
                        with open(PATH_RECOGNIZE, "w") as file:
                            file.write("True")
                    self.cart()


                except json.JSONDecodeError as e :
                    print(f"❌ Mã vạch không chứa dữ liệu JSON hợp lệ {e}")

                # Hiển thị lên ảnh
                x, y, w, h = barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, raw_data, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                cv2.imshow("Barcode Scanner", frame)
                time.sleep(1)

            cv2.imshow("Barcode Scanner", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()


    def exit(self):
        self.running = False
    def start(self):
        self.running = True

    def cart(self):
        with open(PATH_CART, "w") as file:
            file.write("hi")
        with open(PATH_CART, "w") as file:
            json.dump(self.total_list, file, indent=4)

        update_from_file()





