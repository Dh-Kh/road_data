from pypdf import PdfReader
from typing import List
import tabula
import os
import re
#import pandas as pd

os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64"

class PdfExtract(object):
    
    """
    WIM_звіт_2021_в3.pdf
    Can be installed at http://bit.ly/wimrprt21 (14,5 Мб.).
    """
    
    def __init__(self, file_name: str):
        self.file_name = file_name
        
    """
    retrieves all pages that correspond to regex
    """
        
    def _retrieve_pages(self, pattern_data: str) -> List[int]:
        
        #r'Середня швидкість руху на майданчику\s*(.*?)\s*у\s*2021\s*році'
        
        reader = PdfReader(self.file_name)
        
        pattern = re.compile(pattern_data)
        
        page_list = []
        for index, page in enumerate(reader.pages):
            text = page.extract_text()
            if pattern.search(text):
                page_list.append(index+1)
        return page_list
    
    """
    Generate CSV file in root folder
    """
    
    def retrieve_tables(self, pattern_data: str) -> None:
        
        pages_data = self._retrieve_pages(pattern_data)
        
        tabula_options = {
            "pages": pages_data,
            "guess": False,
            "lattice": True,
            "stream": True,
        }
        dfs = tabula.read_pdf(self.file_name, **tabula_options)

        #inccorect data retrieves        
  
if __name__ == "__main__":
    """      
    pdf = PdfExtract("WIM_звіт_2021_в3.pdf")

    pdf.retrieve_tables(r'Середня швидкість руху на майданчику\s*(.*?)\s*у\s*2021\s*році')
    
    """
    pdf = PdfExtract("WIM_звіт_2021_в3.pdf")
    print(pdf.retrieve_tables(r'Середня швидкість руху на майданчику\s*(.*?)\s*у\s*2021\s*році'))
    pass
