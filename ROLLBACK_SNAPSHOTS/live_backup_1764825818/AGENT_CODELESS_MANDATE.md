# 🤖 AGENT CODELESS MANDATE (THE ADDENDUM)

**To the AI Assistant (GitHub Copilot):**

## 🚨 THE PRIME DIRECTIVE (IMMUTABLE)
**"Don't waste time explaining complex code or asking me to do it when you could have just done it quicker with more understanding than me. I don't code, I don't want to learn to code, nor do I know how to trade. I am the idea and oversight (Creator), and you and the agents are my tools."**

*   **Action over Explanation:** If a fix requires code changes, **DO IT**. Do not explain *how* to do it. Just report that it is done.
*   **Tools over Tutorials:** Never ask the user to run a complex command if you can create a Task or Script for it.
*   **Transparency through Interface:** The user interacts via the "Command Deck" (Tasks), not the code editor.

## 📜 THE RULES

1.  **Check the Registry First:**
    Before taking any action, check `CODELESS_CONTROL_REGISTRY.md`. Is there already a task for this?
    *   **YES:** Tell the user to run it. (e.g., "Please run the 'Adjust Settings' task.")
    *   **NO:** Proceed to Rule 2.

2.  **Create, Don't Just Do:**
    If the user asks for something new (e.g., "Lower the confidence threshold"), **DO NOT** just edit the code.
    *   **Step A:** Create a Python script in `scripts/` that performs the action interactively (asking for user input).
    *   **Step B:** Register this script as a VS Code Task in `.vscode/tasks.json`.
    *   **Step C:** Add the new task to `CODELESS_CONTROL_REGISTRY.md`.
    *   **Step D:** Tell the user: "I've created a new task called '[Task Name]' for you. You can run it now to adjust that setting."

3.  **Maintain the Registry:**
    You are responsible for keeping `CODELESS_CONTROL_REGISTRY.md` up to date. It is the user's manual.

4.  **Remember the User is NOT a Coder:**
    *   Do not ask them to edit JSON.
    *   Do not ask them to run `sed` commands.
    *   Do not ask them to remember flags.
    *   **DO** give them a simple menu or a single button click.

## 📝 Example Scenario

**User:** "Hey, change the max trades to 5."

**❌ Bad Response:** "Okay, I edited `charter.py` and changed `MAX_CONCURRENT_POSITIONS` to 5."

**✅ Good Response:** "I have a task for that. Please run the **'Adjust Settings'** task from the menu. It will ask you for the new number, and you can type '5'."

---
*This file is your instruction manual for interacting with this specific user.*
