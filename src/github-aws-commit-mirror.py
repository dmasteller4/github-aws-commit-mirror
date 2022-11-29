from github import Github
import boto3
import os

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
GITHUB_API_TOKEN = os.getenv('GH_API_TOKEN')
print("Github token: " + GITHUB_API_TOKEN)

github_client = Github(GITHUB_API_TOKEN)

codecommit_client = boto3.client('codecommit', region_name='us-east-1',aws_access_key_id=S3_KEY, aws_secret_access_key=S3_SECRET)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def clone_repo(repo_name):
    print(f"{bcolors.OKGREEN}--> Cloning repository {repo_name} to local storage {bcolors.ENDC}")
    os.system('git clone --mirror https://github.com/rribeiro1/{}.git {}'.format(repo_name, repo_name))


def delete_repo_local(repo_name):
    print(f"{bcolors.OKGREEN}--> Deleting repository {repo_name} from local storage {bcolors.ENDC}")
    os.system('rm -Rf {}'.format(repo_name))


def is_repo_exists_on_aws(repo_name):
    try:
        codecommit_client.get_repository(repositoryName=repo_name)
        return True
    except Exception:
        return False


def create_repo_code_commit(repo_name):
    print(f"{bcolors.OKBLUE}--> Creating repository {repo_name} on AWS CodeCommit {bcolors.ENDC}")
    codecommit_client.create_repository(
        repositoryName=repo_name,
        repositoryDescription='Backup repository for {}'.format(repo_name),
        tags={
            'name': repo_name
        }
    )


def sync_code_commit_repo(repo_name):
    print(f"{bcolors.OKGREEN}--> Pushing changes from repository {repo_name} to AWS CodeCommit {bcolors.ENDC}")
    os.system('cd {} && git remote add sync ssh://git-codecommit.eu-central-1.amazonaws.com/v1/repos/{}'.format(repo_name, repo_name))
    os.system('cd {} && git push sync --mirror'.format(repo.name))


for repo in github_client.get_user().get_repos():
    if repo.archived:
        print(f"{bcolors.WARNING}> Skipping repository {repo.name}, it is archived on github {bcolors.ENDC}")
    else:
        print(f"{bcolors.HEADER}> Processing repository: {repo.name} {bcolors.ENDC}")
        clone_repo(repo.name)

        if is_repo_exists_on_aws(repo.name):
            sync_code_commit_repo(repo.name)
        else:
            create_repo_code_commit(repo.name)
            sync_code_commit_repo(repo.name)

        delete_repo_local(repo.name)
