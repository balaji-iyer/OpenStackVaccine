#!/bin/bash

module load novaclient

if [! -f ${HOME}/.futuregid/novarc]
then
     module load cloudmesh
     cm-manage config sierra-openstack-grizzly
fi

python ${HOME}/OpenstackVaccine/instance.py


