#!/usr/bin/python3
import logging
import subprocess
import os,shutil
DBG=True

plugins=[("invertEnabled",""),("invertWindow",""),("magnifierEnabled",""),("lookingglassEnabled",""),("trackmouseEnabled",""),("zoomEnabled",""),("snaphelperEnabled",""),("mouseclickEnabled","")]
windows=[("FocusPolicy","")]
kde=[("singleClick",""),("ScrollbarLeftClickNavigatesByPage","")]
bell=[("SystemBell",""),("VisibleBell","")]
hotkeys_kwin=[("ShowDesktopGrid",""),("Invert",""),("InvertWindow",""),("ToggleMouseClick",""),("TrackMouse",""),("view_zoom_in",""),("view_zoom_out","")]
mouse=[("cursorSize","")]
general=[("fixed",""),("font",""),("menuFont",""),("smallestReadableFont",""),("toolBarFont","")]
dictFileData={"kaccesrc":{"Bell":bell},"kwinrc":{"Plugins":plugins,"Windows":windows},"kdeglobals":{"KDE":kde,"General":general},"kglobalshortcutsrc":{"kwin":hotkeys_kwin},"kcminputrc":{"Mouse":mouse}}
settingsHotkeys={"invertWindow":"InvertWindow","invertEnabled":"Invert","trackmouseEnabled":"TrackMouse","mouseclickEnabled":"ToggleMouseClick","view_zoom_in":"","view_zoom_out":""}

def _debug(msg):
	if DBG==True:
		logging.warning("FH: {}".format(msg))

def getSystemConfig(wrkFile='',sourceFolder=''):
	dictValues={}
	data=''
	#_debug("Reading folder {}".format(sourceFolder))
	if wrkFile:
		if dictFileData.get(wrkFile,None):
			data={wrkFile:dictFileData[wrkFile].copy()}
	if isinstance(data,str):
		data=dictFileData.copy()
	for kfile,groups in data.items():
		for group,settings in groups.items():
			settingData=[]
			for setting in settings:
				key,value=setting
				value=_getKdeConfigSetting(group,key,kfile,sourceFolder)
				settingData.append((key,value))
			data[kfile].update({group:settingData})
	return (data)

def _getKdeConfigSetting(group,key,kfile="kaccessrc",sourceFolder=''):
	if sourceFolder=='':
		sourceFolder=os.path.join(os.environ.get('HOME',"/usr/share/acccessibility"),".config")
	kPath=os.path.join(sourceFolder,kfile)
	value=""
	if os.path.isfile(kPath):
		cmd=["kreadconfig5","--file",kPath,"--group",group,"--key",key]
		try:
			value=subprocess.check_output(cmd,universal_newlines=True).strip()
		except Exception as e:
			print(e)
	#_debug("Read value: {}".format(value))
	return(value)

def setSystemConfig(config,wrkFile=''):
	for kfile,sections in config.items():
		for section,data in sections.items():
			for setting in data:
				(desc,value)=setting
				_setKdeConfigSetting(section,desc,value,kfile)

def _setKdeConfigSetting(group,key,value,kfile="kaccessrc"):
	#kfile=kaccessrc
	#_debug("Writing value {} from {} -> {}".format(key,kfile,value))
	if len(value):
		cmd=["kwriteconfig5","--file",os.path.join(os.environ['HOME'],".config",kfile),"--group",group,"--key",key,"{}".format(value)]
	else:
		cmd=["kwriteconfig5","--file",os.path.join(os.environ['HOME'],".config",kfile),"--group",group,"--key",key,"--delete"]
	ret='false'
	try:
		ret=subprocess.check_output(cmd,universal_newlines=True).strip()
	except Exception as e:
		print(e)
	#_debug("Write value: {}".format(ret))
	return(ret)

def getHotkey(setting):
	hk=""
	hksection=""
	data=""
	name=""
	hksetting=settingsHotkeys.get(setting,"")
	if hksetting:
		sc=getSystemConfig(wrkFile="kglobalshortcutsrc")
		for kfile,sections in sc.items():
			for section,settings in sections.items():
				hksection=section
				for setting in settings:
					(name,data)=setting
					if name.lower()==hksetting.lower():
						data=data.split(",")
						hk=data[0]
						data=",".join(data)
						break
				if hk!="":
					break
			if hk!="":
				break
	return(hk,data,name,hksection)

def cssStyle():
	style="""
		QListWidget{
			}
		QListWidget::item{
			margin:3px;
			padding:3px;
			}
	"""
	return(style)
