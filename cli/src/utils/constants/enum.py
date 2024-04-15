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

