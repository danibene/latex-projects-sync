import os
import re
import pathlib
from warnings import warn
from github import Github
from json_tricks import load


def get_secrets(local_secrets_path=None):
    if local_secrets_path is None:
        local_secrets_path = os.path.join("local_secrets", "secrets.json")
    if os.path.isfile(local_secrets_path):
        with open(local_secrets_path, "r") as json_file:
            secrets = load(json_file)
    else:
        secrets = os.environ
    return secrets


def github_authentication(secrets=os.environ):
    access_token = secrets["ACCESS_TOKEN_GITHUB"]
    return Github(access_token)
    
def get_github_repos(g, repo_paths=None, secrets=os.environ):
    if repo_paths is None:
        repo_paths = secrets["REPO_PATHS_GITHUB"].split(", ")
    return [g.get_repo(repo_path) for repo_path in repo_paths]

def get_sync_results(repos, sync_direction="TO"):
    results = {}
    for repo in repos:
        contents = repo.get_contents("")
        suffixes = [".bib", ".tex"]
        content_paths = [content.path for content in contents]
        content_paths_for_sync = [p for p in content_paths if 
                                  pathlib.Path(p).suffix in suffixes]
        
        for p in content_paths_for_sync:
            decoded_content = repo.get_contents(p).decoded_content.decode()
            s = decoded_content
            sync_labels = re.findall(r"%%%START_SYNC_" + sync_direction + 
                                     "_(.*?)%", s, re.DOTALL|re.MULTILINE)
            if len(sync_labels) > 0:
                for sync_label in sync_labels:
                    
                    start_str = ("%%%START_SYNC_" + sync_direction + 
                                        "_" + sync_label + "%")
                    stop_str = ("%%%STOP_SYNC_" + sync_direction + 
                    "_" + sync_label + "%")
                    result = re.findall(r"" + start_str + "(.*?)" + stop_str, 
                                         s, re.DOTALL|re.MULTILINE)
                    if len(result)==0:
                        warn("There was no matching stop label found for " + sync_label)
                    elif len(result) > 1:
                        warn("There were multiple instances found for " + sync_label)
                    else:
                        results[sync_label] = {}
                        results[sync_label]["repo_owner"] = repo.owner.login
                        results[sync_label]["repo_name"] = repo.name
                        results[sync_label]["path"] = p
                        results[sync_label]["content"] = start_str + result[0] + stop_str
                        
    return results

if __name__ == "__main__":
    
    secrets = get_secrets()
    g = github_authentication(secrets=secrets)
    repos = get_github_repos(g, secrets=secrets)
    
    to_results = get_sync_results(repos, sync_direction="TO")
    from_results = get_sync_results(repos, sync_direction="FROM")
    
    for sync_label in from_results.keys():
        old_replace_content = from_results[sync_label]["content"]
        new_replace_content = to_results[sync_label]["content"]
        repo_paths = [from_results[sync_label]["repo_owner"] + "/" 
                                  + from_results[sync_label]["repo_name"]]
        repo = get_github_repos(g, repo_paths)[0]
        contents = repo.get_contents(from_results[sync_label]["path"])
        decoded_content = contents.decoded_content.decode()
        sha = contents.sha
        new_decoded_content = decoded_content.replace(old_replace_content, new_replace_content)
        repo.update_file(from_results[sync_label]["path"], "sync from " + sync_label, new_decoded_content, sha=sha)
        
    
