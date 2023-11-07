import http.client
import json
import pandas as pd
import string
import re

# formulate call
conn = http.client.HTTPSConnection("api.peoplehr.net")
payload = json.dumps({
  "APIKey": "get ur own",
  "Action": "GetAllEmployeeDetail",
  "IncludeLeavers": False
})

headers = {
  'Content-Type': 'application/json',
  'Content-Type': 'application/json'
}

# make request
conn.request("POST", "//Employee", payload, headers)
res = conn.getresponse()

# format
data = res.read().decode("utf-8")
data_json = json.loads(data)
result = data_json.get("Result")

# enter into dataframe
df = pd.json_normalize(result)

# Define a function to extract "DisplayValue" from nested structures
def extract_display_value(item):
    if isinstance(item, dict):
        return item.get("DisplayValue")
    elif isinstance(item, list):
        return [extract_display_value(subitem) for subitem in item if subitem == "DisplayValue"]
    else:
        return item
    
df = df.applymap(extract_display_value)

# format dataframe

def column_names(column_name):
    # Convert to lowercase
    column_name = column_name.lower()

    # Remove prefixes and suffixes using regular expressions
    column_name = re.sub(r'^employmentdetail|displayvalue$', '', column_name)

    # Remove punctuation
    column_name = ''.join(char for char in column_name if char not in string.punctuation)

    return column_name

df.columns = [column_names(col) for col in df.columns]

headers = [
"UniqueKey",
"EmployeeId",
"FirstName",
"LastName",
"KnownAs",
"StartDate",
"DateOfBirth", 
"JobRole",
"Department", 
"ReportsTo",
"ReportsToEmailAddress",
"EmploymentType", 
"HolidayAllowanceDays",
"AnalysisCode2LabelText", 
"TimeAndAttendanceID"
]

headers = [i.lower() for i in headers]
df = df.loc[:, headers]

df.to_csv('./api/employees.csv', index=False)

print("(❁´◡`❁)")
