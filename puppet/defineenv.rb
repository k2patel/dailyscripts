#!/usr/bin/env ruby
require 'facter'
require 'socket'

subenv = Socket.gethostname.split('.').first.sub(/^.*$?-/, '')

compenv = [ "dev", "stage" ]

unless compenv.include?(subenv.downcase)
   subenv = 'prod'
end

if compenv.include?(subenv.downcase)
	git_branch = 'master'
else
	git_branch = 'prod'
end
   
Facter.add('ornlsubenv') {
   setcode {
       subenv
   }
}

Facter.add('git_branch') {
	setcode {
		git_branch
	}
}
