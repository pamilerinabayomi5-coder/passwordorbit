# PasswordOrbitBot 🔑

PasswordOrbitBot is a modular, high-entropy, production-ready Telegram bot engineered using Python 3.12+ and `python-telegram-bot` (v21+). It generates cryptographically sound passwords using Python's `secrets` module, strictly ensuring compliance with structural parameters requested by users.

## 🚀 Features
- **Cryptographically Secure**: Built purely with Python's native `secrets` module (never uses `random`).
- **Granular Customization**: Interactive controls over upper, lower, numeric, symbol inclusions, string bounds lengths (4-128), and output counts (1-20).
- **Ambiguous Character Exclusions**: Safely filters confusing character structures like `0, O, l, I` on demand.
- **Persistent Preferences**: Saves settings across interactions using an internal SQLite database layer.
- **Clean Markdown Display**: Passwords display inside individual monospace block highlights for simple click-to-copy capability.

---

## 📂 Project Architecture
```text
PasswordOrbitBot/
├── bot.py                  # Operational Entrypoint Routine 
├── config.py               # Settings and Core Logging Infrastructure
├── database.py             # SQLite Queries Engine Layer
├── handlers.py             # Update Request Interceptors and Routing Logic
├── keyboards.py            # Inline Layout UI Generation Templates
├── password_generator.py   # Cryptographic Randomization Rules Engine
├── utils.py                # Regex Data Handlers and Transformers
├── requirements.txt        # Runtime Library Specifications
├── runtime.txt             # Target Execution Version Pointer
├── render.yaml             # Render Deployment Blueprint Configuration
├── .env.example            # Environment Configurations Configuration Reference Blueprint
└── .gitignore              # Version Control Filters Index
