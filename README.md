## Guidelines
1. Don't directly push to master branch.
2. Don't merge the PR to master without my approval.
3. I will merge the PR when all the comments are fixed(if any).
4. Follow basic pep8 conventions.
5. Use Black for code formatting(we'll start using it).

## Project SETUP
1. $ mkdir imagefix
2. $ cd imagefix
3. $ virtualenv -p python3 venv
4. $ git pull https://github.com/dbms/imagefix.git
5. $ source venv/bin/activate
6. $ cd imagefix && pip install -r requirements.txt

## Branching Conventions

The different types of branches we will be using are:
  - Feature branches (branch name should be like - feat/image-to-pdf)
  - Bug branches (branch name should be like - bug/image-download)
  - Hotfix branches (branch name should be like - hot/image-spelling)
