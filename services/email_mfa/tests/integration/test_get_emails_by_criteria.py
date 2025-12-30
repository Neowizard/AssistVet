from pytest import fixture
import email_fetcher
import os
import provet_config


@fixture()
def configuration():
    return config.MfaConfig(os.getenv('TEST_ASSISTVET_IMAP_URL'),
                            os.getenv('TEST_ASSISTVET_USERNAME'),
                            os.getenv('TEST_ASSISTVET_PASSWORD'),
                            mfa_sender='dont-care')


def test_get_emails_by_criteria(configuration):
    subject = email_fetcher.EmailFetcher(configuration)
    actual = subject.get_emails_by_sender('forwarding-noreply@google.com')
    assert (len(actual) > 0,
            f"No emails found by criteria: (FROM \"{os.getenv('TEST_SENDER_ADDRESS')}\")"
            )
