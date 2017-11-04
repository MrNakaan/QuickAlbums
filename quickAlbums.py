from http.server import HTTPServer, SimpleHTTPRequestHandler
from chameleon import PageTemplateLoader
import os, urllib, re, socketserver

class ThreadingSimpleServer(socketserver.ThreadingMixIn, HTTPServer):
    pass

def buildRows(files):
	rows = []
	row = 0
	col = 0
	
	for file in files:
		if col == 4:
			row += 1
			col = 0
		if col == 0:
			rows.append([])
		rows[row].append(file)
		col += 1
		
	return rows
	
def buildAlbumPages(template, albums):
	for key in albums.keys():
		files = sorted(os.listdir(albums[key][0]))
		rows = buildRows(files)
		
		lastRowClasses = None
		if (len(rows[len(rows) - 1]) % 2 is 1):
			lastRowClasses = " push-s3"
		
		markup = template(title=key, count=len(files), dir=albums[key][0], images=rows, lastRowCss=lastRowClasses)
		output = open(albums[key][1] + ".htm", "w")
		output.write(markup)
		output.close()

def buildTagPages(template, albums):
	pattern = re.compile("[^a-zA-Z0-9]")
	
	tagList = [albums[x][2] for x in albums.keys()]
	for tag in sorted(tagList):
		tagList.remove(tag)
		for subTag in tag.split('~'):
			tagList.append(subTag)

	tagList = list(set(tagList))
	
	for tag in tagList:
		albumKeys = []
		for key in albums.keys():
			if tag in albums[key][2].split('~'):
				albumKeys.append(key)
		pageList = [[x, albums[x][1] + ".htm", albums[x][0], os.listdir(albums[x][0])[0]] for x in sorted(albumKeys)]
		pageList = [pageList[x:x + 2] for x in range(0, len(pageList), 2)]
		lastRowClasses = None
		if (len(pageList[len(pageList) - 1]) % 2 is 1):
			lastRowClasses = "offset-m3"
		markup = template(count=len(albumKeys), albums=pageList, lastRowCss=lastRowClasses, tag=tag)
		output = open(pattern.sub("", tag) + ".htm", "w")
		output.write(markup)
		output.close()
	
	return [[tag, pattern.sub("", tag)] for tag in tagList]
		
def buildIndex(template, albums, tags):
	pageList = [[x, albums[x][1] + ".htm", albums[x][0], os.listdir(albums[x][0])[0]] for x in sorted(albums.keys())]
	pageList = [pageList[x:x + 2] for x in range(0, len(pageList), 2)]
	lastRowClasses = None
	if (len(pageList[len(pageList) - 1]) % 2 is 1):
		lastRowClasses = "offset-m3"
	markup = template(albumCount=len(albums), tagCount=len(tags), albums=pageList, tags=tags, lastRowCss=lastRowClasses)
	output = open("index.htm", "w")
	output.write(markup)
	output.close()
	
def readAlbumDefinitions():
	albums = {}
	definitions = open("definitions.txt", "r")
	lines = definitions.readlines()
	definitions.close()
	for line in lines:
		line = line.strip().split('|')
		albums[line[0]] = [line[2], line[3], line[1]]
	return albums
	
def clearBuiltTemplates():
	for file in os.listdir("."):
		if (file.endswith(".htm")):
			os.remove(file)
	
def buildTemplates(albums):
	templates = PageTemplateLoader("templates")
	buildAlbumPages(templates["album.pt"], albums)
	tagList = buildTagPages(templates["tag.pt"], albums)
	buildIndex(templates["index.pt"], albums, tagList)
	
def runServer():
    serverAddress = ('', 8000)
    httpd = ThreadingSimpleServer(serverAddress, SimpleHTTPRequestHandler)
    httpd.serve_forever()
	
def main():
	os.chdir(os.path.dirname(os.path.realpath(__file__)))
	albums = readAlbumDefinitions()
	clearBuiltTemplates()
	buildTemplates(albums)
	print("Pages built, starting server.")
	runServer()
	
if __name__ == "__main__":
	main()