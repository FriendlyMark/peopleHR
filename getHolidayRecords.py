import http.client
import json
import pandas as pd
from datetime import datetime

# read employee details
employees = pd.read_csv('API\employees.csv')

# define the date ramge
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

# Initialize a list to store the results
results_list = []
# call for each ID
for id in employees['employeeid']:

    payload = json.dumps(
        {
        "APIKey": "get ur own",
        "Action": "GetHolidayDetail",
        "EmployeeId": id,
        "StartDate": start_date,
        "EndDate": end_date
    }
    )
    # make request
    conn.request("POST", "//Holiday", payload, headers)
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



headers = [
"employeeID",
"AnnualLeaveTxnId",
"StartDate",
"EndDate",
"DurationType",
"DurationInDays",
"DurationInMinutes",
"DurationInDaysThisPeriod",
"DurationInMinutesThisPeriod",
"Approver",
"Status"
]

headers = [i for i in headers]
df = df.loc[:, headers]



print("( ´･･)ﾉ(._.`)")
