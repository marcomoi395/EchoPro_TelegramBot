from datetime import datetime
import gspread


def total_price_income_this_month(data, month) -> str:
    total_price = 0

    for row in data:
        time_str = row[0]
        price = int(row[2])
        time = datetime.strptime(time_str, "%d/%m/%Y %H:%M:%S")
        if str(time.month) == str(month):
            total_price += price
    return "⏰ Thưa ngài!!!" + f"\n\nThống kê chi tiêu tháng {month}: {total_price} đồng" + "\n\nChúc ngài một ngày tốt lành 🍀🍀🍀🍀🍀🍀🍀🍀"


def count_number_working_days_this_month(data, month_query) -> str:
    count_both = 0
    count_morning = 0
    count_afternoon = 0
    for row in data:
        time_str = row[0]
        morning = row[1]
        afternoon = row[2]
        both = row[3]
        if len(time_str) > 10:
            time = datetime.strptime(time_str, "%d/%m/%Y %H:%M:%S")
            if str(time.month) == str(month_query):
                if morning:
                    count_morning += 1
                elif afternoon:
                    count_afternoon += 1
                else:
                    count_both += 1
        else:
            time = datetime.strptime(time_str, "%d/%m/%Y")
            if str(time.month) == str(month_query):
                if morning:
                    count_morning += 1
                elif afternoon:
                    count_afternoon += 1
                else:
                    count_both += 1
    return "⏰ Thưa ngài!!!" + f"\n\nThống kê tháng {month_query}" + f"\nCa Sáng: {count_morning} buổi\nCa Chiều: {count_afternoon} buổi\nCả ngày: {count_both} ngày " + "\n\nChúc ngài một ngày tốt lành 🍀🍀🍀🍀🍀🍀🍀🍀"


