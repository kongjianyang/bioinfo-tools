#!/usr/bin/python
# This script was written to filter raw fastq files from Illumina.
# It filters Adapter sequence, low quality basesand finally removes
# sequences shorter than 25bp. Short reads have
# a higher chance to align to multiple locations and are therefore
# removed. 

import sys, getopt, os
from timeit import default_timer as timer
from multiprocessing import Process


def trimAdap(seq, qual, adapter):
	# This function accepts a sequence of base calls and the associated
	# quality values. The quality values are not used at this stage.
	# The function starts at the right (3') end of the sequence and
	# moves left one base at a time in 8 bp windows. Within each window
	# it searches for matches to the adapter sequence. If 7 or more bases
	# match the adapter the read is trimmed to the start of the window.
	# The matching quality string is also trimmed to the same size and
	# both are returned.
	bases = list(seq)
	AdB = list(adapter)
	i = 0
	flag = 0
	for i in range(0, (len(bases) - 8), 1):
		sum = 8
		c = i
		for j in range(0, 8, 1):
			if not bases[c] == AdB[j]:
				sum -= 1
				if (sum < 7):
					break
			c += 1
		if sum > 6:
			flag = 1
			break
	if flag:
		Newseq = seq[0:i]
		Newqual = qual[0:i]
	else:
		Newseq = seq
		Newqual = qual
	return Newseq, Newqual


def trimQual(seq, qual, qt):
	# This function accepts a sequence of base calls and the associated
	# quality values. The sequence is then trimmed from the right to
	# remove low quality bases at the 3' end. This pattern is typical
	# of most sequencing runs. The function starts from the right end
	# moves left one base at a time in 5 bp windows. The mean quality
	# of the window is calculated and if this mean falls below the
	# user-specified threshold the sequence is trimmed to the start of
	# the window. Again the quality string is trimmed to the same length
	# and returned.
	quals = list(qual)
	i = 0
	flag = 0
	sum = 0
	for i in range(0, 4, 1):
		sum += ord(quals[i]) - 33
	for i in range(5, (len(quals) - 5), 1):
		j = i
		curQual = ord(quals[j]) - 33
		sum += curQual
		curQual = ord(quals[j - 5]) - 33
		sum -= curQual
		if sum < int(qt) * 5:
			flag = 1
			break
	if not flag:
		i = len(quals)
	Newseq = seq[0:i]
	Newqual = qual[0:i]
	return Newseq, Newqual

def processReads(leftfile,rightfile):
	try:
		R1 = file(leftfile, "r")
	except IOError:
		print "Cannot open leftfile for reading\n"
		sys.exit(1)
	outputfile = leftfile + '.trimmed'
	try:
		R1out = file(outputfile, "w")
	except IOError:
		print "Failed to open R1.trimmed\n"
		sys.exit(1)
	if pe:
		try:
			R2 = file(rightfile, "r")
		except IOError:
			print "Cannot open rightfile for reading\n"
			sys.exit(1)
		outputmate = rightfile + '.trimmed'
		try:
			R2out = file(outputmate, "w")
		except IOError:
			print "Failed to open R2.trimmed\n"
			sys.exit(1)
	if singletons:
		singletFile = 'Singletons.trimmed'
		try:
			Sout = file(singletFile,"w")
		except IOError:
			print "Failed to open Singletons.trimmed\n"
			sys.exit(1)
	while 1:
		# Read each line from the fastq file. First line will be the sequence ID
		Fid = R1.readline()
		if not Fid:
			break
		# Second line will be the base calls of the read.
		Fseq = R1.readline()
		# Third line will be a repetition of the ID or simply '+'
		FQid = R1.readline()
		# Fourth line will be the quality values for the base calls.
		Fqual = R1.readline()

		# remove the newline character from sequence and quality lines
		Fseq = Fseq.rstrip()
		Fqual = Fqual.rstrip()

		if pe:
			#Repeat for the mate pair
			Rid = R2.readline()
			Rseq = R2.readline()
			RQid = R2.readline()
			Rqual = R2.readline()
			# remove the new line character from sequence and quality lines
			Rseq = Rseq.rstrip()
			Rqual = Rqual.rstrip()
	
		# Call the function to trim user-provided adapter sequence from each read
		Fseq, Fqual = trimAdap(Fseq, Fqual, adapter)
		# If read remains longer than 25bp after adapter trimming invoke the quality trimming.
		if len(Fseq) >= minLen:
			Fseq, Fqual = trimQual(Fseq, Fqual, qualThreshold)
		if pe:
			Rseq, Rqual = trimAdap(Rseq, Rqual, adapter)
			if len(Rseq) >= minLen:
				Rseq, Rqual = trimQual(Rseq, Rqual, qualThreshold)

		# If the read becomes < minLen bp remove it. This prevents short reads from getting through.
		# IMPORTANT : Do not use this filter for small RNA processing
		if singletons:
			if len(Fseq) >= minLen and len(Rseq) >= minLen:
				R1out.write(Fid + Fseq + "\n" + FQid + Fqual + "\n")
				R2out.write(Rid + Rseq + "\n" + RQid + Rqual + "\n")
			elif len(Fseq) >= minLen:
				Sout.write(Fid + Fseq + "\n" + FQid + Fqual + "\n")
			elif len(Rseq) >= minLen:
				Sout.write(Rid + Rseq + "\n" + RQid + Rqual + "\n")
		else:
			if len(Fseq) >= minLen:
				R1out.write(Fid + Fseq + "\n" + FQid + Fqual + "\n")
				if pe:
					if len(Rseq) >= minLen:
						R2out.write(Rid + Rseq + "\n" + RQid + Rqual + "\n")
					else:
						R2out.write(Rid + "NNNNNNNNNN\n" + RQid + "BBBBBBBBBB\n")
			elif pe and len(Rseq) >= minLen:
				if len(Fseq) >=minLen:
					R1out.write(Fid + Fseq + "\n" + FQid + Fqual + "\n")
				else:
					R1out.write(Fid + "NNNNNNNNNN\n" + FQid + "BBBBBBBBBB\n")
				R2out.write(Rid + Rseq + "\n" + RQid + Rqual + "\n")
	R1.close()
	R1out.close()
	if pe:
		R2.close()
		R2out.close()

