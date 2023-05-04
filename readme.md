# pre-commit-hooks

This repository contains pre-commit hook called `insert-header-hook` which inserts file header to python files.

### Using pre-commit-hooks with pre-commit

Add this to your `.pre-commit-config.yaml`

```yaml
- repo: https://github.com/RamuniN/insert-header-hook
  rev: 1.0.0 # Use the ref you want to point at
  hooks:
    - id: insert-header-hook
      args: ["--project=MyProjectName", "--organisation=MyOrganisationName"]
```

The below is the sample of header that will be added to your python scripts.

```python
# test.py file

# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# PYTHONSCRIPT: test.py
# ------------------------------------------------------------------------------
# Copyright:    My Organisation Ltd.
# Project:      My project
#
# Created by:   2020-11-17 by example_1 <example_1@test.com>
# Last Update:  2020-11-17 by example_2 <example_2@test.com>
# ------------------------------------------------------------------------------
from setuptools import setup
setup()
......
```
