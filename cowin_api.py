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
number = input("Enter your mobile number : ")

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
        account_sid = 'Enter your api id here'
        auth_token = 'Enter your auth token here'
        client = Client(account_sid, auth_token)

        message = client.messages \
                        .create(
                            body=f"Hey, {capacity} {vaccine} vaccine slots are availabe at {name}.",
                            from_='Enter the number from the api',
                            to=f'{number}'
                        )


csv_file.close()
