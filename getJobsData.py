import sqlite3
import requests
import json
import displayData
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QListWidget
from PyQt5 import QtWidgets
import sys

MY_API_KEY = 'f9824e1322236e2ede0a4929e3eb27c8'
MY_API_ID = '51e101b5'
START_URL = f"http://api.adzuna.com/v1/api/jobs/gb/search/1?app_id={MY_API_ID}&app_key={MY_API_KEY}" \
            f"&what="
END_URL = "%20developer&content-type=application/json "


class JobsWindow(QListWidget):
    def __init__(self, to_display):
        super().__init__()
        self.data_to_display = to_display
        self.data_item_displayed = 0
        self.filter, self.connection, self.cursor, self.jobs, self.window = [None] * 5
        self.current_data = self.data_to_display[self.data_item_displayed]
        main_layout = QtWidgets.QVBoxLayout()
        top_label = QLabel("Job Title:")
        main_layout.addWidget(top_label)
        self.title_display = QListWidget()
        self.title_display.addItem(remove_characters(self.current_data['title']))
        main_layout.addWidget(self.title_display)
        display_name = QLabel("Company Name:")
        main_layout.addWidget(display_name)
        self.com_display = QListWidget()
        main_layout.addWidget(self.com_display)
        self.com_display.addItem(self.current_data['company'].get('display_name'))
        get_next = QPushButton("Get Next Job")
        main_layout.addWidget(get_next)
        loc_filter = QPushButton("Filter Location")
        main_layout.addWidget(loc_filter)
        company_filter = QPushButton("Filter Company")
        main_layout.addWidget(company_filter)
        tech_list = ['python', 'java', 'javascript', 'golang', 'devops', 'database']
        self.tech_box = QComboBox(self)
        self.tech_box.addItems(tech_list)
        self.tech_label = QLabel(self)
        main_layout.addWidget(self.tech_box)
        self.tech_box.move(50, 150)
        self.setLayout(main_layout)
        get_next.pressed.connect(self.show_next_job)
        loc_filter.pressed.connect(self.filter_loc)
        company_filter.pressed.connect(self.filter_company)
        self.tech_box.currentIndexChanged[str].connect(self.tech_choice)

    def show_next_job(self):
        self.data_item_displayed += 1
        self.current_data = self.data_to_display[self.data_item_displayed]
        self.title_display.addItem(remove_characters(self.current_data['title']))
        self.com_display.addItem(self.current_data['company'].get('display_name'))

    def tech_choice(self, text):
        self.filter = displayData
        self.connection = sqlite3.connect("jobs.db")
        self.cursor = self.connection.cursor()
        self.jobs = self.filter.get_filtered_menu(self.cursor, text)
        self.window = displayData.TestWindow()
        self.window.display_data(self.jobs)
        self.window.show()

    def filter_loc(self):
        self.filter = displayData
        self.connection = sqlite3.connect("jobs.db")
        self.cursor = self.connection.cursor()
        self.jobs = self.filter.get_filtered_loc(self.cursor)
        self.window = displayData.TestWindow()
        self.window.display_data(self.jobs)
        self.window.show()

    def filter_company(self):
        self.filter = displayData
        self.connection = sqlite3.connect("jobs.db")
        self.cursor = self.connection.cursor()
        self.jobs = self.filter.get_filtered_company(self.cursor)
        self.window = displayData.TestWindow()
        self.window.display_data(self.jobs)
        self.window.show()


def display_data(to_display):
    window = JobsWindow(to_display)
    return window


def get_data(location):
    response = requests.get(location)
    if response.status_code != 200:
        return []
    data = response.json()
    return data['results']


def save_data(jobs: list, cursor: sqlite3.Cursor):
    for job in jobs:
        cursor.execute("INSERT INTO jobs(company, description, web_address, location, title) "
                       "VALUES (?,?,?,?,?);",
                       (job['company'].get('display_name'), job['description'], job['redirect_url'],
                        job['location'].get('display_name'), job['title']))


def setup_database(cursor: sqlite3.Cursor):
    create_statement = """CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT,
    description TEXT,
    web_address TEXT,
    location TEXT,
    title TEXT);"""
    cursor.execute(create_statement)


def write_database(data):
    connection = sqlite3.connect("jobs.db")
    cursor = connection.cursor()
    setup_database(cursor)
    save_data(data, cursor)
    connection.commit()
    connection.close()


def get_params():
    job_type = input("Full Time or Part Time?: Capital F/P ")
    if job_type == 'F':
        job_type = 'full_time=1'
    else:
        job_type = 'part_time=1'
    salary_min = input("Please Enter Minimum Salary: ")
    return job_type, salary_min


def write_data(to_file):
    with open('data.txt', 'w') as f:
        json.dump(to_file, f)


def get_tech_data(choice):
    tech_list = []
    loc = START_URL + choice + END_URL
    print(loc)
    data = get_data(loc)
    tech_list += data
    window = display_data(tech_list)
    return window


def get_jobs_data():
    jobs_list = []
    params = get_params()
    search_list = ['python', 'java', 'javascript', 'golang', 'devops', 'database']
    for element in search_list:
        loc = START_URL + element + END_URL
        print(loc)
        data = get_data(loc)
        jobs_list += data
    loc_params = f"https://api.adzuna.com/v1/api/jobs/gb/search/1?app_id=51e101b5&app_key" \
                 f"=f9824e1322236e2ede0a4929e3eb27c8&salary_min={params[1]}&{params[0]} "
    print(loc_params)
    data_params = get_data(loc_params)
    jobs_list += data_params
    window = display_data(jobs_list)
    return window


def save_to_database():
    choice = get_params()
    search_list = ['python', 'java', 'javascript', 'golang', 'devops', 'database']
    for element in search_list:
        loc = START_URL + element + END_URL
        print(loc)
        data = get_data(loc)
        write_data(data)
        write_database(data)
    loc_params = f"https://api.adzuna.com/v1/api/jobs/gb/search/1?app_id=51e101b5&app_key" \
                 f"=f9824e1322236e2ede0a4929e3eb27c8&salary_min={choice[1]}&{choice[0]} "
    print(loc_params)
    data_params = get_data(loc_params)
    write_database(data_params)
    write_data(data_params)


# <strong> </strong>
def remove_characters(data):
    bad_chars = ['<', '/', '>', "strong"]

    for i in bad_chars:
        data = data.replace(i, '')
    return data


def main():
    usr_input = input("Enter 1 to Save to Database, 2 to see GUI")
    if usr_input == '1':
        save_to_database()
    else:
        app = QApplication(sys.argv)
        window = get_jobs_data()
        window.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    main()
