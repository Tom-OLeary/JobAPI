from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
import sqlite3


class TestWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QtWidgets.QHBoxLayout()
        title_label = QtWidgets.QLabel("Job Title:")
        self.main_layout.addWidget(title_label)
        self.list_control = QtWidgets.QListWidget()
        self.connection, self.cursor, self.data, self.window = [None] * 4
        self.main_layout.addWidget(self.list_control)
        data_display_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addItem(data_display_layout)
        self.setLayout(self.main_layout)
        self.list_control.itemClicked.connect(self.item_clicked)

    # Displays Filtered Data to New Window
    def display_data(self, jobs_data: list, filter_data: list, category_type):
        self.category_label = QtWidgets.QLabel(category_type)
        self.main_layout.addWidget(self.category_label)
        self.category_display = QtWidgets.QListWidget()
        self.main_layout.addWidget(self.category_display)
        for job, category in zip(jobs_data, filter_data):
            self.current_item = QtWidgets.QListWidgetItem(job, self.list_control)
            self.category_item = QtWidgets.QListWidgetItem(category, self.category_display)
            self.current_item.setData(Qt.UserRole, job)
            self.category_item.setData(Qt.UserRole, category)

    def item_clicked(self, item):
        self.connection = sqlite3.connect("jobs.db")
        self.cursor = self.connection.cursor()
        self.data, self.category = get_info(self.cursor, item, "company", "jobs", "title", "web_address", "title")
        self.window = TestWindow()
        self.window.display_data(self.data, self.category, "Web Address")
        self.window.show()


# Handles Data from Location and Company Push Buttons
def get_filtered_data(cursor: sqlite3.Cursor, category_type, selection, table, filters,
                      selection_two, filters_two):
    category, category_ok = QtWidgets.QInputDialog.getText(None, "Choose " + category_type,
                                                           "Choose " + category_type + " to Filter")
    results = collect_filtered_data(cursor, selection, table, filters, category)
    category_list = collect_filtered_data(cursor, selection_two, table, filters_two, category)
    return results, category_list


# Retrieves Specific Data from the Jobs Database
def collect_filtered_data(cursor: sqlite3.Cursor, selection, table, filters, category):
    results = []
    sql_select = f"SELECT {selection} FROM {table} WHERE {filters} LIKE '%{category}%';"
    cursor.execute(sql_select)
    for row in cursor.fetchall():
        jobs_data = row[0]
        results.append(jobs_data)
    return results


# Handles Selection from Technology Drop-Down Menu
def get_filtered_menu(cursor: sqlite3.Cursor, text, selection, table, filters, selection_two, filters_two):
    results = collect_filtered_data(cursor, selection, table, filters, text)
    category_list = collect_filtered_data(cursor, selection_two, table, filters_two, text)
    return results, category_list


# Collects Data Pertaining to a Clicked Title Name
def get_info(cursor: sqlite3.Cursor, item, selection, table, filters, selection_two, filters_two):
    tmp = item.text()
    results = collect_filtered_data(cursor, selection, table, filters, tmp)
    category_list = collect_filtered_data(cursor, selection_two, table, filters_two, tmp)
    return results, category_list
