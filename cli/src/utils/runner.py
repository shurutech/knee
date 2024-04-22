import ansible_runner


def run_playbook(playbook, environment):
    response  = ansible_runner.run(private_data_dir="./", playbook=f"playbooks/{playbook}", inventory=f"inventories/{environment}")
    if response.status == 'failed':
        raise Exception("Something went wrong")
        