# Extract PDF pages containing specific string from
# PFM and create a target pdf file with all matching
# pages. If there are no matches, you will only have 
# Index page from the source PDF
import PyPDF2
import re
import os
#import csv
from tabula import read_pdf
from tabulate import tabulate

# target file
target_file_name = "hidmet_gov_rs"
target_file_ext = "pdf"
found = False

print("Starting extractor...")

# Strings to find in a page
# Zemun, Pancevo, Belgrade
S = {"Zemun":"Земун","Pancevo":"Панчево", "Belgrade":"Београд"}
CP = "ZEMUN_PANCEVO_BELGRADE"

# For all the files in the folder
HIDMET_FOLDER="E:/Omdena/Omdena Serbia - Reducing floods risks/data_raw"
for file in os.listdir(HIDMET_FOLDER):
    # Match only PDF File
    if file.endswith(".pdf"):
        file_name = HIDMET_FOLDER+"/" + file
        print("Searching " + file_name)

        # Open file in read and binary mode
        f = open(file_name, 'rb')
        obj = PyPDF2.PdfReader(f)

        # Total number of pages
        pgno = len(obj.pages)

        # First add index page always
        #if (pgno > 0):
            #pdf_writer.add_page(obj.pages[0])
        
        # Traverse through all pages and extract 
        # text from each page and search for given
        # string and if there is a match add the page
        # into the target pdf file. We should not
        # duplicate meaning if the page is already added
        # we should not add them again so that we can avoid
        # duplicates at one level
        pdf_writer = PyPDF2.PdfWriter()
        for i in range(0, pgno):
            PgOb = obj.pages[i]
            Text = PgOb.extract_text()
            #print(Text)
            found_page = []
            pdf_output_file = target_file_name + "_" + os.path.splitext(file)[0] + "_" + CP + "." + target_file_ext
            for key in S:
                s = S[key]
                if re.search(s,Text):
                    log = "String {" + s + "} Found on Page: " + str(i) + " on file " + file_name
                    print(log)
                    if (found_page.count(i) == 0):
                        pdf_writer.add_page(PgOb)
                        found_page.append(i)
                        
        with open(pdf_output_file,'wb') as out:
            pdf_writer.write(out)
                    #df = read_pdf(pdf_output_file,pages="all")
                    #print(tabulate(df))
    #break
                    

