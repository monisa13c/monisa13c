import argparse
import pandas as pd
import os

import time


def merge_and_filter_files(folder_path, file_name_begins):
    try:
        # List all files in the folder
        file_list = os.listdir(folder_path)

        all_data = []
        for file_name in file_list:
            # Construct the  file path
            file_path = os.path.join(folder_path, file_name)
            if file_name.startswith(file_name_begins):
                if os.path.isfile(file_path):
                    # Example: Read the contents of the file
                    df1 = pd.read_csv(file_path, low_memory=False, dtype=str)
                    all_data.append(df1)
                    # Concatenate all dataframes into a single dataframe (assuming they have the same structure)
                    merged_df = pd.concat(all_data, ignore_index=True)
                    # Write the merged dataframe to a CSV file

                    # Output filenames

                    merged_outfile = os.path.join(folder_path, 'merged.csv')
                    remove_mapping_output_file = os.path.join(folder_path, file_name_begins+"Removemappings.txt")
                    Not_Matched_output_file = os.path.join(folder_path,file_name_begins+'Not_Matched.csv')
                    invalid_decision_outputfile = os.path.join(folder_path, file_name_begins+'invalid_decision.csv')

                    merged_df.to_csv(merged_outfile, index=False)
                    # Filter
                    data = pd.read_csv(merged_outfile, low_memory=False, dtype=str)

                    # ,'9779699535','872688602','45620405412','8265472435','9759731825','253422122','18952732812']
                    df = data[data['RI_DECISION'] == 'NOT_MATCHED']
                    # for reference purpose
                    df.to_csv(Not_Matched_output_file)
                    # remove mapping format
                    Namespace = "AMZN"
                    Qualifier = "NEW"
                    MatchingType = "EXACT"
                    Location = " "
                    source = "ONLINE"
                    asin = df['ASIN']
                    mp = df["MARKETPLACE_ID"]
                    comp_name = df["COMPETITOR_NAME"]
                    urls = df['RI_COMPETITOR_PRODUCT_URL']
                    # creating file for remove_mappings
                    with open(remove_mapping_output_file, "w") as outfile:
                        outfile.write(
                            f"Namespace\tSku\tQualifier\tCompId\tMarketplaceId\tMatchingType\tLocation\tSource\tMapStatus\tUrl\n")
                        for ASIN, url, comp, mp in zip(asin, urls, comp_name, mp):
                            MapStatus = "IF" if url else "INF"
                            outfile.write(
                                f"{Namespace}\t{ASIN}\t{Qualifier}\t{comp}\t{mp}\t{MatchingType}\t{Location}\t{source}\t{MapStatus}\t{url}\n")
                    # File for invalid decisions
                    df1 = data[(data['RI_DECISION'] != "MATCHED") & (data['RI_DECISION'] != "NOT_MATCHED")]
                    asin1 = df1['ASIN'].to_list()
                    mp1 = df1["MARKETPLACE_ID"].to_list()
                    comp_name1 = df1["COMPETITOR_NAME"].to_list()
                    urls1 = df1['RI_COMPETITOR_PRODUCT_URL'].to_list()
                    # creating file for reuploads
                    with open(invalid_decision_outputfile, "w", encoding='utf-8') as out_file:
                        out_file.write(f"MARKETPLACE_ID\tASIN\tCOMPETITOR_NAME\tRI_COMPETITOR_PRODUCT_URL\n")
                        for ASIN, url, comp, mp in zip(asin1, urls1, comp_name1, mp1):
                            out_file.writelines(f"{mp}\t{ASIN}\t{comp}\t{url}\n")
    except Exception as e:
        print(f"Error processing data: {str(e)}")


def main():
    parser = argparse.ArgumentParser(description="Tool to merge and process CSV files based on specified criteria.")
    parser.add_argument('folder_path', type=str, help='Path to the folder containing CSV files.')
    parser.add_argument('file_name_begins', type=str, help='Beginning of the file name')


    args = parser.parse_args()

    start_time = time.time()

    merge_and_filter_files(args.folder_path,args.file_name_begins)

    execution_time = time.time() - start_time
    print(f'Execution time: {execution_time:.2f} seconds')
    print(f'Files have been created successfully.')
    print(f'Execution time: {execution_time:.2f} seconds')


if __name__ == "__main__":
    main()
