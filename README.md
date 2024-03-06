# Ansible Template Skeletons

## Overview
`ansible-template-skeletons` is an automated tool designed to keep your Ansible project's directory structure in sync with the latest recommendations from the official Ansible documentation. Utilizing GitHub Actions, this project checks the Ansible documentation daily for changes in the recommended project layout and automatically updates this repository to reflect those changes, ensuring best practices are always followed.

## Features
- **Automated Updates**: Leverages GitHub Actions to regularly check the Ansible documentation for any updates or changes in the directory structure.
- **Pull Request Management**: Automatically generates pull requests for changes, allowing for human review before merging.
- **Version Tagging**: Upon acceptance and merging of changes, the project is tagged with the current date, marking the version of the directory structure.

## Assumptions
This workflow is predicated on several stable factors:
- The [Ansible Sample Setup Documentation](https://docs.ansible.com/ansible/latest/tips_tricks/sample_setup.html) remains accessible and unchanged in its URL.
- Sample Ansible setups, illustrating best practices for project structures, continue to be provided within this documentation.
- The documentation's underlying HTML, particularly the CSS selectors, remain consistent for `retrieve.py`.

For minor changes to these factors, see `config.ini`.  For significant changes to these factors, adjustments to the workflow and parsing scripts may be necessary to maintain the functionality of this automated tool.

## Current Templates
<!-- TEMPLATE_START -->
#### sample-directory-layout:

```
📄 production                   # inventory file for production servers
📄 staging                      # inventory file for staging environment
📁 group_vars                  
    📄 group1.yml               # here we assign variables to particular groups
    📄 group2.yml              
📁 host_vars                   
    📄 hostname1.yml            # here we assign variables to particular systems
    📄 hostname2.yml           
📁 library                      # if any custom modules, put them here (optional)
📁 module_utils                 # if any custom module_utils to support modules, put them here (optional)
📁 filter_plugins               # if any custom filter plugins, put them here (optional)
📄 site.yml                     # main playbook
📄 webservers.yml               # playbook for webserver tier
📄 dbservers.yml                # playbook for dbserver tier
📁 tasks                        # task files included from playbooks
    📄 webservers-extra.yml     # <-- avoids confusing playbook with task files
📁 roles                       
    📁 common                   # this hierarchy represents a "role"
        📁 tasks               
            📄 main.yml         # <-- tasks file can include smaller files if warranted
        📁 handlers            
            📄 main.yml         # <-- handlers file
        📁 templates            # <-- files for use with the template resource
            📄 ntp.conf.j2      # <------- templates end in .j2
        📁 files               
            📄 bar.txt          # <-- files for use with the copy resource
            📄 foo.sh           # <-- script files for use with the script resource
        📁 vars                
            📄 main.yml         # <-- variables associated with this role
        📁 defaults            
            📄 main.yml         # <-- default lower priority variables for this role
        📁 meta                
            📄 main.yml         # <-- role dependencies and optional Galaxy info
        📁 library              # roles can also include custom modules
        📁 module_utils         # roles can also include custom module_utils
        📁 lookup_plugins       # or other types of plugins, like lookup in this case
    📁 webtier                  # same kind of structure as "common" was above, done for the webtier role
    📁 monitoring               # ""
    📁 fooapp                   # ""
```

#### alternative-directory-layout:

```
📁 inventories                 
    📁 production              
        📄 hosts                # inventory file for production servers
        📁 group_vars          
            📄 group1.yml       # here we assign variables to particular groups
            📄 group2.yml      
        📁 host_vars           
            📄 hostname1.yml    # here we assign variables to particular systems
            📄 hostname2.yml   
    📁 staging                 
        📄 hosts                # inventory file for staging environment
        📁 group_vars          
            📄 group1.yml       # here we assign variables to particular groups
            📄 group2.yml      
        📁 host_vars           
            📄 stagehost1.yml   # here we assign variables to particular systems
            📄 stagehost2.yml  
📁 library                     
📁 module_utils                
📁 filter_plugins              
📄 site.yml                    
📄 webservers.yml              
📄 dbservers.yml               
📁 roles                       
    📁 common                  
    📁 webtier                 
    📁 monitoring              
    📁 fooapp                  
```

<!-- TEMPLATE_END -->