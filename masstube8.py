#!/usr/bin/env python
import requests, sys, urllib2, re, os.path
from bs4 import BeautifulSoup

def main():
	
	for arg in sys.argv:

		if arg == __file__:
			continue

		if len(sys.argv) > 1:

			url=arg
			s = requests.Session()

			response = s.get(url, headers={ 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0' })

			soup = BeautifulSoup(response.text)
			title = re.sub('[^\w\-_\. ]', '_', soup.title.string)

			file_name = title +'.mp4'
			name_check=True
			count=1
			while name_check:
				if (os.path.isfile(file_name)):
					file_name = title + '(' + str(count) + ').mp4'
					count += 1
				else:
					name_check=False

			vid_url_match = re.search("(?<=videoUrlJS\t= ')[^}]*(?=',)", response.text)
			vid_url = vid_url_match.group()

			u = urllib2.urlopen(vid_url)
			f = open(file_name, 'wb')
			meta = u.info()
			file_size = int(meta.getheaders("Content-Length")[0])
			print "\nDownloading: %s Bytes: %s" % (file_name, file_size)

			file_size_dl = 0
			block_sz = 8192
			while True:
				buffer = u.read(block_sz)
				if not buffer:
					break

				file_size_dl += len(buffer)
				f.write(buffer)
				status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
				status = status + chr(8)*(len(status)+1)
				print status,

			f.close()

		else:
			print "Please provide at least one video url"

if __name__ == '__main__':
	main()