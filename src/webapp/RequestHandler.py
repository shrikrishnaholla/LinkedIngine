from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import threading
import urlparse
# import profilefetcher
import dbinterface

class Handler(BaseHTTPRequestHandler):
	def log_message(self, format, *args): 
		log = open("log.txt", "a").write("%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format%args)) 

	# def do_GET(self):
	# 	try:
	# 		parsed_path = urlparse.urlparse(self.path)
	# 		message = '\n'.join([
	# 		'CLIENT VALUES:',
	# 		'client_address=%s (%s)' % (self.client_address,
	# 		self.address_string()),
	# 		'command=%s' % self.command,
	# 		'path=%s' % self.path,
	# 		'real path=%s' % parsed_path.path,
	# 		'query=%s' % parsed_path.query,
	# 		'request_version=%s' % self.request_version,
	# 		'',
	# 		'SERVER VALUES:',
	# 		'server_version=%s' % self.server_version,
	# 		'sys_version=%s' % self.sys_version,
	# 		'protocol_version=%s' % self.protocol_version,
	# 		'',
	# 		])
	# 		# message = parsed_path
	# 		self.send_response(200)
	# 		self.end_headers()
	# 		self.wfile.write(message)
	# 		return
	''''first_name_r=on&last_name_r=on&headline_r=on&industry_r=on&degrees_r=on&majors_r=on&colleges_r=on&skills_r=on&job_titles_r=on&companies_r=on&public_profile_url_r=on&count=10&first_name=test&last_name=test&last_name=test&last_name=test&last_name=test&last_name=test&last_name=test&skills=test&job_titles=test&companies=test&public_profile_url=test'''

	def do_GET(self):
		# try:
			parsed_path = urlparse.urlparse(self.path)

			self.send_response(200)
			self.end_headers()
			message = parsed_path
			# self.log_message(message)
			if parsed_path.path is not '/':
				# print "Fume"
				pass
				# raise Exception
			# # print parsed_path.query
			# querySet = parsed_path.query.split('')
			# for i in range(0,len(querySet)):
			# 	querySet[i] = querySet[i].split('=')
			# print querySet
			# wish = dict()
			# for choice in querySet:
			# 	# wish[choice[0]]= choice[1]
			# 	# print choice[0],choice[1]
			# 	if len(choice)==2 :
			# 		wish[choice[0]]= choice[1]
			# 	else:
			# 		pass
			# print wish
			options = ["first_name_r","last_name_r","headline_r","industry_r","degrees_r","majors_r","colleges_r","skills_r","job_titles_r","companies_r","public_profile_url_r"]
			required = list()
			querySet = urlparse.parse_qs(parsed_path.query)
			for key in querySet:
				if key in options:
					try:
						required.append(key.replace("_r","")) 			#hard coded client dependent
						# print querySet[key]
					except:
						pass
			# for key in querySet:
			# 	if key in options:
			# 		try:
			# 			del querySet[key]
			# 			print querySet[key]
			# 			break
			# 		except:
			# 			pass
			print required
			print querySet
			self.send_response(200)
	 		self.end_headers()
			self.wfile.write(message)
			self.wfile.write('\n')
			return

		# except :
		#  	self.send_response(404)
		#  	return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    server = ThreadedHTTPServer(('localhost', 8080), Handler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()