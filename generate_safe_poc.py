# Safe Research PoC Generator
# Author: [Your Name]
# Purpose: Demonstrate the "Zero-Click" Logic Chain safely.

import os

def create_safe_poc():
    print("[*] Starting Safe PoC Generation...")

    # Stage 1: The "XSS" Trigger (Simulated)
    # Instead of an actual exploit, we create a harmless HTML file.
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Safe Research PoC</title>
        <script>
            // This script simulates the "Zero-Click" logic.
            // In a real scenario, this would be injected via XSS.
            window.onload = function() {
                console.log("[Stage 1] Page Loaded. Simulating Blob Construction...");

                // Stage 2: Blob Construction (Safe Text)
                const blobContent = "PoC Research Success: Stage 2 Complete. This is a harmless text file.";
                const blob = new Blob([blobContent], { type: 'text/plain' });

                // Simulate the "Download" or "Open" action
                const link = document.createElement('a');
                link.href = URL.createObjectURL(blob);
                link.download = "safe_research_poc.txt"; // Safe extension
                document.body.appendChild(link);
                link.click();

                console.log("[Stage 2] Blob Constructed & Download Triggered.");
            };
        </script>
    </head>
    <body>
        <h1>Safe Research PoC</h1>
        <p>This page demonstrates the logical flow of the research.</p>
        <p>Check your console (F12) for status messages.</p>
    </body>
    </html>
    """

    with open("safe_poc.html", "w") as f:
        f.write(html_content)
    print("[+] Created 'safe_poc.html' - Open this in your browser to test the flow.")

    # Stage 3: The "Polyglot" Explanation (Text File)
    # This file explains the "Semantic Duality" without being executable.
    polyglot_explanation = """
    [Research Note: Semantic Duality]

    In a real attack scenario, this file would be a .wsf or .ps1xml file.
    Because of the "Semantic Duality" gap, the browser sees it as a document (XML),
    but the OS sees it as executable code.

    This text file proves you have reached Stage 3.
    """

    with open("polyglot_explanation.txt", "w") as f:
        f.write(polyglot_explanation)
    print("[+] Created 'polyglot_explanation.txt' - For documentation.")

    print("[*] PoC Generation Complete. Stay Safe.")

if __name__ == "__main__":
    create_safe_poc()
