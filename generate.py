#!/usr/bin/python
# -*- coding: utf-8 -*-
##
## @author Edouard DUPIN
##
## @copyright 2012, Edouard DUPIN, all right reserved
##
## @license APACHE v2.0 (see license file)
##

import os
import shutil
import errno
import fnmatch
import stat
import sys
import subprocess
import shlex

##
## @brief Execute the command with no get of output
##
def run_command(cmd_line):
	# prepare command line:
	args = shlex.split(cmd_line)
	print("[INFO] cmd = " + str(args))
	try:
		# create the subprocess
		p = subprocess.Popen(args)
	except subprocess.CalledProcessError as e:
		print("[ERROR] subprocess.CalledProcessError : " + str(args))
		return False
	#except:
	#	debug.error("Exception on : " + str(args))
	# launch the subprocess:
	output, err = p.communicate()
	# Check error :
	if p.returncode == 0:
		return True
	else:
		return False



##
## @brief Get list of all Files in a specific path (with a regex)
## @param[in] path (string) Full path of the machine to search files (start with / or x:)
## @param[in] regex (string) Regular expression to search data
## @param[in] recursive (bool) List file with recursive search
## @param[in] remove_path (string) Data to remove in the path
## @return (list) return files requested
##
def get_list_of_file_in_path(path, filter, recursive = False, remove_path=""):
	out = []
	if os.path.isdir(os.path.realpath(path)):
		tmp_path = os.path.realpath(path)
	else:
		print("[E] path does not exist : '" + str(path) + "'")
	
	#print("basePath: " + tmp_path)
	for root, dirnames, filenames in os.walk(tmp_path):
		deltaRoot = root[len(tmp_path):]
		while     len(deltaRoot) > 0 \
		      and (    deltaRoot[0] == '/' \
		            or deltaRoot[0] == '\\' ):
			deltaRoot = deltaRoot[1:]
		if     recursive == False \
		   and deltaRoot != "":
			return out
		if     len(deltaRoot) >= len(remove_path) \
		   and deltaRoot[:len(remove_path)] == remove_path:
			continue
		#print("deltaRoot: " + deltaRoot)
		tmpList = []
		for elem in filter:
			tmpppp = fnmatch.filter(filenames, elem)
			for elemmm in tmpppp:
				tmpList.append(elemmm)
		# Import the module :
		for cycleFile in tmpList:
			#for cycleFile in filenames:
			#add_file = os.path.join(tmp_path, deltaRoot, cycleFile)
			add_file = os.path.join(deltaRoot, cycleFile)
			out.append(add_file)
	return out;




def rename_group(list_element, extention):
	for elem in list_files:
		reduced_name = elem[:-(len(extention)+1)]
		base_path = reduced_name[:-len(reduced_name.split('/')[-1])]
		file_name = reduced_name.split('/')[-1]
		if file_name[:3] == "ic_":
			file_name = file_name[3:]
		if file_name[-5:] == "_48px":
			file_name = file_name[:-5]
		reduced_name = base_path + file_name;
		out = reduced_name + "." + extention;
		if elem != out:
			print(elem + " ==> " + out)
			cmd_line = "mv " + elem.replace(" ", "\ ").replace("'", "\\'") + " " + out.replace(" ", "\ ").replace("'", "\\'")
			ret = run_command(cmd_line)

def generate_css(list_element):
	tmpFile = open("google-material-images.css", 'w')
	tmpFile.write( "// Auto generate css for material design from google (use only svg)\n\n")
	for elem in list_files:
		tmpFile.write( ".gmi-" + elem.replace("/","-").replace(".svg","").replace("_","-") + " {\n")
		tmpFile.write( '	background-image: url("' + elem + '");\n')
		tmpFile.write( "	background-repeat: no-repeat;\n")
		tmpFile.write( "	background-position: center;\n")
		tmpFile.write( "}\n\n")
	tmpFile.flush()
	tmpFile.close()

def generate_html(list_element):
	tmpFile = open("view.html", 'w')
	tmpFile.write( "<html>\n")
	tmpFile.write( "	<header>\n")
	tmpFile.write( '		<title>Liste des vignette google</title>\n')
	tmpFile.write( '		<link rel="stylesheet" type="text/css" href="google-material-images.css">\n')
	tmpFile.write( "		<style>\n")
	tmpFile.write( "		.color-red {\n")
	tmpFile.write( "			filter: opacity(50%);\n")
	tmpFile.write( "			filter: invert(100%);\n")
	tmpFile.write( "			filter: contrast(1,0%);\n")
	tmpFile.write( "		}\n")
	tmpFile.write( "		.base-size {\n")
	tmpFile.write( "			width:64px;\n")
	tmpFile.write( "			height:64px;\n")
	tmpFile.write( "		}\n")
	tmpFile.write( "		body {\n")
	tmpFile.write( '			//background-image: url("background.svg");\n')
	tmpFile.write( "			background-repeat: repeat;\n")
	tmpFile.write( "		}\n")
	tmpFile.write( "		</style>\n")
	tmpFile.write( "	</header>\n")
	tmpFile.write( "	<body>\n")
	tmpFile.write( "		<center>\n")
	tmpFile.write( "			<table>\n")
	for elem in list_files:
		if elem == "background.svg":
			continue
		tmpFile.write( "				<tr>\n")
		#tmpFile.write( '				<td><div class="gmi-' + elem.replace("/","-").replace(".svg","").replace("_","-") + ' base-size color-red"></div></td>\n')
		tmpFile.write( '				<td><right>' + elem.split("/")[1].replace(".svg","").replace("_"," ") + '</right></td>\n')
		tmpFile.write( '				<td><div class="gmi-' + elem.replace("/","-").replace(".svg","").replace("_","-") + ' base-size"></div></td>\n')
		tmpFile.write( '				<td>gmi-' + elem.replace("/","-").replace(".svg","").replace("_","-") + '</td>\n')
		tmpFile.write( '				<td><img src="' + elem + '" height="64" width="64"/></td>\n')
		tmpFile.write( '				<td>' + elem + '</td>\n')
		tmpFile.write( "				</tr>\n")
	tmpFile.write( "			</table>\n")
	tmpFile.write( "		</center>\n")
	tmpFile.write( "	</body>\n")
	tmpFile.write( "</html>\n")
	tmpFile.flush()
	tmpFile.close()

for extention in ["svg"]:
	list_files = get_list_of_file_in_path(".", ["*."+extention], recursive = True, remove_path=".git")
	rename_group(list_files, extention)
	list_files = get_list_of_file_in_path(".", ["*."+extention], recursive = True, remove_path=".git")
	generate_css(list_files)
	generate_html(list_files)




