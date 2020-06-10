#!/usr/bin/env python
# coding: utf-8

# In[8]:


import sqlite3
import os
import tarfile
import shutil
import dhlab.nbtokenizer as tok


# In[4]:


def alto_extract(altofile, to_path = '.'):
    """
    Pakk ut tarfil til ramdisk og returnerer mappen filene ligger i
    """


    tf = tarfile.open(altofile, 'r')
    # lag mappe på disk med navnet foran det som står foran .tar
    filename = os.path.basename(altofile)
    dname = filename.split('.tar')[0]
    ndir = os.path.join(to_path, dname )
    os.mkdir(ndir)
    # Pakk ut alt til mappen
    tf.extractall(ndir)
    tf.close()
    return ndir


# In[19]:



def process_alto(ndir):
    """Hent ut alle ordene i alto-filen, og legg til paragraf og sidenummer. Mappen ndir peker til mappen der tarfilene ligger"""
    
    import xml.etree.ElementTree as ET
    import shutil
    
    # XML-filene ligger i mappen ndir, så gå gjennom med os.walk()
    # Alle filene blir liggende i variabelen f
    r,d,f = next(os.walk(ndir))
    
    # hent sidene i teksten og legg dem i variabelen pages
    # skip metadatafilene - tekstene har sidenummer representert som 4-sifrede nummer, f.eks. 0014
    pages = []
    
    for page in f:
        pag = page.split('.xml')[0].split('_')[-1]
        try:
            int(pag)
            pages.append((page, int(pag)))
        except:
            True
        
    # Gå gjennom side for side og hent ut teksten. Delte ord blir lagt i variabelen hyph,
    # teksten i text. Alle ord får et sekvensnummer relativt til boka det står i, samtidig
    # som alle avsnitt blir nummerert fortløpende
    
    para_num = 1
    word_num = 1

    text = []
    hyph = []

    hyp1 = ""
    hyp2 = ""
    
    # sorter variabelen pages på sidenummer, andre ledd i tuplet
    for page in sorted(pages, key=lambda x: x[1]):
        page_file = os.path.join(r, page[0])
        page_num = page[1]
        
        # parse XML-fila og få tak i rotelementet root
        tree = ET.parse(page_file)
        root = tree.getroot()
        
        # Gå gjennom XML-strukturen via TextBlock, som er avsnittselementet
        for paragraph in root.findall(".//TextBlock"):
            
            # Finn alle ordene i avsnittet, som attributter til elementet String,
            # og sjekk om det foreligger en orddeling -
            # i så fall ligger hele ordet i attributtet SUBS_CONTENT, mens første ledd av orddelingen
            # ligger i CONTENT. Om det ikke er noen orddeling ligger ordet i attributtet CONTENT.
            # Burde fungere også med orddelinger over sideskift
            
            # Ordet lagres sammen med sekvensnummeret og sekvensnummeret for avsnittet står i,
            # i tillegg til sidenummeret, som kan være greit for oppslag i bokhylla, i forbindelse
            # med generering av konkordanser.
            
            for string in paragraph.findall(".//String"):
                if 'SUBS_TYPE' in string.attrib:
                    if string.attrib['SUBS_TYPE'] == "HypPart1":
                        #tokens = tok.tokenize(string.attrib['SUBS_CONTENT'])
                        tokens = [string.attrib['SUBS_CONTENT']]
                        for token in tokens:
                            text.append((token, word_num, para_num, page_num))
                            word_num += 1
                    elif string.attrib['SUBS_TYPE'] == "HypPart2":
                        hyp2 = string.attrib['CONTENT']
                        hyph.append((hyp1, hyp2))
                else:
                    #tokens = tok.tokenize(string.attrib['CONTENT'])
                    tokens = [string.attrib['CONTENT']]
                    for token in tokens:
                        text.append((token, word_num, para_num, page_num))
                        word_num += 1
            para_num += 1
    # returner teksten som en sekvens av tupler, sammen med orddelingene, også som en sekvens av tupler
    return text #, hyph


# In[5]:


alto_extract("/home/larsj/terra/iness/digibok_2006080900016_ocr_xml.tar")


# In[20]:


process_alto("digibok_2006080900016_ocr_xml/")

