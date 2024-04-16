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


