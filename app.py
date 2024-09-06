 
from flask import Flask, request, redirect, render_template, send_file, jsonify, Response
from flask_sse import sse
import os, json
from datetime import datetime, timedelta


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), "Data")
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix="/stream")


def get_week_dates(week_offset):
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)      # Lấy thứ 2 của tuần được chỉ định
    end_of_week = start_of_week + timedelta(days=6)                                             # Lấy chủ nhật của tuần        
    return start_of_week.strftime('%Y-%m-%d'), end_of_week.strftime('%Y-%m-%d')



def is_item_in_week(item, week_start, week_end):
    # Kiểm tra xem môn học (item) có nằm trong khoảng thời gian từ week_start đến week_end hay không.
    Date_end = item['Date_end']
    Date_start = item['Date_start']
    Date_end_format = datetime.strptime(Date_end, '%Y-%m-%d')
    Date_start_format = datetime.strptime(Date_start, '%Y-%m-%d')

    # Nếu ngày bắt đầu của môn học lớn hơn ngày kết thúc của tuần và ngày kết thúc của môn học nhỏ hơn ngày bắt đầu của tuần
    if Date_end < week_start or Date_start > week_end :  
        return False  # Không hiển thị môn học này

    # Kiểm tra nếu môn học nằm trong tuần cuối cùng và ngày học không lớn hơn ngày kết thúc
    date_0f_week = int(item.get('Date_week'))
    week_start = datetime.strptime(week_start, '%Y-%m-%d')
    current_date = week_start + timedelta(days=date_0f_week - 1) 
    if Date_end <= week_end and current_date > Date_end_format:
        return False 

    # Kiểm tra nếu môn học nằm trong tuần đầu tiên và ngày học không bé hơn ngày bắt đầu
    if Date_start_format >= week_start and current_date < Date_start_format:
        return False  

    return True

# def thu_trong_tuan(item):
#     item_end = item['Date_end']
#     item_end_2 = datetime.strptime(item_end, '%Y-%m-%d')
#     weekday_number = item_end_2.weekday()
#     weekdays = [1, 2, 3, 4, 5, 6, 7]
#     return weekdays[weekday_number]

# def test_thu_ngay_trong_tuan(items):
#     result = []
#     for item in items:
#         thu = thu_trong_tuan(item)  # Lấy tên ngày trong tuần
#         result.append({
#             'Subject': item.get('Subject', 'N/A'),
#             'Date_end': item['Date_end'],
#             'Day_of_week': thu  
#         })
#     return result

def filter_items_for_week(items, week_offset):
    week_start, week_end = get_week_dates(week_offset)
    filtered_items = [item for item in items if is_item_in_week(item, week_start, week_end)]
    return filtered_items





# ----------------RENDER HTML ------------------ #
@app.route('/next-week')
def next_week():
    week_offset = request.args.get('week_offset', '0')  # Giá trị mặc định là '0' nếu không có tham số
    try:
        week_offset = int(week_offset)
    except ValueError:
        week_offset = 0  # Nếu giá trị không hợp lệ, sử dụng tuần hiện tại

    # Đọc dữ liệu từ tệp JSON
    path_folder = os.path.join(os.getcwd(), "Data")
    filename = "All_Data.json"
    path_file_data = os.path.join(path_folder, filename)

    if os.path.exists(path_file_data):
        with open(path_file_data, 'r') as file:
            data = json.load(file)
    else:
        data = []

    for item in data:
        item['Period_from'] = int(item['Period_from'])
        item['Period_to'] = int(item['Period_to'])
        item['Date_week'] = int(item['Date_week'])

    # Lọc các môn học cho tuần hiện tại
    week_start, week_end = get_week_dates(week_offset)
    filtered_items = filter_items_for_week(data, week_offset)

    return jsonify({
        'filtered_items': filtered_items,
        'week_start': week_start,
        'week_end': week_end
    })



@app.route('/')
def index_1():
    week_offset = 0

    # Đọc dữ liệu từ tệp JSON
    path_folder = os.path.join(os.getcwd(), "Data")
    filename = "All_Data.json"
    path_file_data = os.path.join(path_folder, filename)

    if os.path.exists(path_file_data):
        with open(path_file_data, 'r') as file:
            data = json.load(file)
    else:
        data = []

    for item in data:
        item['Period_from'] = int(item['Period_from'])
        item['Period_to'] = int(item['Period_to'])
        item['Date_week'] = int(item['Date_week'])

    # Lọc các môn học cho tuần hiện tại
    filtered_items = filter_items_for_week(data, week_offset)
    return render_template('index.html', data=filtered_items)



