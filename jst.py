from bs4 import BeautifulSoup
import urllib
import csv




def get_name(body):
	return body.find('span', {'class':'jcn'}).a.string

def get_phone_number(body):
	try:
		return body.find('p', {'class':'contact-info'}).span.a.string
	except AttributeError:
		return ''


def get_address(body):
	return body.find('span', {'class':'mrehover'}).text.strip()

#page count for page
page_number = 1
service_count = 1


fields = ['Name', 'Phone', 'Address']
out_file = open('Mumbai_electricians.csv','w')
csvwriter = csv.DictWriter(out_file, delimiter=',', fieldnames=fields)

while True:


	if page_number > 10:
		break

	url="https://www.justdial.com/Mumbai/Electricians"
	req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"}) 
	page = urllib.request.urlopen( req )


	soup = BeautifulSoup(page.read(), "html.parser")
	services = soup.find_all('li', {'class': 'cntanr'})


	
	for service_html in services:
		dict_service = {}
		name = get_name(service_html)
		phone = get_phone_number(service_html)
		address = get_address(service_html)
		
		if name != None:
			dict_service['Name'] = name
		if phone != None:
			print('getting phone number')
			dict_service['Phone'] = phone
	
		if address != None:
			dict_service['Address'] = address
	
		csvwriter.writerow(dict_service)

		print("#" + str(service_count) + " " , dict_service)
		service_count += 1

	page_number += 1

out_file.close()