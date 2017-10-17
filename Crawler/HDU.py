import urllib.request, urllib.parse
import http.cookiejar
import base64
from bs4 import BeautifulSoup
import re

class OnlineJudge:

	def __init__(self):
		self.index_url = 'http://acm.split.hdu.edu.cn/'
		self.login_url = self.index_url + 'userloginex.php?action=login'
		self.submit_url = self.index_url + 'submit.php?action=submit'
		self.status_url = self.index_url + 'status.php'

		self.encoding = 'GB2312'
		self.language = {
			'G++':    0,
			'GCC':    1,
			'C++':    2,
			'C':      3,
			'PASCAL': 4,
			'JAVA':   5,
			'C#':     6 
		}

		self.login_username_key = 'username'
		self.login_password_key = 'userpass'
		self.status_table_class = 'table_text'

	def login(self, username, password):
		self.username = username
		self.password = password

		cookiejar = http.cookiejar.CookieJar()
		handler = urllib.request.HTTPCookieProcessor(cookiejar)
		self.opener = urllib.request.build_opener(handler)

		data = {
			self.login_username_key: username,
			self.login_password_key: password
		}
		data = urllib.parse.urlencode(data).encode()
		request = urllib.request.Request(self.login_url, data)
		html = self.opener.open(request).read().decode(self.encoding)

		if (html.find('Sign Out') != -1):
			return True
		else:
			return False

	def submit(self, problemid, language, code):
		data = {
			'problemid': problemid,
			'language': self.language[language.upper()],
			'usercode': code
		}
		data = urllib.parse.urlencode(data).encode(self.encoding)
		request = urllib.request.Request(self.submit_url, data)
		html = self.opener.open(request).read().decode(self.encoding)

		if (html.find('Status') != -1):
			return True
		else:
			return False

	def status(self, problemid, username = None):
		if (username == None):
			username = self.username
		data = {
			'pid': problemid,
			'user': username
		}
		url = self.status_url + '?' + urllib.parse.urlencode(data)
		html = self.opener.open(url).read().decode(self.encoding)

		soup = BeautifulSoup(html, 'lxml')
		table = soup.find('table', class_ = self.status_table_class)
		tr = table.find_all('tr')[1]
		td = tr.find_all('td')[2]
		result = td.find('font').string
		return result;

if __name__ == '__main__':
	username = 'DaDaMr_X'
	password = '199707161239x'

	hdu = OnlineJudge()
	if (hdu.login(username, password)):
		print('Login Successfully!')
	else:
		print('Username or Passowrd is Wrong!')

	problemid = '1000'
	language = 'g++'
	code = '''
	#include <cstdio>
	int main()
	{
		int a, b;
		while (~scanf("%d%d", &a, &b))
			printf("%d\\n", a + b);
		return 0;
	}
	'''

	if (hdu.submit(problemid, language, code)):
		print('Submit Successfully!')
	else:
		print('Submit Failid!')

	result = hdu.status(problemid)
	print(result)