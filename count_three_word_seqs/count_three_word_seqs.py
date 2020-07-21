#!/usr/bin/env python3
import fileinput
import string
from collections import Counter

## count_three_word_seqs(): Reads text from files specified by command line arguments or from 
## stdin and constructs a Counter object of all three word sequences.
# Input: optional parameter for specifying files outside the command line
# Returns: Counter object in the form {('one', 'two', 'three'):53, ('by', 'the', 'way'):33}
def count_three_word_seqs(files_str=None):
    seqs_count = Counter()

    # Read each line of text from files specifed or stdin, ignore case and punctuation
    with fileinput.input(files=files_str) as f:
        words = (word
                    for line in f 
                        for word in 
                            line.translate(str.maketrans("", "", string.punctuation)).lower().split())

        # Try to get the first three words if there are three
        try:
            word1, word2, word3 = next(words), next(words), next(words)
        except StopIteration:
            return seqs_count

        # Get and count every three word sequence
        for next_word in words:
            seqs_count.update({(word1, word2, word3)})
            word1 = word2
            word2 = word3
            word3 = next_word
        # Capture the last sequence (or only sequence if the text contains only one)
        seqs_count.update({(word1, word2, word3)})

    return seqs_count

if __name__ == '__main__':
    seqs_count = count_three_word_seqs()

    # Print the 100 most common three word sequences in the text in the format "33 - by the way"
    for count_tuple in seqs_count.most_common(100):
        print(f"{count_tuple[1]} - {' '.join(count_tuple[0])}")