def fuzzyCount():
	fileStat = os.stat(inputfile)
	fileSize = fileStat.st_size
	#print "File size is %d" % fileSize
	try:
		TR = file(inputfile, "r")
	except IOError:
		print "Cannot open TR for reading\n"
		sys.exit(1)
	first4 = TR.readline() + TR.readline() + TR.readline() + TR.readline()
	recordSize = len(first4.encode())
	#print "First record size is %d" % recordSize
	recCount = int(fileSize/recordSize)
	return recCount

def createParts(seqPerPart):
	# Default: single-end reads
	pe = 0
	if matefile is not None:
		pe = 1
	try:
		leftFile = file(inputfile,"r")
	except IOError:
		print "Cannot open  for reading\n"
		sys.exit(1)
	if pe:
		try:
			rightFile = file(matefile,"r")
		except IOError:
			print "Cannot open R2 for reading\n"
			sys.exit(1)

	for i in range (1, (threads+1), 1):
		#print "Creating partition %d:" % i
		# Create a left and right fastq file per thread. Each file should contain seqPerPart sequences
		partLeft = tmpDir + '/Part-%d' % i + '.left.fastq'
		partRight = tmpDir + '/Part-%d' % i + '.right.fastq'
		try:
			PF = file(partLeft, "w")
		except IOError:
			print "Unable to create partLeft\n"
			sys.exit(1)
		if pe:
			try:
				PR = file(partRight,"w")
			except IOError:
				print "Unable to open partRight\n"
				sys.exit(1)

		for s in range (1, (seqPerPart+1), 1):
			PF.write(leftFile.readline())
			PF.write(leftFile.readline())
			PF.write(leftFile.readline())
			PF.write(leftFile.readline())
			if pe:
				PR.write(rightFile.readline())
				PR.write(rightFile.readline())
				PR.write(rightFile.readline())
				PR.write(rightFile.readline())

		PF.close()
		if pe:
			PR.close()
	leftFile.close()
	if pe:
		rightFile.close()

def joinParts(threads,dir):
	LeftDst = 'left.fastq.trimmed'
	RightDst = 'right.fastq.trimmed'
	for i in threads:
	   LeftSrc = tmpDir + '/Part-' + i + '.left.fastq.trimmed'
	   RightSrc = tmpDir + '/Part-' + i + '.right.fastq.trimmed'

