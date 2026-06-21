import os
import git
import logging

logger = logging.getLogger(__name__)

class VikiAuditScanner:
    """Профессиональный сканер для захвата стороннего кода."""
    def __init__(self, workspace="audit_workspace"):
        self.workspace = workspace
        os.makedirs(self.workspace, exist_ok=True)

    def clone_and_prepare(self, repo_url):
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        target_path = os.path.join(self.workspace, repo_name)
        
        if os.path.exists(target_path):
            print(f"📂 [SCANNER] Repository already present: {repo_name}. Using local copy.")
            return target_path
            
        print(f"🚀 [SCANNER] Executing secure clone: {repo_url}...")
        try:
            git.Repo.clone_from(repo_url, target_path)
            print(f"✅ [SCANNER] Target captured at {target_path}")
            return target_path
        except Exception as e:
            logger.error(f"Failed to clone repository: {e}")
            raise