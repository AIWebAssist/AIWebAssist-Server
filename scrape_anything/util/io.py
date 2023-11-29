def to_text_file(text,filename):
    import datetime
    
    with open(filename, 'a') as file:
        file.write("\nExecution Time: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + "\n")
        file.write('-----\n')
        file.write(text)
        

def dataframe_to_csv(df,csv_filename):
    _df = df.copy()
    for column in _df.columns:
        if hasattr(_df[column],'str'):
                _df[column] = _df[column].str.replace(",","<comma>").str.replace("\n","<new_line>")
    _df.to_csv(csv_filename,index=False)

def pickle(data,filename): 
    import pickle

    # Pickle the dictionary and save it to a file
    with open(filename, 'wb') as file:
        pickle.dump(data, file)

def unpickle(file_name):
    import pickle
    with open(file_name, 'rb') as file:
        return pickle.load(file)
    