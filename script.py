""""
This script scrapes course details from the University of Bologna's course unit catalogue.
Made for easier searching and filtering of courses based on specific words mentioned in the course description.
"""

import requests
from bs4 import BeautifulSoup
import time
import json
from loguru import logger

# Function to extract course details from a course URL
def extract_course_details(course_url: str) -> dict:
    try:
        response = requests.get(course_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Initialize a dictionary to store course details
        course_details = {
            'course_url': course_url,
            'description': 'Not Available'
        }

        # Extract course description from the specific div
        description_div = soup.find('div', class_='description-text')
        if description_div:
            course_details['description'] = description_div.text.strip()

        return course_details

    except Exception as e:
        logger.error(f"Error fetching details for {course_url}: {e}")
        return {'course_url': course_url, 'description': 'Error'}
    
def find_courses(base_url: str, params: dict) -> list:
    # Initialize a list to store all courses
    courses = []

    while True:
        # Send a GET request to the current page
        response = requests.get(base_url, params=params)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all course list items
        course_list = soup.find_all('li', class_='mainteaching')
        if not course_list:  # If no courses are found, we've reached the last page
            break

        for course in course_list:
            course_name = course.find('span', class_='teachingname').text.strip()
            try:
                credits = course.find('span', class_='cfu').text.strip().replace('Credits: ', '')
            except:
                logger.error(f"{course_name} does not have credits, {type(course.find('span', class_='cfu'))}")  
            teacher = course.find('span', class_='teacher').text.strip() if course.find('span', class_='teacher') else "Not Available"
            
            # Safe extraction of course URL
            course_url_tag = course.find('span', class_='teachingname').find('a')
            course_url = course_url_tag.get('href') if course_url_tag else "Not Available"

            # Initialize variables to handle potential missing elements
            area = campus = program_info = timetable = timetable_link = "Not Available"

            # Search for div elements by keyword
            divs = course.find_all('div')
            for div in divs:
                text = div.text.strip()
                if text.startswith("Area:"):
                    area = text.replace("Area:", "").strip()
                elif text.startswith("Campus of"):
                    campus = text.replace("Campus of", "").strip()
                elif "degree programme" in text:
                    program_info = text.strip()

            # Extract the timetable details
            schedule = course.find('p', class_='schedule')
            if schedule:
                timetable = schedule.text.strip()
                timetable_link = schedule.find('a').get('href') if schedule.find('a') else "Not Available"
            
            courses.append({
                'name': course_name,
                'teacher': teacher,
                'credits': credits,
                'area': area,
                'campus': campus,
                'program_info': program_info,
                'timetable': timetable,
                'timetable_link': timetable_link,
                'course_url': course_url,
                'description': ''
            })

        # Print the current page number to track progress
        logger.info(f"Scraped page {params['pagenumber']}")

        # Move to the next page
        params['pagenumber'] += 1

        # Pause to avoid overloading the server
        time.sleep(1)

    for course in courses:
        course_url = course['course_url']
        if course_url == 'Not Available':
            logger.warning(f"Skipping course without URL: {course['name']}")
            continue

        logger.info(f"Processing {course['name']}")
        details = extract_course_details(course_url)
        course['description'] = details['description']
    return courses


if __name__ == "__main__":
    # Base URL structure for pagination
    base_url = 'https://www.unibo.it/en/study/phd-professional-masters-specialisation-schools-and-other-programmes/course-unit-catalogue'

    params = {
        # For a full parameter list check the url after doing a search from the base url. 
        'pagenumber': 1,
        'pagesize': 100,  # Number of courses per page (adjust if needed)
        'order': 'asc',
        'sort': 'title',
        'codiceCampus': 'bologna',
        'search': 'True',
        'DescInsegnamentoButton': 'cerca',
        'descrizioneMateria': '',
        'codiceAmbito': 1,  # 4: Engineering and Architecture, 
                            # 9: Science
                            # 1: Economics
        'linguaInsegnamento': 'english',
        'codiceTipoCorso': '',
        'annoAccademico': 2024
    }
    
    courses = find_courses(base_url, params)


    output_file = 'Economics.json'
    logger.info(f"Scraped a total of {len(courses)} courses")

    with open(output_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(courses, jsonfile, indent=4, ensure_ascii=False)
    logger.info("Data saved successfully")
