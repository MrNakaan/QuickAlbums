from http.server import HTTPServer, SimpleHTTPRequestHandler
from chameleon import PageTemplateLoader
import os

def readAlbumDefinitions():
	albums = {}
	definitions = open("definitions.txt", "r")
	lines = definitions.readlines()
	definitions.close()
	for line in lines:
		line = line.strip().split('|')
		albums[line[0]] = [line[2], line[3], line[1]]
	return albums
	
def runServer():
    serverAddress = ('', 8000)
    httpd = HTTPServer(serverAddress, SimpleHTTPRequestHandler)
    httpd.serve_forever()
	
def buildTemplates(albums):
	templates = PageTemplateLoader("templates")
	buildAlbumPages(templates["album.pt"], albums)
	buildCategoryPages(templates["category.pt"], albums)
	buildIndex(templates["index.pt"], albums)
	
def buildCategoryPages(template, albums):
	return
	
def buildIndex(template, albums):
	pageList = [[x, albums[x][1] + ".htm", albums[x][0], os.listdir(albums[x][0])[0]] for x in sorted(albums.keys())]
	pageList = [pageList[x:x + 2] for x in range(0, len(pageList), 2)]
	lastRowClasses = None
	if (len(pageList[len(pageList) - 1]) % 2 is 1):
		lastRowClasses = "pull-s3"
	markup = template(count=len(albums), pages=pageList, lastRowCss=lastRowClasses)
	output = open("index.htm", "w")
	output.write(markup)
	output.close()
	
def buildRows(files):
	rows = []
	row = 0
	col = 0
	
	for file in files:
		if col == 3:
			row += 1
			col = 0
		if col == 0:
			rows.append([])
		rows[row].append(file)
		col += 1
		
	return rows
	
def buildAlbumPages(template, albums):
	for key in albums.keys():
		files = os.listdir(albums[key][0])
		rows = buildRows(files)
		
		lastRowClasses = None
		if (len(rows[len(rows) - 1]) % 3 is 1):
			lastRowClasses = "push-s4"
		elif (len(rows[len(rows) - 1]) % 3 is 2):
			lastRowClasses = "push-s2"
		
		markup = template(title=albums[key][2] + " - " + key, count=len(files), dir=albums[key][0], images=rows, lastRowCss=lastRowClasses)
		output = open(albums[key][1] + ".htm", "w")
		output.write(markup)
		output.close()
	
def clearBuiltTemplates():
	for file in os.listdir("."):
		if (file.endswith(".htm")):
			os.remove(file)
	
def main():
	os.chdir(os.path.dirname(os.path.realpath(__file__)))
	albums = readAlbumDefinitions()
	clearBuiltTemplates()
	buildTemplates(albums)
	print("Pages built, starting server.")
	runServer()
	
if __name__ == "__main__":
	main()