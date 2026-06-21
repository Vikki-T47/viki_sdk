import subprocess
import os
import sys

class VikiAuditScanner:
    """Инструмент для автоматического развертывания полигона над чужим кодом."""
    def __init__(self, workspace="audit_workspace"):
        self.workspace = workspace
        os.makedirs(self.workspace, exist_ok=True)

    def clone_and_prepare(self, repo_url):
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        target_path = os.path.join(self.workspace, repo_name)
        if not os.path.exists(target_path):
            subprocess.run(["git", "clone", repo_url, target_path], check=True)
        sys.path.append(target_path)
        return target_path