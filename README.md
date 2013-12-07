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
