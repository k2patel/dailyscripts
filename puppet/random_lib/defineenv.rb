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
	rev_git_branch = 'dev'
else
	git_branch = 'prod'
	rev_git_branch = 'master'
end
   
Facter.add('subenv') {
   setcode {
       subenv
   }
}

Facter.add('git_branch') {
	setcode {
		git_branch
	}
}

Facter.add('rev_git_branch') {
	setcode {
		rev_git_branch
	}
}
