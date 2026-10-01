"""
Check whether the links in a PDF file are working.

Install: pip install pymupdf requests
Run:     python check_pdf_links.py file.pdf
Output:  prints to the console + saves link_report.csv
"""
import csv
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor

import pymupdf
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL_REGEX = re.compile(r"https?://[^\s<>\"')\]]+")
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; LinkChecker/1.0)"}
TIMEOUT = 15
# Protected / bot-blocking / login-required pages: still counted as reachable
PROTECTED_CODES = {401, 403, 429, 999}


def extract_links(pdf_path):
    """Collect links from embedded PDF hyperlinks and from URLs in the page text."""
    links = {}  # url -> first page number where it appears
    with pymupdf.open(pdf_path) as doc:
        for page_num, page in enumerate(doc, start=1):
            # Clickable hyperlinks embedded in the PDF
            for link in page.get_links():
                uri = link.get("uri")
                if uri and uri.startswith("http"):
                    links.setdefault(uri.strip(), page_num)
            # Plain-text URLs; strip trailing punctuation captured by the regex
            for url in URL_REGEX.findall(page.get_text()):
                links.setdefault(url.rstrip(".,;:"), page_num)
    return links


def check_url(item):
    url, page = item
    try:
        r = requests.head(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True, verify=False)
        # Some sites don't support HEAD -> retry with GET
        if r.status_code >= 400:
            r = requests.get(url, headers=HEADERS, timeout=TIMEOUT,
                             allow_redirects=True, stream=True, verify=False)
        # Protected pages are treated as OK
        if r.status_code in PROTECTED_CODES:
            return url, page, r.status_code, "OK", "Protected/bot-blocking page (opens in a browser)"
        ok = r.status_code < 400
        return url, page, r.status_code, "OK" if ok else "ERROR", r.url
    except requests.exceptions.RequestException as e:
        # Connection errors, timeouts, invalid URLs, etc.
        return url, page, "-", "ERROR", type(e).__name__


def main():
    if len(sys.argv) >= 2:
        pdf_path = sys.argv[1]
    else:
        # No argument given -> open a file picker dialog
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        pdf_path = filedialog.askopenfilename(
            title="Select the PDF file to check",
            filetypes=[("PDF", "*.pdf")],
        )
        if not pdf_path:
            sys.exit("No file selected.")

    links = extract_links(pdf_path)
    print(f"Found {len(links)} links. Checking...\n")

    # Check links concurrently with 10 threads
    with ThreadPoolExecutor(max_workers=10) as pool:
        results = list(pool.map(check_url, links.items()))

    results.sort(key=lambda x: x[1])  # sort by page number
    for url, page, status, state, final in results:
        print(f"[{state}] page {page} | {status} | {url}")

    # Save the CSV report next to the PDF (utf-8-sig so Excel reads UTF-8 correctly)
    report_path = os.path.join(os.path.dirname(os.path.abspath(pdf_path)), "link_report.csv")
    with open(report_path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["Page", "URL", "Status Code", "Result", "Final URL / Error"])
        for url, page, status, state, final in results:
            w.writerow([page, url, status, state, final])

    # Summary: count failed links
    bad = [r for r in results if r[3] != "OK"]
    print(f"\nWorking: {len(results) - len(bad)} | Errors: {len(bad)}")
    print("Report saved:", report_path)
    input("\nPress Enter to exit...")  # keep the window open when double-clicked


if __name__ == "__main__":
    main()