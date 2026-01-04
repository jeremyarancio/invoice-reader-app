export PDF_FOLDER="data/my_invoices_pdf"
export PNG_FOLDER="data/my_invoices_png"

for pdf in $PDF_FOLDER/*.pdf; do \
    filename=$(basename "$pdf" .pdf); \
    pdftoppm -png -r 300 -f 1 -l 1 -singlefile "$pdf" "$PNG_FOLDER/$filename"; \
  done