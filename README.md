# The MUYA Workspace for Collaborative Editing (MUYA-WCE)

This Django project, together with all of the apps included as submodules, is the MUYA workspace for collaborative
editing. It provides all of the functions necessary to upload TEI transcriptions, collate them and produce a critical
apparatus.

This project is mainly a container for the apps but it also includes some static files that are used by many of the
apps, the user documentation and a few basic views and templates.

The user documentation is included in ```.rst``` format in the ```docs```. The rst file can be converted to pdf using
various tools, Pandoc (https://pandoc.org/) was used for the project.

## Installation

The following linux packages are required (these are the Ubuntu package names):

- python3
- python3-dev
- postgres (tested on 12)
- postgres-server-dev

You will also need a web server such as nginx. A python virtual environment is also recommended but not essential.

The requirements.txt file in the repository lists the Python package dependencies.

All of the apps are included as submodules in this repository. They must be initialised when the repository is cloned.
The collation app also contains a submodule which must be initialised from the collation app directory.

Submodules can be initialised as follows:

```bash
git submodule init
git submodule update
```

Once all of the submodules have been initialised the migrations should be applied to build the database structure.

```bash
python manage.py migrate
```


## Configuration

The settings-example.py, urls-example.py, uwsgi-example.py and celery-example.py files provided in the repository are provided as the
basis for configuration.

In the settings.py file the basic changes required for deployment should be made. This is covered in the Django
documentation which is linked from the settings-example.py file. The correct configuration details for the Postgres
database also needs to be added. The CELERY_BROKER_URL setting should also be changed to match the RabbitMQ
configuration.

In the urls.py file the only path that needs to be changed is the url for the admin interface. It is recommended not to
run the admin interface at 'admin' in production.

The celery-example.py and wsgi-example.py files need to reference to the settings file used. This may be different in
test and production systems which is why these files are provided only as examples in the repository.

If the settings are specified in a file not called settings.py then the manage.py file will also need to be updated.

In production several processes need to be running as services/daemons. These are:

- Celery
- uWSGI
- CollateX

The first two of these are well covered in documentation online. CollateX can be run as a service in systemd with the
following code:

```bash
[Unit]
Description=The collateX server

[Service]
Type=simple

User=USER
ExecStart=/usr/bin/java -jar /path/to/django/app/collation/collateX/collatex-tools-1.8-SNAPSHOT.jar -http

Restart=on-failure

[Install]
WantedBy=multi-user.target

```

If you are using the collation app then a JavaScript file should be added to the ```common-static/js``` directory in
the main Django project with the file name ```static_url.js```. This file should set the staticUrl variable to the full
url to the static directory for example:

```js
const staticUrl = 'https://example.com/static/';
```

## License

This app is licensed under the GNU General Public License v3.0.

## Acknowledgments

This application was released as part of the Multimedia Yasna Project funded by the European Union Horizon 2020
Research and Innovation Programme (grant agreement 694612).

The software was created by Catherine Smith at the Institute for Textual Scholarship and Electronic Editing (ITSEE) in
the University of Birmingham. It is based on a suite of tools developed for and supported by the following research
projects:

- The Workspace for Collaborative Editing (AHRC/DFG collaborative project 2010-2013)
- COMPAUL (funded by the European Union 7th Framework Programme under grant agreement 283302, 2011-2016)
- CATENA (funded by the European Union Horizon 2020 Research and Innovation Programme under grant agreement 770816,
  2018-2023)

[![DOI](https://zenodo.org/badge/431938558.svg)](https://zenodo.org/badge/latestdoi/431938558)
