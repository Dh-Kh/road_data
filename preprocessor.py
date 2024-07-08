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

    def _process_row(self, row: List[str]) -> List[str]:

        data = " ".join(row.astype(str)).split()

        data = [0 if x == "-" else x for x in data]
        
        data = [x for x in data if x is not None]

        data = data[:24] + [0] * (24 - len(data))
        
        return data
      
    def retrieve_tables(self) -> str:

        """
        calculate mean of cells from different dataframes
        """        

        correlation_matrices = [] 

        
        pages_data = self._retrieve_pages(
            r'Середня швидкість руху на майданчику\s*(.*?)\s*у\s*2021\s*році'
        )
        
        
        for page in pages_data:
           
            tables = camelot.read_pdf(
                "WIM_звіт_2021_в3.pdf", pages=str(page),
                table_area=[180, 180, 820, 820]                      
            )
            
            
            df = tables[0].df
            
            df = df.iloc[1:]
            
            df.reset_index(drop=True, inplace=True)
            
            df = df.apply(self._process_row, axis=1, result_type='expand')
            
            df = df.apply(pd.to_numeric, errors='coerce')
            
            correlation_matrices.append(df)
        
        combined_df = pd.concat(correlation_matrices, axis=0)
        
        mean_values = combined_df.mean(axis=0)
        
        result_df = mean_values.reset_index()
        
        result_df.columns = ["Time Interval", "Mean Speed"]
        
        result_df.to_csv("data.csv")
        """
        plus all values of rows and divide them on df length
        """
        
        
    @staticmethod
    def plot_tables(pdf_path: str = None, pages: str = None) -> None:
        
        """Method to get coords"""
        
        if not (pdf_path, pages):
            return
                
        img = camelot.read_pdf(pdf_path, pages=pages)
        
        for i in range(0, img.n):
            camelot.plot(img[i], kind='grid').show()
        
  
if __name__ == "__main__":
    
    pdf = PdfExtract("WIM_звіт_2021_в3.pdf")
    print("Loading... Please, wait...")
    pdf.retrieve_tables()   
    print("Executed!")
    
