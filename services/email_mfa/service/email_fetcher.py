import imaplib
import email
import traceback

import fetched_email
import email.utils
import email.policy
from mfa_config import MfaConfig
from logging import getLogger

logger = getLogger(__name__)


class EmailFetcher:
    def __init__(self, config):
        self._config: MfaConfig = config

    def _connect(self) -> imaplib.IMAP4_SSL:
        logger.debug(f"Connecting to {self._config.imap_url}")
        mail = imaplib.IMAP4_SSL(self._config.imap_url)
        mail.login(self._config.username, self._config.password)
        mail.select("INBOX")
        return mail

    def get_emails_by_sender(self, sender_pattern: str, limit: int = 1,
                             retries: int = 3) -> list[fetched_email.FetchedEmail]:
        return self.get_emails_by_criteria(f'(FROM "{sender_pattern}")', limit, retries)

    def get_emails_by_criteria(self, criteria: str, limit: int = 1,
                               retries: int = 3) -> list[fetched_email.FetchedEmail]:
        mail = None
        tries = 1
        logger.info(f"Getting emails matching: {criteria}")
        while tries <= retries:
            try:
                mail = self._connect()
                email_ids = self._search_emails_by_criteria(mail, criteria, limit)
                emails = self._fetch_emails_by_ids(mail, email_ids)
                logger.info(f"Fetched {len(emails)} emails")
                return emails
            except Exception as e:
                traceback.print_exc()
                logger.error(f"({tries}/{retries}) Error getting emails: {e} ")
                tries += 1
            finally:
                if mail is not None:
                    mail.close()
                    mail.logout()
        return []

    def _search_emails_by_criteria(self, mail: imaplib.IMAP4_SSL, criteria: str,
                                   limit: int) -> list[str]:
        status, email_ids_bytes = mail.search(None, criteria)
        if status == "OK" and email_ids_bytes[0]:
            email_ids = email_ids_bytes[0].decode('utf-8').split(' ')
            logger.info(f"Found {len(email_ids)} ({limit=}) emails")
            emails_count = min(limit, len(email_ids))
            return email_ids[-emails_count:]
        else:
            return []

    def _fetch_emails_by_ids(self, mail: imaplib.IMAP4_SSL, email_ids: list[str]) -> list[fetched_email.FetchedEmail]:
        emails = []
        for email_id in email_ids:
            data: list[bytes | tuple[bytes, bytes]]
            status, data = mail.fetch(email_id, '(RFC822)')
            if status == 'OK':
                raw_email = data[0][1]
                parsed_email = email.message_from_bytes(raw_email, policy=email.policy.default)
                emails.append(fetched_email.FetchedEmail(parsed_email['Subject'],
                                                         parsed_email['From'],
                                                         email.utils.parsedate_to_datetime(parsed_email['Date']),
                                                         self._email_body(parsed_email)))
            else:
                logger.error(f"Error fetching email id {email_id}: '{status}'")
        return emails

    def _email_body(self, parsed_email: email.message.Message) -> str:
        if parsed_email.is_multipart():
            for part in parsed_email.walk():
                if part.get_content_type() == 'text/plain':
                    return part.get_payload(decode=True).decode(errors='ignore')
            raise Exception("No text/plain part found in multipart email_mfa")
        else:
            return parsed_email.get_payload()
