# WIP
# AssistVet

AssistVet is a microservices-based veterinary practice management assistant that integrates with Provet veterinary practice management software.
It uses MCP to provide an LLM interface into the Provet data-system to identify and resolve management issues.

## Architecture

The project consists of multiple microservices:

- **Provet Service**: Core service for querying and updating Provet data
- **Email MFA Service**: Handles multi-factor authentication via email
- **Frontend Service**: User interface
- **Chat Service**: AI chatbot conversational interface

## Prerequisites

- **Docker** and **Docker Compose**
- **Python 3.12+**
- **pyenv** (recommended for Python version management)
- **make** (recommended for easy command execution)
- Valid Provet account credentials
- Email account credentials for MFA

## Running

To run the system, update the config.yaml files or set the appropriate environment variables to override the config. 
The override format is:
```
ASSISTVET_<SERVICE>_<UPCASE_CONFIG_NAME>=<value>
```
For example, to override the `provet_username` config for the `provet` service, set the environment variable:

```
ASSISTVET_PROVET_PROVET_USERNAME=my_username
```
To set the `imap_url` config for the `email_mfa` service, set the environment variable:

```
ASSISTVET_EMAIL_MFA_IMAP_URL=imap.example.com
```

### Run with Make
After setting the necessary configurations, you can start the services with `make up` (or `make debug` to troubleshoot). 
Take the service down with `make down`


## First Setup
To set up the project, you first need to start the services with `make up`, and then run the DB setup Make task with `make migrate` 

