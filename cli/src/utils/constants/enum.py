from enum import Enum

class Database(Enum):
    POSTGRESQL = "postgresql"
    MONGODB = "mongodb"
    MYSQL = "mysql"

class Webserver(Enum):
    RUBY = "ruby"
    PYTHON = "python"
    NODEJS = "nodejs"
    GOLANG = "golang"

class CachingTool(Enum):
    REDIS = "redis"

class Environment(Enum):
    LOCAL = "local"
    STAGING = "staging"
    PRODUCTION = "production"

class InitialOption(Enum):
    KNEE_DEFAULTS = "knee-defaults"
    CUSTOM_SELECTIONS = "custom-selections"

class HostGroup(Enum):
    DATABASE_MAIN_SERVER = "databasemainserver"
    DATABASE_REPLICA_SERVER = "databasereplicaservers"
    REDIS_SERVER = "redisservers"
    WEB_SERVER = "webservers"

class MongodbFile(Enum):
    MONGODB_MAIN_SERVER = "mongodbmainserver.yml"
    MONGODB_REPLICA_SERVER = "mongodbreplicaservers.yml"
    MONGODB_REPLICA_SERVER_PLAYBOOK = "mongodb_replica_server.yml"
    MONGODB_SERVER_PLAYBOOK = "mongodb_server.yml"

class MysqlFile(Enum):
    MYSQL_MAIN_SERVER = "mysqlmainserver.yml"
    MYSQL_REPLICA_SERVER = "mysqlreplicaservers.yml"
    MYSQL_REPLICA_SERVER_PLAYBOOK = "mysql_replica_server.yml"
    MYSQL_SERVER_PLAYBOOK = "mysql_server.yml"

class PostgresqlFile(Enum):
    POSTGRESQL_MAIN_SERVER = "postgresmainserver.yml"
    POSTGRESQL_REPLICA_SERVER = "postgresreplicaservers.yml"
    POSTGRESQL_REPLICA_SERVER_PLAYBOOK = "postgres_replica_server.yml"
    POSTGRESQL_SERVER_PLAYBOOK = "postgres_server.yml"

class GolangFile(Enum):
    GOLANG_WEBSERVERS = "golangwebservers.yml"
    GOLANG_SERVER_PLAYBOOK = "golang_server.yml"

class NodejsFile(Enum):
    NODEJS_WEBSERVERS = "nodewebservers.yml"
    NODEJS_SERVER_PLAYBOOK = "node_server.yml"

class PythonFile(Enum):
    PYTHON_WEBSERVERS = "pythonwebservers.yml"
    PYTHON_SERVER_PLAYBOOK = "python_webservers.yml"

class RubyFile(Enum): 
    RUBY_WEBSERVERS = "rubywebservers.yml"
    RUBY_SERVER_PLAYBOOK = "ruby_webservers.yml" 

class WebserverBaseFile(Enum):
    WEBSERVER_BASE_PLAYBOOK = "webserver_base.yml"               
