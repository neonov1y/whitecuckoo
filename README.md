# About the project
Goal of the project is scan PDF and DOC files and detect anomaly behavior.

# Method
Project based on Cuckoo Sandbox program which produce report about file behavior. Main principle is creating of white-list by scanning "clean" files and save them behavior in database. When the white-list ready we are can scan files by Cuckoo and compare them behavior to white-list. This methon allows detect malicious behavior.
