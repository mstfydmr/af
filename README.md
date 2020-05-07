# AF
  
## Install & Upgrade
```bash
curl -sSL https://raw.githubusercontent.com/mstfydmr/af/master/install.sh | bash
```
  
# Usage Commands
  
## Overview
```bash
# Overview
af
```
![Overview](https://github.com/mstfydmr/af/raw/master/ss/1.png)
  
## Open MRs
```bash
# List all MRs from current branch to any branch.
af mr
```
![Open MRs](https://github.com/mstfydmr/af/raw/master/ss/2.png)
  
## Create New MR
```bash
  
# Template
af mr {target-branch}
  
# Create a MR to `master`
af mr master
  
# Create a MR to `staging`
af mr staging
  
# Create a MR to `develop`
af mr staging
...
```
![Create New MR](https://github.com/mstfydmr/af/raw/master/ss/3.png)
![Create New MR](https://github.com/mstfydmr/af/raw/master/ss/4.png)
![Create New MR](https://github.com/mstfydmr/af/raw/master/ss/5.png)
  
## Create a branch for a task
```bash
af branch
```
![Create a branch for a task](https://github.com/mstfydmr/af/raw/master/ss/6.png)