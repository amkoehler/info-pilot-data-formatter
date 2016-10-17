import csv

def first_lower(s):
   if len(s) == 0:
      return s
   else:
      return s[0].lower() + s[1:]

with open('Info_PilotData.csv', 'rb') as f:
    reader = csv.reader(f)
    csvData = list(reader)

# Force all column names to lowercase to make their indices easier to find later
for i in range (0, len(csvData[0])):
  csvData[0][i] = csvData[0][i].lower()

# Find max numtrials in order to know column length
maxTrials = 0
for i in range (1, len(csvData)):
  if csvData[i][6] >= maxTrials:
    maxTrials = csvData[i][6]

# Get number of participants by counting unique participant numbers
participants = list()
for i in range (1, len(csvData)):
  participants.append(csvData[i][0])

numParticipants = len(set(participants))
print numParticipants

trialColumnLabels = list([
  'Candidate',
  'rt',
  'rtsq',
  'CandPID',
  'OutParty'
])

columnHeadings = list([
  'Participant'
])

# Create column headings for each trial formatted as "TrialX.Field"
for i in range (0, int(maxTrials)):
  for j in range (0, len(trialColumnLabels)):
    columnHeadings.append('Trial' + str(i) + '.' + trialColumnLabels[j])

formattedData = [['.' for i in range(len(columnHeadings))] for j in range(numParticipants + 1)]
formattedData[0] = columnHeadings

###
### List is now formatted and set up with the correct size and column headings. Next step is to
### parse through csvData and add the appropriate data to formattedData
###

csvRow = 1 # Start at 1 since row 0 is the headings
for i in range (1, numParticipants + 1):

  formattedData[i][0] = csvData[csvRow][csvData[0].index('participant')]
  numTrialsIdx = csvData[0].index('numtrials')
  candidateIndex = csvData[0].index('candidate')

  # Per-trial data gets added here
  for j in range (0, int(csvData[i][numTrialsIdx])):

    # Candidate
    trialIdx = formattedData[0].index('Trial' + str(j) + '.Candidate')
    formattedData[i][trialIdx] = csvData[csvRow][candidateIndex]

    csvRow += 1
print formattedData
###
### List is now formatted correctly. Next step is to write list formattedData to a csv file.
###

output = open('output.csv', 'wb')
outputFile = csv.writer(output)
for row in formattedData:
    outputFile.writerow(row)



