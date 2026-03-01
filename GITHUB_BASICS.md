# GitHub Basics — Plain-English Guide

**Written for someone who is new to GitHub. No coding knowledge required.**

## ⚠️ IMPORTANT — This Repository Has Two Key Branches

**The `main` branch** (what you see by default) only has **the instruction documents** — the setup guides and the agent prompt. That is all that is supposed to be here.

**The `master` branch** has the **actual trading system code** — all the Python strategy files, broker connectors, wolf pack files, shell scripts, and everything else the VS Code agent needs to work with.

**You need to download the `master` branch, not `main`.** The download instructions below show you exactly how to get the right one.

---

## What Is GitHub?

GitHub is a website where people store and share computer files — mostly code. Think of it like Google Drive, but designed for software projects. This repository (the folder you are looking at right now) contains all the instructions needed to rebuild your RBOTZILLA PHOENIX trading system.

---

## GitHub Words You Will See (And What They Mean)

### Repository (or "Repo")
A folder on GitHub that holds all the files for a project. This entire project — all the setup instructions, the agent prompt, everything — is stored in one repository.

### Branch
A separate copy of the files inside a repository. Think of it like making a photocopy of a notebook so you can write changes on the copy without messing up the original.

- The main copy is usually called **main** or **master**
- Other branches have names like `copilot/help-with-vscode-download`

### Commits
Every time someone saves a change to the files, that save is called a **commit**. Each commit has a short description of what changed.

### "This branch is X commits ahead, Y commits behind" — What does that mean?
This message means the branch you are looking at has **some changes that the main branch does not have yet**, and/or the main branch has changes that this branch does not have yet.

**Example:** "This branch is 11 commits ahead, 4 commits behind"

- **11 commits ahead** → This branch has 11 saved changes that are *not* in the main branch yet
- **4 commits behind** → The main branch has 4 saved changes that are *not* in this branch yet

**What should you do about it?** Nothing, unless you are the person managing the code. If you just need to use the files, simply download or view the files you need (see below).

### Fork
A personal copy of someone else's entire repository saved to your own GitHub account.

### Clone
Downloading a full copy of a repository to your own computer so you can work on the files locally.

### Pull Request (PR)
A request to merge (combine) changes from one branch into another branch.

---

## How to Download the Files From This Repository

**You need the `master` branch** — that is where all the actual code lives. Here are two easy ways to get it:

### Option A — Download the `master` Branch as a ZIP File (Easiest — Do This One)

**Direct download link — click this to get the ZIP immediately:**

> **https://github.com/rfingerlin9284/live_lean_pheonix/archive/refs/heads/master.zip**

Just click that link in your browser and the ZIP will start downloading automatically. No GitHub account needed.

Or manually:
1. Go to: `https://github.com/rfingerlin9284/live_lean_pheonix/tree/master`
2. Click the green **"Code"** button near the top right of the file list
3. In the dropdown that appears, click **"Download ZIP"**
4. A ZIP file will download to your computer
5. Find the ZIP file in your Downloads folder and extract (unzip) it
6. You now have all the code files on your computer

### Option B — View and Copy Individual Files

1. Go to the repository page on GitHub
2. Click on any file name (for example, `SETUP_INSTRUCTIONS.md`)
3. The file contents will display on the screen
4. You can read it right there, or click the **"Raw"** button to see plain text that you can copy and paste

---

## How to Download and Install VS Code on Linux

VS Code is the program you will use to run the AI agent that rebuilds your trading system.

### Step 1 — Go to the VS Code Download Page
Open a web browser and go to: **https://code.visualstudio.com/download**

### Step 2 — Choose the Right Linux Version

On the download page you will see options for Linux. Choose based on your Linux distribution:

| If you use… | Download this |
|---|---|
| Ubuntu, Debian, Linux Mint, Pop!_OS | `.deb` file (64-bit) |
| Fedora, CentOS, Red Hat, openSUSE | `.rpm` file (64-bit) |
| Any Linux (universal option) | `.tar.gz` or snap package |

If you are not sure which Linux you have, open a terminal and type `cat /etc/os-release` — look for the `NAME=` line.

### Step 3 — Install VS Code

**For Ubuntu / Debian (.deb file):**

1. Open your file manager and find the downloaded `.deb` file in your Downloads folder
2. Double-click it — the Software Center should open automatically and offer to install it
3. Click **Install** and enter your password if asked

Or open a terminal and type:
```
cd ~/Downloads
sudo dpkg -i code_*.deb
sudo apt-get install -f
```

**For Fedora / Red Hat (.rpm file):**

Open a terminal and type:
```
cd ~/Downloads
sudo rpm -ivh code_*.rpm
```

**For any Linux (snap — simplest method if snap is available):**

Open a terminal and type:
```
sudo snap install --classic code
```

### Step 4 — Open VS Code

After installing, open VS Code by:
- Searching for "Visual Studio Code" or "Code" in your application launcher
- Or typing `code` in a terminal

### Step 5 — Install the GitHub Copilot Extension

Once VS Code is open:
1. Click the **Extensions** icon on the left sidebar (it looks like four squares)
2. In the search box, type `GitHub Copilot`
3. Click **Install** on the GitHub Copilot extension
4. Sign in with your GitHub account when prompted

After that, follow the instructions in [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) starting at **Step 2**.

---

## What Are All These Branches?

This repository has around 19 branches. Here is what the most important ones are:

| Branch name | What it contains |
|---|---|
| **`master`** | ✅ **The full trading system code** — strategies, brokers, wolf packs, scripts. **This is the one you need.** |
| **`main`** | 📄 Only the instruction/documentation files (like this one). No code here. |
| `feature/core-engines` | An older working copy of the code, same as master |
| `worktree-2025-12-*` | Automatic snapshots taken at specific points in time |
| `copilot/*` | Branches where the GitHub Copilot AI assistant made changes |
| `archive/*` | Old versions kept for reference |

**The short answer: download `master`. Ignore all the other branches.**

To switch to the `master` branch while browsing on GitHub:
1. On the GitHub repository page, look for a button near the top left that shows the current branch name (it probably says `main`)
2. Click that button
3. A dropdown will appear — click **master**
4. Now the file list shows all the code

Or just use the direct ZIP download link above and skip the branch switching entirely.

---

## Summary — What You Actually Need to Do

1. **Download the `master` branch ZIP** using the direct link above: `https://github.com/rfingerlin9284/live_lean_pheonix/archive/refs/heads/master.zip`
2. **Extract the ZIP** — you will get a folder called `live_lean_pheonix-master`
3. **Download VS Code** for Linux using the instructions above (or from code.visualstudio.com)
4. **Open the extracted folder** in VS Code
5. **Follow [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)** step by step

You do not need to understand branches, commits, or any other GitHub concepts to get started. The single ZIP download link above gives you everything you need.

---

*If you have more questions, ask the VS Code AI agent anything in plain English after you have it installed.*
