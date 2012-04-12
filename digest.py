# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.

from hashlib import md5
import webapp2
from Crypto.Random import random
from google.appengine.api import memcache

class Digest(webapp2.RequestHandler):
	REALM = "Secure Area"
	# you might want to use a user database for this
	USER = "admin"
	PASSWORD = "helloworld"
	def get(self):
		auth_response = self.request.headers.get("AUTHORIZATION", "none")
		data = self.getDigestCredentials(auth_response)
		data['method'] = self.request.method
		
		ok = None
		nonce = data.get("nonce")
		
		if nonce:
			dbnonce = memcache.get(key=nonce, namespace='nonce')
			if dbnonce:
				ok = self.getDigestResponse(data)
				memcache.delete(key=nonce, namespace='nonce')
			else:
				ok = False
		
		if ok:
			self.response.out.write('<html><body>Authorized.</body></html>')
		else:
			nonce = md5()
			nonce.update(str(random.getrandbits(64)))
			nonce = nonce.hexdigest()
			
			memcache.add(key=nonce, namespace='nonce', value='t', time=3600)
			
			if ok == False:
				stale = ' stale=TRUE'
			else:
				stale = ''
			
			self.response.status = 401
			self.response.status_message = 'Unauthorized'
			self.response.headers.add('WWW-Authenticate', 'Digest realm="%s" nonce="%s"%s' % (Digest.REALM, nonce, stale))
			self.response.out.write('<html><body>Unauthorized.</body></html>')
	
	# The rest of the code is based on http://orangepalantir.org/topicspace/index.php?idnum=50

	def getDigestCredentials(self, auth_response):
		"""Parses the return values from 'HTTP_AUHORIZATION' string"""
		data = {} 
		for item in auth_response.split(','):
			part = item.find("=")
			if part>0:
				data[item[:part].strip()] = item[part+1:].strip("\"")
	
		return data
	
	def getDigestResponse(self, data):
		"""Creates the hash values that are returned"""
		
		#first section could probably be stored in a data base
		valueA = md5()
		valueA.update('%s:%s:%s' % (Digest.USER, Digest.REALM, Digest.PASSWORD))
		hashA = valueA.hexdigest()
		
		#this section will change on request
		nonce = data.get("nonce")
		uri = data.get("uri")
		method = data.get('method')
		valueB = md5()
		valueB.update("%s:%s"%(method,uri))
		hashB = valueB.hexdigest()
		
		value = md5()
		value.update("%s:%s:%s"%(hashA,nonce,hashB))
		
		return data.get("response")==value.hexdigest()
