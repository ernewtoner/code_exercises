#!/usr/bin/env python3
from collections import Counter
from count_three_word_seqs import count_three_word_seqs

## Tests that should result in an empty Counter()
def test_empty_results():
   seqs_counter = count_three_word_seqs("tests/empty.txt")
   assert seqs_counter == Counter(), "Counter should be empty"

   seqs_counter = count_three_word_seqs("tests/oneword.txt")
   assert seqs_counter == Counter(), "Counter should be empty"

   seqs_counter = count_three_word_seqs("tests/twowords.txt")
   assert seqs_counter == Counter(), "Counter should be empty"

## Tests passing multiple files including the same one repeatedly
def test_multiple_arguments():
   seqs_counter = count_three_word_seqs(("tests/oneword.txt", "tests/oneword.txt", "tests/oneword.txt"))
   assert seqs_counter == Counter({('hello', 'hello', 'hello'): 1}), "Counter should match expected result"
   
   seqs_counter = count_three_word_seqs(("tests/empty.txt", "tests/oneword.txt", "tests/twowords.txt"))
   assert seqs_counter == Counter({('hello', 'hello','there'): 1}), "Counter should match expected result"

   seqs_counter = count_three_word_seqs(("tests/twowords.txt", "tests/twowords.txt", "tests/twowords.txt"))
   assert seqs_counter == Counter({('hello', 'there','hello'): 2, ('there', 'hello','there'): 2}), "Counter should match expected result"

## Tests with small text files
def test_small_texts():
   seqs_counter = count_three_word_seqs("tests/threewords.txt")
   assert seqs_counter == Counter({('three', 'words', 'here'): 1}), "Counter should match expected result"

   seqs_counter = count_three_word_seqs("tests/test1.txt")
   assert seqs_counter == Counter({('test', 'test', 'test'): 4, ('test', 'test', 'one'): 1, 
                                   ('test', 'one', 'one'): 1, ('one', 'one', 'one'): 1 }), "Counter should match expected result"

   ## Lorem ipsum text, should have one of each word sequence
   seqs_counter = count_three_word_seqs("tests/test2.txt")
   for v in seqs_counter.values():
      assert v == 1, "Count of each word sequence should be 1"
      
   seqs_counter = count_three_word_seqs("tests/test3.txt")
   assert seqs_counter == Counter({('one', 'two', 'three'): 1, ('two', 'three', 'four'): 1, 
                                   ('three', 'four', 'five'): 1, ('four', 'five', 'six'): 1, 
                                   ('five', 'six', 'seven'): 1}), "Counter should match expected result"

   seqs_counter = count_three_word_seqs("tests/test4.txt")
   assert seqs_counter == Counter({('i', 'love', 'sandwiches'): 6, ('love', 'sandwiches', 'i'): 5, 
                                   ('sandwiches', 'i', 'love'): 5}), "Counter should match expected result"

## Tests with larger text files
def test_larger_texts():
   ## metamorphosis.txt - manually verified counts
   seqs_counter = count_three_word_seqs("tests/metamorphosis.txt")
   assert seqs_counter[('the','chief', 'clerk')] == 34, "Counter should match expected result"
   assert seqs_counter[('project','gutenbergtm', 'electronic')] == 18, "Counter should match expected result"
   assert seqs_counter[('the','three', 'gentlemen')] == 14, "Counter should match expected result"

   # Process text three times and verify counts have tripled
   seqs_counter = count_three_word_seqs(("tests/metamorphosis.txt", "tests/metamorphosis.txt", "tests/metamorphosis.txt"))
   assert seqs_counter[('the','chief', 'clerk')] == 102, "Counter should match expected result"
   assert seqs_counter[('project','gutenbergtm', 'electronic')] == 54, "Counter should match expected result"
   assert seqs_counter[('the','three', 'gentlemen')] == 42, "Counter should match expected result"

   ## originofspecies.txt
   seqs_counter = count_three_word_seqs("tests/originofspecies.txt")
   assert seqs_counter[('of','the', 'same')] == 320, "Counter should match expected result"
   assert seqs_counter[('the','same', 'species')] == 126, "Counter should match expected result"
   assert seqs_counter[('conditions','of', 'life')] == 125, "Counter should match expected result"

   # Process text twice and verify counts have doubled
   seqs_counter = count_three_word_seqs(("tests/originofspecies.txt", "tests/originofspecies.txt"))
   assert seqs_counter[('of','the', 'same')] == 640, "Counter should match expected result"
   assert seqs_counter[('the','same', 'species')] == 252, "Counter should match expected result"
   assert seqs_counter[('conditions','of', 'life')] == 250, "Counter should match expected result"

if __name__ == '__main__':
   test_empty_results()
   test_multiple_arguments()
   test_small_texts()
   test_larger_texts()