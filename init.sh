#!/bin/bash

module load novaclient

if  test ! -s ${HOME}/.futuregrid/novarc
then
     module load cloudmesh
     cm-manage config sierra-openstack-grizzly
fi

python ${HOME}/OpenStackVaccine/instance.py


