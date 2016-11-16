import json, urllib, csv

teamRosterUrl = 'http://www.extra-life.org/index.cfm?fuseaction=donorDrive.teamParticipants&teamID={teamId}&format=json'
participantUrl = 'http://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID={participantId}&format=json'
teamUrl = 'http://www.extra-life.org/index.cfm?fuseaction=donorDrive.team&teamID={teamId}&format=json'
reference = json.loads(open('reference.json').read())

def getTeamRoster():
    teamRosterWithMoneyRaised = {}
    sourceRoster = json.loads(urllib.urlopen(teamRosterUrl.format(teamId = reference['team number'])).read())
    for participant in sourceRoster:
        teamRosterWithMoneyRaised[participant['participantID']] = json.loads(urllib.urlopen(participantUrl.format(participantId = participant['participantID'])).read())
    return teamRosterWithMoneyRaised

def getSubTeamTotals(teamRoster):
    subteams = {}
    for subteamName, subteamParticipants in reference['teams'].iteritems():
        subteams[subteamName] = {'raised': 0, 'goal': 0}
        for participant in subteamParticipants:
            subteams[subteamName]['raised'] += teamRoster[participant['participantID']]['totalRaisedAmount']
            subteams[subteamName]['goal'] += teamRoster[participant['participantID']]['fundraisingGoal']
    return subteams

def sortResults(subteamTotals):
    return sorted(subteamTotals.items(), key = lambda item: item[1]['raised'], reverse = True)

def printResults(subteamTotals):
    totalJson = json.loads(urllib.urlopen(teamUrl.format(teamId = reference['team number'])).read())
    print('TOTAL          ${0:.2f} / ${1:.2f}'.format(totalJson['totalRaisedAmount'],totalJson['fundraisingGoal']))
    print('='*35)
    for team in sortResults(subteamTotals):
        print('{0:14} ${1:.2f} / ${2:.2f}'.format(team[0], team[1]['raised'], team[1]['goal']))

if __name__ == "__main__":
    printResults(getSubTeamTotals(getTeamRoster()))
    