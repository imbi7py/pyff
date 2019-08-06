#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function
import sys
import subprocess

_LIST_FIXERS = [sys.executable, "-m", "modernize", "--list"]
_RUN_FIXER = [sys.executable, "-m", "modernize", "-wnf"]
_GIT_STATUS = ["git", "status", "--porcelain", "--untracked-files=no"]
_GIT_ADD = ["git", "add", "-u", "."]
_GIT_COMMIT = ["git", "commit", "-m"]

def iter_available_fixers():
    fixer_info = subprocess.check_output(_LIST_FIXERS, text=True).splitlines()
    fixer_lines = (line for line in fixer_info if '(' in line)
    return (line.partition('(')[2].partition(')')[0] for line in fixer_lines)

def have_git_changes():
    return bool(subprocess.check_output(_GIT_STATUS).strip())

def add_updated_files():
    subprocess.check_call(_GIT_ADD)

def commit_changes(message):
    subprocess.check_call(_GIT_COMMIT + [message])

def apply_fixer(fixer_name, *, no_six=False):
    if have_git_changes():
        raise RuntimeError("Git repository is not clean")
    print(("======== {} ========".format(fixer_name)))
    cmd = _RUN_FIXER + [fixer_name, "."]
    if subprocess.call(cmd):
        print("Issues reported when attempting to apply fixer")
    if have_git_changes():
        print("Changes made by fixer, committing to git")
        add_updated_files()
        commit_changes("Applied modernize changes for fixer: " + fixer_name)
        return True
    return False

# Allow selected fixers to be forced to be applied last
# TODO: Make this a command line option
_APPLY_LAST = ["unicode_type"]
# Allow selected fixers to be skipped entirely
# TODO: Make this a command line option
_DO_NOT_APPLY = set()

if __name__ == "__main__":
    all_fixer_names = set(iter_available_fixers())
    fixer_names = sorted(all_fixer_names - set(_APPLY_LAST) - _DO_NOT_APPLY)
    applied = set()
    # First apply all the fixers that don't need six
    for fixer_name in fixer_names:
        if apply_fixer(fixer_name, no_six=True):
            applied.add(fixer_name)
    # On the second pass, allow fixers that need six
    for fixer_name in fixer_names:
        if fixer_name in applied:
            continue
        apply_fixer(fixer_name)
    # Apply the explicitly delayed fixers
    for fixer_name in fixer_names:
        apply_fixer(fixer_name)
