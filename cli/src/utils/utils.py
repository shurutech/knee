from InquirerPy import inquirer


def get_user_input(key, default_value):
    return input(f"💼 Enter {key}: (Default: {default_value}) :: ") or default_value


def get_user_confirmation(key):
    user_confirmation = inquirer.confirm(
        message=f"Do you want to keep the default value for {key}?", default=True
    ).execute()
    return user_confirmation is False


def hosts_configuration_parameters(impacted_host_groups, hosts_config):
    for group, group_info in hosts_config.items():
        if group in impacted_host_groups:
            for hosts, host_info in group_info["hosts"].items():
                print(f"-----{group}--> {hosts} Configuration")
                for key, value in host_info.items():
                    hosts_config[group]["hosts"][hosts][key] = get_user_input(
                        key, value
                    )
    return hosts_config


def load_configuration(configs):
    for group, group_values in configs.items():
        for key, value in group_values.items():
            configs[group][key] = get_user_input(key, value)
    return configs
