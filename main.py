import os, time, json, csv, pandas

#create buffer - limit-500 lines-> and then append life -> Store it as pandas df -> resample at some timeframe and save it to CSV
#-> Next: Date time-Create new CSV
#try : json

def json_to_csv(jsonfilelines):
	i = len(jsonfilelines)
	j = 1
	for line in jsonfilelines:
		cleanline = line[line.find('{'):]	
		l = json.loads(cleanline)
		if l["type"] == 'print_reading':
  			print_reading.append(l)
		elif l["type"] == 'trigger_data':
  			trigger_data.append(l)
		elif l["type"] == 'system_start':
  			system_start.append(l)
		else:
  			others.append(l)
		j+=1
		if j == 500 or j>=i:
        write_file(print_reading, 'Print_Reading.cs')
        write_file(trigger_data, 'Trigger_Data.csv')
			  write_file(system_start, 'System_Start.csv')
			  write_file(others, 'Others.csv')
			  print_reading = []
			  trigger_data = []
			  system_start = []
			  others = []
		if j >= i:
  			break
		j+=1
	return