from zipfile import ZipFile
from bs4 import BeautifulSoup
import os

def extract_zip(zipfile):
    with ZipFile(zipfile) as z:
        z.extractall()

def soup_to_lines(soup):
    """Returns the lines in a hocr-file, typically representing one page"""
    para_text = []
    for para in soup.find_all('p', {'class': 'ocr_par'}):
        for line in para.find_all('span', {'class': 'ocr_line'}):
            para_text.append(" ".join([w.text for w in line.find_all('span', {'class':'ocrx_word'})]))
    return para_text

def folder_to_book(folder):
    pages = dict()
    contents = os.walk(folder)
    for _,_,files in contents:
        for file in files:
            with open(os.path.join(folder, file), encoding = 'utf-8') as f:
                soup = BeautifulSoup(f.read())
                #print(soup.prettify())
                pages[file] = soup_to_lines(soup)
    return pages