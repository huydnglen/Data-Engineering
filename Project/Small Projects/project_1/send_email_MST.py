import psycopg2
import pandas as pd
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import io
from datetime import date
import tkinter as tk
from tkinter import messagebox

# Biến toàn cục để lưu trữ lựa chọn
selected_policy = None
selected_table = None
selected_subject_prefix = None
selected_file_prefix = None


# Hàm để xử lý lựa chọn và chạy script
def run_script(choice):
    global selected_policy, selected_table, selected_subject_prefix, selected_file_prefix

    if choice == "JNT":
        selected_policy = "jnt_policy"
        selected_table = "mst_data.mst_jnt_230321878_data"
        selected_subject_prefix = "CA63-JNT"
        selected_file_prefix = "CA63-JNT"
    elif choice == "Flash":
        selected_policy = "flash_policy"
        selected_table = "mst_data.mst_flash_230321878_data"
        selected_subject_prefix = "CA63-FLASH"
        selected_file_prefix = "CA63-FLASH"

    messagebox.showinfo("Thông báo", f"Đã chọn {choice}. Script sẽ chạy với lựa chọn này.")
    root.destroy()


# Tạo giao diện chọn
root = tk.Tk()
root.title("Chọn bảng dữ liệu")

label = tk.Label(root, text="Vui lòng chọn chính sách:")
label.pack(pady=10)

jnt_button = tk.Button(root, text="JNT", command=lambda: run_script("JNT"))
jnt_button.pack(pady=5)

flash_button = tk.Button(root, text="Flash", command=lambda: run_script("Flash"))
flash_button.pack(pady=5)

root.mainloop()

# Kết nối PostgreSQL
try:
    conn = psycopg2.connect(
        dbname="mspeedy",
        user="mspeedy",
        password="mspeedy",
        host="localhost",
        port="5432"
    )
    print("Kết nối cơ sở dữ liệu thành công!")
except Exception as e:
    print(f"Lỗi kết nối cơ sở dữ liệu: {e}")

cur = conn.cursor()

# Truy vấn dữ liệu
print(f"Đang sử dụng bảng {selected_policy} và {selected_table}")
cur.execute(f"""
    SELECT
    {selected_policy}."warehouse_name" AS "Sender",
    msx."Waybill Number",
    msx."Sender Name",
    msx."Sender Phone",
    msx."Receiver Name",
    msx."Receiver Phone",
    msx."Weight (gram)",
    msx."Shipping Fee",
    msx."Shipping Fee Tax",
    msx."COD",
    msx."COD Fee",
    msx."COD Fee Tax",
    msx."Insurance Value",
    msx."Insurance Fee",
    msx."Return Fee",
    msx."Return Fee Tax",
    msx."Return Fee Adjustment",
    msx."Total Fee",
    msx."Input Date",
    {selected_policy}.email
    FROM {selected_table} msx
    JOIN {selected_policy} ON msx."Sender Name" = {selected_policy}."warehouse_name"
    WHERE msx."Input Date" = CURRENT_DATE;
""")

rows = cur.fetchall()

# Kiểm tra số dòng trả về
print(f"Số dòng dữ liệu truy vấn được: {len(rows)}")

# Lấy tên cột
columns = [desc[0] for desc in cur.description]
print(f"Tên các cột: {columns}")

# Chuyển dữ liệu thành DataFrame
df = pd.DataFrame(rows, columns=columns)

# Nhóm dữ liệu theo "Sender Name"
grouped = df.groupby("Sender Name")
print("Đã nhóm dữ liệu theo Sender Name.")

# SMTP thông tin
SMTP_SERVER = "pro13.emailserver.vn"
SMTP_PORT = 587
EMAIL_ADDRESS = "vipsupport@mspeedyexpress.com"
EMAIL_PASSWORD = "MSX@Top1"


# Hàm gửi email
# Hàm gửi email (có hỗ trợ CC)
def send_email(recipient_email, subject, body, attachment_data, attachment_name, cc_emails=None):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = recipient_email
        if cc_emails:  # Nếu có email CC
            msg["Cc"] = ", ".join(cc_emails)  # Gộp danh sách email CC thành chuỗi
        msg["Subject"] = subject

        # Nội dung email
        msg.attach(MIMEText(body, "html"))

        # Tệp đính kèm
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment_data)
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={attachment_name}",
        )
        msg.attach(part)

        # Kết nối SMTP và gửi email
        with SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            # Gửi email với cả danh sách người nhận và CC
            recipients = [recipient_email] + (cc_emails if cc_emails else [])
            server.sendmail(EMAIL_ADDRESS, recipients, msg.as_string())
        print(f"Email đã gửi đến {recipient_email} với CC: {cc_emails} và tệp đính kèm {attachment_name}")
    except Exception as e:
        print(f"Lỗi gửi email: {e}")

