# Darig Query

Darig Query provides a SQL query interface for YAML data.
It was formerly known as YAQL.

The idea is to use the Darig Schema to dynamically create a database schema and populate the database with YAML file data enabling standard SQL access.  
This should also allow data to be exported back to YAML based on the Darig Schema for storage in a version control system.

In addition to offering "live" DB access, we may also create a YAML schema for queries that could be run in an repeatable manner (i.e. within a CI/CD pipeline).