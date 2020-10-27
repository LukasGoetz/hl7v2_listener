# HL7v2 Listener
The 'HL7v2 Listener' reads HL7v2 messages and stores them in a database. Afterwards the HL7v2 messages are forwarded to another listener mapping the messages to HL7 FHIR.

## Prerequisites

* container environment like docker
* k8s cluster
* postgreSQL database

## Getting Started

* create schema and table in postgreSQL database:
	* `CREATE SCHEMA hl7v2msg;`
	* `DROP TABLE IF EXISTS hl7v2msg.messages;`
	* `CREATE TABLE hl7v2msg.messages (id serial primary key, sender varchar(128), receiver varchar(128), rectime_utc timestamp, message_type text, raw_message text);`
* A) run locally
	* install required packages (python >= 3.7) `pip3 install -r requirements`
	* run application
* B) run as container locally
	* build container `docker build -t hl7v2_listener:v1.0.0 -f dply/Dockerfile $PATH_TO_REPO`
	* run container with environment variables LISTENER_HOST_IP, LISTENER_PORT (8788), LISTENER_RCV_HOST, LISTENER_RCV_PORT, DATABASE_HOST, DATABASE_DBNAME, DATABASE_USR, DATABASE_PWD
* C) run as container on k8s cluster
	* build container `docker build -t hl7v2_listener:v1.0.0 -f dply/Dockerfile $PATH_TO_REPO`
	* push container to registry
	* create secret/ config in k8s cluster for environment variables LISTENER_HOST_IP, LISTENER_PORT (8788), LISTENER_RCV_HOST, LISTENER_RCV_PORT, DATABASE_HOST, DATABASE_DBNAME, DATABASE_USR, DATABASE_PWD
	* run container on cluster `kubectl apply -f dply/k8s_dply.yaml`

## Features

* Storing of messages in a PostgreSQL database
* Forwarding the messages to another service mapping the HL7v2 messages to HL7 FHIR
* (TO DO: Pseudonymizing encounter and patient ID)

## Authors

* [Cosa-Linan, Alejandro](http://10.3.8.51/alejandro.cosa-linan)
* [Goetz, Lukas](http://10.3.8.51/goetzlu)

## License

GNU GPL version 3.0

Additionally, whenever the python-hl7 library is used the following rules apply:
  Copyright (C) 2009-2020 John Paulett (john -at- paulett.org)
  All rights reserved.

  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions
  are met:

   1. Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
   2. Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in
      the documentation and/or other materials provided with the
      distribution.
   3. The name of the author may not be used to endorse or promote
      products derived from this software without specific prior
      written permission.

  THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS
  OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
  ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
  GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
  IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
  OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
  IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.