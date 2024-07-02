from pypdf import PdfReader
from typing import List
import camelot
import pandas as pd
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
    Generate JSON file in root folder
    """
    
    def retrieve_tables(self) -> str:
        
        
        """need modify data to merge all of them 
        for instance all rows which are fisrt must be merged with each other
        and so on
        """
       
        pages_data = self._retrieve_pages(
            r'Середня швидкість руху на майданчику\s*(.*?)\s*у\s*2021\s*році'
        )
        
        pages = ','.join(map(str, pages_data))

        tables = camelot.read_pdf("WIM_звіт_2021_в3.pdf", pages=pages)

        merged_data = pd.DataFrame()

        for table in tables:
            
            df = table.df.drop(columns=table.df.columns[:2], axis=1)
            
            df.reset_index(drop=True, inplace=True)
            
            values = df.iloc[2].values
                        
            concatenated_values = ' '.join(values)
            
            array = concatenated_values.split()

            array = [0 if x == "-" else x for x in array]    
               
            n = 24

            array = [array[i:i+n] for i in range(0, len(array), n)]
            
            df_v = pd.DataFrame(array)
            
            merged_data = pd.concat([merged_data, df_v], ignore_index=True)
        
        merged_data.to_csv("data.csv")
        
  
if __name__ == "__main__":
    
    """
    pdf = PdfExtract("WIM_звіт_2021_в3.pdf")
    print("Loading... Please, wait...")
    print(pdf.retrieve_tables())   
    """
    pass
