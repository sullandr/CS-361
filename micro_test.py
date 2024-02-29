#test program that calls the micro service and displays the information returned by the micro service
#communication occurs via http from a get request. the service has a pre-compiled list of cities and states
#in the format "city,state" . it will randomly generate a number based on the number of cities in the list
#whatever city corresponds with that number will be selected and then returned to the test program. the test
#program will then spit out the information that is sent back. The information is sent in json format.
# python -m http.server
import requests

micro_server = 'http://127.0.0.1:5000/companies'

response = requests.get(micro_server)
code = response.json()

print(code)