@app.route('/index.html')
def index_2():
    week_offset = 0

    # Đọc dữ liệu từ tệp JSON
    path_folder = os.path.join(os.getcwd(), "Data")
    filename = "All_Data.json"
    path_file_data = os.path.join(path_folder, filename)

    if os.path.exists(path_file_data):
        with open(path_file_data, 'r') as file:
            data = json.load(file)
    else:
        data = []

    for item in data:
        item['Period_from'] = int(item['Period_from'])
        item['Period_to'] = int(item['Period_to'])
        item['Date_week'] = int(item['Date_week'])

    # Lọc các môn học cho tuần hiện tại
    filtered_items = filter_items_for_week(data, week_offset)
    return render_template('index.html', data=filtered_items)


@app.route('/new_timetable.html')
def new_data_page():
    return render_template('new_timetable.html')


@app.route('/edit_timetable.html')
def edit_timetable_page():
    return render_template('edit_timetable.html')


@app.route('/get-data')
def get_data():
    path_folder = os.path.join(os.getcwd(), "Data")
    filename = "All_Data.json"
    path_file_data = os.path.join(path_folder, filename)

    if os.path.exists(path_file_data):
        with open(path_file_data, 'r') as file:
            data = json.load(file)
    else:
        data = []

    selected_fields = [{"Subject": item["Subject"], "id": item["id"]} for item in data]
    return jsonify({"data": selected_fields, "status": "success"}), 200



@app.route('/get-data-details')
def get_data_details():
    id_subject = request.args.get('id_subject', None)  # Giá trị mặc định là None nếu không có tham số
    try:
        id_subject = int(id_subject)
    except ValueError:
        id_subject = None  

    path_folder = os.path.join(os.getcwd(), "Data")
    filename = "All_Data.json"
    path_file_data = os.path.join(path_folder, filename)
    
    if os.path.exists(path_file_data):
        with open(path_file_data, 'r') as file:
            data = json.load(file)
    else:
        data = []

    filtered_data = [item for item in data if item.get("id") == id_subject]
    return jsonify({"data": filtered_data, "status": "success"}), 200



@app.route('/add-new-data', methods=['POST'])
def add_new_data():
    try:
        # Nhận dữ liệu từ biểu mẫu
        subject = request.form.get('subject')
        ID_class = request.form.get('ID_class')
        date_week = request.form.get('date_week')
        Period_from = request.form.get('Period_from')
        Period_to = request.form.get('Period_to')
        Date_start = request.form.get('Date_start')
        Date_end = request.form.get('Date_end')
        Learning_facility = request.form.get('Learning_facility')
        Room = request.form.get('Room')
        Teacher = request.form.get('Teacher')
        Team = request.form.get('Team')
        Code_online = request.form.get('Code_online')
        Learning_software = request.form.get('Learning_software')
        type_class = request.form.get('type_class')

        # nếu folder chưa tồn tại thư mục Data thì tạo mới
        path_folder = os.path.join(os.getcwd(), "Data")
        if not os.path.exists(path_folder):
            os.mkdir(path_folder)

        # Tạo đường dẫn tệp lưu dữ liệu
        filename = "All_Data.json"
        path_save_data = os.path.join(path_folder, filename)

        # Kiểm tra xem file đã tồn tại hay chưa
        if not os.path.exists(path_save_data):
            with open(path_save_data, 'w') as file:
                json.dump([], file)  # Ở đây, chúng ta tạo file mới với một list trống

        # Đọc dữ liệu hiện tại từ file JSON
        with open(path_save_data, 'r+') as file:
            try:
                current_data = json.load(file)  # Cố gắng đọc dữ liệu hiện tại
            except json.JSONDecodeError:
                current_data = []  # Nếu không đọc được (file rỗng), tạo một list mới

            # Tạo id mới dựa trên số lượng các bản ghi hiện có
            new_id = len(current_data) + 1

            data = {
                "id": new_id,
                "Subject": subject,
                "ID_class": ID_class,
                "Date_week": date_week,
                "Period_from": Period_from,
                "Period_to": Period_to,
                "Date_start": Date_start,
                "Date_end": Date_end,
                "Learning_facility": Learning_facility,
                "Room": Room,
                "Teacher": Teacher,
                "Team": Team,
                "Code_online": Code_online,
                "Learning_software": Learning_software,
                "Type_class": type_class
            }

            current_data.append(data)                   # Thêm dữ liệu mới vào list
            file.seek(0)                                # Quay lại đầu file để ghi đè
            json.dump(current_data, file, indent=4)     # Lưu lại file JSON

        return jsonify({"message": "Bạn đã thêm lịch học thành công!", "status": "success"}), 200
    
    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 500



