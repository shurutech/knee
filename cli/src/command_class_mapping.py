from commands.python_postgres import PythonPostgres
from commands.node_mongo import NodeMongo
from commands.golang_mongo import GolangMongo
from commands.ruby_mysql import RubyMysql


COMMAND_TO_CLASS_MAP = {
    "python-postgres": PythonPostgres,
    "node-mongo": NodeMongo,
    "golang-mongo": GolangMongo,
    "ruby-mysql": RubyMysql,
}