import json
import traceback
import os
from os import listdir
from os.path import isfile, join
import copy
import sys
import psycopg2
import urllib
import time

urllib.parse.uses_netloc.append("postgres")
try:
	url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
except:
	pass

oldData = {}


def create_connection():

    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    return conn

'''
def create_connection():
    conn = psycopg2.connect(
        database='invitestest',
        user='postgres',
        password='Ak6rnhOON94P',
        host='192.168.1.76',
        port=5432
    )
    return conn
'''

def start_database_table(table,*datatypes):
	datatypes = ",".join(datatypes)
	conn = create_connection()
	cursor = conn.cursor()
	#cursor.execute("SET sql_notes = 0;")
	cursor.execute('CREATE TABLE IF NOT EXISTS '+str(table)+' ('+str(datatypes)+')')
	#cursor.execute("SET sql_notes = 1;")
	conn.commit()
	cursor.close()
	conn.close()

def replace_into_table(table,dataFieldNames,*data):
	
	dataFieldNamesSent = dataFieldNames
	if not dataFieldNames == "":
		dataFieldNames = " ("+ dataFieldNames+")"
	
	valuesString = ""
	counter = 0
	for item in data:
		if valuesString == "":
			valuesString ="E'"+str(item).replace("'","''")+"'"
		else:
			valuesString = valuesString + ",E'"+str(item).replace("'","''")+"'"
		counter = counter +1
	
	conn = create_connection()
	cursor = conn.cursor()
	dataFields = dataFieldNamesSent.split(",")
	#print(dataFieldNames)
	#print(valuesString)
	key = ""
	counter = 0
	updateString = ""
	for item in dataFields:
		if counter > 0:
			updateString = updateString +str(item).replace("'","''")+"=E'"+str(data[counter]).replace("'","''")+"'"
		else:
			key=str(item).replace("'","''")+"=E'"+str(data[counter]).replace("'","''")+"'"
		counter = counter +1
	
	cursor.execute("SELECT * FROM "+str(table)+" WHERE "+str(key))
	rows = cursor.fetchall()
	if len(rows) > 0:
		query2 = "UPDATE "+str(table)+" SET "+str(updateString)+" WHERE "+str(key)
		print(query2)
		#cursor.execute("UPDATE "+str(table)+" SET %s WHERE "+str(key), (str(updateString)))
		cursor.execute(query2)
	else:
		query = "INSERT INTO "+str(table)+str(dataFieldNames)+" VALUES ("+str(valuesString)+")"
		print(query)
		cursor.execute(query)
		#cursor.execute("INSERT INTO "+str(table)+str(dataFieldNames)+" VALUES (%s)", (str(valuesString)))
		
	conn.commit()
	cursor.close()
	conn.close()

def delete_from_table(table,key):
	
	conn = create_connection()
	cursor = conn.cursor()
	cursor.execute("DELETE FROM "+str(table)+" WHERE id='"+str(key)+"'")	
	conn.commit()
	cursor.close()
	conn.close()

def save_data(obj, name ):
	global oldData
	
	if (not isinstance(obj, (list,)) and (not isinstance(obj, str))):
		#if not os.path.exists('save/'+ name):
			#os.makedirs('save/'+ name)
		
		if not name in oldData:
			oldData[name] = {}
		
		for id in obj:
			needsSave = False
			if not id in oldData[name]:
				#print("id "+str(id)+" does not exist in save")
				needsSave = True
			else:
				if oldData[name][id] != obj[id]:
					#print("id "+str(id)+" has changed")
					needsSave = True
				#else:
					#print(oldData[name][id],obj[id])
			
			if needsSave:
				start_database_table(name,"id TEXT PRIMARY KEY","data TEXT")
				try:
						#print("Save data start")
						replace_into_table(name,"id,data",str(id),str(json.dumps(obj[id])))
						#print("Save data finish")
				except:
					traceback.print_exc()
			#else:
				#print("id "+str(id)+" has not changed")
		
		for oldId in oldData[name]:
			validToRemove = True
			if str(oldId) in obj:
				validToRemove = False
			try:
				if int(oldId) in obj:
					validToRemove = False
			except:
				pass
			
			if validToRemove:
				try:
					delete_from_table(name,oldId)
				except:
					traceback.print_exc()
			
		oldData[name] = copy.deepcopy(obj)

def get_SETTING(table):
	results = {}
	try:
		GET_SETTING = "SELECT * FROM {0}"
		
		conn = create_connection()
		cursor = conn.cursor()
		cursor.execute(GET_SETTING.format(table))
		rows = cursor.fetchall()
		for row in rows:
			id = row[0]
			value = str(row[1])
			results[id] = value
		cursor.close()
		conn.close()
		#print(results)
		return results
	except:
		traceback.print_exc()
		#print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
		cursor.close()
		conn.close()
		return results

def load_data(name):
	global oldData
	
	oldData[name] = {}
	
	results = get_SETTING(name)
	
	for id in results:
		#print(results[id])
		oldData[name][id] = json.loads(results[id])
	
	return copy.deepcopy(oldData[name])