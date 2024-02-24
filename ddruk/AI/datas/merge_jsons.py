import json

if __name__ == "__main__":
    # this is the raw review data
    json_file_paths = [
        './phase1_result_GooglePay_v0_0_200.json',
        './phase1_result_GooglePay_v0_200_500.json',
    ]

    merged_res = []
    for json_file_path in json_file_paths:
        with open(json_file_path, "r") as json_file:
            merged_res += json.load(json_file)
    
    # Stroe Merged result
    with open('./phase1_result_GooglePay_v0_0_500.json', 'w') as json_file:
        json.dump(merged_res, json_file, indent=4)

    #Validate the merged result
    with open('./phase1_result_GooglePay_v0_0_500.json', "r") as json_file:
        merged_res = json.load(json_file)
        print(len(merged_res)) 