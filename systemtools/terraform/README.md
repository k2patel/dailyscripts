# Script Index

## [tf_env_gen](./tf_env_gen)

* Manage state of the instance for specific service in consul.
* Require environment variable.
  * `GITLAB_ACCESS_TOKEN`
  * `GITLAB_URL`
* Required python module `requests`, `argparse`, `os`.

## Help
```bash
usage: tf_env_gen [-h] [--search SEARCH] [--override OVERRIDE] [--environment ENVIRONMENT]
generate environment paste for specific project
options:
  -h, --help            show this help message and exit
  --search SEARCH, -s SEARCH
                        provide string to search all project (uses gitlab search),
                        limit search result by adding longer string to match.
  --override OVERRIDE, -o OVERRIDE
                        override state file name, default is 'project name'
  --environment ENVIRONMENT, -e ENVIRONMENT
                        Enbable / Disable environment variable
```
