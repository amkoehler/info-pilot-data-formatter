import csv

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
  'BoxSelection',
  'Candidate',
  'rt',
  'rtsq',
  'CandPID',
  'OutParty'
])

columnHeadings = list([
  'Participant',
  'Condition'
])

# Create column headings for each trial formatted as "TrialX.Field"
for i in range (0, int(maxTrials)):
  for j in range (0, len(trialColumnLabels)):
    columnHeadings.append('Trial' + str(i) + '.' + trialColumnLabels[j])

formattedData = [['.' for i in range(len(columnHeadings))] for j in range((numParticipants) * 3)]
formattedData[0] = columnHeadings

###
### List is now formatted and set up with the correct size and column headings. Next step is to
### parse through csvData and add the appropriate data to formattedData
###

# Get all the column indices in csvData. This is more safe and flexible than assuming a
# column is at a certain index but does assume that the column names in the original csv
# do not change. 
maxFlagIndex = csvData[0].index('max')
participantIndex = csvData[0].index('participant')
candidateIndex = csvData[0].index('candidate')
conditionIndex = csvData[0].index('condition')
rtIndex = csvData[0].index('rt')
rtsqIndex = csvData[0].index('rtsq')
candpidIndex = csvData[0].index('candpid')
outpartyIndex = csvData[0].index('outparty')

# Box selection
boxIndices = {
  csvData[0].index('demogbox') : 'DemogBox',  
  csvData[0].index('socissuebox') : 'SocIssueBox',  
  csvData[0].index('econissuebox') : 'EconIssueBox',  
  csvData[0].index('religbox') : 'ReligBox',  
  csvData[0].index('scandalbox') : 'ScandalBox',  
  csvData[0].index('personbox') : 'PersonBox',  
  csvData[0].index('pictbox') : 'PictBox',  
  csvData[0].index('viabilbox') : 'ViabilBox',  
  csvData[0].index('experbox') : 'ExperBox',  
  csvData[0].index('partyidbox') : 'PartyIDBox'
}

boxMinIndex = min(boxIndices.keys(), key=int)
boxMaxIndex = max(boxIndices.keys(), key=int)

fParticipantIndex = formattedData[0].index('Participant')
fConditionIndex = formattedData[0].index('Condition')
trialNum = 0
x = 1

for i in range (1, len(csvData)):

  # Participant
  if formattedData[x][participantIndex] == '.': 
    formattedData[x][fParticipantIndex] = csvData[i][participantIndex]
  
  # Condition
  if formattedData[x][conditionIndex] == '.': 
    formattedData[x][fConditionIndex] = csvData[i][conditionIndex]

  # Candidate
  trialIdx = formattedData[0].index('Trial' + str(trialNum) + '.Candidate')
  formattedData[x][trialIdx] = csvData[i][candidateIndex]

  # rt
  trialIdx = formattedData[0].index('Trial' + str(trialNum) + '.rt')
  formattedData[x][trialIdx] = csvData[i][rtIndex]

  # rtsq
  trialIdx = formattedData[0].index('Trial' + str(trialNum) + '.rtsq')
  formattedData[x][trialIdx] = csvData[i][rtsqIndex]

  # CandPID
  trialIdx = formattedData[0].index('Trial' + str(trialNum) + '.CandPID')
  formattedData[x][trialIdx] = csvData[i][candpidIndex]

  # OutParty
  trialIdx = formattedData[0].index('Trial' + str(trialNum) + '.OutParty')
  formattedData[x][trialIdx] = csvData[i][outpartyIndex]

  # BoxSelection
  trialIdx = formattedData[0].index('Trial' + str(trialNum) + '.BoxSelection')
  for j in range (boxMinIndex, boxMaxIndex): 
    if int(csvData[i][j]) == 1: 
      formattedData[x][trialIdx] = boxIndices[j]

  trialNum += 1

  if int(csvData[i][maxFlagIndex]) == 1:
    x += 1
    trialNum = 0

###
### List is now formatted correctly. Final step is to write list formattedData to a csv file.
###

output = open('output.csv', 'wb')
outputFile = csv.writer(output)
for row in formattedData:
    outputFile.writerow(row)



