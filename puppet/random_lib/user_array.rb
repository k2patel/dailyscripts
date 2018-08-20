require 'puppet'

def getusers
  @users = Array.new
  Puppet::Type.type("user").instances.find_all do |user|
    @values = user.retrieve
    @users.push(user.name)
  end
  @users unless @users.empty?
end

Facter.add("users") do
  setcode do
    getusers.join(",")
  end
end

