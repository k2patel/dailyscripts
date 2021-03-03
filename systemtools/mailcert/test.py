import requests, os

url = "http://localhost:8080/register"

payload="{\n    \"hostname\": \"testing.test.com\",\n    \"ssl_cert\": \"----- START CERTIFICATE -----\\nada87dyfahdsfoas87dsyfasudifhaos8d7fyas87dfyasdfiuahs8d7\\nadsf89asdfaisudfa8dsgaiodsd87faysdf87yasufhae/a8afgausdi\\najdfhaishfasjfia8we/873592734975278hfuashfuahfaksjbfkuag\\n----- END CERTIFICATE -----\"\n}"
headers = {
  'accept': 'application/json',
  'Content-Type': 'text/plain'
}

response = requests.request("GET", url, headers=headers, data=payload)
test = response.text.strip('"').replace('\\n', '\n')

print(test)

