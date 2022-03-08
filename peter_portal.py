import requests
import json 

current_quarter = '2020 Spring'
current_term = '2022%Spring'

# !Professors COMPSCI 161 -> {Professors}
def get_professors(department, course_number):
    professors = []
    current_term = '2022%22Spring'

    # update the department to insert correctly into URL
    if department.lower() == 'i&csci':
        department = 'I%26C%20SCI'
    elif department.lower() == 'crm/law':
        department = 'CRM%2FLAW'

    # make the response and fetch the data in JSON
    response = requests.get('https://api.peterportal.org/rest/v0/schedule/soc?term=' + current_term + '&department=' + department + '&courseNumber=' + course_number)
    json_data = json.loads(response.text)

    # parse through the data, appending it to the list of professors if the length of the list of instructors = 1 
    # (preventing uplicates due to TAs)
    for section in json_data['schools'][0]['departments'][0]['courses'][0]['sections']:
        if len(section['instructors']) == 1:
            professors.append(section['instructors'][0])
    
    return set(professors)

# !Courses Richard Pattis -> [Courses]
def get_courses(first_name, last_name):
    # make the response and fetch the data in JSON
    response = requests.get("https://api.peterportal.org/rest/v0/instructors/all")
    json_data = json.loads(response.text)

    # if the professor matches 
    for professor in json_data:
        if first_name.lower() in professor['name'].lower() and last_name.lower() in professor['name'].lower():
            # create a list of all the courses that the professor teaches/have taught
            courses = [course for course in professor['course_history']]
    
    return courses

# !Grades Richard Pattis ICS 33 -> (year, quarter, {A: #, B: #, C: #, D: #, F: #})
def get_grades(professor_name, department, course_number):
    # split professor name into list by spaces
    professor_name_list = professor_name.split(' ')

    # update the department to insert correctly into URL
    if department.lower() == 'i&csci':
        department = 'I%26C%20SCI'
    elif department.lower() == 'crm/law':
        department = 'CRM%2FLAW'

    # first get all the available years for grade distribution
    response = requests.get('https://api.peterportal.org/rest/v0/grades/calculated?instructor=' + professor_name_list[-1].upper() + ',%20' + professor_name_list[0][0] + '.&department=' + department + '&number=' + course_number)

    # get the most recent year
    json_data = json.loads(response.text)
    year = json_data['courseList'][-1]['year']
    quarter = json_data['courseList'][-1]['quarter']
    
    # parse through the information
    response = requests.get('https://api.peterportal.org/rest/v0/grades/calculated?year=' + year + '&instructor=' + professor_name_list[-1].upper() + ',%20' + professor_name_list[0][0] + '.&department=' + department + '&quarter=' + quarter + '&number=' + course_number)

    # return the most recent year and the list of grade distribution
    json_data = json.loads(response.text)
    return (json_data['courseList'][0]['year'], json_data['courseList'][0]['quarter'], json_data['gradeDistribution'])