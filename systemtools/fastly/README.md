# CLI Scripts - `Fastly`

## Instructions
- Script Holder for script related to fastly.

## Individual Script Readme's
#### [purge](./purge)
- Configuration is stored in `~/.fastlyctl_token`
##### Prequisites
- python3
- python3 modules `argparse`, `requests` and `os`
###### Sample Usage
```
usage: purge [-h] [--service [SERVICE]] [--list] [--purge] [--all] [--type [TYPE]] [--url [URL]] [--config CONFIG]

List / purge fastly services.

options:
  -h, --help            show this help message and exit
  --service [SERVICE], -s [SERVICE]
                        Provide string to search.
  --list, -l            List all services.
  --purge, -p           string to match services, must provide '-s' argument.
  --all, -a             full purge of all services
  --type [TYPE], -t [TYPE]
                        Type of perge needed, default is 'hard' but you can define type.
  --url [URL], -u [URL]
                        Provide URL to purge from fastly
  --config CONFIG, -c CONFIG
                        Configuration file location, default to '~/.fastlyctl_token'.
```

This script will do following:
* Full purge `-all` for specific service
* Purge for specific URL.

##### Prequisites
- This script tested on mac and require bash / zsh

