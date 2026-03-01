# RBOTZILLA PHOENIX — Setup Instructions for Your New Computer

**Written for someone who does not code. Every step uses plain English.**

---

## What You Are Building

You are rebuilding the RBOTZILLA PHOENIX trading system on your new computer. This system automatically trades Forex on OANDA and cryptocurrency on Coinbase. It uses five proven trading strategies, a wolf pack regime detection system, an AI hive that uses three AI models to verify trades, and a full risk management system with automatic stop losses.

The code comes entirely from your existing GitHub repositories. Nothing new is being invented.

---

## What You Need Before Starting

**1. Your GitHub account** — You already have one at github.com/rfingerlin9284

**2. Your OANDA API credentials** — Log into oanda.com:
- Go to your account settings
- Find "Manage API Access"
- Generate a new Personal Access Token
- Copy your Account ID (shown at top of your dashboard)
- Write both down somewhere safe

**3. Your Coinbase Advanced Trade API credentials** — Log into advanced.coinbase.com:
- Go to Settings
- Go to API
- Create a new API key with "Trade" and "View" permissions
- Copy the API Key Name (it looks like organizations/xxx/apiKeys/xxx)
- Copy the Private Key (it is a long block of text starting with -----BEGIN EC PRIVATE KEY-----)
- Write both down somewhere safe

**4. Optional — AI API keys for the Hive Agent:**
- OpenAI: platform.openai.com (create account, go to API keys)
- Grok/XAI: x.ai or console.x.ai (create account, get API key)
- DeepSeek: platform.deepseek.com (create account, get API key)

---

## Step 1 — Open VS Code

Open VS Code on your new computer. If you do not have it yet:

- **Windows or Mac:** Download it from **code.visualstudio.com** and run the installer.
- **Linux:** See the detailed Linux install steps in [GITHUB_BASICS.md](GITHUB_BASICS.md) — it covers Ubuntu, Debian, Fedora, and all other common Linux distributions with exact commands.

**Not sure how to download the files from GitHub first?** See [GITHUB_BASICS.md](GITHUB_BASICS.md) for a plain-English guide on downloading this repository as a ZIP file, and for explanations of GitHub terms like "commits ahead" and "branches".

---

## Step 2 — Open the AI Chat / Copilot in VS Code

In VS Code, look for the GitHub Copilot chat icon on the left sidebar, or press Ctrl+Shift+I (Windows) or Cmd+Shift+I (Mac) to open the chat.

---

## Step 3 — Give the Agent This Instruction

Copy and paste this exact message into the VS Code AI chat:

---

> I need you to rebuild my RBOTZILLA trading system on this new computer. The complete instructions are in the file called VSCODE_AGENT_MEGA_PROMPT.md in my current project, and the source map is in REPO_SOURCE_MAP.md. Please read both files completely before doing anything, then follow every phase in order from Phase 1 to Phase 24. Please communicate with me only in simple plain English — do not show me any code, JSON, or terminal output in the chat. Just tell me what you are doing and when each phase is complete. If you need anything from me, ask in plain English.

---

Then press Enter and let the agent work.

---

## Step 4 — When the Agent Asks for Your API Keys

When the agent reaches Phase 19 (Setting up your .env file), it will ask you for your API keys one at a time. Simply type each one when asked. The agent will put them in the right place in your configuration file.

---

## Step 5 — When the Agent Says It Is Ready

When the agent tells you the system is assembled and ready, ask it:

> "Please run the system audit and tell me in plain English what passed and what failed."

---

## Step 6 — Your First Test Run

When everything passes the audit, ask the agent:

> "Please start the trading system on OANDA practice mode so I can see it working safely."

This runs the system connected to a practice (paper money) OANDA account. No real money is at risk. You can watch it analyze markets and make trading decisions in the log.

---

## Step 7 — Going Live

When you are satisfied the system is working correctly on practice mode, ask the agent:

> "Please switch me to live trading mode on OANDA with real money."

The agent will update your configuration to point to your live OANDA account.

---

## How to Stop the System at Any Time

Tell the agent:

> "Please stop all trading immediately."

Or if you need to stop it yourself manually, open VS Code terminal (press Ctrl+` or Cmd+`) and type:

```
bash ~/RBOTZILLA_PHOENIX/RBOTZILLA_LAUNCH.sh
```

Then choose Option 7 (Emergency Stop).

---

## How to Check What the System Is Doing

Ask the agent at any time:

> "What is the system doing right now? Show me a plain English summary of any open positions and recent trades."

---

## What Happens While the System Runs

The system runs completely automatically. Here is what it does without you doing anything:

- Every 60 seconds: Scans all six Forex pairs and two crypto pairs for trading signals
- Every 60 seconds: Uses three AI models to verify any signals it finds
- Every 30 seconds: Checks every open position and adjusts trailing stops
- Automatically closes positions that hit their stop loss or take profit targets
- Automatically closes positions that have been open for more than 6 hours
- Automatically stops trading for the day if daily loss limit is reached
- Automatically pauses if 5 trades in a row lose money

---

## The Five Trading Strategies

The system runs all five of these at once, automatically choosing which ones apply based on current market conditions:

1. **FABIO AAA** — Finds oversold markets using the RSI indicator. RSI threshold is set to 40, which was proven in backtesting to produce a 64.7% win rate and 369% ROI.

2. **Holy Grail** — Trades with the main trend when multiple timeframes all agree. This is the highest-weight strategy at 30%.

3. **EMA Scalper** — Catches fast short-term moves when moving averages cross each other.

4. **Institutional Supply and Demand** — Finds price zones where large banks and institutions are buying and selling.

5. **Trap Reversal** — Catches fake breakouts where price shoots past a level then immediately comes back.

---

## The Wolf Pack System

Before any trade is placed, the system checks what kind of market it is in right now:

- **Bull market** (prices trending up): Routes signals through the Bullish Wolf strategy weighting
- **Bear market** (prices trending down): Routes signals through the Bearish Wolf strategy weighting
- **Sideways market** (prices moving sideways): Routes signals through the Sideways Wolf strategy weighting

This ensures the right strategy is emphasized for current market conditions.

---

## Safety Rules That Cannot Be Turned Off

These rules are enforced by the trading charter and cannot be bypassed:

- Every trade must have a risk-to-reward ratio of at least 3.2 to 1 (you risk 1 dollar to make at least 3 dollars 20 cents)
- Trades are only placed on 15-minute, 30-minute, or 1-hour charts
- No trade stays open for more than 6 hours
- Every trade has a stop loss set before it opens
- Daily loss is capped at 2% of your account
- An emergency stop triggers at 3% daily loss
- Maximum 5 losses in a row before system pauses

---

## Questions?

Ask the VS Code agent anything in plain English and it will answer in plain English. Do not be afraid to ask "what is that in simple terms?" or "what does that mean for me?" at any time.

---

*This system is assembled entirely from code that exists in your GitHub repositories at github.com/rfingerlin9284. Nothing has been invented. Every strategy, connector, and risk rule has been proven and deployed before.*
