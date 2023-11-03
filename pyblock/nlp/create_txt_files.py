import pandas as pd
df = pd.read_csv("/Users/kpandey/Desktop/3-1/Blockchain Technology/Project/BlockchainProject2/WELFake_Dataset.csv")
n = 4
for index, row in df.iterrows():
    if index >= n:
        break
    title = row["title"]
    text = row["text"]

    # Define the file name
    file_name = f"{title}.txt"

    # Write the data to the text file
    with open(file_name, "w") as file:
        file.write(f"{title}\n{text}")
        
    print("DONE")
