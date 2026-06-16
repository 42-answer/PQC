import fitz

doc = fitz.open("report/main.pdf")

for page_num in range(doc.page_count):
    page = doc.load_page(page_num)
    pix = page.get_pixmap(dpi=300)
    pix.save(f"report/page_{page_num+1}.png")
