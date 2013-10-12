#!/bin/bash

module load novaclient

NOVARC=${HOME}/.futuregrid/novarc
echo $NOVARC
if  test ! -s $NOVARC
then
     module load cloudmesh
     cm-manage config sierra-openstack-grizzly
fi
. ${NOVARC}

python ${HOME}/OpenStackVaccine/instance.py


