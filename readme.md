# Final Project

## Overview:
+ Data Source: Home Sensor data [.txt files with lists in it]
+ Result of project:
  + ETL - Extracting data from .txt, tranforming those into serilized data and loading into CSV file.
  + Data cleaning - cleaning data and dividing it into different types. Also ignoreing data with unxexpected time occurence.
  + Data Sampling - Resample data and interpolate on montly, weekly and daily bases.
  + API application - created flask application:
    + getDataHour - Gives average data of the hour of a particular day.
    + getDataDay - Gives average data of a particular day.
    + compare temperature: uses above links to get api of homesensor data and api.worldweatheronline.com for historical weather data.
        + compareHour - compare average hour home temperature data with weather that day.
        + compareDay - compare average day home temperature data with weather that day.


## Big Data Processing:

### 1. ETL and Data cleaning:
#### Execution and Explanation:
Since there were lot of files in one folder(actual data source - HOMESENSOR) I have used `os` library to go though each .txt file in the directory. 
```python
  for r,d,f in os.walk(path):
    #following variables will be used when setting headers
    prheader = 0
    ptheader = 0
    tdheader = 0
    ssheader = 0
    otheader = 0
    for file in f:
		readfile = open(os.path.join(r, file), 'r')
		filelines = readfile.read().split('\n')
      # logic - see below code
    readfile.close()
```
The following ETL is done on entire data source and also creates file with data pertainling within the dates given at the runtime
```
python3 json_to_CSV.py 2019-01-31 2019-03-30
```

Every line in each file has list (you can also say json) which starts with `{` but some lines may start with something other than that. That would be compile time error of the home sensors. Not only that some values of keys in this list may be missing, null, or even garbage as we cannot check each and every keys of each list of each file we need to make decision on what bases we want to clean our data. Since further I am going to resample this data and also use this data to build flask application which works on datetime, I will clean this data on `pitime` field. pitime is time and date msg was received by server. The list in this data house are of 3 main different types: `print_reading`, `trigger_data` and `system_data`. So I have created 3 different json list and 3 different CSV files for each type and also 1 extra for others, if there were any other type of data found.
```python
i = len(filelines)
j = 1
for line in filelines:
  if j >= i:
    break
  j+=1
  cleanline = line[line.find('{'):]
  l = json.loads(cleanline)
  print(str(l["pitime"][:2]))
  if str(l["pitime"][:2]) != '20':
      continue
  if l["type"] == 'print_reading':
    compdate = datetime.strptime(l["pitime"].split("T")[0]+ " " + str(l["pitime"].split("T")[1][1:].split(".")[0]), '%Y-%m-%d %H:%M:%S')
    l["pitime"] = compdate
    print_reading.append(l)
    if startd <= compdate <= endtd:
      print_reading_dt.append(l)
  elif l["type"] == 'trigger_data':
    trigger_data.append(l)
  elif l["type"] == 'system_start':
    system_start.append(l)
  else:
    others.append(l)
```
Setting header was another difficult part as the above loop is reading data from 338 files and the header for those 4 types are different, so I can't simply put logic to write header when this loop runs for the first time. I can't also use the logic that when 1 file is done reading then write the header in those 4 CSV files as there is no gurantee to say whether I found data(header) for `trigger_data` in just after first file. So I used few flags to do so, when I found 1st data for each type then write the header and set the flag to false after that. To write actual header I have created function that will write header/data and/or create file(see code after writing data section).
```python
if len(print_reading) == 1 and prheader == 0:
  write_file(print_reading,'Print_Reading.csv',0)
  prheader = 1

if len(print_reading_dt) == 1 and ptheader == 0:
  write_file(print_reading_dt,'Print_Reading_DT.csv',0)
  ptheader = 1
  
if len(trigger_data) == 1 and tdheader == 0:
  write_file(trigger_data,'Trigger_Data.csv',0)
  tdheader = 1

if len(system_start) == 1 and ssheader == 0:
  write_file(system_start,'System_Start.csv',0)
  ssheader = 1

if len(others) == 1 and otheader == 0:
  write_file(others,'Others.csv',0)
  otheader = 1
```
Writing data in file may take significant amount of time. So I used buffer to do so, that will write json list when it's lenght is 500 or its end of the file. Also I ccreated a function to actually write header and or data in the CSV files.
```python
if len(print_reading) == 500 or j>=i:
  write_file(print_reading,'Print_Reading.csv',1)
  del print_reading[:]
if len(print_reading_dt) == 500 or j>=i:
  write_file(print_reading_dt,'Print_Reading_DT.csv',1)
  del print_reading_dt[:]
if len(trigger_data) == 500 or j>=i:
  write_file(trigger_data,'Trigger_Data.csv',1)
  del trigger_data[:]
if len(system_start) == 500 or j>=i:
  write_file(system_start,'System_Start.csv',1)
  del system_start[:]
if len(others) == 500 or j>=i:
  write_file(others,'Others.csv',1)
  del others[:]
```
Write file function is below. Paramters:
+ List/data
+ File name
+ Flags: 2: Create CSV, 1: write json list into CSV, 0: write header into CSV.

```python
def write_file(json_list, file_name, c):
	if c == 2:
		data_file = open(file_name, 'w')
		csv_writer = csv.writer(data_file)
		data_file.close()
		return
	data_file = open(file_name, 'a')
	csv_writer = csv.writer(data_file)
	for row in json_list:
		if c == 0:
			csv_writer.writerow(row.keys())
		else:
			csv_writer.writerow(row.values())
	data_file.close()
```

There is another way to write json list into CSV file using pandas, but it takes significance amount of time and I also data inconsistancy and data loss with those CSV files.
```python
pandas.read_json(json.dumps(print_reading)).to_csv('P_PrintReading.csv', index= None, header= True)
```

#### Purpose/Application:
__Big data processing is very significant these days. There are sotwares/applications which handles enterprice level big data but this give us ability of understand what happends behind the scene. Null or garbage data from data soruces are no suprise in these big data so cleaning data becomes significantly important for future use or analysis.__

### 2. Data Sampling:
#### Execution and Explanation:
#### Purpose/Application:

### 3. Flask Application for API:
#### Execution and Explanation:
The Flask application has 5 endpoints and one home(root).
##### 1. Home - Root:
At this endpoint `Home.html` file is rendered and this .html file contains API and endpoint documentation
```python
@app.route("/")
def root():
    return render_template('home.html')
```
Result at: `http://127.0.0.1:5000/`
![Home]('images/../images/flaskhome.png')

 ##### 2. 
#### Purpose/Application: