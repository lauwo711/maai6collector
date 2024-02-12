# **maai6collector**:iphone:

## Intro<br>
A project just to collect some opensource data.

## Project structure<br>
Each datasource has its own directory to store its pyproject.toml in order to minimize dependency. <br>
Each datasource has its own docker image build.<br>
Goal is to deploy each image with their schedule on ECS using infra as code. :sparkles:

docker build --build-arg DATA_DIR=hk_tradable_stocks --tag=<tag_name> .
