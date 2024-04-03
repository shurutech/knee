# Knee
## Introduction
Welcome to Knee, the streamlined Ansible playbook for developers! Our mission is simple: to make the setup and deployment of various services like Python servers, PostgreSQL databases, and more, as easy and efficient as possible. Designed with both novice and seasoned developers in mind, Knee not only offers current solutions for server setup and database management but is also evolving to include technologies like Docker, Ruby, and Node.js. Dive into Knee for a smoother, more efficient development experience!

## Prerequisites
Before you start using Knee, it's important to ensure you have the following prerequisites covered:

1. **Basic Ansible Knowledge**: A fundamental understanding of Ansible, including concepts like playbooks, roles, tasks, and inventory, is essential for using Knee effectively.

2. **Infrastructure Fundamentals**: Knowledge of key infrastructure concepts such as virtual machines, networking, and cloud services will greatly aid in the deployment and management of services with Knee.

3. **System Requirements**: Your system should meet the minimum requirements for running Ansible. This includes a compatible operating system and the necessary hardware resources to handle your deployment needs.


## Getting Started

- Ensure Python is Installed:  
  
  Download and install Python from [https://www.python.org/downloads/]. 🐍  

- To begin, clone this Git repository:
  
    ```bash
    git clone https://github.com/shurutech/ansible-base.git
    ```

- Create virtualenv
  
  ```bash
  virtualenv -p python3.12.x venv
  ```

- Activate Virtualenv

    ```bash
    source venv/bin/activate
    ```

- Install Dependencies:

    ```bash
    pip install -r requirements.txt
    ```

- Execute the Command:
    ```bash
    ./knee execute
    ```
## Components
Detail each component that your playbook supports. Since you have multiple components, each should have its subsection.

### Webserver
Every web server deployment would need a basic setup like setting a new user for the service, installing the necessary packages, and configuring the server, and creating a systemd service. The webserver_base playbook does the same here. It creates a new user, installs the necessary packages, and creates a systemd service for the webserver. It accepts the following variables:
1. `user_name`: The name of the user and group to be created in linux.
2. `project_name`: The name of the project using which it would create the project directory and sytemd service.
3. `start_command`: The command to start the server.

### Python Server
The python_webserver playbook is used to deploy a python web server. It accepts the following variables:
1. `user_name`: The name of the user using which it would install pyenv and install the required python version.
2. `python_version`: The version of python to be installed and scoped to the user.

### PostgreSQL Server
The postgresql_main playbook is used to deploy a PostgreSQL server. It accepts the following variables:
1. `postgres_version`: The version of PostgreSQL to be installed.
2. `postgres_database_cidr_address`: The CIDR address to be used for the database.
3. `postgres_database_user`: The user to be created for the database.
4. `postgres_database_password`: The password for the user to be created for the database.
5. `postgres_database_name`: The name of the database to be created.

#### ToDo
- [ ] Change default user permissions from Superuser to minimum required permissions.
- [ ] Make postgres user trust permission configurable.
- [ ] Make all local connections to the database trust permission configurable.
- [ ] 


### PostgreSQL Replica Servers
The postgresql_replica playbook is used to deploy a PostgreSQL replica server. The current setup only sets up streaming replication. It accepts the following variables:
1. `postgres_replication_user`: The user to be created for the replication on the master server.
2. `postgres_replication_user_password`: The password for the user to be created for the replication on the master server.
3. `postgres_version`: The version of PostgreSQL to be installed.
4. `replica_host`: The replica server host ip to be allowed in pg_hba.conf file of the master server.
5. `postgres_database_cidr_address`: The CIDR address to be used for the database.
6. `postgres_data_directory`: The data directory for the database.
7. `master_host`: The master server host ip to be allowed in pg_hba.conf file of the replica server.

#### ToDo
- [ ] Add support for logical replication.
- [ ] Make wal_level, max_wal_senders, wal_keep_size configurable.
- [ ] Make postgres user trust permission configurable.
- [ ] Make all local connections to the database trust permission configurable.
- [ ] Verify the replica server is in sync with the master server.
- [ ] Add support for multiple replica servers.
- [ ] 


### User Management to VMs
The user_management playbook is used to manage users on the VMs. It creates a user in linux, with login ability and also adds their ssh key to the VM. It works on a local playbook variable called users which is a list of users to be created along with their ssh keys.

## Usage Examples
[WIP]

## Future Additions
[WIP]

## FAQs
Answer frequently asked questions or common issues users might encounter.

## License
[WIP]

## Contact Information
[WIP]
