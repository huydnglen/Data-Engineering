import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
import pandas as pd

# Hàm dịch trạng thái đơn hàng sang tiếng Việt
def translate_status_to_vietnamese(status):
    status_mappings = {
        0: 'Mới', 17: 'Chờ xác nhận', 11: 'Chờ hàng', 12: 'Chờ in', 13: 'Đã in', 20: 'Đã đặt hàng',
        1: 'Đã xác nhận', 8: 'Đang đóng hàng', 9: 'Chờ chuyển hàng', 2: 'Đã gửi hàng', 3: 'Đã nhận',
        16: 'Đã thu tiền', 4: 'Đang hoàn', 15: 'Hoàn 1 phần', 5: 'Đã hoàn', 6: 'Đã hủy', 7: 'Đã xóa',
        10: 'Đơn Webcake', 21: 'Đơn Storecake',
    }
    return status_mappings.get(status, status)


# Lấy danh sách nhân viên từ API
def get_employees():
    url_employees = 'https://pos.pages.fm/api/v1/shops/100152026/users?api_key=721a8743f2ab4afe9150100dceb543a3'
    response = requests.get(url_employees)
    response.raise_for_status()
    result = response.json()
    employees = {}

    # Lưu thông tin nhân viên vào dictionary với key là user_id và value là name
    for employee in result['data']:
        user_id = employee['user_id']
        name = employee['user']['name']
        employees[user_id] = name

    return employees


# Tìm tên nhân viên dựa trên editor_id
def get_editor_name(editor_id, employees):
    return employees.get(editor_id, "Unknown")


# Hàm chuyển đổi giờ sang múi giờ Việt Nam và định dạng tiếng Việt
def convert_time_to_vietnamese_time(time_str):
    try:
        time_obj = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
        time_obj = time_obj + timedelta(hours=7)  # Cộng thêm 7 giờ
        return time_obj.strftime("%H:%M %d/%m/%Y")  # Định dạng giờ, phút và ngày tháng
    except Exception as e:
        print(f"Error parsing time: {e}")
        return "Invalid time"


# Xử lý đơn hàng
def process_orders(data, employees):
    processed_orders = []
    seen = set()  # Giới hạn trùng lặp bằng cách theo dõi các phần tử đã gặp
    for order_data in data:
        id = order_data['order_id']
        order = order_data['order']
        nguondon = order['order_sources_name']
        ngaytaodon = (datetime.strptime(order['inserted_at'], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(hours=7)).strftime("%d/%m/%Y %H:%M")
        sodienthoai = order['bill_phone_number']
        tags = ', '.join(tag['name'] for tag in order.get('tags', []))
        ghichunoibo = order.get('note', '')
        trang_thai = translate_status_to_vietnamese(order['status'])
        needs_call_at = (datetime.strptime(order_data.get('needs_call_at', ''), '%Y-%m-%dT%H:%M:%S') + timedelta(hours=7)).strftime("%d/%m/%Y %H:%M")

        gomcacSP = ""
        for item in order['items']:
            variationinfo = item['variation_info']
            sl = item['quantity']
            sp = variationinfo.get('name')
            gomcacSP += f'{sp} x {sl}; '
        gomcacSP = gomcacSP.rstrip('; ')

        customer = order['customer']
        notes = customer.get('notes', [])
        ghichutraodoi = ""
        for note in notes:
            message = note.get('message', ' ')
            name = note['created_by']['fb_name']
            created_at_raw = note.get('created_at', None)
            if isinstance(created_at_raw, (int, float)):
                try:
                    created_at = datetime.fromtimestamp(created_at_raw / 1000).strftime("%d/%m/%Y %H:%M:%S")
                except (OSError, OverflowError, ValueError) as e:
                    print(f"Error processing timestamp {created_at_raw}: {e}")
                    created_at = "Invalid timestamp"

            ghichutraodoi += f'Người tạo: {name} - Ghi chú: {message} - Thời điểm tạo: {created_at}\n'
        ghichutraodoi = ghichutraodoi.rstrip('\n')

        histories = order.get('histories', [])

        tag_changes = []
        for history in histories:
            editor_id = history.get('editor_id', '')
            editor_name = get_editor_name(editor_id, employees)

            if 'tags' in history:
                old_tags = [tag['name'] for tag in history['tags']['old']] if 'old' in history['tags'] else []
                new_tags = [tag['name'] for tag in history['tags']['new']] if 'new' in history['tags'] else []

                if old_tags != new_tags:
                    added_tags = [tag for tag in new_tags if tag not in old_tags]
                    removed_tags = [tag for tag in old_tags if tag not in new_tags]

                    for added_tag in added_tags:
                        time_added = convert_time_to_vietnamese_time(history['updated_at'])
                        tag_changes.append(f"Thêm thẻ {added_tag} bởi {editor_name} lúc {time_added}")

                    for removed_tag in removed_tags:
                        time_removed = convert_time_to_vietnamese_time(history['updated_at'])
                        tag_changes.append(f"Xóa thẻ {removed_tag} bởi {editor_name} lúc {time_removed}")

                    if old_tags and new_tags:
                        edited_tags = [tag for tag in old_tags if tag not in new_tags]
                        if edited_tags:
                            time_edited = convert_time_to_vietnamese_time(history['updated_at'])
                            tag_changes.append(f"Chỉnh sửa thẻ từ {', '.join(edited_tags)} thành {', '.join(new_tags)} bởi {editor_name} lúc {time_edited}")

        order_tuple = (id, trang_thai, nguondon, ngaytaodon, sodienthoai, gomcacSP, ghichunoibo, tags,
                       ghichutraodoi, needs_call_at, "\n".join(tag_changes))

        # Kiểm tra nếu order_tuple đã tồn tại trong seen
        if order_tuple not in seen:
            processed_orders.append(order_tuple)
            seen.add(order_tuple)

    # Loại bỏ trùng lặp sử dụng pandas
    df = pd.DataFrame(processed_orders)
    df.drop_duplicates(inplace=True)

    return df.values.tolist()


# Lấy danh sách nhân viên
employees = get_employees()

# Fetch dữ liệu đơn hàng từ API
url_api = 'https://pos.pages.fm/api/v1/shops/100152026/order_call_laters?api_key=721a8743f2ab4afe9150100dceb543a3'
response = requests.get(url_api)
response.raise_for_status()
result = response.json()
data = result['data']

# Xử lý đơn hàng
processed_orders = process_orders(data, employees)

# Connect to Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open('DATA HẸN GỌI RESALE').worksheet('DATA POS')

# Cập nhật Google Sheets
header_row = ['Mã đơn hàng', 'Trạng thái', 'Nguồn đơn', 'Ngày tạo đơn', 'Số điện thoại', 'Gồm các SP', 'Ghi chú nội bộ',
              'Thẻ', 'Ghi chú trao đổi', 'Hẹn gọi', 'Lịch sử chỉnh sửa thẻ']
data_rows = [header_row] + processed_orders
sheet.clear()  # Clear existing data
sheet.update('A1', data_rows)  # Update sheet with new data
