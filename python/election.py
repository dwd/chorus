
# Rules:
# Electors start by an election, round = 0
# Electors send votes to each other, choosing the lowest non-compromised peer >= round % N
# If Electors receive 2f+1 votes for a peer, this is now the leader.
# If not, increase round.

# Initiate an election by sending compromises to each Elector.
# If Electors receive f+1, they have received at least 1 valid complaint => advertise concur to all peers.
# Elections start when received 2f+1 complaints or concurs.

import json

electors = []
failtolerance = 1

class Elector:
  def __init__(self, id):
    self.id = id
    self.round = 0
    self.current = None
    self.votes = {}
    self.voting = True
    self.complaints = 0
    self.concurs = 0
    self.all_votes = 0
    self.concurred = False

  def start_election(self):
    self.voting = True
    self.vote()

  def vote(self):
    global electors
    leader = self.round % len(electors)
    if leader == self.current:
      leader = (leader + 1) % len(electors)
    msg = {
      'type': 'VOTE',
      'round': self.round,
      'vote': leader
    }
    msgs = json.dumps(msg)
    for peer in electors:
      peer.rx_message(msgs)

  def evil(self):
    msg = {
      'type': 'COMPLAIN',
      'leader': self.current
    }
    msgs = json.dumps(msg)
    for peer in electors:
      peer.rx_message(msgs)

  def rx_message(self, msgs):
    msg = json.loads(msgs)
    if msg['type'] == 'VOTE':
      if not self.voting:
        return
      if msg['round'] != self.round:
        return
      if msg['vote'] not in self.votes:
        self.votes[msg['vote']] = []
      self.votes[msg['vote']].append(msg['vote'])
      self.all_votes += 1
      if len(self.votes[msg['vote']]) > (2 * failtolerance):
        print "Winner!!!: ", msg['vote']
        self.current = msg['vote']
        self.round = 0
        self.votes = {}
        self.voting = False
        self.complaints = 0
        self.concurs = 0
        self.all_votes = 0
      elif self.all_votes > (2 * failtolerance):
        self.round += 1
        self.votes = {}
        self.all_votes = 0
    elif msg['type'] == 'COMPLAIN':
      if self.concurred:
        return
      self.complaints += 1
      if self.complaints > failtolerance:
        msg = {
          'type': 'CONCUR',
          'leader': self.current
        }
        msgs = json.dumps(msg)
        for peer in electors:
          peer.rx_message(msgs)
        self.concurred = True
      if (self.concurs + self.complaints) > (2 * failtolerance):
        self.start_election()
    elif msg['type'] == 'CONCUR':
      if self.voting:
        return
      self.concurs += 1
      if (self.concurs + self.complaints) > (2 * failtolerance):
        self.start_election()

for i in range((3 * failtolerance) + 1):
  electors.append(Elector(i))

for el in electors:
  el.start_election()

print "1 says evil"
electors[1].evil()
print "2 says evil"
electors[3].evil()
