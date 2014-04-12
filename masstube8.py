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

			vid_url_match = re.search("(?<=videoUrlJS\t= ')[^}]*(?=',)", response.text)
			vid_url = vid_url_match.group()

			u = urllib2.urlopen(vid_url)			
			meta = u.info()
			file_size = int(meta.getheaders("Content-Length")[0])

			file_name = title +'.mp4'
			name_check=True
			jump_to_next_video=False
			count=1
			while name_check:
				if (os.path.isfile(file_name)):

					f = open(file_name, "r")
					current_file_size = len(f.read())
					f.close()
					if current_file_size == file_size:
						print 'Skipped: ' + file_name + ' (identical file already exists)'
						jump_to_next_video=True
						name_check=False

					file_name = title + '(' + str(count) + ').mp4'
					count += 1

				else:
					name_check=False

			if jump_to_next_video:
				continue

			f = open(file_name, 'wb')

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