import xmlrpclib, config, pickle, os, sys, subprocess, time

#Back Channel
proxy = []
#create servers
# number of servers
num_servers   	= sys.argv[1]
num_servers   	= int(num_servers)
print(num_servers)
portNum 		= 8000

for i in range(num_servers) :
	# append to the list of client proxies
	print('running server #' + str(portNum+i))
	proxy.append(xmlrpclib.ServerProxy("http://localhost:" + str(portNum + i) + "/"))
	'''
	os.system('start cmd /k C:/ProgramData/Anaconda3/python.exe C:/Users/Administrator/Desktop/Project/hw4/server_stub.py '+ str(portNum + i))
	'''
	print(	  'gnome-terminal -e \"python server_stub.py ' + str(portNum + i) + '\"')
	os.system('gnome-terminal -e \"python server_stub.py ' + str(portNum + i) + '\"')
	time.sleep(1)

while True:
	serverNum = int(raw_input("Select Server to Corrupt (enter from 0 to 3)..."))
	try :
		retVal =  proxy[serverNum].corruptData()
		retVal =  pickle.loads(retVal)
		if(retVal[1] == False):
			print(retVal[0])
	except Exception as err :
		print('connection error')
