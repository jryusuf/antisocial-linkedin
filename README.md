# DEV CONTAINER TEMPLATE for FASTAPI
Dev container project with readily populated vscode extensions and some basic github actions

## CI/CD
When you commit it will run Black for linting and correct the formatting errors

When you push your project to any branch other than main or release it will run pytest with github actions

When you create a pull request to release branch it will run the tests, generate your docker image and push it your docker image repository

When you create a pull request it will run the test, you  can more step for your application

## Python Modules
Fastapi

Pytest for unit tests

Black

Pre-commit for linting

## Running
To run this docker dev container in your local or remote machine you need to install Docker and vscode to start

After installation pull this repo or click to run dev container button

It comes with requirements.txt file and automatically install all modules during setup, no need to virtual environment

## Creating your project
After running up the dev container, you need to rename your project and change the remote of your origin for git

Create master for deployment and release branches for builds, or you can rename them however you see fit. If you change the branch names do not forget to change the github action on tags with the new ones in the .github/workflows folder.


    on:

        pull_request:

            branches:

            - master or release(<-----update here)

Don't forget to create branch protection rules for these branches with the listed options:

    Require a pull request before merging

    Require review from Code Owners

    Require status checks to pass before merging

    Require bracnhes to be up to date before merging

    Status checks that are required: Select [Deployment-Test] or [Release-Test-And-Artifact]

This project containes a docker image file and when you create a pull request to relase branch it will create the docker image and publish it to your docker image hub

Update the tags at the end of the release-test-and-image-creating.yaml file with your own docker repo information

For authentication of your docker repo you need to create 2 repository secrets in your repo settings:

    DOCKER_PASSWORD

    DOCKER_USERNAME

For deployment you can update the master-test-and-deployment.yaml file for custom deployment strategy with some other github actions
