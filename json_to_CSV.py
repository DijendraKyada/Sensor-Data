import os, time, json, csv, pandas, sys
from datetime import datetime

#create buffer - limit-500 lines-> and then append fife -> Store it as pandas df -> resample at some timeframe and save it to CSV
#-> Next: Date time-Create new CSV
#try : json


#order file, convert the json to df, do filtering, append (use pandsas) new df to existing file
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

print_reading = []
print_reading_dt = []
trigger_data = []
system_start = []
others = []
write_file(print_reading, 'Print_Reading.csv', 2)
write_file(print_reading_dt, 'Print_Reading_DT.csv', 2)
write_file(trigger_data, 'Trigger_Data.csv', 2)
write_file(system_start, 'System_Start.csv', 2)
write_file(others, 'Others.csv', 2)
start = time.time()
path = '/Users/dijendrakyada/OneDrive - clarkson.edu/Clarkson/Big_Data/Final-Project/DataSource.txt/'
startd = datetime.strptime(sys.argv[1], '%Y-%m-%d')
endtd = datetime.strptime(sys.argv[2], '%Y-%m-%d')
for r,d,f in os.walk(path):
	k = 1
	prheader = 0
	ptheader = 0
	tdheader = 0
	ssheader = 0
	otheader = 0
	for file in f:
		readfile = open(os.path.join(r, file), 'r')
		filelines = readfile.read().split('\n')
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
		readfile.close()
		k+=1
print(time.time() - start)
#print('end')
#pandas.read_json(json.dumps(print_reading)).to_csv('P_PrintReading.csv', index= None, header= True)
#create_file(print_reading, 'Print_Reading.csv')
#pandas.read_json(json.dumps(trigger_data)).to_csv('P_TriggerData.csv', index= None, header= True)
#create_file(trigger_data, 'Trigger_Data.csv')
#pandas.read_json(json.dumps(system_start)).to_csv('P_SystemStart.csv', index= None, header= True)
#create_file(system_start, 'System_Start.csv')
#pandas.read_json(json.dumps(others)).to_csv('P_Others.csv', index= None, header= True)
#create_file(others, 'Others.csv')
