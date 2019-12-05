from setuptools import setup, find_packages


base_packages = [
    "click",
    "gevent",
    "flask",
    "requests"
]

dev_packages = [
    "mypy",
    "flake8",
    "pytest",
]

setup(
    name="MoleRelay",
    version='1.0.0',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=base_packages,
    extras_require={
        'dev': dev_packages
    },
    description="",
    entry_points={"console_scripts": ["molerelay = molerelay.cli:main"]},
    author="Jorrick Sleijster",
)
