#!/bin/sh

bin/cassandra -R
sleep 60
bin/cqlsh -f setup.cql
