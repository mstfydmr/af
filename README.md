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

## Open MRs
```bash
# List all MRs from current branch to any branch.
af mr
```

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

