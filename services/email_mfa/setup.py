from setuptools import setup, find_packages

setup(
    name="AssistVet MFA Service",
    version="0.1.0",
    description="An AssistVet microservice for retrieving MFA codes from email",
    author="Neowizard",
    author_email="hk.neowizard@gmail.com",
    package_dir={"": "service"},
    install_requires=[],
    include_package_data=True,
    python_requires=">=3.12",
)
