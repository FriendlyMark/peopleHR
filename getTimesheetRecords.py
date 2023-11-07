import http.client
import json
import pandas as pd
from datetime import datetime

# read employee details
employees = pd.read_csv('API\employees.csv')

# define the date range
current_date = datetime.now()
start_date = current_date.replace(month=1, day=1)
end_date = current_date.replace(month=12, day=31)
start_date = start_date.strftime("%d-%m-%Y")
end_date = end_date.strftime("%d-%m-%Y")

# formulate call
conn = http.client.HTTPSConnection("api.peoplehr.net")

headers = {
    'Content-Type': 'application/json',
    'Content-Type': 'application/json'
}

results_list = []

# call for each ID
for id in employees['employeeid']:
    
    payload = json.dumps(
        {
            "APIKey": "get ur own",
            "Action": "GetTimesheetDetail",
            "EmployeeId": id,
            "StartDate": start_date,
            "EndDate": end_date
        }
    )

    # make request
    conn.request("POST", "//Timesheet", payload, headers)
    res = conn.getresponse()

    # format
    data = res.read().decode("utf-8")
    data_json = json.loads(data)
    result = data_json.get("Result")

    # add the employeeID if there is a valid record
    if len(result) > 0:
        for item in result:
            item['employeeID'] = id

    # append result to the list
    results_list.extend(result)

df = pd.DataFrame(results_list)  # Convert the list of dictionaries to a DataFrame
selected_columns = ['employeeID', 'TimesheetDate', 'TimeIn1', 'TimeOut1', 'TimeIn2', 'TimeOut2']
df = df[selected_columns]
df.to_csv('./api/timesheets.csv', index=False)

print("ᓚᘏᗢ")