def processReads_w_threads():
	seqCount = fuzzyCount()
	#print "Fuzzy count took : "
	#print(end - start)
	#print "Total Sequence Count is %d." % seqCount
	seqPerPart = int(seqCount/threads)
	#print "Therefore, sequences per partition is %d." % seqPerPart

	createParts(seqPerPart)
	# Initiate threads and wait for them to finish
	processList = []
	for i in range(1, (threads+1), 1):
		processName = "Part-%d" % i
		partLeft = tmpDir + '/' + processName + ".left.fastq"
		partRight = tmpDir + '/' + processName + ".right.fastq"
		p = Process(target=processReads, args=(partLeft,partRight))
		processList.append(p)
	# Start all the sub-processes
	for j in processList:
		j.start()
	# Wait for the subprocesses to finish
	for j in processList:
		j.join()
	# After all threads finish stitch together the output file
	#print "All threads finished execution. Combining output.\n"
	LName = inputfile + '.trimmed'
	try:
		Lout = file(LName,"w")
	except IOError:
		print "Unable to open Lout for writing\n"
		sys.exit(1)
	if pe:
		RName = matefile + '.trimmed'
		try:
			Rout = file(RName,"w")
		except IOError:
			print "Unable to open Rout for writing\n"
			sys.exit(1)

	cmdString = "cat %s/*left.fastq.trimmed >> %s" % (tmpDir, LName)
	#print cmdString
	os.system(cmdString)
	if pe:
		cmdString = "cat %s/*right.fastq.trimmed >> %s" % (tmpDir, RName)
		os.system(cmdString)
	cleanUp(tmpDir)

def cleanUp(tmpdir):
	# Clean up the temporary files from tmpDir to save disk space.
	# print "Will clean later\n"
	cleaning =1

inputfile = None
matefile = None
adapter = 'AGATCGGAA'
qualThreshold = 20
minLen = 25  # If the read becomes shorter than this value after trimming it is eliminated.
threads = 1 # Default is to run this program on a single core. Higher integer values will invoke the threaded version of the program.
tmpDir = './tmp'
singletons = 0
pe = 0


try:
	opts, args = getopt.getopt(sys.argv[1:], "Amqltdi",
							   ["adapter=", "inputFile=", "mateFile=", "minLength=", "qualityThreshold=", "threads=", "tempDir=", "singletons="]);
except getopt.GetoptError:
	print 'trimMe.py --inputFile <inputfile> --mateFile <matefile> --adapter <adapter sequence> --minLength <min. allowed read length> --qualityThreshold <min. quality threshold> --threads <number of threads> --tempDir </path/to/tempdirectory>\n'
	print 'The only required argument is the name of the input file. If processing paired end reads, provide name of the mate file\n'
	print 'Default values for other parameters are: Adapter AGATCGGAAGAGC\n'
	print 'Quality threshold : 20\n'
	print 'Minimum read length : 25\n'
	print 'Threads : 1 WARNING: Each thread has its own I/O stream on tempDir. Too many threads might lead to severe performance degradation, especially on filesystems mounted from a network.\n'
	print 'Temp. directory : Current dir.'
	sys.exit(2)
for opt, arg in opts:
	if opt in ("-i", "--inputFile"):
		inputfile = arg
	elif opt in ("-A", "--adapter"):
		adapter = arg
	elif opt in ("-m", "--mateFile"):
		matefile = arg
	elif opt in ("-q", "--qualityThreshold"):
		qualThreshold = int(arg)
	elif opt in ("-l", "--minLength"):
		minLen = int(arg)
	elif opt in ("-t", "--threads"):
		threads = int(arg)
	elif opt in ("-d", "--tempDir"):
		tmpDir = arg
	elif opt in ("-s", "--singletons"):
		singletons = arg
print "Input file is %s, Mate file is %s, Adapter is %s. Quality, and length thresholds are %d, %d. Threads requested: %d" % (inputfile, matefile, adapter, qualThreshold, minLen, threads)
if inputfile is '':
	print "No input file given\n"
	sys.exit(1)
try:
	os.makedirs(tmpDir)
except OSError:
	if not os.path.isdir(tmpDir):
		raise
if matefile is not None:
	pe = 1
if singletons in ("True", "TRUE", 'T','1'):
	singletons = 1
if singletons == 1 and pe == 0:
	print "Cannot set singletons to True if mateFile is not specified.\nSingleton flag will be ignored\n"
	singletons = 0
start = timer()

if threads == 1:
	processReads(inputfile,matefile)
else:
    processReads_w_threads()

end = timer()
timePassed = (end - start)
print "Processing with %s threads took : %.2f seconds" % (threads, timePassed)
