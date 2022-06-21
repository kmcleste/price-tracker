# Amazon Price Tracker

![GitHub last commit](https://img.shields.io/github/last-commit/kmcleste/price-tracker?style=flat-square)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/kmcleste/price-tracker/Build%20docker%20image?label=docker%20build&logo=docker&style=flat-square)

The goal of this project is to function as a basic price tracking API - while also teaching the fundamentals of deploying a full stack project to the cloud.

## Getting Started

Prerequisites: [poetry](https://python-poetry.org/docs/), [pyenv](https://github.com/pyenv/pyenv), [pre-commit](https://pre-commit.com/)

1. Clone the repository:

    ```bash
    git clone https://github.com/kmcleste/price-tracker
    cd price-tracker
    ```

2. Initialize the project:

    ```bash
    make repo-init
    ```

    This script will install all of the necessary dependencies using poetry, then it will install the pre-commit hooks.
