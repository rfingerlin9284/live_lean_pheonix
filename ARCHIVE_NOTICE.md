# Archive Notice

This commit documents the archiving of duplicate files found on the operator's workspace.

Archive location: /home/ing/RICK/RICK_PHOENIX_ARCHIVE/20251222T073750Z

Summary:
- Files identified as duplicates and moved to archive (see manifest). These were external or not tracked in this repository, so there were no tracked files to remove in this checkout.
- Total archived candidates: 51,470 (see archive manifest and moved_files_list.txt in the archive)

Reason for archiving:
- Remove duplicate/stale files and worktrees from the workspace and centralize them in an archive for easier maintenance and smaller repo surface area.

Restore instructions and scripts are included inside the above archive directory (`restore.sh`, `restore_originals.sh`).

Maintenance marker: the operator placed a maintenance marker at `/home/ing/RICK/RICK_PHOENIX/var/maintenance/TRADING_DISABLED.txt` to prevent accidental restarts of trading behavior.

