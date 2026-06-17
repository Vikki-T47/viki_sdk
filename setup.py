from setuptools import setup, find_packages
setup(
    name="viki-core",
    version="0.1.0",
    description="Reality Synchronization Architecture (RSA) for Agentic Workflows. Zero-Trust Middleware.",
    author="Viktor Trompak",
    packages=find_packages(),
    install_requires=["anthropic>=0.18.0"],
)
