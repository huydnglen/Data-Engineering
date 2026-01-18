import requests
import concurrent.futures
from datetime import datetime, timedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, DateType

def translate_status_to_vietnamese(status):
    status_mappings = {
        0: 'Mới', 17: 'Chờ xác nhận', 11: 'Chờ hàng', 12: 'Chờ in', 13: 'Đã in', 20: 'Đã đặt hàng',
        1: 'Đã xác nhận', 8: 'Đang đóng hàng', 9: 'Chờ chuyển hàng', 2: 'Đã gửi hàng', 3: 'Đã nhận',
        16: 'Đã thu tiền', 4: 'Đang hoàn', 15: 'Hoàn 1 phần', 5: 'Đã hoàn', 6: 'Đã hủy', 7: 'Đã xóa',
        10: 'Đơn Webcake', 21: 'Đơn Storecake',
    }
    return status_mappings.get(status, status)

def get_total_order_count():
    base_url = 'https://pos.pages.fm/api/v1'
    shop_id = '1290192859'
    api_key = '0e4929a92b65471c9fa8afbb0643265a'
    api_url = f'{base_url}/shops/{shop_id}/orders?api_key={api_key}&locale=vi'
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json().get('total_entries', 0)
    else:
        print(f'Đã xảy ra lỗi khi lấy số lượng đơn hàng. Mã lỗi: {response.status_code}')
        return 0

def fetch_orders(page):
    base_url = 'https://pos.pages.fm/api/v1'
    shop_id = '1290192859'
    api_key = '0e4929a92b65471c9fa8afbb0643265a'
    page_size = 250

    api_url = f'{base_url}/shops/{shop_id}/orders?api_key={api_key}&page_size={page_size}&page={page}&locale=vi'
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json().get('data', [])
    else:
        print(f'Đã xảy ra lỗi khi lấy dữ liệu từ trang {page}. Mã lỗi: {response.status_code}')
        return []

def get_formatted_date(status_histories, target_status, hour_offset=7, date_format="%d/%m/%Y"):
    """
    Tìm trạng thái đầu tiên khớp với target_status, cộng thêm giờ, và định dạng ngày.
    """
    for history in status_histories:
        if history.get('status') == target_status:
            original_date = datetime.strptime(history['updated_at'], "%Y-%m-%dT%H:%M:%S")
            offset_date = original_date + timedelta(hours=hour_offset)
            return offset_date.strftime(date_format)
    return None  # Trả về None nếu không tìm thấy trạng thái khớp

def process_order(order):
    partner = order.get('partner', {})
    extend_code = partner.get('extend_code', '') if partner else ''
    # ngay_tao_don = datetime.strptime(order['inserted_at'], '%Y-%m-%dT%H:%M:%S.%f').strftime("%d/%m/%Y")
    trang_thai = translate_status_to_vietnamese(order['status'])
    ID = order.get('id')
    system_id = order.get('system_id')
    full_ID = f'S1290192859O{system_id}'
    cod = order.get('cod')
    returned_time = ''
    status_histories = order.get('status_history', [])

    # Sử dụng hàm cho hai trạng thái
    returned_time = get_formatted_date(status_histories, target_status=5)
    pickup_time = get_formatted_date(status_histories, target_status=2)

    processed_orders = []
    items = order.get('items', [])

    for item in items:
        variationinfo = item['variation_info']
        sl = item['quantity']
        sp = variationinfo.get('name', '')
        mmm = variationinfo.get('display_id')
        msp = variationinfo.get('product_display_id')
        detail = variationinfo.get('detail', '')
        if detail == '' or detail == None:
            sp_name = sp
        else:
            sp_name = f'{sp} / {detail}'
        # Append each product with order info
        processed_orders.append((ID, full_ID, extend_code, pickup_time, trang_thai, sp_name, sl, msp, mmm, returned_time, cod))

    return processed_orders


def main():
    # Khởi tạo SparkSession
    spark = SparkSession.builder.appName("OrderProcessing").getOrCreate()

    # Kết nối tới Google Sheets
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('NEW_INVENTORY M95').worksheet('DATA POS')

    total_order_count = get_total_order_count()
    if total_order_count == 0:
        print("Không có đơn hàng nào.")
        return

    page_size = 250
    total_pages = (total_order_count + page_size - 1) // page_size  # Ensure correct number of pages

    all_orders = set()
    processed_orders = []

    # Fetch and process orders concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_to_page = {executor.submit(fetch_orders, page): page for page in range(1, total_pages + 1)}
        for future in concurrent.futures.as_completed(future_to_page):
            page = future_to_page[future]
            try:
                orders = future.result()
                if not orders:
                    print(f'Trang {page} không có dữ liệu, dừng lấy dữ liệu.')
                    break
                for order in orders:
                    order_id = order.get('id')
                    if order_id not in all_orders:
                        all_orders.add(order_id)
                        processed_orders.extend(process_order(order))  # Extend to include all products
            except Exception as e:
                print(f'Lỗi khi lấy dữ liệu từ trang {page}: {e}')

    # Chuyển đổi danh sách dữ liệu sang DataFrame của PySpark
    schema = StructType([
        StructField("ID", StringType(), True),
        StructField("Mã đơn hàng đầy đủ", StringType(), True),
        StructField("Mã vận đơn", StringType(), True),
        StructField("Ngày đẩy đơn sang DVVC", StringType(), True),
        StructField("Trạng thái", StringType(), True),
        StructField("Sản phẩm", StringType(), True),
        StructField("Số lượng", IntegerType(), True),
        StructField("Mã Sản phẩm", StringType(), True),
        StructField("Mã mẫu mã", StringType(), True),
        StructField("Ngày cập nhật trạng thái đã hoàn", StringType(), True),
        StructField("COD", IntegerType(), True)
    ])

    if processed_orders:
        # Tạo DataFrame từ danh sách dữ liệu đã xử lý
        rdd = spark.sparkContext.parallelize(processed_orders)
        orders_df = spark.createDataFrame(rdd, schema=schema)

        # Hiển thị một vài dòng dữ liệu để kiểm tra
        orders_df.show(5)

        # Ghi dữ liệu vào Google Sheets
        header_row = ['ID', 'Mã đơn hàng đầy đủ', 'Mã vận đơn', 'Ngày đẩy đơn sang DVVC', 'Trạng thái', 'Sản phẩm', 'Số lượng', 'Mã sản phẩm','Mã mẫ mã', 'Ngày cập nhật trạng thái đã hoàn', 'COD']
        data_rows = [header_row] + processed_orders
        sheet.clear()  # Clear existing data
        sheet.update(values=data_rows, range_name='A1')  # Update sheet with new data

if __name__ == "__main__":
    main()