# Xử lý từng nhóm và gửi email
for sender_name, group in grouped:
    email = group.iloc[0]["email"]  # Lấy email tương ứng từ nhóm
    today_date = date.today().strftime("%Y%m%d")  # Lấy ngày hôm nay theo định dạng YYYYMMDD
    subject = f"{today_date}-{selected_subject_prefix}-{sender_name}_SOA"

    # Tính toán các tổng phí từ nhóm dữ liệu
    Total_Shipping_Fee = group['Shipping Fee'].sum()
    Total_value_added_fee = group['Insurance Fee'].sum()
    Total_COD_Amount = group['COD'].sum()
    Total_COD_Fee = group['COD Fee'].sum()
    Total_Return_Fee = group['Return Fee'].sum()
    Return_Fee_Adjustment = group['Return Fee Adjustment'].sum()
    Total_Fee = Total_Shipping_Fee + Total_value_added_fee + Total_COD_Fee + Total_Return_Fee - Return_Fee_Adjustment
    Total_Amount = Total_COD_Amount - Total_Fee

    # Tạo nội dung email với bảng HTML
    html_table = f"""
    <table style="border-collapse: collapse; width: 100%;">
        <tr>
            <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">Total Shipping Fee</td>
            <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">Total value-added fee</td>
            <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">Total COD Amount</td>
            <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">Total COD Fee</td>
            <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">Total Return Fee</td>
            <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">Return Fee Adjustment</td>
            <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">Total Fee</td>
            <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">Total Amount</td>
        </tr>
        <tr>
            <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">₱{Total_Shipping_Fee}</td>
            <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">₱{Total_value_added_fee}</td>
            <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">₱{Total_COD_Amount}</td>
            <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">₱{Total_COD_Fee}</td>
            <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">₱{Total_Return_Fee}</td>
            <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">₱{Return_Fee_Adjustment}</td>
            <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">₱{Total_Fee}</td>
            <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">₱{Total_Amount}</td>
        </tr>
    </table>
    """

    body = (f"Dear valued customer,<br><br>"
            f"We are sending statement of account (SOA) for the period {today_date}.<br>"
            f"Please review the attached summary and the attached billing for your information and guidance.<br>"
            f"All COD remittance will be deposited or transferred to the bank account registered for COD remittance only.<br>"
            f"<br>{html_table}<br>"
            f"If current net remittance is negative, no remittance for the current period and will be creditable for succeeding billing.<br>"
            f"If you have any questions, please contact us at finance@mspeedyexpress.com in this subject format: COD Settlement Inquiry - {sender_name}.<br>"
            f"For questions and concerns regarding claims, loss, damage, and delay of deliveries, email us at cs@mspeedyexpress.com.<br>"
            f"If feedback is not received within 3 days, the contents of this SOA will be considered correct.<br><br>"
            f"Thank you,<br>Mspeedy Express Team")

    # Tạo tên file Excel
    file_name = f"{today_date}-{selected_file_prefix}-{sender_name.replace(' ', '_').replace('(', '').replace(')', '')}_SOA.xlsx"

    # Xuất dữ liệu nhóm ra file Excel trong bộ nhớ (in-memory)
    with io.BytesIO() as output:
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            group.drop(columns=["email", "Sender Name"], inplace=True)  # Không lưu email và Sender Name trong Excel
            group.to_excel(writer, sheet_name="Order Detail", index=False)

            # Tạo sheet "BILLING STATEMENT"
            billing_data = [
                ["BILLING STATEMENT", None],
                ["CLIENT", sender_name],
                ["DATE", today_date],
                ["Total Shipping Fee", Total_Shipping_Fee],
                ["Total value-added fee", Total_value_added_fee],
                ["Total COD Amount", Total_COD_Amount],
                ["Total COD Fee", Total_COD_Fee],
                ["Total Return Fee", Total_Return_Fee],
                ["Return Fee Adjustment", Return_Fee_Adjustment],
                ["Total Fee", Total_Fee],
                ["Total Amount", Total_Amount]
            ]
            billing_df = pd.DataFrame(billing_data, columns=["MSPEEDY EXPRESS", None])
            billing_df.to_excel(writer, sheet_name="BILLING STATEMENT", index=False)

        # Đọc dữ liệu từ bộ nhớ
        attachment_data = output.getvalue()

    # Gửi email
    send_email(
        recipient_email=email,
        subject=subject,
        body=body,
        attachment_data=attachment_data,
        attachment_name=file_name,
        cc_emails=["accountant@mspeedyfulfillment.com", "bd@mspeedyfulfillment.com", "adam@mspeedyfulfillment.com", "bangoc.leo@mspeedyfulfillment.com"]
    )

# Đóng kết nối
cur.close()
conn.close()

print("Đã hoàn thành quá trình gửi email.")
