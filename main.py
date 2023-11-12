import pandas as pd


def lzw_compress(input_string):
    # Initialize dictionary with individual characters
    dictionary = {chr(i): i for i in range(256)}
    next_code = 256
    current_string = ""
    compressed = []

    for char in input_string:
        combined_string = current_string + char
        if combined_string in dictionary:
            current_string = combined_string
        else:
            compressed.append(dictionary[current_string])
            dictionary[combined_string] = next_code
            next_code += 1
            current_string = char

    # Output the code for the remaining string
    if current_string:
        compressed.append(dictionary[current_string])

    return compressed

def lzw_decompress(compressed_data):
    dictionary = {i: chr(i) for i in range(256)}
    next_code = 256

    current_string = dictionary[compressed_data[0]]
    decompressed = [current_string]

    for code in compressed_data[1:]:
        if code in dictionary:
            new_string = dictionary[code]
        else:
            new_string = current_string + current_string[0]

        decompressed.append(new_string)

        dictionary[next_code] = current_string + new_string[0]
        next_code += 1

        current_string = new_string

    return "".join(decompressed)


def calculate_redundancy(original_data, compressed_data):
    original_size = len(original_data)
    compressed_size = len(compressed_data)

    redundancy = 1 - (compressed_size / original_size)
    return redundancy


def LZW(sequence):
    # Apply LZW compression to the input sequence
    compressed_sequence = lzw_compress(sequence)
    # Calculate redundancy
    redundancy = calculate_redundancy(sequence, compressed_sequence)

    return compressed_sequence, redundancy


if __name__ == '__main__':

    # Read the DataFrame from the TSV file
    df = pd.read_csv('lineages_added_seq_summary.tsv', sep='\t')
    # Add a column of clean sequences without '-'
    df['clean_seq'] = df['sequence'].str.replace('-', '')

    # Apply the LZW function to the 'clean_seq' column
    compressed_data, redundancy = zip(*df['clean_seq'].apply(LZW))

    # Add the 'compressed_seq' and 'redundancy' columns to the DataFrame
    df['compressed_seq'] = compressed_data
    df['redundancy'] = redundancy

    grouped = df.groupby('gene')
    # Calculate the total sales for each product group
    mean_redundancy = grouped['redundancy'].mean()
    stds_redundancy = grouped['redundancy'].std()
    # Save or display the modified DataFrame
    print(df)