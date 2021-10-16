#!/bin/bash

s3fs blender-rudy-set `pwd`/output -o passwd_file=/etc/passwd-s3fs -o url=https://s3.wasabisys.com -o allow_other

