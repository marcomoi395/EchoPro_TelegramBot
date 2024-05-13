from datetime import datetime, timedelta
import requests
import json


# show to-do list
def show_to_do_list(data_after_filter, title):
    if not data_after_filter:
        return "Không có công việc hôm nay!!!"
    message = f" 📌 Danh sách công việc {title}:\n\n"
    for task in data_after_filter:
        checkbox = task["properties"]["Checkbox"]["checkbox"]
        name = task["properties"]["Name"]["title"][0]["text"]["content"]
        priority = task["properties"]["Priority"]["select"]["name"]
        start_time = task["properties"]["Date"]["date"]["start"]
        end_time = task["properties"]["Date"]["date"]["end"]
        description = task["properties"]["Description"]["rich_text"]
        course = task["properties"]["Courses"]["relation"]
        name_course = ""
        if description:
            description = description[0]["text"]["content"]
        else:
            description = []
        if course:
            name_course = get_name_course_by_id(course[0]["id"])
            print(name_course)

        if start_time and end_time:
            start_time = start_time.split("T")[1][:5]  # Lấy giờ và phút từ thời gian bắt đầu
            end_time = end_time.split("T")[1][:5]  # Lấy giờ và phút từ thời gian kết thúc

            if checkbox:
                message += f"✅   Tên: {name}\n"
            else:
                message += f"❌   Tên: {name}\n"
            message += f"         Mô tả: {description}\n"
            message += f"         Thuộc khóa học: {name_course}\n"
            message += f"         Mức ưu tiên: {priority}\n"
            message += f"         Thời gian bắt đầu: {start_time}\n"
            message += f"         Thời gian kết thúc: {end_time}\n\n"

        else:
            if checkbox:
                message += f"✅   Tên: {name}\n"
            else:
                message += f"❌   Tên: {name}\n"
            message += f"         Mô tả: {description}\n"
            message += f"         Thuộc khóa học: {name_course}\n"
            message += f"         Mức ưu tiên: {priority}\n\n"
    return message


def read_json(title):
    with open(title, 'r') as file:
        data = json.load(file)
    pages = data.get('results', [])
    return pages


def get_name_course_by_id(id_course):
    pages = read_json("courses_database.json")
    for task in pages:
        if task["id"] == id_course:
            return task["properties"]["Name"]["title"][0]["text"]["content"]
    return None


def filter_todo_list(filter_type):
    # Xác định thứ tự ưu tiên
    priority_order = {"Top": 3, "Medium": 2, "Low": 1}

    # Lấy ngày hiện tại và đặt giờ về 00:00:00 để so sánh với các ngày trong dữ liệu
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    start_month = today.replace(day=1)
    start_of_week = today - timedelta(days=today.weekday())
    pages = read_json("to_do_list_database.json")

    # Lọc danh sách theo filter_type
    if filter_type == "today":
        filtered_tasks = [task for task in pages if
                          "Deleted" in task["properties"]
                          and task["properties"]["Deleted"]["status"].get("name") == "false" and
                          "Date" in task["properties"]
                          and task["properties"]["Date"]["date"].get("start")
                          and datetime.strptime(task["properties"]["Date"]["date"]["start"][:10], '%Y-%m-%d')
                          == today]
    elif filter_type == "week":
        end_of_week = today + timedelta(days=6 - today.weekday())
        filtered_tasks = [task for task in pages if
                          "Deleted" in task["properties"]
                          and task["properties"]["Deleted"]["status"].get("name") == "false" and
                          "Date" in task["properties"]
                          and task["properties"]["Date"]["date"].get("start")
                          and datetime.strptime(task["properties"]["Date"]["date"]["start"][:10], '%Y-%m-%d')
                          >= start_of_week
                          and datetime.strptime(
                              task["properties"]["Date"]["date"]["start"][:10], '%Y-%m-%d')
                          <= end_of_week]
    elif filter_type == "month":
        end_of_month = today.replace(day=1, hour=23, minute=59, second=59) + timedelta(days=32)
        end_of_month = end_of_month.replace(day=1, hour=0, minute=0, second=0) - timedelta(days=1)
        filtered_tasks = [task for task in pages if
                          "Deleted" in task["properties"]
                          and task["properties"]["Deleted"]["status"].get("name") == "false" and
                          "Date" in task["properties"]
                          and task["properties"]["Date"]["date"].get("start")
                          and datetime.strptime(task["properties"]["Date"]["date"]["start"][:10], '%Y-%m-%d')
                          >= start_month
                          and datetime.strptime(
                              task["properties"]["Date"]["date"]["start"][:10], '%Y-%m-%d')
                          <= end_of_month]
    else:
        return []  # Trả về danh sách rỗng nếu filter_type không hợp lệ

    # Sắp xếp danh sách theo mức ưu tiên
    sorted_tasks = sorted(filtered_tasks,
                          key=lambda x: priority_order.get(x["properties"]["Priority"]["select"]["name"], 0),
                          reverse=True)

    # print(sorted_tasks)
    return sorted_tasks
    # return self.pages


class NotionAPI:
    def __init__(self, token, to_do_list_database_id, courses_database_id):
        self.token = token
        self.to_do_list_database_id = to_do_list_database_id
        self.courses_database_id = courses_database_id
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-02-22"
        }

    # def response_database(self):
    #     read_url = f"https://api.notion.com/v1/databases/{self.database_id}"
    #     res = requests.get(read_url, headers=self.headers)
    #     print(res.status_code)

    def read_to_do_list_database(self):
        read_url = f"https://api.notion.com/v1/databases/{self.to_do_list_database_id}/query"
        res = requests.post(read_url, headers=self.headers)
        data = res.json()
        with open("to_do_list_database.json", 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False)

    def read_courses_database(self):
        read_url = f"https://api.notion.com/v1/databases/{self.courses_database_id}/query"
        res = requests.post(read_url, headers=self.headers)
        data = res.json()
        with open("courses_database.json", 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False)
