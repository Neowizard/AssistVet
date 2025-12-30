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
- Valid Provet account credentials
- Email account credentials for MFA

## Running

To run the system, set up the following environment variables, before invoking `docker compose up`

```

ASSISTVET_PROVET_ACCOUNT_ID - Account ID for the Provet account
ASSISTVET_PROVET_USERNAME - Username for the Provet system 
ASSISTVET_PROVET_PASSWORD - User password for the Provet system
ASSISTVET_MFA_PROVET_ACCOUNT_ID - Account ID for the Provet account
ASSISTVET_MFA_USERNAME - User for email service that receives Provet MFA codes
ASSISTVET_MFA_PASSWORD - Email service password
ASSISTVET_MFA_IMAP_URL - URL of the email service
```