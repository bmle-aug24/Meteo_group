import subprocess as sp
from datetime import datetime

def main():
    files = ["data/raw"]
    message_commit  = f"Update_DVC {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}"
    for file in files:
        sp.run(["dvc", "add", file], check=True)
        sp.run(["git", "add", file+".dvc"], check=True)
    sp.run(["dvc", "push"], check=True)
    sp.run(["git", "commit", "-m", message_commit], check=True)
    sp.run(["git", "push"], check=True)
    print("Data pushed for versioning")

if __name__ == "__main__":
    main()