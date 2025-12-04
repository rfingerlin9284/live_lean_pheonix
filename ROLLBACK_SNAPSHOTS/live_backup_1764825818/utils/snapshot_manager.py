#!/usr/bin/env python3
"""
Snapshot manager helpers based on git for lightweight save/restore snapshots.
This is intentionally small and dependency-free (uses subprocess and git).
"""
from __future__ import annotations

import subprocess
from datetime import datetime
from typing import Optional
import logging

logger = logging.getLogger("snapshot_manager")


def _run_git(*args, check: bool = True) -> str:
    cmd = ["git"] + list(args)
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
        return out.strip()
    except subprocess.CalledProcessError as ex:
        if check:
            logger.error("git command failed: %s; output: %s", ex.cmd, ex.output)
            raise
        return ex.output or ""


def create_snapshot(tag_prefix: str = "manual_snapshot") -> str:
    """Commit current changes (if any) and tag HEAD with a timestamped tag.
    Returns the tag name.
    """
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    tag = f"{tag_prefix}_{timestamp}"
    # Ensure we are inside a git repo
    try:
        _run_git("rev-parse", "--is-inside-work-tree")
    except Exception:
        raise RuntimeError("Not inside a git repository")

    # Add & commit current changes (ignore if nothing to commit)
    _run_git("add", "-A")
    try:
        _run_git("commit", "-m", f"Snapshot: {tag}")
    except Exception:
        logger.debug("No commit necessary or commit failed; continuing to tag")

    # Create tag
    _run_git("tag", tag)
    logger.info("Created snapshot tag %s", tag)
    return tag


def restore_snapshot(tag: str, new_branch: Optional[str] = None) -> str:
    """Create a new branch at the tag and check it out for safe restore.
    Returns the branch name created.
    """
    if not new_branch:
        new_branch = f"restore_{tag}"

    # Validate tag exists
    try:
        _run_git("rev-parse", "--verify", tag)
    except Exception:
        raise RuntimeError(f"Tag {tag} not found in repo")

    # Create a branch and checkout
    _run_git("checkout", "-b", new_branch, tag)
    logger.info("Restored snapshot %s to branch %s", tag, new_branch)
    return new_branch


__all__ = ["create_snapshot", "restore_snapshot"]