@app.route('/change-data', methods=['POST'])
def save_data():
    try:
        # Nhận dữ liệu từ biểu mẫu
        Subject = request.form.get('subject')
        id_subject = request.form.get('subject_id')
        ID_class = request.form.get('ID_class')
        date_week = request.form.get('date_week')
        Period_from = request.form.get('Period_from')
        Period_to = request.form.get('Period_to')
        Date_start = request.form.get('Date_start')
        Date_end = request.form.get('Date_end')
        Learning_facility = request.form.get('Learning_facility')
        Room = request.form.get('Room')
        Teacher = request.form.get('Teacher')
        Team = request.form.get('Team')
        Code_online = request.form.get('Code_online')
        Learning_software = request.form.get('Learning_software')
        type_class = request.form.get('type_class')

        # nếu folder chưa tồn tại thư mục Data thì tạo mới
        path_folder = os.path.join(os.getcwd(), "Data")
        if not os.path.exists(path_folder):
            os.mkdir(path_folder)

        # Tạo đường dẫn tệp lưu dữ liệu
        filename = "All_Data.json"
        path_save_data = os.path.join(path_folder, filename)

        # Đọc dữ liệu hiện tại từ file JSON
        if not os.path.exists(path_save_data):
            with open(path_save_data, 'r+') as file:
                json.dump([], file)  # Ở đây, chúng ta tạo file mới với một list trống

        # Đọc dữ liệu hiện tại từ file JSON
        with open(path_save_data, 'r+') as file:
            try:
                current_data = json.load(file)  # Đọc dữ liệu hiện tại

            except json.JSONDecodeError:
                return jsonify({"message": "File dữ liệu rỗng!", "status": "error"}), 500

            # Tìm bản ghi có id cần cập nhật
            record_found = False
            for record in current_data:
                if record["id"] == int(id_subject):
                    record_found = True

                    # Cập nhật dữ liệu mới
                    record["Subject"] = Subject if Subject else record["Subject"]
                    record["ID_class"] = ID_class if ID_class else record["ID_class"]
                    record["Date_week"] = date_week if date_week else record["Date_week"]
                    record["Period_from"] = Period_from if Period_from else record["Period_from"]
                    record["Period_to"] = Period_to if Period_to else record["Period_to"]
                    record["Date_start"] = Date_start if Date_start else record["Date_start"]
                    record["Date_end"] = Date_end if Date_end else record["Date_end"]
                    record["Learning_facility"] = Learning_facility if Learning_facility else record["Learning_facility"]
                    record["Room"] = Room if Room else record["Room"]
                    record["Teacher"] = Teacher if Teacher else record["Teacher"]
                    record["Team"] = Team if Team else record["Team"]
                    record["Code_online"] = Code_online if Code_online else record["Code_online"]
                    record["Learning_software"] = Learning_software if Learning_software else record["Learning_software"]
                    record["Type_class"] = type_class if type_class else record["Type_class"]
                    break
            
            # Nếu không tìm thấy bản ghi với ID cần cập nhật
            if not record_found:
                return jsonify({"message": "Không tìm thấy dữ liệu với ID này!", "status": "error"}), 404

            # Ghi đè dữ liệu mới vào file JSON
            file.seek(0)  # Quay lại đầu file để ghi đè
            json.dump(current_data, file, indent=4)
            # file.truncate()  # Xóa bất kỳ dữ liệu dư thừa nào (nếu có)

        return jsonify({"message": "Bạn đã sửa lịch học thành công!", "status": "success"}), 200
    
    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 500




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)