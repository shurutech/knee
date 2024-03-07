import ansible_runner

def run_playbook(playbook, environment):
    response  = ansible_runner.run(private_data_dir="./", playbook=f"playbooks/{playbook}", inventory=f"inventories/{environment}")
    if response.stats == "failed":
        raise Exception("Playbook failed")
    else:
        print("Playbook success")