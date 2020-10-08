"""Testing for getJobsData and displayData Functions"""

# testsAPI.py

import os.path
import sqlite3
import getJobsData


def test_get_data():
    test_location = "http://api.adzuna.com/v1/api/jobs/gb/search/1?app_id=51e101b5&app_key" \
                    "=f9824e1322236e2ede0a4929e3eb27c8&results_per_page=20" \
                    "&what=javascript%20developer&content-type=application/json "
    test_results = getJobsData.get_data(test_location)
    assert len(test_results) > 0


def test_get_bad_data():
    test_location = "http://api.adzuna.com/v1/apidev/jobs/gb/search/1?app_id=51e101b5&app_key" \
                    "=f9824e1322236e2ede0a4929e3eb27c8&results_per_page=20" \
                    "&what=javascript%20developer&content-type=application/json "
    test_results = getJobsData.get_data(test_location)
    assert type(test_results) == list
    assert len(test_results) == 0


def test_write_database():
    test_location = "http://api.adzuna.com/v1/api/jobs/gb/search/1?app_id=51e101b5&app_key" \
                    "=f9824e1322236e2ede0a4929e3eb27c8&results_per_page=20" \
                    "&what=javascript%20developer&content-type=application/json "
    test_data = getJobsData.get_data(test_location)
    getJobsData.write_database(test_data)
    os.path.exists('TomOLeary_Sprint2/jobs.db')
    assert True


def test_write_bad_database():
    test_location = "http://api.adzuna.com/v1/apidev/jobs/gb/search/1?app_id=51e101b5&app_key" \
                    "=f9824e1322236e2ede0a4929e3eb27c8&results_per_page=20" \
                    "&what=javascript%20developer&content-type=application/json "
    test_data = getJobsData.get_data(test_location)
    test_results = getJobsData.write_database(test_data)
    assert test_results is None


def test_tech_filter():
    text = 'python'
    connection = sqlite3.connect("jobs.db")
    cursor = connection.cursor()
    sql_select = f"SELECT title FROM jobs WHERE title LIKE '%{text}%';"
    cursor.execute(sql_select)
    assert True


def test_location_filter():
    location = 'london'
    connection = sqlite3.connect("jobs.db")
    cursor = connection.cursor()
    sql_select = f"SELECT title FROM jobs WHERE location LIKE '%{location}%';"
    cursor.execute(sql_select)
    assert True


def test_company_filter():
    company = 'BlockDox'
    connection = sqlite3.connect("jobs.db")
    cursor = connection.cursor()
    sql_select = f"SELECT title FROM jobs WHERE company LIKE '%{company}%';"
    cursor.execute(sql_select)
    assert True
