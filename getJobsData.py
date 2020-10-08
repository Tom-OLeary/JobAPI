"""
Thomas O'Leary
JobAPI - Retrieve Data from Adzuna API
https://developer.adzuna.com/

Python 3.8

"""
# getJobsData.py

import sqlite3
import requests
import json
import displayData
import config
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QListWidget
from PyQt5 import QtWidgets
import sys

MY_API_KEY = config.MY_API_KEY
MY_API_ID = config.MY_API_ID
START_URL = f"http://api.adzuna.com/v1/api/jobs/gb/search/1?app_id={MY_API_ID}&app_key={MY_API_KEY}" \
            f"&what="
END_URL = "%20developer&content-type=application/json "


class JobsWindow(QListWidget):
    def __init__(self, to_display):
        super().__init__()
        self.data_to_display = to_display
        self.data_item_displayed = 0
        self.filter, self.connection, self.cursor, self.jobs, self.window = [None] * 5
        self.location, self.description, self.web, self.category = [None] * 4
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
        self.loc_filter = QPushButton("Filter Location")
        self.loc_filter.setCheckable(True)
        main_layout.addWidget(self.loc_filter)
        self.company_filter = QPushButton("Filter Company")
        self.company_filter.setCheckable(True)
        main_layout.addWidget(self.company_filter)
        tech_list = ['python', 'java', 'javascript', 'golang', 'devops', 'database']
        self.tech_box = QComboBox(self)
        self.tech_box.addItems(tech_list)
        self.tech_label = QLabel(self)
        main_layout.addWidget(self.tech_box)
        self.tech_box.move(50, 150)
        self.setLayout(main_layout)
        get_next.pressed.connect(self.show_next_job)
        self.loc_filter.pressed.connect(self.initiate_filter)
        self.company_filter.pressed.connect(self.initiate_filter)
        self.tech_box.currentIndexChanged[str].connect(self.tech_choice)

    # Show Next Job Push Button
    def show_next_job(self):
        self.data_item_displayed += 1
        self.current_data = self.data_to_display[self.data_item_displayed]
        self.title_display.addItem(remove_characters(self.current_data['title']))
        self.com_display.addItem(self.current_data['company'].get('display_name'))

    # Handles Technology Drop-Down Menu
    def tech_choice(self, text):
        self.filter = displayData
        self.connection = sqlite3.connect("jobs.db")
        self.cursor = self.connection.cursor()
        self.jobs, self.location = self.filter.get_filtered_menu(self.cursor, text, "title", "jobs", "title",
                                                                 "location", "title")
        self.window = displayData.TestWindow()
        self.window.display_data(self.jobs, self.location, "Location:")
        self.window.show()

    # Determines Which Filter Push Button was Pressed
    def initiate_filter(self):
        if self.company_filter.isChecked():
            self.filter_items("Company:", "title", "jobs",
                              "company", "description", "company", "Description:")
            self.company_filter.setChecked(False)
        elif self.loc_filter.isChecked():
            self.filter_items("Location:", "title", "jobs",
                              "location", "web_address", "location", "Web Address:")
            self.loc_filter.setChecked(False)

    # Filters and Displays New Data
    def filter_items(self, name: str, selection: str, table: str, filter_in: str, selection_two: str,
                     filter_two_in: str, category_type: str):
        self.filter = displayData
        self.connection = sqlite3.connect("jobs.db")
        self.cursor = self.connection.cursor()
        self.jobs, self.category = self.filter.get_filtered_data(self.cursor, name, selection, table,
                                                                 filter_in, selection_two, filter_two_in)
        self.window = displayData.TestWindow()
        self.window.display_data(self.jobs, self.category, category_type)
        self.window.show()


# Displays Initial Window Data (JobsWindow)
def display_data(to_display):
    window = JobsWindow(to_display)
    return window


# Connects to Adzuna API
def get_data(location):
    response = requests.get(location)
    if response.status_code != 200:
        return []
    data = response.json()
    return data['results']


# Cleans Up Data Format and Saves Results to Jobs Database
def save_data(jobs: list, cursor: sqlite3.Cursor):
    for job in jobs:
        job['title'] = remove_characters(job['title'])
        job['description'] = remove_characters(job['description'])
        cursor.execute("INSERT INTO jobs(company, description, web_address, location, title) "
                       "VALUES (?,?,?,?,?);",
                       (job['company'].get('display_name'), job['description'], job['redirect_url'],
                        job['location'].get('display_name'), job['title']))


# Create Jobs Table
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


# Save Data to Text File
def write_data(to_file):
    with open('data.txt', 'w') as f:
        json.dump(to_file, f)


# Retrieves JSON Data from Website
def get_jobs_data():
    jobs_list = []
    search_list = ['python', 'java', 'javascript', 'golang', 'devops', 'database']
    for element in search_list:
        loc = START_URL + element + END_URL
        print(loc)
        data = get_data(loc)
        save_to_database(data)
        jobs_list += data
    return display_data(jobs_list)


def save_to_database(data):
    print("Saving to Database...")
    write_data(data)
    write_database(data)


# Removes Unwanted Characters from Data
def remove_characters(data):
    bad_chars = ['<', '/', '>', "strong"]

    for i in bad_chars:
        data = data.replace(i, '')
    return data


def main():
    app = QApplication(sys.argv)
    window = get_jobs_data()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
