import os
import re
import json
import string
import urllib
import urllib2
import thread

exts = ['avi','mp4','mkv','3gp','mov']
exclude_list = ['xvid','dvdscr', 'dvdrip','dvd','brrip','ddr','x264','aac','720p','1080p','bluray','rip','exclusive','eng','dvl']
torrents = ['axxo','anoxmous','extratorrent','yify']

exclude_list = exclude_list + exts + torrents

def main():
	#Creates the directories for storing movie data and images
	if not os.path.exists("moviedb/images"):
		os.makedirs("moviedb/images")
	
	#
	file_list = os.listdir(".")
	
	#fetch_and_save(format_file_name(file_list[2]))
	for file in file_list:
		formatted_name = format_file_name(file)
		try:
			thread.start_new_thread(fetch_and_save,(formatted_name,))
		except:
			print "Error "
	
	raw_input()

def fetch_and_save(movie_name):
#	print "[+] Retrieving : " + movie_name
	url = urllib.quote(movie_name)
	url = "http://omdbapi.com/?t="+ url
	json_string = urllib2.urlopen(url).read()
	#print json_string
	extract_contents(movie_name, json_string)
	
def extract_contents(movie_name, json_string):
	data = json.loads(json_string)
	if data[u"Response"] == "True":
#		print "[+] Processing  :  " + data[u"Title"]
		save_movie(data)
	else:
		if movie_name[-1] == "1":
			fetch_and_save(movie_name[0:-1])
		else:
			print "[-] Not Found " + movie_name
		
def save_movie(data):
	f = open("moviedb/" + data[u"Title"] + ".htm" , "w")
	html = format_as_html(data)
	f.write(html.encode('utf8'))
	f.close()
	
def format_as_html(data):
	html = "<html><body>"
	html += "<center><h2>" + data[u"Title"]+ "</h2></center>"
	html += "<table margin=4><tr><td>"
	if data["Poster"] != u"N/A":
		html += "<img src='images/" + download(data[u"Poster"])+ "'>"
	
	data.pop("Poster", None)
	
	html += '</td><td><table>'
	for key, value in data.iteritems():
		html += "<tr><td><b>" + key +"</b></td><td>" + value+ "</td></tr>"
	
	html += "</td></tr></table></body></html>"	
	
	return html

def download(url):
	fn=url.split("/")[-1]
	fpath = "moviedb/images/"+fn
	urllib.urlretrieve(url,"moviedb/images/"+fn)
	return fn
	

def format_file_name(fn):
	fn = fn.lower()
	
	if os.path.isfile(fn):
		fn = fn[0:fn.rfind(".")]
	# if check_ext(fn)==1 :
		# return ""	
	
	for i in string.punctuation:
		if i != "'":
			fn = fn.replace(i," ")
	fn = re.split('[1-9][0-9]{3}',fn)[0]
	
	for i in exclude_list:
		if re.search(r"\b" + re.escape(i) + r"\b",fn):
			fn = fn.replace(i,"")
	
	return fn.capitalize()


if __name__ == "__main__":
	main()
