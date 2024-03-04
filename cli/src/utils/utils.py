from InquirerPy import inquirer
import os
import yaml

def get_user_input(key, default_value):
        return input(f"💼 Enter {key}: (Default: {default_value}) :: ") or default_value

def get_user_confirmation(key):
            user_confirmation = inquirer.confirm(message=f"Do you want to keep the default value for {key}?", default=True).execute()
            return user_confirmation is False

def write_to_file(directory, filename, data):
        with open(os.path.join(directory, filename), "w") as file:
            yaml.dump(data, file)

def read_from_file(directory, filename):
         with open(os.path.join(directory, filename), "r") as file:
            return yaml.safe_load(file)


def hosts_configuration_parameters(impacted_host_groups, environment, dir_path, hosts_config):
        for group, group_info in hosts_config.items():  
            if group in impacted_host_groups:
                for hosts, host_info in group_info["hosts"].items():
                    print(f"-----{group}--> {hosts} Configuration")
                    for key, value in host_info.items():
                        hosts_config[group]["hosts"][hosts][key] = get_user_input(key, value)
        return hosts

def node_configuration_parameters(configs):
    for group, group_values in configs.items():
        for key, value in group_values.items():
            configs[group][key] = get_user_input(key, value)
    return configs       