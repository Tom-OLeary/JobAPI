"""Testing for getJobsData and displayData Functions"""

# testsAPI.py

import os.path
import sqlite3
import getJobsData
import displayData

URL = getJobsData.START_URL + getJobsData.END_URL


def test_get_data():
    test_location = URL
    test_results = getJobsData.get_data(test_location)
    assert len(test_results) > 0


def test_get_bad_data():
    test_location = getJobsData.START_URL + "xxxyyyyy" + getJobsData.END_URL
    test_results = getJobsData.get_data(test_location)
    assert type(test_results) == list
    assert len(test_results) == 0


def test_write_database():
    test_location = URL
    test_data = getJobsData.get_data(test_location)
    getJobsData.write_database(test_data)
    assert os.path.exists('jobs.db')


def test_write_bad_database():
    test_location = getJobsData.START_URL + "xxxyyyyy" + getJobsData.END_URL
    test_data = getJobsData.get_data(test_location)
    test_results = getJobsData.write_database(test_data)
    assert test_results is None


def test_tech_filter():
    text = 'python'
    connection = sqlite3.connect("jobs.db")
    cursor = connection.cursor()
    sql_select = f"SELECT title FROM jobs WHERE title LIKE '%{text}%';"
    cursor.execute(sql_select)
    jobs_data = cursor.fetchone()
    substring = 'Python'

    assert substring in jobs_data[0]


def test_collect_filtered_data():
    connection = sqlite3.connect("jobs.db")
    cursor = connection.cursor()
    results = displayData.collect_filtered_data(cursor, "title", "jobs", "company", "Capita")
    assert len(results) > 0


def test_get_filtered_menu():
    connection = sqlite3.connect("jobs.db")
    cursor = connection.cursor()
    results, category_list = displayData.get_filtered_menu(cursor, "javascript", "title", "jobs", "title",
                                                           "location", "title")
    substring = 'JavaScript'
    substring_two = 'python'
    assert substring in results[0]
    assert substring_two not in results
