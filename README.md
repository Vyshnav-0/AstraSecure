# AstraSecure - Advanced Security Toolkit

AstraSecure is a comprehensive, Python-based security auditing toolkit designed for security professionals and enthusiasts. It provides a suite of tools for password auditing, hash extraction, strength analysis, and attack simulation, all wrapped in a modern, user-friendly GUI.

**This project was assigned by Unified Mentor Pvt Ltd, and I am happy to have worked on it.**

## 🚀 Features

### 1. 🔍 Hash Extractor
*   **Automatic Detection:** Scans raw text or files to identify and extract potential hashes.
*   **Regex Pattern Matching:** Supports various hash types including MD5, SHA-1, SHA-256, SHA-512, NTLM, and bcrypt.
*   **Export:** Save extracted hashes to CSV or text files for further analysis.

### 2. 📝 Dictionary Generator (Wordlist Creator)
*   **Targeted Generation:** Create highly personalized wordlists based on user inputs (names, dates, keywords).
*   **Smart Mutations:** Applies intelligent transformations including:
    *   **Leetspeak:** Basic and advanced character substitutions.
    *   **Case Permutations:** Logic for lower, UPPER, Capitalized, and Inverted case.
    *   **Affix Analysis:** Appends common years, symbols, and number patterns.
    *   **Hybrid Modes:** Combines inputs to form complex phrases.

### 3. 💪 Password Strength Analyzer
*   **Real-time Analysis:** Evaluates passwords against complexity rules and entropy calculations.
*   **Feedback:** Provides actionable feedback (e.g., "Add special characters," "Avoid common patterns").
*   **Time to Crack:** Estimates the time required to crack the password derived from entropy and common hardware speeds.

### 4. ⚔️ Attack Simulators
*   **Dictionary Attack:** Perform file-based dictionary attacks against known hashes. Supports single and multi-threaded modes.
*   **Brute-Force Simulator:** Visualize the process of brute-forcing generic hashes to understand the exponential difficulty of length and charset increments.

### 5. 📊 Reporting
*   **Comprehensive Reports:** Generate detailed PDF or HTML reports summarizing findings from hash extractions or audit sessions.
*   **Visual Analytics:** Includes charts and graphs for password strength distribution (if applicable).

## 🛠️ Installation

### Prerequisites
*   Python 3.8+
*   pip (Python Package Manager)

### Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/astrasecure.git
    cd astrasecure
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## 🖥️ Usage

1.  **Run the Application**
    ```bash
    python main.py
    ```

2.  **Navigate the Interface**
    *   Use the sidebar to switch between different modules.
    *   **Dashboard:** Overview of the toolkit.
    *   **Tools:** Access individual tools like Extractor, Generator, etc.

## 📋 Requirements
The project relies on the following key libraries:
*   `customtkinter`: For the modern, dark-themed GUI.
*   `passlib`: For password hashing and verification.
*   `pandas`: For data manipulation and reporting.
*   `argon2-cffi` & `bcrypt`: For modern hash implementation support.

## ⚠️ Disclaimer
**AstraSecure is intended for educational and authorized security auditing purposes only.**
The developers are not responsible for any misuse of this tool. Always ensure you have permission before analyzing or attacking any system or data.

## 🤝 Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your features or fixes.

## 📄 License
This project is licensed under the MIT License.

## 📚 Third-Party Licenses

This software uses the following open-source packages:

*   **CustomTkinter**
    *   Copyright (c) 2023 Tom Schimansky
    *   License: MIT License

*   **Passlib**
    *   Copyright (c) 2008-2023 Eli Collins
    *   License: BSD License

*   **Pandas**
    *   Copyright (c) 2008-2011, AQR Capital Management, LLC, Lambda Foundry, Inc. and PyData Development Team
    *   License: BSD 3-Clause License

*   **Regex**
    *   Copyright (c) 2013-2024 Matthew Barnett
    *   License: Apache License 2.0

*   **Bcrypt**
    *   Copyright (c) 2006 The OpenBSD Project
    *   License: Apache License 2.0

*   **Argon2-cffi**
    *   Copyright (c) 2015 Hynek Schlawack
    *   License: MIT License
