# Description: Inventory directory paths
LOCAL_HOSTS_DIR = "inventories/local"
STAGING_HOSTS_DIR = "inventories/staging"
PRODUCTION_HOSTS_DIR = "inventories/production"

DIRECTORY_PATH = {
    "staging": STAGING_HOSTS_DIR,
    "local": LOCAL_HOSTS_DIR,
    "production": PRODUCTION_HOSTS_DIR,
}

INITIAL_OPTION_KNEE_DEFAULTS = "knee-defaults"
INITIAL_OPTION_CUSTOM_SELECTIONS = "custom-selections"

COMMAND_SERVICE_MAP = {
    "python-postgres": {"server": "python", "db": "postgresql"},
    "node-mongo": {"server": "nodejs", "db": "mongodb"},
    "golang-mongo": {"server": "golang", "db": "mongodb"},
    "ruby-mysql": {"server": "ruby", "db": "mysql"},
}

SUBCOMMAND_DESCRIPTION_MAP = {
    "knee-defaults": {
        "description": "These are the default commands provided by Knee.",
        "commands": {
            "python-postgres": "Sets up python server with a PostgreSQL.",
            "golang-mongo": "Sets up golang server with a MongoDB.",
            "node-mongo": "Sets up node server with a MongoDB.",
            "ruby-mysql": "Sets up ruby server with a MySQL.",
        }
    },
    "custom-selections": {
        "description": "These are the commands available for customization.",
        "commands": {
            "python": "Sets up python server.",
            "node": "Sets up node server.",
            "golang": "Sets up golang server.",
            "ruby": "Sets up ruby server.",
            "postgres": "Sets up a PostgreSQL",
            "mongo": "Sets up a MongoDB",
            "mysql": "Sets up a MySQL",
            "redis": "Sets up a Redis",
        }
    }
}

COMMANDS_DESCRIPTION_MAP = {
    "execute": "Prompts for user input, processes selected option, and executes related actions"
}


