import csv
import sys


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run



def main():


    with open(sys.argv[2], "r") as data2:
        sequence = data2.read()

       # Find longest match of each STR in DNA sequence

    seq1 = str(longest_match(sequence, 'AGATC'))
    # print(seq1)
    seq2 = str(longest_match(sequence, 'TTTTTTCT'))
    # print(seq2)
    seq3 = str(longest_match(sequence, 'AATG'))
    # print(seq3)
    seq4 = str(longest_match(sequence, 'TCTAG'))
    # print(seq4)
    seq5 = str(longest_match(sequence, 'GATA'))
    # print(seq5)
    seq6 = str(longest_match(sequence, 'TATC'))
    # print(seq6)
    seq7 = str(longest_match(sequence, 'GAAA'))
    # print(seq7)
    seq8 = str(longest_match(sequence, 'TCTG',))
    # print(seq8)
    
    #Check database for matching profiles
    profile = [seq1, seq2, seq3, seq4, seq5, seq6, seq7, seq8]
    with open(sys.argv[1], "r") as data:
        dat = csv.reader(data)
        count = ()
        for subsequence in dat:
            test = subsequence[1:]
            test2 = int(longest_match(profile, test))
            if test2 == 1:
                print(subsequence[0])
                count =+ 1

    if count != 1:
        print("No match")
        

main()



