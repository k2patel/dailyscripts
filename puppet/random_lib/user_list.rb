require 'etc'

Etc.passwd { |user|

    Facter.add("user_home_" + user.name) {
      setcode {
        user.dir
      }
    }

    Facter.add("user_uid_" + user.name) {
      setcode {
        user.uid
      }
    } 

    Facter.add("user_gid_" + user.name) {
      setcode {
        user.gid
      }
    }
}
