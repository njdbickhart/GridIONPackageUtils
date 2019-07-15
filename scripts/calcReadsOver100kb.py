# This is a comment line! It is not processed by python
# This is a python3 script

# The following statement imports the "os" library which
import os
import sys
import numpy as np

# This is a function. It's a good habit to define functions for reuse later
# Python wants functions defined first (at the top of the code)
def fastq_reader_fh(infile):
  name = infile.readline().rstrip()
  # The above reads a line of a file and removes the terminating \n
  while True:
    seq = ""
    # Fastqs have four lines, so we want to process four lines at a time
    for s in infile:
      if s[0] == '+':
        commentp = s.rstrip()
        # If you run into the 3rd line (+) stop the loop
        break
      else:
        seq += s.rstrip()
        # Otherwise the 2nd line should be your sequence!
    qual = ""
    for q in infile:
      if len(qual) > 0 and  q[0] == '@':
        yield name, seq, qual
        # Once you reach the fourth line, then you can return the entire fastq entry
        name = q.rstrip()
        break
      else:
        qual += q.rstrip()
    else:
      yield name, seq, qual
      return

if len(sys.argv) < 2:
    print("Usage = python3 calcReadsOver100kb.py <input fastq file [can use wildcards for bulk processing]>")
    # If the number of input arguments is less than 1, exit the program
    sys.exit()

lengths = list()
# Above is the list that contains the lengths of the reads
lenover100 = list()
# Above is the list that contains the reads > 100kb in size
for filename in sys.argv[1:]:
    with open(filename, 'r') as input:
        for name, seq, qual in fastq_reader_fh(input):
            lengths.append(len(seq))
            # we use the fastq_reader_fh subroutine to get just the sequence
            if len(seq) >= 100000:
                lenover100.append(len(seq))
                # add the length of the sequence (len function) to the lists
                # if it's greater than 100kb, then add it to the special list

totLen = len(lengths)
intLen = len(lenover100)
# These are easy to calculate. Just use the length function to get the sizes of the arrays

# Next, we use the numpy library functions to calculate the median and sums of the lengths
totMedian = np.median(lengths)
totSum = np.sum(lengths)
intSum = np.sum(lenover100)

# Finally, we calculate the X coverage against an approximation of the size of the cattle genome
totXCov = totSum / 2800000000
intXCov = intSum / 2800000000

#print("TotalLen {}\tAbove 100kb len {}".format(str(totLen), str(intLen)))
#print("Total Median {}".format(str(totMedian)))
#print("Total sum {}\tAbove 100kb sum {}".format(str(totSum), str(intSum)))
#print("Total Xcov {}\tAbove 100kb cov {}".format(str(totXCov), str(intXCov)))
print("TotalReadNum\tReadsGt100kbNum\tTotalReadLenMedian\tTotalReadBases\tReadsGt100kbBases\tTotalReadXCov(cattle)\tReadsGt100kbXcov(cattle)")
print("\t".join([str(x) for x in [totLen,intLen,totMedian,totSum,intSum,totXCov,intXCov]]))
