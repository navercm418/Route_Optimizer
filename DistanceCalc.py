#!/usr/bin/python3
# THIS IS TO TAKE A REQUEST FROM THE USER OF ADRESSESES, SEND THEM TO OSRM (OPEN STREET MAPS) AND RETURN TRAVEL TIME
#	1st beta release 1.0 - 6/7/2019
#	GitHub navercm519

#---------- Imports --------------------------
# OS File manage
import os
from pathlib import Path
# URL Stuff
import urllib.request

# GUI Stuff
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
#---------------------------------------------

############################################################################################################################################
#################################### GETLONLAT BEGIN #######################################################################################

def GetLonLat(xadd):
	
	zvFmtAdd = xadd.replace(",","%2C")
	zvFmtAdd = zvFmtAdd.replace(" ","+")
	zvFmtAdd = zvFmtAdd.upper()
	
	zvAdd = zvFmtAdd
	
	zvHttp = 'https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address=' + zvFmtAdd + '&benchmark=9&format=json'
	
		# SEND REQUEST TO SERVER
	
	try:
		zvOut = urllib.request.urlopen(zvHttp).read()
		zvOut = zvOut.decode()
	except KeyboardInterrupt:
		return
	except:
		zvOut = r'coordinates":{"x":ERROR"y":ERROR'
	
	try:
		zvOutStr = zvOut.split(r'coordinates":{"x":',1)[1]
		zvOutStr = zvOutStr.split("}")[0]
		zvLat = zvOutStr.split(r'"y":')[1]
		zvLon = zvOutStr.split(",")[0]
	
	except:
		zvLon = 'ERROR'
		zvLat = 'ERROR'
	
	return zvLon+","+zvLat
	
######################################################### GETLONLAT## END ###################################################################
#############################################################################################################################################

#--------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------

#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX OPTIMIZE BEGIN XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

def OptiAddr():
	
	zvStartText = str(tbx_start.get())
	zvEndText = str(tbx_end.get())
	zvList = tbx_list.get('0.0', tk.END)
	
	zvAddList = zvList.splitlines()
	
	zvLocList = []
	zvMatchList = []
	zvAddList2 = []
	zvRtnList = []
	
	zvOpts = "?source=first&destination=any&roundtrip=true"
	zvLocStr = ""
	zvId = ""
	
	#--------------------------------------------------------------------------
	#      loc list add
	
	zvCnt = 0
	
	zvLocList.append(str(zvCnt)+"^"+zvStartText+"|;"+GetLonLat(zvStartText))
	
	zvCnt = 1
	
	for i in zvAddList:
	
		zvLocList.append(str(zvCnt)+"^"+i+"|;"+GetLonLat(i))
		zvCnt = zvCnt + 1
	
	if len(zvEndText) > 1:
		zvLocList.append(str(zvCnt)+"^"+zvEndText+"|;"+GetLonLat(zvEndText))
		zvOpts = "?source=first&destination=last&roundtrip=false"
		
	#---------------------------------------------------------------------------
	
	for i in zvLocList:
	
		if "ERROR" not in i:
			zvLocStr = zvLocStr + i.split("|")[1]
		
	zvLocStr = zvLocStr[1:]
	
	zvHttpTrip = 'http://router.project-osrm.org/trip/v1/driving/'+zvLocStr+zvOpts
		
	zvTripOut = urllib.request.urlopen(zvHttpTrip).read()
	zvTripOutFmt = zvTripOut.decode()
	zvTripOutFmt = zvTripOutFmt.split(r'"waypoints":[')[1]
	zvTripOutFmt = zvTripOutFmt.split(r'],"code":')[0]
	zvTripOutFmt = zvTripOutFmt.split(r']},')
	
	#-------------------------------------------------------------------------------
	
	zvFmt = ""
	
	zvCnt = 0
	
	for i in zvTripOutFmt:
	
		zvFmt = i.split(r'"waypoint_index":')[1]
		zvFmt2 = zvFmt.split(r',"trips_index"')[0]
		
		zvId = zvFmt2
		
		zvFmt = ""
		zvFmt2 = ""
		
		zvFmt = i.split(r'"location":[')[1]
		zvFmt2 = zvFmt.split(r']}')[0]		
		
		zvLoc = zvFmt2
		
		zvId = int(zvId)
		
		zvMatchList.append(str(zvCnt)+"^"+str(zvId)+"|"+zvLoc)
		
		zvCnt = zvCnt + 1
		
	#----------------------------------------------------------------------------------
	
	zvCnt = 0
	
	while zvCnt < len(zvMatchList):
		for i in zvMatchList:
			
			zvId = i.split("^")[0]
			zvTrId = i.split("^")[1]
			zvTrId = zvTrId.split("|")[0]
			
			
			for i in zvLocList:
				
				zvId2 = i.split("^")[0]
				zvAdd = i.split("^")[1]
				zvAdd = zvAdd.split("|;")[0]
					
				if zvId == zvId2:
				
					zvAddList2.append(zvId+"^"+zvTrId+"|"+zvAdd)
					
					zvCnt = zvCnt + 1
	
	#---------------------------------------------------
	
	zvCnt = 0
	zvMapStr = ""
	zvMapStr = 'https://www.google.com/maps/dir/'
	
	while zvCnt < len(zvAddList2):
	
		for i in zvAddList2:
		
			zvTrId = i.split("^")[1]
			zvTrId = zvTrId.split("|")[0]
			zvTrId = int(zvTrId)
			
			zvAdd = i.split("|")[1]
			
			if zvCnt == zvTrId:
			
				zvRtnList.append(zvAdd)
				zvMapStr = zvMapStr + zvAdd + "/"
				zvCnt = zvCnt + 1
	
	#---------------------------------------------------
	
	zvMapStr = zvMapStr[:-1]
	zvMapStr = zvMapStr.replace(" ","+")
	
	#-------------------- Finish Up -------------------------
	# clear text
	tbx_list.delete('1.0',tk.END)
	tbx_list.update()
	
	# write list to box
	for x in zvRtnList:
		tbx_list.insert(tk.END, x + '\n')
	
	tbx_list.insert(tk.END,'\n')
	
	# write error addresses to box
	for i in zvLocList:	
		if "ERROR" in i:
			tbx_list.insert(tk.END, i + '\n')
			
	# write Google Maps url to box
	tbx_list.insert(tk.END,'\n')
	tbx_list.insert(tk.END,'Google Maps = ' + zvMapStr)
	
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX OPTIMIZE END   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

