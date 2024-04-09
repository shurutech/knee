# Knee
## Introduction
Welcome to Knee, the streamlined Ansible playbook for developers! Our mission is simple: to make the setup and deployment of various services like Python servers, PostgreSQL databases, and more, as easy and efficient as possible. Designed with both novice and seasoned developers in mind, Knee not only offers current solutions for server setup and database management but is also evolving to include technologies like Docker, Ruby, and Node.js. Dive into Knee for a smoother, more efficient development experience!

## Prerequisites
Before you start using Knee, it's important to ensure you have the following prerequisites covered:

1. **Basic Ansible Knowledge**: A fundamental understanding of Ansible, including concepts like playbooks, roles, tasks, and inventory, is essential for using Knee effectively.

2. **Infrastructure Fundamentals**: Knowledge of key infrastructure concepts such as virtual machines, networking, and cloud services will greatly aid in the deployment and management of services with Knee.

3. **System Requirements**:  
    
    - Your system should meet the minimum requirements for running Ansible.

    - This requires a suitable operating system and sufficient hardware capabilities for your tasks.

    - Target System should be Ubuntu for the intended installation.

## Getting Started

- Ensure Python is Installed:  
  
  Download and install Python from [https://www.python.org/downloads/] 🐍  

- Clone the Git repository:
  
    ```bash
    git clone [https://github.com/shurutech/knee]
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

## Usage Examples

1. **Setting Up a Python Server:** If you're a Python developer looking to quickly set up a server for your application, you can use Knee. Simply run `./knee execute` and choose the server option in the custom selection.

2. **Deploying a PostgreSQL Database:** If you need to deploy a PostgreSQL database, Knee can help streamline the process. Run `./knee execute` and select the database option in the custom selection.

3. **Quickly Setting Up a Common Software Stack:** If you're not sure what software to install, or if you want to quickly set up a popular software combination, you can use the Knee defaults option. Run `./knee execute` and choose the Knee defaults option.

4. **Customizing Your Setup:** If you have specific needs for your project, you can customize your setup with Knee. Run `./knee execute` and use the custom selection option to choose the server, database, and additional services that fit your needs

## Next Steps/Features
We plan to continue building after the initial release and look forward to the feedback from the community. As of now we have following features planned out for next releases.

  - **Platform Compatibility:** Knee plans to support more OS and configurations.  
  
  - **Adaptation to Trends:** Staying updated with emerging technologies to meet the changing needs of users.

## Contribution Guidelines
We value the contributions of each developer and encourage you to share your ideas, improvements, and fixes with us. To ensure a smooth collaboration process, please follow these guidelines.

Before you begin:

 - Make sure you have a GitHub account.
 - Familiarize yourself with the project by reading the README, exploring the issues, and understanding the tool's architecture and coding standards.

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

