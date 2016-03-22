require 'resolv'
require 'socket'
addr = Resolv.getaddress(Socket.gethostbyname(Socket.gethostname).first)
print addr
