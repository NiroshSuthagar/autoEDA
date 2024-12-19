import argparse
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import re

class dataCleaner():
    def __init__(self, df):
        self.__init__
        self.df = df
    
    def startClean(self):
        originalDFLen = len(self.df)
        
        #Checking null counts
        nullSummary= self.df.isnull().sum()
    
        #Dropping NAs
        cleanDF = self.df.dropna()
        naRowCount = originalDFLen - len(cleanDF)
        # Checking duplicates:
        dupeCount = cleanDF.duplicated().sum()
        cleanDF = self.df.drop_duplicates()
        
        # Removing outliers 
        for col in cleanDF.columns:
            try:
                q1 = cleanDF[col].quantile(0.25)
                q3 = cleanDF[col].quantile(0.75)
                IQR = q3-q1
                
                cleanDF = cleanDF[(cleanDF[col] < q1-(1.5*IQR)) | (cleanDF[col] > q3+(1.5*IQR))]
                
            except:
                pass
        outlierCount = originalDFLen - len(cleanDF)
        
        #Summary outputs
        print("******************SUMMARY******************")
        print(f"Original dataset length: {originalDFLen}")
        print(f"Dropped NA rows: {naRowCount}")
        print("Null/NA value counts:")
        print(nullSummary)
        print(f"Duplicate row counts:{dupeCount}")
        print(f"Outlier count: {outlierCount}")
        print(f"Cleaned dataset lenght:{len(cleanDF)}")
        print("******************END******************")
        return cleanDF
    
def main(): 
    parser = argparse.ArgumentParser(description="Add csv filepath")
    parser.add_argument("filepath", type=str, help="Use filepaths with /.")
    args = parser.parse_args()
    
    filepath = str(args.filepath).lower()
    strFilePath = f'{filepath}'
    df = pd.read_csv(strFilePath)
    
    cleaner = dataCleaner(df)
    
    print("Starting Cleaning...")
    
    output = cleaner.startClean()
    output.to_csv("claned_file.csv")
    
    print("Cleaning Done & Output file Available")


if __name__ == "__main__":
    main()
