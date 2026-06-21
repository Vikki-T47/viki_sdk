import subprocess
import os
import sys
import logging

logger = logging.getLogger(__name__)

class VikiAuditScanner:
    """Автоматический сканер чужих репозиториев."""
    def __init__(self, workspace="audit_workspace"):
        self.workspace = workspace
        os.makedirs(self.workspace, exist_ok=True)

    def clone_and_prepare(self, repo_url):
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        target_path = os.path.join(self.workspace, repo_name)
        
        if not os.path.exists(target_path):
            print(f"🚀 [SCANNER] Cloning: {repo_url}...")
            subprocess.run(["git", "clone", repo_url, target_path], check=True)
        
        sys.path.append(target_path)
        print(f"✅ [SCANNER] Target ready at {target_path}")
        return target_path