#--------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------

#/\/\/\/\/\/\/\//\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\#
#/\/\/\/\/\/\/\//\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\    GUI BEGIN   /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\#

# setup
root = tk.Tk()

root.title("Route Calc")

fileStr = r"img\busyhwy.ico"
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, fileStr)

my_file = Path(filename)
if my_file.is_file():
	
	root.iconbitmap(filename)


# configure
s = ttk.Style()
if os.name == 'nt':
	s.theme_use('vista')

s.configure(".", font=('Mono', 20, 'bold'), foreground="#bbbcd0", background='#293134')
s.configure('TButton', font=('Mono', 20), foreground='black', background='#293134')
s.configure('TEntry', font=('Mono', 20), foreground='#293134', background='#293134')


#----------- GUI LAYOUT BEGIN  ---------------------

#--- START LABEL & ENTRY ----------------
lbl_name = ttk.Label(root, text = "Start", anchor="c")
lbl_name.pack(fill="y", expand="yes", padx=10, pady=1)

tbx_start = ttk.Entry(width = 80)
tbx_start.pack(fill="y", expand="yes", padx=10, pady=1)

#--- END LABEL & ENTRY ----------------
lbl_age = ttk.Label(root, text = "End", anchor="c")
lbl_age.pack(fill="y", expand="yes", padx=10, pady=1)

tbx_end = ttk.Entry(width = 80)
tbx_end.pack(fill="y", expand="yes", padx=10, pady=1)

#--- LIST LABEL & ENTRY ----------------
lbl_job = ttk.Label(root, text = "List", anchor="c")
lbl_job.pack(fill="y", expand="yes", padx=10, pady=1)


tbx_list = ScrolledText(root)
tbx_list.pack(fill="both", expand="yes", padx=10, pady=1)

#----- BUTTON ---------------------
btn_opt = ttk.Button(text = "Optimize", command = OptiAddr, width = 30)
btn_opt.pack(fill="y", expand="yes", padx=10, pady=10)
#----------- GUI LAYOUT END   ---------------------

#===================================================================================

root.configure(background='#293134')
root.mainloop()

#/\/\/\/\/\/\/\//\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\    GUI END     /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\#
#/\/\/\/\/\/\/\//\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\#