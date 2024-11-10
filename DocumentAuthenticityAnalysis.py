import fitz  # PyMuPDF

def highlight_pdf_annotations(pdf_file_path, highlighted_pdf_path, highlight_color=(1, 0, 0), text_box_color=(1, 0, 0)):
    """
    Highlights shape and text box annotations in a PDF file and saves the modified file.

    Parameters:
        pdf_file_path (str): Path to the input PDF file.
        highlighted_pdf_path (str): Path to save the output highlighted PDF.
        highlight_color (tuple): RGB tuple for highlighting shapes (default is red).
        text_box_color (tuple): RGB tuple for highlighting text boxes (default is red).
    
    Returns:
        dict: A dictionary containing the count of shape and text box annotations per page.
    """
    try:
        # Load the PDF
        document = fitz.open(pdf_file_path)

        # Initialize dictionaries to store counts of annotations per page
        annotations_count = {"shapes": 0, "text_boxes": 0}

        # Loop through each page
        for page_num in range(document.page_count):
            page = document.load_page(page_num)
            
            # Extract all annotations (if any)
            annotations = page.annots()

            # Loop through annotations to find shape and text box annotations
            if annotations:
                for annot in annotations:
                    annot_type = annot.type[0]
                    
                    if annot_type == 1:  # Type 1 indicates a text box annotation
                        rect = annot.rect
                        content = annot.info.get("content", "")
                        
                        annotations_count["text_boxes"] += 1

                        # Draw highlight around the text box annotation
                        page.draw_rect(rect, color=text_box_color, width=1)

                    elif annot_type in [2, 3, 4, 5, 6, 7, 8]:  # 4 = highlight, 8 = shape (circle, rectangle)
                        rect = annot.rect
                        
                        annotations_count["shapes"] += 1

                        # Draw highlight around the shape annotation
                        page.draw_rect(rect, color=highlight_color, width=2)

        # Save the modified PDF with highlighted shapes and text boxes
        document.save(highlighted_pdf_path)
        document.close()

        return annotations_count

    except Exception as e:
        return {"error": str(e)}

# Usage:
# annotations_count = highlight_pdf_annotations("BankStatementQR.pdf", "BankStatementQRScanned.pdf")

# shapes_count = annotations_count.get('shapes', 0)
# text_boxes_count = annotations_count.get('text_boxes', 0)

