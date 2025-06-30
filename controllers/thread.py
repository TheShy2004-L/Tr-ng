import threading

from test_code.scan import ScanBarcode


class ThreadController:
        def __init__(self):
            self.scanning_instance = ScanBarcode()  # Lưu đối tượng quét barcode
            self.scanning_thread = None  # Lưu thread
            self.running = False  # Biến điều khiển chạy/quét

        def start_scanning(self):
            """Bắt đầu quét mã vạch"""
            if not self.running:  # Kiểm tra nếu chưa chạy
                self.running = True
                self.scanning_thread = threading.Thread(target=self.scanning_instance.start_order_scanning, daemon=True)
                self.scanning_thread.start()
                print("Đã bật quét mã vạch.")


        def stop_scanning(self):
            """Dừng quét mã vạch"""
            if self.running:
                self.running = False
                self.scanning_instance.exit()  # Gọi hàm dừng trong ScanBarcode
                print("Đã tắt quét mã vạch.")

                # Chờ cho thread quét mã vạch kết thúc trước khi tiếp tục
                self.scanning_thread.join()

