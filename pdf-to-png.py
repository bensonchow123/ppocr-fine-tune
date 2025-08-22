import os
from pathlib import Path
from pdf2image import convert_from_path

pdf_dir = "your-pdfs-directory"  # Replace with your actual PDF directory path

def pdf_all_pages_to_png():
    """A sinple script to convert all pages of all PDFs in the specified directory to PNG images."""
    output_dir = Path("ppocr-labeled-data")
    output_dir.mkdir(exist_ok=True)
    
    pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')]

    if not pdf_files:
        print("No PDF files found in the current directory.")
        return
    
    print(f"Found {len(pdf_files)} PDF file(s). Converting all pages to PNG...")
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_dir, pdf_file)
        try:
            images = convert_from_path(pdf_path, dpi=200)

            if images:
                base_name = Path(pdf_file).stem
                
                for page_num, page_image in enumerate(images, 1):
                    output_filename = output_dir / f"{base_name}_page_{page_num:03d}.png"
                    
                    page_image.save(output_filename, "PNG")
                    
                    print(f"✓ Converted: {pdf_file} page {page_num} -> {output_filename}")
                
                print(f"  Total pages converted for {pdf_file}: {len(images)}")
            else:
                print(f"✗ No pages found in {pdf_file}")
                
        except Exception as e:
            print(f"✗ Error processing {pdf_file}: {str(e)}")
    
    print(f"\nConversion complete! PNG files saved to '{output_dir}' directory.")

if __name__ == "__main__":
    pdf_all_pages_to_png()