import requests, sys, re
class bcolors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

host = sys.argv[1]

print """
$$$$$$$\            $$\                  $$\                                       
$$  __$$\           $$ |                 $$ |                                      
$$ |  $$ | $$$$$$\  $$$$$$$\   $$$$$$\ $$$$$$\    $$$$$$$\      $$$$$$\  $$\   $$\ 
$$$$$$$  |$$  __$$\ $$  __$$\ $$  __$$\\_$$  _|  $$  _____|    $$  __$$\ $$ |  $$ |
$$  __$$< $$ /  $$ |$$ |  $$ |$$ /  $$ | $$ |    \$$$$$$\      $$ /  $$ |$$ |  $$ |
$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ | $$ |$$\  \____$$\     $$ |  $$ |$$ |  $$ |
$$ |  $$ |\$$$$$$  |$$$$$$$  |\$$$$$$  | \$$$$  |$$$$$$$  |$$\ $$$$$$$  |\$$$$$$$ |
\__|  \__| \______/ \_______/  \______/   \____/ \_______/ \__|$$  ____/  \____$$ |
                                                               $$ |      $$\   $$ |
                                                               $$ |      \$$$$$$  |
                                                               \__|       \______/ 
                                                                                          
                                                                             """

print 'Trying to fetch robots.txt from the supplied URL'
robotsURL = host+'/robots.txt'
fakeUAHeader = {'User-Agent': 'Googlebot/2.1'} # spoof googlebot UA in order to bypass whitelist

try:
	r = requests.get(robotsURL, headers=fakeUAHeader)
except:
	print 'Invalid URL supplied\r\nUsage: robots.py <URL>'
	sys.exit()

robotsPaths = re.findall('Disallow: (.*)', r.text)
robotsPaths = list(set(robotsPaths)) #remove duplicates

for path in robotsPaths:
	pathURL = host + path
	try:
		r = requests.get(pathURL)
		finalResult = pathURL + ' ' + str(r.status_code) + ' ' + r.headers['content-length'] + bcolors.ENDC
		if r.status_code == 200:
			print bcolors.GREEN + finalResult
		if r.status_code == 404 or r.status_code == 403:
			print bcolors.RED + finalResult
		if r.status_code == 500 or r.status_code == 302:
			print bcolors.YELLOW + finalResult 
	except:
		print 'Failed fetch URL: ' + pathURL
