from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import threading
import urlparse

class Handler(BaseHTTPRequestHandler):

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
	def do_GET(self):
		# try:
			parsed_path = urlparse.urlparse(self.path)
			self.send_response(200)
			self.end_headers()
			message = parsed_path
			self.wfile.write(message)
			self.wfile.write('\n')
			return

		# except:
		# 	self.send_error(404)
		# 	return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    server = ThreadedHTTPServer(('localhost', 8080), Handler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()