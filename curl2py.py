'''
curl2py.py
Script to turn a "copy as curl (bash)" command from the Chrome Network tab
in Developer Tools into a urllib2 Request object
'''

#import requests #TODO
import urllib2,urllib


def curl2urllib(curl_str):
	req_data={}
	if ('--data' in curl_str):
		data=curl_str.strip().split('--data')[1].split(' ')[1].replace('\'','')
		params=urllib.unquote(data).split('&')
		req_data={}
		for param in params:
			p=param.split('=')
			req_data[p[0]]=p[1]
	orig_headers=curl_str.split('-H')
	i=0
	for header in orig_headers:
		header=header.replace('\'','').replace('"','').split(":")
		if (len(header)>2):
			header_v=':'.join(header[1:]).strip().split(' ')[0]
			header_k=header[0]
			header=[header_k,header_v]
		orig_headers[i]=header
		i+=1
	headers=[]
	i=0
	for header in orig_headers:
		if (i>0):
			headers.append((header[0].strip(),header[1].strip()))
		i+=1
	i=0
	for header in headers:
		key,value = header
		if (key.lower() == "accept-encoding"):
#			print header
			headers[i]=(key,"plain")
		i+=1

	url=':'.join(orig_headers[0][0:]).split(' ')[1]
	print url
	if (len(req_data)==0):
		request = urllib2.Request(url)
		opener = urllib2.build_opener()
		opener.addheaders = headers
	#	return (request,opener)
		data = opener.open(request).read()
		print data
	else:
		request = urllib2.Request(url,urllib.urlencode(req_data))
		opener = urllib2.build_opener()
		opener.addheaders = headers
	#	return (request,opener)
		data = opener.open(request).read()
		print data


curl_str= "" #right-click on request on Chrome's network tab and press Copy->As Curl (bash) then paste here
curl2urllib(curl_str)
