OpenStackVaccine
================

A framework to simulate outages in Open Stack deployments to test for resilience and recoverability.The outages could be at various levels: physical layer (nodes ) ,process level,network layer,services etc.

OpenStack Vaccine (OSV) is a fault injection framework that helps cloud applications become highly available and resilient to failures in cloud.

It provides a test platform by recreating failure scenarios to evaluate the resiliency of the cloud instances and thus help in optimizing the cloud instances for fault tolerance. Real world failures such as instance failures, network failures and process failures are recreated and injected at run time.

Example for Openstack has been implemented.

Following failure scenarios are replicated:

1. Instance Failure
2. Volume Failure
3. Process Failure
4. DNS Failure
5. Network Corruption
6. Packet Loss
7. CPU Crash


As a user of Openstack Implementation all you need to do is define config/clients.json and config/auth.json. Example jsons are present in config directory which can be directly modified.


To run the Openstack module from Openstack directory, run

```
    $ python OSV.py -c openstack
```

Some of the configs that needs to defined in configs/clients.json are:

1. Owner Information (Mandatory)
    For getting updates about the menace created and for persisting information on menaces, owner information is required. It needs to added to clients.json dictionary under owner. Fields needed are given below

```
        "owner": {
            "name": "OpenstackVaccine",
            "email": "owner@example.com",
            "phone": "+1 XXX-XXX-XXXX"
        },
```

2. Notifier (Manatory, but can be empty)
    This information is needed for system to send email to owner and others. Contains authentication information and stmp details of sender(May or maynot be owner).

```
        "notifier": {
            "email": {
                "name": "OpenstackVaccine",
                "from": "owner@example.com",
                "smtp": "smtp.example.com:587", // smtp server path
                "username": "johndoe",
                "password": "XXXXXXX"
            }
        },

```

    If you donot want email notification, leave notifier dict empty

```

        "notifier": {
        },
```

3. Scheduler(Optional):
    This field contains scheduling information for fault injection. The fields are as follows:
    a.) start_time : What time of the day should scheduler start injecting fault.(in 24 hours format)
    b.) duration: How long past start_time should it be carried on.
    c.) frequency: How many times during this interval, fault should be injected.
    d.) applied_duration: How long should fault stay in the system
    e.) timezone: Default is US/Eastern.

Sample of scheduler config.

```

        "schedule": {
            "frequency": 10,
            "start_time": 10,
            "duration": 20,
            "apply_duration": 10,
            "timezone": "US/Eastern"
        },

```

4. SSH(Optional, required if the fault injected needs server access):
    SSH credentials of instances, so that fault can be injected by logging in.

```
            "ssh": {
                "key_file": "/home/johndoe/.ssh/openstack-key",
                "username": "ubuntu",
                "port": 22,
                "server_dir": "/tmp"
            }
```

In addition to this. We need to specify our openstack credential to be able to start and stop instances, attach and detach volumes. These credentials are defined in config/auth.json

```

{
    "openstack": {
        "username": "johndoe",
        "password": "XXXXXXXXXX",
        "tenant_name": "fg362",
        "auth_url":"https://s77r.idp.sdsc.futuregrid.org:5000/v2.0"
    }
}
```
