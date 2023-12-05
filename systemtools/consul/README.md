## [consul_service](./consul_service)

* Manage state of the instance for specific service in consul.
* Require environment variable.
  * `CONSUL_HTTP_TOKEN`
  * `CONSUL_CACERT`
  * `CONSUL_CLIENT_CERT`
  * `CONSUL_CLIENT_KEY`
  * `CONSUL_DOMAIN`
* Required python module `requests`, `argparse`, `os`.

```bash
usage: consul_service [-h] [--service SERVICE] [--maintanance {enable,disable}]
                      [--status STATUS] [--node NODE] [--domain DOMAIN]
                      [--instance-id INSTANCE_ID] [--list-instances]

Consul script to manage maintanace mode, list services, status of service.

options:
  -h, --help            show this help message and exit
  --service SERVICE, -s SERVICE
                        Name of the service instance to mark
  --maintanance {enable,disable}, -m {enable,disable}
                        Desired maintanance state change (enable/disable),
                        requires --instance-id/-i and --node/-n
  --status STATUS, -st STATUS
                        Get the status of the service instances
  --node NODE, -n NODE  Name of the node where instance is defined
  --domain DOMAIN, -d DOMAIN
                        Domain name of the service node
  --instance-id INSTANCE_ID, -i INSTANCE_ID
                        ID of the service instance to mark,
                        required when --maintanance/-m is used.
  --list-instances, -l  List all services when combined,
                        with --service/-s list all instances of a service (default)
```
