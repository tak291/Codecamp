eduNEXT Coding Challenge
========================

This is the challenge for the DevOps position. You only need to answer it if you want to apply for a job in software development for operations monitoring and testing.


Situation description
====================

As a DevOps team member your job is to write software to automate our deployments, infrastructure management, testing.
The tools of trade that we use include:

- Ansible
- Vagrant
- AWS
- Docker
- Git (hosted on github & bitbucket)
- CircleCI
- Jenkins


Using this tools we keep an continuous integration pipeline that involves many services as the one you just launched in the challenge stack section.


Challenge
=========

Using the tools from our stack perform ONE of the following tasks.


## Deploy on VM

Deploy a copy of the customer_data_api django project to a local Vagrant VM on ubuntu 18.04.

- All the interactions that you do on the VM must be scripted using ansible.
- Put your ansible code and Vagrantfile on a git repository that you can share with us.
Bonus point: Use mysql or any other production grade database as the django.db.backends


## Deploy to docker image

Deploy a copy of the customer_data_api django project to a docker container.

- All the interactions that you do on the container must be scripted using ansible.
- Put your ansible code and composer file on a git repository that you can share with us.
Bonus point: Use mysql or any other production grade database as the django.db.backends


## Testing Pipeline

Upload a copy of the customer_data_api django project to git hosting provider and incorporate an automated testing pipeline on CircleCI V2.0.

- Test for quality of code using static testing tools. E.g: pylint, pycodestyle
- Add a few unit tests to the code and run them on the pipeline
Bonus point: Track the test coverage and reach 100%
