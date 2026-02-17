# Safe Research PoC Toolkit

This toolkit is designed to safely demonstrate the "Zero-Click" vulnerability chain (XSS -> Blob -> Disk -> Polyglot) without using any external domains or malware.

## What's Included?

1.  **`generate_safe_poc.py`**: A Python script that creates the self-contained HTML exploit.
2.  **`Check-MotW.ps1`**: A PowerShell tool to prove the "Mark of the Web" bypass.
3.  **`safe_proof.wsf`**: A harmless "Polyglot" file that opens a message box (proof of code execution).
4.  **`Vendor_Reports.md`**: Ready-to-use templates for reporting this to Google, Microsoft, and Adobe.

## Step-by-Step Instructions

### Step 1: Generate the PoC
1.  Download `generate_safe_poc.py`.
2.  Run it using Python:
    ```bash
    python generate_safe_poc.py
    ```
3.  This will create a new file called `local_poc.html` in the same folder.

### Step 2: Trigger the Exploit (Simulated)
1.  Open `local_poc.html` in Google Chrome (just double-click it).
2.  Wait 2 seconds. The page will simulate a "Zero-Click" event and automatically download a file named `research_payload.pdf`.
3.  Go to your **Downloads** folder to find the file.

### Step 3: Verify the Vulnerability (The Evidence)
1.  Open PowerShell in your Downloads folder.
2.  Run the checker script against the downloaded file:
    ```powershell
    .\Check-MotW.ps1 -FilePath .\research_payload.pdf
    ```
3.  **Success:** If it says `[!] VULNERABLE: No Mark of the Web found`, you have proof that Chrome failed to secure the file.

### Step 4: Report It
1.  Open `Vendor_Reports.md`.
2.  Copy the section for **Google Chrome** and submit it to the [Chromium Bug Tracker](https://issues.chromium.org/).
3.  Attach your `local_poc.html` and the screenshot of the PowerShell output as evidence.

**Stay Safe & Ethical:** This tool is for educational and defensive research purposes only.
