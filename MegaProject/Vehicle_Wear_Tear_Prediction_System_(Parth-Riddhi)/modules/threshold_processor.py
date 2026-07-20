
# import data_loader as data  
# threshold_data, dummy_data = data.load_data()

def process_threshold(threshold_data) :
    
    dict_data = {}
    # print(threshold_data.shape)  
    # print(threshold_data.columns)
    # print("Rows : \n" ,threshold_data.iloc[1])
    
    for index, row in threshold_data.iterrows():
        
        dict_data[row["Parameter"]] = {
        "GREEN" : row["Green Range"] ,
        "YELLOW" : row["Yellow Range"] ,
        "RED" : row["Red Range"] }


    return dict_data

    # return threshold_data


