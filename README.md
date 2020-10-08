## Thomas O'Leary
# JobAPI
This project collects jobs data from the Adzuna API and displays the data with a simple GUI.
* Data can be filtered by programming language, job location or company name
* Each filter displays a new window along with additional data such as web address, description, location, etc.

# Requirements:
* sqlite3, PyQT5, Python 3.7

# Files:
    > getJobsData - Main file, collects data and displays to initial GUI window
    > displayData - Provides pop up windows for displaying filtered data

# Potential Improvements:
* Create a separate function to create/save the database so that it is not repopulated with the same data
* Create a separate function which allows the user to populate new tables with specific parameters 
* Write more tests
* Modify the JobsWindow() __init__ method for better readability and cleanliness 
* Improve filters to retrieve and display more data
* Utilize dictionaries instead of lists, allowing for primary key access displaying data specific to a single job title
* Handle filtered searches for companies and locations that do not exist within the database
