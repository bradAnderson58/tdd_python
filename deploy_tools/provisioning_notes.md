Provisioning a new site
======================

## Required packages:

* nginx
* Python 3.6
* virtualenv + pip
* Git

eg, on AWS Ubuntu:

```bash
sudo add-apt-repository ppa:fkrull/deadsnakes
sudo apt-get install nginx git python36 python3.6-env
```

## Nginx Virtual Host config

* see `nginx.template.conf`
* replace SITENAME with site name, eg `staging.mydomain.com`

## Systemd service

* see `gunicorn-systemd.template.service`
* replace SITENAME with site name, eg `staging.mydomain.com`

## Folder structure
Assume we have a user account at /home/ubuntu

/home/ubuntu

    └── sites
        └── SITENAME
            ├── database
            ├── source
            ├── static
            └── virtualenv
