# This is a comment line! It is not processed by python
# This is a python3 script

# The following statement imports the "os" library which
import os
import sys
import numpy as np

def fastq_reader_fh(infile):
  name = infile.readline().rstrip()
  while True:
    seq = ""
    for s in infile:
      if s[0] == '+':
        commentp = s.rstrip()
        break
      else:
        seq += s.rstrip()
    qual = ""
    for q in infile:
      if len(qual) > 0 and  q[0] == '@':
        yield name, seq, qual
        name = q.rstrip()
        break
      else:
        qual += q.rstrip()
    else:
      yield name, seq, qual
      return

if len(sys.argv) < 2:
    print("Usage = python3 calcReadsOver100kb.py <input fastq file>")
    # If the number of input arguments is less than 1, exit the program
    sys.exit()

lengths = list()
lenover100 = list()
for filename in sys.argv[1:]:
    with open(filename, 'r') as input:
        for name, seq, qual in fastq_reader_fh(input):
            lengths.append(len(seq))
            if len(seq) >= 100000:
                lenover100.append(len(seq))

totLen = len(lengths)
intLen = len(lenover100)

totMedian = np.median(lengths)
totSum = np.sum(lengths)
intSum = np.sum(lenover100)

totXCov = totSum / 2800000000
intXCov = intSum / 2800000000

#print("TotalLen {}\tAbove 100kb len {}".format(str(totLen), str(intLen)))
#print("Total Median {}".format(str(totMedian)))
#print("Total sum {}\tAbove 100kb sum {}".format(str(totSum), str(intSum)))
#print("Total Xcov {}\tAbove 100kb cov {}".format(str(totXCov), str(intXCov)))
print("\t".join([str(x) for x in [totLen,intLen,totMedian,totSum,intSum,totXCov,intXCov]]))