class GoogleSheet:
    def __init__(self, gs_credentials: str, idSheet: str):
        self.gs = gspread.service_account(gs_credentials)
        self.idSheet = idSheet
        self.spreadsheet = self.gs.open_by_key(self.idSheet)

    # Lay data tu bang
    def get_data(self, number_sheet):
        data = self.spreadsheet.get_worksheet(number_sheet).get_all_values()[1:]
        return data

    # Them thu nhap
    def add_new_income(self, new_content, new_date_str):
        infor_content = new_content.group(1)[2:]
        amount = int(new_content.group(2))
        note = new_content.group(3)
        self.spreadsheet.get_worksheet(1).append_row([new_date_str, infor_content, amount, note])
        if note is None:
            return "📌 Thưa ngài!!!" + "\n\nDữ liệu đã được ghi lại như sau:" + f"\nVào {new_date_str} đã thu {infor_content} với giá là {amount}" + "\n\nChúc ngài một ngày tốt lành 🍀🍀🍀🍀🍀🍀🍀🍀"
        else:
            return "📌 Thưa ngài!!!" + "\n\nDữ liệu đã được ghi lại như sau:" + f"\nVào {new_date_str} đã thu {infor_content} với giá là {amount} và được ghi chú như sau '{note}'" + "\n\nChúc ngài một ngày tốt lành 🍀🍀🍀🍀🍀🍀🍀🍀"

    # Them chi thu
    def add_new_exponse(self, new_content, new_date_str):
        infor_content = new_content.group(1)
        amount = int(new_content.group(2))
        note = new_content.group(3)
        self.spreadsheet.sheet1.append_row([new_date_str, infor_content, amount, note])
        if note is None:
            # return infor_content + "\n" + amount
            return "📌 Thưa ngài!!!" + "\n\nDữ liệu đã được ghi lại như sau:" + f"\nVào {new_date_str} đã chi cho {infor_content} với giá là {amount}" + "\n\nChúc ngài một ngày tốt lành 🍀🍀🍀🍀🍀🍀🍀🍀"
        else:
            return "📌 Thưa ngài!!!" + "\n\nDữ liệu đã được ghi lại như sau:" + f"\nVào {new_date_str} đã chi cho {infor_content} với giá là {amount} và được ghi chú như sau '{note}'" + "\n\nChúc ngài một ngày tốt lành 🍀🍀🍀🍀🍀🍀🍀🍀"

    # timekeeping
    def add_new_timekeeping(self, new_content_timekeeping):
        date_timekeeping = new_content_timekeeping.group(1)
        status = new_content_timekeeping.group(2)
        current_year = datetime.now().year
        date_timekeeping = date_timekeeping + "/" + str(current_year)
        if status == 's':
            self.spreadsheet.get_worksheet(2).append_row([date_timekeeping, '✔️'])
            return "📌 Thưa ngài!!!" + "\n\nDữ liệu đã được ghi lại như sau:" + f"\nVào ngày {date_timekeeping} ngài đã đi làm vào buổi sáng'" + "\n\nChúc ngài một ngày tốt lành 🍀🍀🍀🍀🍀🍀🍀🍀"
        elif status == 'c':
            self.spreadsheet.get_worksheet(2).append_row([date_timekeeping, '', '✔️'])
            return "📌 Thưa ngài!!!" + "\n\nDữ liệu đã được ghi lại như sau:" + f"\nVào ngày {date_timekeeping} ngài đã đi làm vào buổi chiều'" + "\n\nChúc ngài một ngày tốt lành 🍀🍀🍀🍀🍀🍀🍀🍀"
        elif status == 'b':
            self.spreadsheet.get_worksheet(2).append_row([date_timekeeping, '', '', '✔️'])
            return "📌 Thưa ngài!!!" + "\n\nDữ liệu đã được ghi lại như sau:" + f"\nVào ngày {date_timekeeping} ngài đã đi làm cả ngày'" + "\n\nChúc ngài một ngày tốt lành 🍀🍀🍀🍀🍀🍀🍀🍀"
        # Get
        else:
            return "Thưa ngài!!!" + "\n\nVl thiệt chứ, cú pháp thế còn sai, thuaaaa" + "\n\n <ngày/tháng> <s, c, b>" + "\nTrong đó: s là sáng, c là chiều và b là cả ngày" + "\n\nChúc ngài một ngày tốt lành 🍀🍀🍀🍀🍀🍀🍀🍀"

    # Undo
    def undo_income(self, number):
        rows = self.get_data(number)
        if len(rows) > 1:
            self.spreadsheet.get_worksheet(number).delete_rows(len(rows) + 1)
        return "📌 Hoàn tác ghi chú thành công"

    # timekeeping during the day
    def timekeeping_during_the_day(self, content, new_date_str):
        if content == 'Sáng':
            self.spreadsheet.get_worksheet(2).append_row([new_date_str, "✔️"])
            return "📌 Thưa ngài!!!" + "\n\nDữ liệu đã được ghi lại như sau:" + f"\nVào ngày {new_date_str[0:10]} ngài đã đi làm vào buổi sáng" + "\n\nChúc ngài một ngày tốt lành 🍀🍀🍀🍀🍀🍀🍀🍀"

        elif content == 'Chiều':
            self.spreadsheet.get_worksheet(2).append_row([new_date_str, "", "✔️"])
            return "📌 Thưa ngài!!!" + "\n\nDữ liệu đã được ghi lại như sau:" + f"\nVào ngày {new_date_str[0:10]} ngài đã đi làm vào buổi chiều" + "\n\nChúc ngài một ngày tốt lành 🍀🍀🍀🍀🍀🍀🍀🍀"

        elif content == 'Cả ngày':
            self.spreadsheet.get_worksheet(2).append_row([new_date_str, "", "", "✔️"])
            return "📌 Thưa ngài!!!" + "\n\nDữ liệu đã được ghi lại như sau:" + f"\nVào ngày {new_date_str[0:10]} ngài đã đi làm cả ngày" + "\n\nChúc ngài một ngày tốt lành 🍀🍀🍀🍀🍀🍀🍀🍀"

    # get one month statistics
    def get_one_month_statistics(self, content):
        if content.startswith("/c "):
            return total_price_income_this_month(self.get_data(0), content[3:4])

        elif content.startswith("/t "):
            return total_price_income_this_month(self.get_data(1), content[3:4])

        elif content.startswith("/w "):
            return count_number_working_days_this_month(self.get_data(2), content[3:4])
