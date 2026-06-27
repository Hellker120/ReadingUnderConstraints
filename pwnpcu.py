import os
import re
import time
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from fpdf import FPDF

# ---------- LOAD UNICODE REPLACEMENT DICTIONARY ----------
def load_unicode_dict():
    uni_dict = {}
    dict_path = "unidict.dict"
    if os.path.exists(dict_path):
        with open(dict_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if ":" in line:
                    key, value = line.split(":", 1)
                    try:
                        key_i = int(key.strip())

                        value_i = int(value.strip())
                        uni_dict[key_i] = value_i
                    except ValueError:
                        pass
    return uni_dict


# ---------- APPLY UNICODE REPLACEMENTS ----------
def apply_unicode_replacements(text, uni_dict):
    new_chars = []
    for ch in text:
        code = ord(ch)
        if code in uni_dict:
            new_chars.append(chr(uni_dict[code]))
        elif code < 256:  # Latin-1 safe
            new_chars.append(ch)
        else:
            new_chars.append("?")
    return "".join(new_chars)


# ---------- SCRAPE FUNCTION WITH RETRIES ----------
def scrape_url(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/109.0.0.0 Safari/537.36"
        )
    }

    def fetch():
        return requests.get(url, timeout=10, headers=headers)

    for attempt in range(50):  # retry up to 3 times
        try:
            response = fetch()

            if response.status_code in (429, 403) or "temporarily from accessing" in response.text.lower():
                print(f"[Cloudflare] Block detected on {url}, waiting 10s...")
                time.sleep(10)
                continue

            if response.status_code != 200:
                print(f"[Retry {attempt+1}/3] HTTP {response.status_code} on {url}")
                time.sleep(1)
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
            text = "\n".join(paragraphs)

            if not text.strip():
                print(f"[Warning] Empty page for {url}")
                return f"[Warning: Empty content from {url}]"

            return text

        except (requests.Timeout, requests.ConnectionError) as e:            print(f"[Retry {attempt+1}/3] Network error for {url}: {e}")
            time.sleep(1)

        except Exception as e:
            return f"[Error fetching {url}]: {e}"

    return f"[Error fetching {url}]: failed after 3 retries"


# ---------- CREATE PDF ----------
def create_pdf(results, output_folder, uni_dict):
    output_path = os.path.join(output_folder, "combined.pdf")

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margins(15, 20, 15)
    pdf.set_font("Arial", "", 12)

    for idx, (url, text) in enumerate(results, start=1):
        pdf.add_page()
        pdf.set_font("Arial", "B", 12)
        pdf.multi_cell(0, 8, f"Chapter {idx}: {url}")
        pdf.ln(5)

        safe_text = apply_unicode_replacements(text, uni_dict)
        pdf.set_font("Arial", "", 12)
        paragraphs = safe_text.split("\n")

        for para in paragraphs:
            para = para.strip()
            if para:
                pdf.multi_cell(0, 7, para)
                pdf.ln(2)

        done = idx
        total = len(results)
        bar = "█" * done + "-" * (total - done)
        print(f"\rProgress: |{bar}| {done}/{total}", end="")

    pdf.output(output_path)
    print(f"\n✅ PDF created successfully: {output_path}")


# ---------- MAIN ----------
def main():
    input_file = input("Enter filename (with URLs, one per line): ").strip()
    output_folder = input("Enter output folder name: ").strip()
    os.makedirs(output_folder, exist_ok=True)

    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    urls = []
    for line in lines:
        for u in re.split(r"[\s,]+", line.strip()):
            if u.startswith("http"):
                urls.append(u)

    print(f"Loaded {len(urls)} URLs. Starting scraping with up to 5 threads...\n")

    results = [None] * len(urls)

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(scrape_url, url): i for i, url in enumerate(urls)}
        for i, future in enumerate(as_completed(futures), 1):
            idx = futures[future]
            url = urls[idx]
            text = future.result()
            results[idx] = (url, text)
            print(f"[W{i}] ({idx + 1}/{len(urls)}) {url} → fetched.")

    print(f"\nScraping finished. Collected {len([r for r in results if r])} items.")
    print("Creating PDF....")

    uni_dict = load_unicode_dict()
    create_pdf(results, output_folder, uni_dict)


if __name__ == "__main__":
    main()