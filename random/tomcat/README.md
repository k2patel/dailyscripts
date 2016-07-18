This script will manage call against the tomcat-manager.
You can reload / stop / start / list / serverinfo / sessions against your application as needed.
while using list / sessions / serverinfo use context to "/"

it's simple and uses base64 password to store in your configuration.

- main script "tomcat_wrapper"
- config "tomcat_wrapper.conf"

example use :

`/usr/local/sbin/tomcat_wrapper -u ${user} -p ${password} -H ${host} -P ${port} -m ${manager} -c ${context} -a ${action} -s ${ssl}`
