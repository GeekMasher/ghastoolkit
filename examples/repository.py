
from ghastoolkit import GitHub

GitHub.init("GeekMasher/ghastoolkit")
# repository from the loading GitHub
repository = GitHub.repository

# clone repo
repository.clone()
print(f" >> {repository.clone_path}")

# get a file from the repo
path = repository.getFile("README.md")
print(f" >> {path}")



