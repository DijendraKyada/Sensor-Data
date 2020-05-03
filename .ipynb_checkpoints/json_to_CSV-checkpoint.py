import os, time, json, csv, pandas

print_reading = []
trigger_data = []
system_start = []
others = []
def json_to_csv(jsonfile):
	readfile = open(jsonfile, 'r')
	filelines = readfile.read().split('\n')
	readfile.close()
	i = len(filelines)
	j = 1
	for line in filelines:
		cleanline = line[line.find('{'):]
		if j >= i:
			break	
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
	return


def create_file(json_list, file_name):
	data_file = open(file_name, 'w')
	csv_writer = csv.writer(data_file)
	count = 0
	for row in json_list:
		if count == 0:
			header = row.keys()
			csv_writer.writerow(header)
			count += 1
		csv_writer.writerow(row.values())
	data_file.close()

start = time.time()
path = '/Users/dijendrakyada/OneDrive - clarkson.edu/Clarkson/Big_Data/Final-Project/DataSource.txt/'
files = []
for r,d,f in os.walk(path):
	for file in f:
		files.append(os.path.join(r, file))
	
k = 1
for f in files:
	print(k)
	json_to_csv(f)
	k+=1
	

#print('end')
#pandas.read_json(json.dumps(print_reading)).to_csv('P_PrintReading.csv', index= None, header= True)
create_file(print_reading, 'Print_Reading.csv')
#pandas.read_json(json.dumps(trigger_data)).to_csv('P_TriggerData.csv', index= None, header= True)
create_file(trigger_data, 'Trigger_Data.csv')
#pandas.read_json(json.dumps(system_start)).to_csv('P_SystemStart.csv', index= None, header= True)
create_file(system_start, 'System_Start.csv')
#pandas.read_json(json.dumps(others)).to_csv('P_Others.csv', index= None, header= True)
create_file(others, 'Others.csv')

print(time.time() - start)