from setuptools import setup, find_packages

setup(
    name="AssistVet AI",
    version="0.1.0",
    description="An AssistVet microservice that serves AI capabilities",
    author="Neowizard",
    author_email="hk.neowizard@gmail.com",
    package_dir={"": "service"},
    install_requires=[],
    include_package_data=True,
    python_requires=">=3.12",
)
