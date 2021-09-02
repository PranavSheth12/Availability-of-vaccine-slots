import requests
import json
import datetime
import csv
import os
from twilio.rest import Client

today = datetime.date.today().strftime("%d-%m-%Y")

csv_file = open('cowin_slots.csv','a+',newline="")
csv_writer = csv.writer(csv_file)
# csv_writer.writerow(['Name','pincode','Vaccine','Availability'])

pincode = input ("Enter your pincode : ")

r = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=' + pincode  +'&date='+today)
CoData = json.loads(r.text)
centers = CoData['centers']

for i in centers:
    # print(i)
    name = i['name']
    print(name)
    s = i['sessions'][0]
    # print(s)
    capacity = s['available_capacity']
    vaccine = s['vaccine']
    print(f"Vaccine : {vaccine}")
    print(f"Available slots : {capacity} ")
    print(" ")

    csv_writer.writerow([name,pincode,vaccine,capacity])

    if capacity > 0:
        account_sid = 'ACd035539dfa3d15dfe5878ce548b5cc19'
        auth_token = '95dd045ef80eb9478a1c881dc5b40a9d'
        client = Client(account_sid, auth_token)

        message = client.messages \
                        .create(
                            body=f"Hey, {capacity} {vaccine} vaccine slots are availabe at {name}.",
                            from_='+12242796914',
                            to='+919328692590'
                        )


csv_file.close()