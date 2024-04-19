# Knee
## Overview
Welcome to Knee, an interactive CLI tool built on top of Ansible, used to automate infrastructure setup, leading to increased efficiency and reduced human error.

## How it works

https://github.com/shurutech/knee/assets/158024046/c95a9dd3-bd7f-46e5-9f24-ae8d90a050e5

## Prerequisites
Before you start using Knee, it's important to ensure you have the following prerequisites covered:

1. **Basic Ansible Knowledge**: A fundamental understanding of Ansible, including concepts like playbooks, roles, tasks, and inventory, is essential for using Knee effectively.

2. **Infrastructure Fundamentals**: Knowledge of key infrastructure concepts such as virtual machines, networking, and cloud services will greatly aid in the deployment and management of services with Knee.

3. **System Requirements**:  
    
    - Your system should meet the minimum requirements for running [Ansible](https://www.ansible.com/).

    - Target System should be Debian based Linux for the intended installation.

    - For replication, MongoDB requires 2 additional hosts, MySQL and PostgreSQL require 1 additional host each.

    - Before running the tool, the details of the target system, such as the IP address and SSH key, are required. Alternatively, refer to [VIRTUAL_MACHINE.md](VIRTUAL_MACHINE.md) for instructions on setting up the virtual machine locally.

## Currently Supported Systems

| Databases | Webservers | Caching Tools |
|-----------|------------|---------------|
| MySQL     | Nodejs     | Redis         |
| PostgreSQL| Python     |               |
| MongoDB   | Golang     |               |
|           | Ruby       |               |
## Getting Started

- Ensure Python is Installed:  
  
  Download and install Python from [https://www.python.org/downloads/] 🐍  

- Clone the Git repository:
  
    ```bash
    git clone https://github.com/shurutech/knee.git
    ```

- Create virtualenv:
  
  ```bash
  virtualenv -p python3.12.x venv
  ```

- Activate Virtualenv:

    ```bash
    source venv/bin/activate
    ```

- Install Dependencies:

    ```bash
    pip install -r requirements.txt
    ```
- To run tests
   ```bash
   pytest cli/tests
   ```
- Execute command to initialize and run setup: Refer [Usage Example](#usage-example) for more details
    ```bash
    ./knee execute
    ```
**Note:** Refer to [VIRTUAL_MACHINE.md](VIRTUAL_MACHINE.md) for instructions on setting up the virtual machine locally.



## Usage 

After you've completed the setup, you can start exploring the functionalities provided by Knee. 

When you run the application, you'll be presented with two main options:

- **Knee Defaults**: This option provides a set of predefined configurations that automate the installation and setup of commonly used software combinations. If you're not sure what software to install, or if you want to quickly set up a popular software combination, this is a good option to choose.

- **Custom Selection**: This option allows you to customize the setup according to your needs. You can select the server, database, additional services, or any combination of these. You can also choose not to select any of these options if you prefer.

Choose the option that best suits your needs and follow the prompts to complete the setup.

- For a comprehensive list of all available commands and options, you can use the help command:
    ```bash
    ./knee --help
    ```
    or  

    ```bash
    ./knee -h
    ```

## Usage Examples <a name=" "></a>

1. **Setting Up a Nodejs-Postgresql-Redis Infrastructure:** Knee quickly sets up a server for your application. Run `./knee execute`, then choose 'Nodejs' for the server option, 'Postgresql' for the database option, and 'Redis' for the caching tool option in the custom selection.

2. **Quickly Setting Up a Common Software Stack:** If you're not sure what software to install, or if you want to quickly set up a popular software combinations`(golang-mongo, python-postgres etc.)`, you can use the Knee defaults option. Run `./knee execute` and choose the Knee defaults option.

3. **Customizing Your Setup:** If you have specific needs for your project, you can customize your setup with Knee. Run `./knee execute` and use the custom selection option to choose the server, database, and additional services that fit your needs

## Next Steps/Features
We plan to continue building after the initial release and look forward to the feedback from the community. As of now we have following features planned out for next releases.

  - **Platform Compatibility:** Knee plans to support more OS and configurations.  
  
  - **Adaptation to Trends:** Staying updated with emerging technologies to meet the changing needs of users.

  - **Interactive Input:** Enable users to input configuration details directly via command-line.

  - **Flexible replica count:** Option for the users to input number of replica host.
    
## Contribution Guidelines
Knee welcomes all constructive contributions. Contributions take many forms, from code for bug fixes and enhancements, to additions and fixes to documentation, additional tests, triaging incoming pull requests and issues, and more!

## How to Contribute
**Reporting Bugs**

Before reporting a bug, please:

 - Check the issue tracker to ensure the bug hasn't already been reported.
 - If the issue is unreported, create a new issue, providing:
    - A clear title and description.
    - Steps to reproduce the bug.
    - Expected behavior and what actually happened.
    - Any relevant error messages or screenshots.

**Suggesting Enhancements**
We love to receive suggestions for enhancements! Please:

- First, check if the enhancement has already been suggested.
- If not, open a new issue, describing the enhancement and why it would be beneficial.

**Pull Requests**
Ready to contribute code? Follow these steps:

1. Fork the repository - Create your own fork of the project.
2. Create a new branch for your changes - Keep your branch focused on a single feature or bug fix.
3. Commit your changes - Write clear, concise commit messages that explain your changes.
4. Follow the coding standards - Ensure your code adheres to the coding standards used throughout the project.
5. Write tests - If possible, write tests to cover the new functionality or bug fix.
6. Submit a pull request - Provide a clear description of the problem and solution. Include the relevant issue number if applicable.

**Conduct**
We are committed to providing a welcoming and inspiring community for all. By participating in this project, you are expected to uphold our Code of Conduct, which promotes respect and collaboration.
