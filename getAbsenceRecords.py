import http.client
import json
import pandas as pd
from datetime import datetime

# read employee details 
employees = pd.read_csv('API\employees.csv')

# define the end date 
current_date = datetime.now()
date_string = current_date.strftime("%d-%m-%Y")

# formulate call
conn = http.client.HTTPSConnection("api.peoplehr.net")

headers = {
  'Content-Type': 'application/json',
  'Content-Type': 'application/json'
}

# Initialize a list to store the results
results_list = []
# call for each ID
for id in employees['employeeid']:

    payload = json.dumps(
        {
        "APIKey": "get ur own",
        "Action": "GetAbsenceDetail",
        "EmployeeId": id,
        "StartDate": "01-01-2023",
        "EndDate": date_string
    }
    )
    # make request
    conn.request("POST", "//Employee/Absence", payload, headers)
    res = conn.getresponse()

    # format
    data = res.read().decode("utf-8")
    data_json = json.loads(data)
    result = data_json.get("Result")
    
    
    # add the employeeID if there is a valid absence record
    if len(result) > 0:
        for item in result:
            item['employeeID'] = id


    # Append the result to the list
    results_list.append(result)

df = pd.concat([pd.json_normalize(result) for result in results_list], ignore_index=True)


df.to_csv('./api/absence.csv', index=False)

print("( ´･･)ﾉ(._.`)")
