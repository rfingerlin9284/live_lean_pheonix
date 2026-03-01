# GitHub Basics — Plain-English Guide

**Written for someone who is new to GitHub. No coding knowledge required.**

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

You do **not** need to understand branches or commits to download the files. Here are two easy ways:

### Option A — Download Everything as a ZIP File (Easiest)

1. Go to the repository page on GitHub: `https://github.com/rfingerlin9284/live_lean_pheonix` (note: the repository name has "pheonix" spelled that way — use it exactly as shown)
2. Click the green **"Code"** button near the top right of the file list
3. In the dropdown that appears, click **"Download ZIP"**
4. A ZIP file will download to your computer
5. Find the ZIP file in your Downloads folder and extract (unzip) it
6. You now have all the files on your computer — no GitHub knowledge needed

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

## What Are the 19 Branches?

When you see multiple branches in this repository, they are different versions or working copies of the files. **You do not need to download or use all of them.** The files you need are all in the **main** branch (the default view when you visit the repository page).

To make sure you are on the main branch:
1. On the GitHub repository page, look for a button near the top left that shows a branch name
2. Click it and select **main** from the list
3. Now the files shown are the main, stable version

---

## Summary — What You Actually Need to Do

1. **Download VS Code** for Linux using the instructions above
2. **Download the files** from this repository using the ZIP download method
3. **Extract the ZIP** and open the folder in VS Code
4. **Follow [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)** step by step

You do not need to understand branches, commits, or any other GitHub concepts to get started. The ZIP download gives you everything you need.

---

*If you have more questions, ask the VS Code AI agent anything in plain English after you have it installed.*
