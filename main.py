import requests
import re
from bs4 import BeautifulSoup
import json

districts = {}
streets = {}
houses = {}
calendar = {}
response = requests.get('https://www.fkf.hu/hulladeknaptar',verify=False)
cookie = response.cookies
soup = BeautifulSoup(response.content, "html.parser")
job_elements = soup.find("select", id="districts")
option_elements = job_elements.select('select option')
for option in option_elements:
     value = re.findall("value=\"(\d+)\"",str(option))
     if len(value) != 0:
        #print(value[0])
        #print(option.text)
        districts[value[0]] = option.text
#print(districts)
debug_district = "1212"
print("District Selected", districts[debug_district])
street_request_header = {
    'X-October-Request-Handler': 'onSelectDistricts',
    'X-October-Request-Partials': 'ajax/publicPlaces',
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Requested-With' : 'XMLHttpRequest'
}
street_request_payload = {'district' : debug_district}
get_streets = requests.post('https://www.fkf.hu/hulladeknaptar', cookies=cookie,headers=street_request_header, data=street_request_payload,verify=False)
print("Sending Header: "+";".join(get_streets.request.headers))
print("Sending Body: "+get_streets.request.body)
print("Received Status: "+str(get_streets.status_code))
print("Received Body: ")
#print(get_streets.content)
street_option_json_result = json.loads(get_streets.content)
#print(json.dumps(street_option_json_result))
street_option_html_div = soup = BeautifulSoup(street_option_json_result['ajax/publicPlaces'], "html.parser")
street_job_elements = street_option_html_div.find("select", id="publicPlaces")
street_option_elements = street_job_elements.select('select option')
for option in street_option_elements:
     value = re.search("(value=\")(.*)(\">)(.*)(</option)",str(option))
     #if len(value) != 0:
     if value != None:
        #print(value[4])
        #print(option.text)
        streets[value[2]] = value[4]
debug_street = "Kassai---utca"
print("Street Selected", streets[debug_street])
house_request_header = {
    'X-October-Request-Handler': 'onSavePublicPlace',
    'X-October-Request-Partials': 'ajax/houseNumbers',
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Requested-With' : 'XMLHttpRequest'
}
house_request_payload = {'publicPlace' : debug_street}
get_houses = requests.post('https://www.fkf.hu/hulladeknaptar', cookies=cookie,headers=house_request_header, data=house_request_payload,verify=False)
print("Sending Header: "+";".join(get_houses.request.headers))
print("Sending Body: "+get_houses.request.body)
print("Received Status: "+str(get_houses.status_code))
print("Received Body: ")
#print(get_houses.content)
houses_option_json_result = json.loads(get_houses.content)
#print(json.dumps(street_option_json_result))
houses_option_html_div = soup = BeautifulSoup(houses_option_json_result['ajax/houseNumbers'], "html.parser")
houses_job_elements = houses_option_html_div.find("select", id="houseNumber")
houses_option_elements = houses_job_elements.select('select option')
for option in houses_option_elements:
     value = re.search("(value=\")(.*)(\">)(.*)(</option)",str(option))
     #if len(value) != 0:
     if value != None:
        #print(value[2])
        #print(value[4])
        houses[value[2]] = value[4]
debug_house = "49"
print("House Selected", houses[debug_house])
calendar_request_header = {
    'X-October-Request-Handler': 'onSearch',
    'X-October-Request-Partials': 'ajax/calSearchResults',
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Requested-With' : 'XMLHttpRequest'
}
calendar_request_payload = {'houseNumber' : debug_house}
get_calendar = requests.post('https://www.fkf.hu/hulladeknaptar', cookies=cookie,headers=calendar_request_header, data=calendar_request_payload,verify=False)
print("Sending Header: "+";".join(get_calendar.request.headers))
print("Sending Body: "+get_calendar.request.body)
print("Received Status: "+str(get_calendar.status_code))
print("Received Body: ")
#print(get_calendar.content)
calendar_option_json_result = json.loads(get_calendar.content)
#print(json.dumps(street_option_json_result))
calendar_option_html_div = soup = BeautifulSoup(calendar_option_json_result['ajax/calSearchResults'], "html.parser")
calendar_job_elements = calendar_option_html_div.select("table tbody tr")
#print(calendar_job_elements)
for row in calendar_job_elements:
    row_data = row.select("td")
    #print(row_data)
    if len(row_data) == 3:
        date = row_data[1].contents[0]
        trash_type =  row_data[2].select("div")
        if len(trash_type) > 0:
            value = re.search("(<div.*><i.*/i>)(.*)(</div)",str(trash_type))
            #print(value[2])
            calendar[date] = value[2]
print(calendar)