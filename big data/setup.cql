


CREATE KEYSPACE chat_keyspace WITH replication = {'class': 'NetworkTopologyStrategy','replication_factor': 1}; 
use chat_keyspace;
CREATE TABLE chat_table (question text PRIMARY KEY, answer text);
exit
