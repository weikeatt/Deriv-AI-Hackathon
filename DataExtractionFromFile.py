import pymupdf4llm

md_text = pymupdf4llm.to_markdown(
	doc="Utilities Statement.pdf",
    write_images=True,
    image_path="images",
    image_format="png",
    force_text=True)

print(md_text)