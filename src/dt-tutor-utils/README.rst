utils plugin for `Tutor <https://docs.tutor.overhang.io>`__
===================================================================================

Installation
------------

::

    pip install git+https://github.com/Dicey-Tech/dt-tutor-utils

Usage
-----

::

    tutor plugins enable utils


License
-------

This software is licensed under the terms of the AGPLv3.


TODO
----
- Backup script
 - Mongodump: 
   - https://gist.github.com/jasonwyatt/4498350 (requires mongodump to be installed) 
   - https://medium.com/@fvergaracl/how-to-make-a-simple-script-to-schechedule-mongodbs-backup-with-python-58e8ea287eeb (python)
   - Example using Click: https://github.com/zhangliyong/mongodb-backup/blob/master/backup.py
 - MySQL
 - Send to S3: 
 - Instruction to setup a cron job
   - Add cron https://pypi.org/project/python-crontab/
 - Restor scripts
- clear or reset data (for dev environment only) 