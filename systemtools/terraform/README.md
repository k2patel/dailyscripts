# [tf_env_gen](./tf_env_gen)
Create Terraform Environment Variables that points to the Gitlab Managed Terraform state backend for a project.

## Configfile
 * Environment Variable
    * GITLAB_ACCESS_TOKEN
    * GITLAB_URL

## Help
```
usage: tf_env_gen [-h] [--search SEARCH]

generate environment paste for specific project

options:
  -h, --help            show this help message and exit
  --search SEARCH, -s SEARCH
                        provide string to search for all project, limit search result by adding longer string to match
```