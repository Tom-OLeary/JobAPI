from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
import sqlite3
import getJobsData


class TestWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QtWidgets.QHBoxLayout()
        self.list_control = QtWidgets.QListWidget()
        self.list_control.itemClicked.connect(self.item_clicked)
        self.connection, self.cursor, self.data, self.window = [None] * 4
        main_layout.addWidget(self.list_control)
        data_display_layout = QtWidgets.QVBoxLayout()
        main_layout.addItem(data_display_layout)
        self.setLayout(main_layout)

    def display_data(self, jobs_data: list):
        for job in jobs_data:
            self.current_item = QtWidgets.QListWidgetItem(job, self.list_control)
            self.current_item.setData(Qt.UserRole, job)

    def item_clicked(self, item):
        self.connection = sqlite3.connect("jobs.db")
        self.cursor = self.connection.cursor()
        self.data = get_info(self.cursor, item)
        self.window = TestWindow()
        self.window.display_data(self.data)
        self.window.show()


def get_filtered_loc(cursor: sqlite3.Cursor):
    location, location_ok = QtWidgets.QInputDialog.getText(None, "Choose Location",
                                                                 "Choose Location to Filter")
    sql_select = f"SELECT title FROM jobs WHERE location LIKE '%{location}%';"
    results = cursor.execute(sql_select)
    return results


def get_filtered_company(cursor: sqlite3.Cursor):
    company, company_ok = QtWidgets.QInputDialog.getText(None, "Choose Company",
                                                         "Choose Company to Filter")
    sql_select = f"SELECT title FROM jobs WHERE company LIKE '%{company}%';"
    results = cursor.execute(sql_select)
    return results


def get_filtered_menu(cursor: sqlite3.Cursor, text):
    results = []
    sql_select = f"SELECT title FROM jobs WHERE title LIKE '%{text}%';"
    cursor.execute(sql_select)
    for row in cursor.fetchall():
        jobs_data = getJobsData.remove_characters(row[0])
        job_titles = "".join(jobs_data)
        results.append(job_titles)
    return results


def get_info(cursor: sqlite3.Cursor, item):
    sql_select = f"SELECT company FROM jobs WHERE title LIKE '%{str(item.text())}%';"
    results = cursor.execute(sql_select)
    return results
