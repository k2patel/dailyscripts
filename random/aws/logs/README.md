# CLI Scripts - `load-balancer`

## Instructions
- Script holder for aws load balancer related scripts.

## Individual Script Readme's
#### [check_lb_logs](./check_lb_logs)
- Environmental scopes for authentication.
- List if logs are enabled or disabled, List all load balancer it iterate over two typs `elb` and `elbv2`.
##### Prequisites
- python3
- python3 modules `argparse`, `boto3`
###### Sample Usage
**usage:** check_logs [-h]

List load balancers categorized by enabled or disabled or all.

```
options:
  -h, --help            show this help message and exit
  --list, -l            List system only (default)
  --enabled, -e         List all elb with logs
  --disabled, -d        List all elb without logs (default)
  --region REGION, -r REGION
                        Override region specified in profile
```

This script will do following:
* List all load balancer in specific environment scope.
* List all load balancer where logs are enabled.
* List all load balancer where logs are not enabled.

##### Prequisites
- This script tested on mac and require bash / zsh

