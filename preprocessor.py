from pypdf import PdfReader
from typing import List
import camelot
import re


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
        
        reader = PdfReader(self.file_name)
        
        pattern = re.compile(pattern_data)
                
        page_list = []

        for index, page in enumerate(reader.pages):
            text = page.extract_text()
            if pattern.search(text):
                if "Середня швидкість руху  за проміжками часу, км/год" in text:
                    page_list.append(index+1)
        return page_list
    
    """
    Generate CSV file in root folder
    """
    
    def retrieve_tables(self) -> List[List[List[int]]]:
        
        pages_data = self._retrieve_pages(
            r'Середня швидкість руху на майданчику\s*(.*?)\s*у\s*2021\s*році'
        )
        
        """
        global_stack = []
        
        for page in pages_data:
            
            tables = camelot.read_pdf("WIM_звіт_2021_в3.pdf", pages=str(page))

            if tables:
                
                table = tables[0]

                df = table.df.drop(columns=table.df.columns[:2], axis=1)

                df.reset_index(drop=True, inplace=True)

                stack = []

                stack.append(df.iloc[2])

                stack = [value for value in stack[0].values]

                array = stack[0].split()

                array = [0 if x == "-" else x for x in array]    
            
                n = 24

                array = [array[i:i+n] for i in range(0, len(array), n)]

                global_stack.append(array)
        """
        #return global_stack
    
  
if __name__ == "__main__":
    pdf = PdfExtract("WIM_звіт_2021_в3.pdf")
    print("Waiting...")
    pdf.retrieve_tables()
    print(pdf.retrieve_tables())
    
