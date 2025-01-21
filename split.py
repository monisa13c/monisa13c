import argparse
import pandas as pd
import os
import time


def split(file_path, output_dir):
    try:

        dataframe = pd.read_csv(file_path, low_memory=False, dtype=str)
        num_rows = len(dataframe)
        rows_per_file = 90000
        for start_row in range(0, num_rows, rows_per_file):
            end_row = min(start_row + rows_per_file, num_rows)
            df_chunk = dataframe.iloc[start_row:end_row]
            chunk_filename = os.path.join(output_dir, f"Remove_part_{start_row // rows_per_file + 1}.csv")
            df_chunk.to_csv(chunk_filename, index=False)
            print(f"Saved: {chunk_filename}")
    except Exception as e:
        print(f"Error processing data: {str(e)}")


def main():
    parser = argparse.ArgumentParser(
        description="Tool to split a  CSV files")
    parser.add_argument('file_path', type=str, help='Path to the folder containing CSV files.')
    parser.add_argument('output_dir', type=str, help='Path to the folder to save output files.')

    args = parser.parse_args()

    start_time = time.time()
    split(args.file_path,args.output_dir)
    execution_time = time.time() - start_time
    print(f'Execution time: {execution_time:.2f} seconds')
    print(f'Files have been created successfully.')
    print(f'Execution time: {execution_time:.2f} seconds')


if __name__ == "__main__":
    main()
