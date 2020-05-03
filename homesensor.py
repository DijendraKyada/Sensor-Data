#key = '0cade1f7eea64fb885a221156200205'
#http://api.worldweatheronline.com/premium/v1/past-weather.ashx?q=13676&date=2009-07-20&enddate=2009-07-21&key=0cade1f7eea64fb885a221156200205
import json, csv, pandas as pd, numpy as np, requests
from flask import Flask, render_template
from flask import request,redirect
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route("/")
def root():
    return render_template('home.html')

@app.route("/compareDay", methods=['GET','POST'])
def compareDay():
    date = request.args.get('date')
    response = requests.get("http://127.0.0.1:5000/getDataDay?date="+date)
    print("2")
    df = pd.read_csv('meandata.csv')
    print("3")
    tempmean = {}
    for i in range(1,10):
        col = "temp_"+str(i)
        colmean = df.loc[:,col].mean()
        tempmean[col] = colmean
        print("4-9")
    response = requests.get("http://api.worldweatheronline.com/premium/v1/past-weather.ashx?q=13676&date="+date+"&key=0cade1f7eea64fb885a221156200205")
    apidata = ET.fromstring(str(response.text))
    print("6")
    #print(apidata)
    temphr = apidata.find('weather/avgtempF').text
    #print(temphr)
    temploc = {"temp_1":"Basement center", "temp_2":"Floor 2", "temp_3":"Floor 1 (on the floor)", "temp_4":"Garage", "temp_5":"Attic crawl space", "temp_6":"Furnace output air duct", "temp_7":"Basement exterior wall", "temp_8":"Outside air temperature", "temp_9":"Floor 1 (ceiling) until 12-2019 then moved to first floor closet" }
    html = '<html><style>th, td {padding: 8px;text-align: left;border-bottom: 1px solid #ddd;}</style><body><table style="border-collapse: collapse;width: 100%;"><tr><th>Location</th><th>Description</th><th>Temperature</th><th>Temperature outside</th><th>Result</th></tr>'
    for key,value in tempmean.items():
        print("8")
        html+='<tr><td>'+str(key)+'</td><td>'+temploc[key]+'</td><td>'+str(round(value,1))+'</td><td>'+str(temphr)+'</td>'
        if int(value) > int(temphr):
            html += '<td style="color:white;background-color:red">Hotter than outside</td></tr>'
        else:
            html += '<td style="color:white;background-color:blue">Colder than outside or similar</td></tr>'
    html+= '</table></body></html>'
    return html

@app.route("/compareHour", methods=['GET','POST'])
def comparehour():
    date = request.args.get('date')
    hour = request.args.get('hour')
    response = requests.get("http://127.0.0.1:5000/getDataHour?date="+date+"&hour="+hour)
    print("2")
    #print(response.text)
    df = pd.read_csv('meandata.csv')
    print("3")
    tempmean = {}
    for i in range(1,10):
        col = "temp_"+str(i)
        colmean = df.loc[:,col].mean()
        tempmean[col] = colmean
        print("4-9")
    hr = 0
    for hrr in range(0, 22, 3):
        print("5-8")
        hour = int(hour)
        if hour == (hrr-1):
            hr= hrr
            break
        elif hour == hrr:
            hr= hrr
            break
        elif hour == (hrr+1):
            hr = hrr
            break
        else:
            pass
    response = requests.get("http://api.worldweatheronline.com/premium/v1/past-weather.ashx?q=13676&date="+date+"&key=0cade1f7eea64fb885a221156200205")
    apidata = ET.fromstring(str(response.text))
    print("6")
    #print(apidata)
    for hourly in apidata.findall('weather/hourly'):
        time = int(int(hourly.find('time').text)/100)
        print("7")
        if time == hr:
            #print(time)
            temphr = hourly.find('tempF').text
            #print(temphr)
    temploc = {"temp_1":"Basement center", "temp_2":"Floor 2", "temp_3":"Floor 1 (on the floor)", "temp_4":"Garage", "temp_5":"Attic crawl space", "temp_6":"Furnace output air duct", "temp_7":"Basement exterior wall", "temp_8":"Outside air temperature", "temp_9":"Floor 1 (ceiling) until 12-2019 then moved to first floor closet" }
    html = '<html><style>th, td {padding: 8px;text-align: left;border-bottom: 1px solid #ddd;}</style><body><table style="border-collapse: collapse;width: 100%;"><tr><th>Location</th><th>Temperature</th><th>Temperature outside</th><th>Result</th></tr>'
    html = '<html><style>th, td {padding: 8px;text-align: left;border-bottom: 1px solid #ddd;}</style><body><table style="border-collapse: collapse;width: 100%;"><tr><th>Location</th><th>Description</th><th>Temperature</th><th>Temperature outside</th><th>Result</th></tr>'
    for key,value in tempmean.items():
        print("8")
        html+='<tr><td>'+str(key)+'</td><td>'+temploc[key]+'</td><td>'+str(round(value,1))+'</td><td>'+str(temphr)+'</td>'
        if int(value) > int(temphr):
            html += '<td style="color:white;background-color:red">Hotter than outside</td></tr>'
        else:
            html += '<td style="color:white;background-color:blue">Colder than outside or similar</td></tr>'
    html+= '</table></body></html>'
    return html

@app.route("/getDataHour", methods=['GET','POST'])
def getdatahour():
    date = request.args.get('date')
    hour = request.args.get('hour')
    reader = csv.DictReader(open("Print_Reading.csv"))
    file = open('meandata.csv','w+')
    file.close()
    i = 1
    j = 1
    for line in reader:
        if i ==1:
            file = open('meandata.csv','a+')
            writer = csv.writer(file)
            writer.writerow(line.keys())
            file.close()
            i = 0
        rdate = line['pitime'].split(' ')[0]
        if rdate == date:
            print("rdate", rdate)
            rhour = line['pitime'].split(' ')[1][:2]
            if rhour == hour:
                j+=1
                file = open('meandata.csv','a+')
                writer = csv.writer(file)
                writer.writerow(line.values())
                file.close()
                if j == 60:
                    break
    df = pd.read_csv('meandata.csv')
    mean = df.mean(axis = 0).to_json()
    print("1")
    return mean

@app.route("/getDataDay", methods=['GET','POST'])
def getdataday():
    date = request.args.get('date')
    reader = csv.DictReader(open("Print_Reading.csv"))
    file = open('meandata.csv','w+')
    file.close()
    i = 1
    j = 1
    for line in reader:
        if i ==1:
            file = open('meandata.csv','a+')
            writer = csv.writer(file)
            writer.writerow(line.keys())
            file.close()
            i = 0
        rdate = str(line['pitime'].split(' ')[0])
        if rdate == date:
            print("rdate", rdate)
            j+=1
            file = open('meandata.csv','a+')
            writer = csv.writer(file)
            writer.writerow(line.values())
            file.close()
            if j == 1440:
                break
    df = pd.read_csv('meandata.csv')
    mean = df.mean(axis = 0).to_json()
    print("1")
    return mean

if __name__ == "__main__":
    app.run(host='127.0.0.1',debug=True)