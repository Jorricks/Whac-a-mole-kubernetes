from setuptools import setup, find_packages


base_packages = [
    "click"
]

dev_packages = [
    "mypy",
    "flake8"
]

setup(
    name="MolePod",
    version='1.0.0',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=base_packages,
    extras_require={
        'dev': dev_packages
    },
    description="",
    entry_points={"console_scripts": ["molepod = molepod.cli:main"]},
    author="Jorrick Sleijster",
)
