import fitz  # PyMuPDF
from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog, simpledialog

DPI = 60

def pick_pdf_file():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(title="Select PDF file", filetypes=[("PDF files", "*.pdf")])

def pick_output_folder():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory(title="Select output folder")

def ask_main_folder_name():
    root = tk.Tk()
    root.withdraw()
    return simpledialog.askstring("Folder name", "Enter main folder name for organization:")

def ask_jpeg_quality():
    root = tk.Tk()
    root.withdraw()
    q = simpledialog.askinteger("JPEG quality", "Enter JPEG quality (1-100):", minvalue=1, maxvalue=100)
    return q if q else 80

def get_range_folder(page_num, range_size):
    start = ((page_num - 1) // range_size) * range_size + 1
    end = start + range_size - 1
    return f"ep_{start}to{end}"

def make_nested_folders(base_path, page_num):
    # Folder grouping sizes, smallest to largest
    sizes = [10, 100, 1000, 10000, 100000, 1000000, 10000000]

    # We build folders from largest to smallest range, but only include folders
    # that actually cover the page (page_num <= end of folder range)
    folders = []
    for size in reversed(sizes):
        folder_name = get_range_folder(page_num, size)
        # Only include this folder if page_num is within the folder range
        start = ((page_num - 1) // size) * size + 1
        end = start + size - 1
        if start <= page_num <= end:
            folders.append(folder_name)

    # folders now is largest to smallest (because we loop reversed)
    # Create folders in that order
    full_path = base_path
    for folder in folders:
        full_path = os.path.join(full_path, folder)
        os.makedirs(full_path, exist_ok=True)

    return full_path

def convert_and_organize(pdf_path, output_base, main_folder, jpeg_quality):
    print(f"📘 Starting conversion of '{os.path.basename(pdf_path)}' ...")
    pdf = fitz.open(pdf_path)
    main_folder_path = os.path.join(output_base, main_folder)
    os.makedirs(main_folder_path, exist_ok=True)
    total_pages = pdf.page_count
    print(f"📄 Total pages: {total_pages}")

    for i in range(total_pages):
        page_num = i + 1
        page = pdf[i]
        pix = page.get_pixmap(matrix=fitz.Matrix(DPI/72, DPI/72))        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        folder_for_page = make_nested_folders(main_folder_path, page_num)
        img_name = f"ep{page_num}.jpg"
        save_path = os.path.join(folder_for_page, img_name)
        img.save(save_path, "JPEG", quality=jpeg_quality)

        print(f"✅ Saved page {page_num} at '{save_path}'")

    pdf.close()
    print("🎉 Conversion and organization complete!")

def main():
    pdf_path = pick_pdf_file()
    if not pdf_path:
        print("❌ No PDF selected. Exiting.")
        return

    output_folder = pick_output_folder()
    if not output_folder:
        print("❌ No output folder selected. Exiting.")
        return

    main_folder = ask_main_folder_name()
    if not main_folder:
        print("❌ No folder name given. Exiting.")
        return

    jpeg_quality = ask_jpeg_quality()

    convert_and_organize(pdf_path, output_folder, main_folder, jpeg_quality)

if __name__ == "__main__":
    main()