# Vendor Submission Drafts

These templates are designed to be copied directly into the respective vulnerability reporting portals.

---

## 1. Google Chrome Security Team (Chromium Bug Tracker)
**Title:** Security Bypass: Blob-Constructed Files Evade 'Mark of the Web' (MotW) on Disk Write
**Component:** Blink > Storage > Blob
**Type:** Security Feature Bypass

**Description:**
I have identified a security gap where files constructed via the `Blob` API and programmatically saved to disk (using `a.download` or `navigator.msSaveBlob`) do not consistently inherit the `Zone.Identifier` (Mark of the Web) alternate data stream.

**Impact:**
This allows a malicious website to drop a file onto the user's local filesystem that the Operating System treats as "Trusted Local Content" rather than "Internet Content". This bypasses OS-level security features like Windows SmartScreen and Protected View, which rely on MotW to trigger.

**Reproduction Steps:**
1. Navigate to the attached PoC page (`safe_poc.html`).
2. Click the "Download Safe Payload" button (or trigger via `onload`).
3. The browser saves `safe_research_poc.txt` to the Downloads folder.
4. Run the attached PowerShell script `Check-MotW.ps1 -FilePath .\safe_research_poc.txt`.
5. **Result:** The script reports "VULNERABLE: No Mark of the Web found".
6. **Expected:** The file should have `ZoneId=3` (Internet).

**Attack Scenario:**
An attacker uses XSS to construct a malicious script (e.g., `.wsf`, `.lnk`) inside a Blob. When saved to disk without MotW, the user can execute it without any security warnings from the OS.

---

## 2. Adobe PSIRT (Product Security Incident Response Team)
**Title:** Security Feature Bypass: Automatic Execution of PDF JavaScript via Open Parameters
**Product:** Acrobat Reader DC

**Description:**
The "Open Parameters" feature (e.g., `file.pdf#script=...`) allows a PDF to execute JavaScript immediately upon opening, bypassing the standard "Yellow Bar" trust warning for privileged operations.

**Impact:**
When combined with a browser-based delivery vector (like the Blob-to-Disk technique), this allows for "Zero-Click" execution of code within the Acrobat sandbox. While the sandbox protects the OS, this mechanism can be used to chain further exploits or exfiltrate local file data.

**Proof of Concept:**
1. Create a PDF with an OpenAction JavaScript trigger.
2. Host it at `http://attacker.com/exploit.pdf#FDF=...`.
3. Force the browser to open this URL using an iframe or new window.
4. **Result:** Acrobat opens and executes the script immediately without user confirmation.

---

## 3. Microsoft MSRC (Microsoft Security Response Center)
**Title:** Defense-in-Depth: Semantic Duality of .WSF Files Bypasses "Safe File" Heuristics
**Component:** Windows Script Host (WSH)

**Description:**
This report highlights a systemic weakness in how Windows handles "Polyglot" file types like `.wsf` (Windows Script File) and `.ps1xml`. These files are valid XML documents (parsable by browsers/readers) but are executable code when passed to `wscript.exe`.

**The Gap:**
Browsers and Email clients often blacklist known executables (`.exe`, `.bat`, `.cmd`). However, `.wsf` files are often permitted or treated as text/xml. When a file is dropped to disk (especially without MotW, as shown in the Chrome report), Windows executes it with full user privileges.

**Recommendation:**
Update Windows Defender or SmartScreen to strictly inspect `.wsf` and `.ps1xml` files originating from the browser, even if they lack the MotW stream (to mitigate the browser gap).

**Proof of Concept:**
See attached `safe_proof.wsf`. It is a valid XML file that executes VBScript to spawn `calc.exe` (simulated by MsgBox).
