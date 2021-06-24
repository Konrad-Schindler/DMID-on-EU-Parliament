import xml.etree.ElementTree as ET
import time
import numpy as np

start_time = time.time()
TOTALMEPS = 800
IGNORERELATIONUNDER = 5

relationship = np.array(np.zeros((TOTALMEPS,TOTALMEPS)))

iterations = 0
meps = dict()
parties = dict()
names = dict()
mepNumber = 0

for i in range(1,23):
    tree = ET.parse(str(i) + '.xml')
    root = tree.getroot()
    for vote in root.findall('RollCallVote.Result'):
        iterations += 1

        voterelationship = np.array(np.zeros((TOTALMEPS,TOTALMEPS)))
        for party in vote.find('Result.For').findall('Result.PoliticalGroup.List'):
            for mep in party.findall('PoliticalGroup.Member.Name'):
                if(mep.get('PersId') not in meps):
                    meps[mep.get('PersId')] = mepNumber
                    parties[mep.get('PersId')] = party.get('Identifier')
                    names[mep.get('PersId')] = mep.text
                    mepNumber += 1

                voterelationship[meps[mep.get('PersId')]] += 1
                voterelationship[:, meps[mep.get('PersId')]] += 1
        for party in vote.find('Result.Against').findall('Result.PoliticalGroup.List'):
            for mep in party.findall('PoliticalGroup.Member.Name'):
                if(mep.get('PersId') not in meps):
                    meps[mep.get('PersId')] = mepNumber
                    parties[mep.get('PersId')] = party.get('Identifier')
                    names[mep.get('PersId')] = mep.text
                    mepNumber += 1

                voterelationship[meps[mep.get('PersId')]] += -0.5
                voterelationship[:, meps[mep.get('PersId')]] += -0.5

        voterelationship[voterelationship==-0.5] = 0
        voterelationship[voterelationship==1] = 0
        voterelationship[voterelationship==2] = 1
        voterelationship[voterelationship==-1] = 1
        voterelationship[voterelationship==0.5] = -1

        relationship = np.where(voterelationship != 0,relationship*((iterations-1)/iterations),relationship)
        relationship = np.add(relationship,((1/iterations)*voterelationship))
relationship = (relationship - relationship.mean())*10

print(relationship.mean())
print(mepNumber)
print(str(iterations) + " Abstimmungen")
print("Programm lief " + str(time.time() - start_time) + " Sekunden")


with open("Mitgliederliste.txt", 'w') as output:
    for key in meps.keys():
        output.write(str(meps[key]) + "; " + str(parties[key]) + "\n")

with open("EdgeList.txt", 'w') as output:
    for i in range(mepNumber):
        for j in range(i+1,mepNumber):
            if(abs(relationship[i][j]) > IGNORERELATIONUNDER):
                output.write(str(i) + " " + str(j) + " " + str(relationship[i][j]) + "\n")
