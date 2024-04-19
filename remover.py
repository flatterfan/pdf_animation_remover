'''
Removes pages from a PDF file by checking for the page number.
If multiple pages have the same page number, every page will be removed, but the last one.

REQUIRES: PyPDF2

'''
import sys

import PyPDF2


# Parses the last line of the file to an int
# Returns -1 on failure
def getpagenumber(text):
    lines = text.splitlines()
    if len(lines) < 1:
        return -1
    try:
        pagenumer = int(lines[-1])
        return pagenumer

    except ValueError:
        return -1


if __name__ == "__main__":

    filename = sys.argv[1]
    # filename = 'folien.pdf'

    with open(filename, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()

        length = len(reader.pages)

        if length <= 2:
            exit(1)

        current_page = reader.pages[0]
        next_page = reader.pages[0]

        # iterate through all pages of the pdf file
        for i in range(1, length):
            current_page = next_page
            next_page = reader.pages[i]

            # extract text from pages
            current_text = current_page.extract_text()
            next_text = next_page.extract_text()

            # add page to new pdf file if next page doesn't have the same page number
            if getpagenumber(current_text) == -1 or getpagenumber(current_text) != getpagenumber(next_text):
                writer.add_page(current_page)

        with open(f'{filename[0:-4]}_animation_removed.pdf', 'wb') as output_pdf:
            writer.write(output_pdf)

    print('Animations successfully removed.')
