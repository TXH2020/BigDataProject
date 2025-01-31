CREATE KEYSPACE if not exists ping_keyspace WITH replication = {'class': 'SimpleStrategy','replication_factor': 1}; 
CREATE TABLE if not exists ping_table (request text PRIMARY KEY, response text);
