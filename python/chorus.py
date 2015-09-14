import json
import time
import hashlib

replicas = {}
total_replicas = 4
fail_tolerance = (total_replicas - 1) / 3

class DataStore:
  def __init__(self):
    self.datasets = {}

  def __getitem__(self, dataset):
    if dataset not in self.datasets:
      self.datasets[dataset] = DataSet(dataset)
    return self.datasets[dataset]

class DataSet:
  def __init__(self, name):
    self.name = name
    self.i = 0

  def pootle(self, i):
    self.i += i

class Replica:
  def __init__(self, id):
    self.tick = 0
    self.id = id
    self.leader = None
    self.queue = {}
    self.datastore = DataStore()
    self.reset_election()
    self.voting = True
    self.init_chorus()
    global replicas
    replicas[self.id] = self

  def broadcast(self, msg, notme=False):
    global replicas
    msgs = json.dumps(msg)
    for id in range(total_replicas):
      if notme == True and id == self.id:
        #print self.id, "Skipping me"
        continue
      #print self.id, "->", id, `msg['type']`
      r = replicas.get(id)
      if r is not None:
        r.rx(self.id, msgs)
        continue
      print "Message unsent"

  def reset_election(self):
    self.round = 0
    self.votes = {}
    self.voting = False
    self.complaints = {}
    self.concurs = {}
    self.all_votes = {}
    self.concurred = False

  def msg_vote(self, sid, msg):
    if not self.voting:
      return
    if msg['round'] != self.round:
      return
    if sid in self.all_votes:
      return
    if msg['vote'] not in self.votes:
      self.votes[msg['vote']] = []
    self.votes[msg['vote']].append(msg['vote'])
    self.all_votes[sid] = True
    if len(self.votes[msg['vote']]) > (2 * fail_tolerance):
      print "Winner!!!: ", msg['vote']
      self.leader = msg['vote']
      self.reset_election()
    elif len(self.all_votes) > (2 * fail_tolerance):
      self.round += 1
      self.votes = {}
      self.all_votes = {}
      self.vote()

  def vote(self):
    global total_replicas
    leader = self.round % total_replicas
    if leader == self.leader:
      leader = (leader + 1) % total_replicas
    msg = {
      'type': 'VOTE',
      'round': self.round,
      'vote': leader
    }
    self.broadcast(msg)

  def complain(self):
    msg = {
      'type': 'COMPLAIN',
      'leader': self.leader
    }
    self.broadcast(msg)

  def msg_complain(self, sid, msg):
    if self.concurred:
      return
    if sid in self.complaints:
      return
    self.complaints[sid] = True
    if len(self.complaints) > fail_tolerance:
      msg = {
        'type': 'CONCUR',
        'leader': self.leader
      }
      self.broadcast(msg)
      self.concurred = True

  def start(self):
    if self.voting:
      self.vote()

  def msg_concur(self, sid, msg):
    if self.voting:
      return
    if sid in self.concurs:
      return
    self.concurs[sid] = True
    if len(self.concurs) > (2 * failtolerance):
      self.start_election()

  def rx(self, sid, msgs):
    msg = json.loads(msgs)
    if msg['type'] == 'VOTE':
      self.msg_vote(sid, msg)
    elif msg['type'] == 'COMPLAIN':
      self.msg_complain(sid, msg)
    elif msg['type'] == 'CONCUR':
      self.msg_concur(sid, msg)
    elif msg['type'] == 'ORDER':
      self.msg_order(sid, msg)
    elif msg['type'] == 'REQUEST':
      self.msg_request(sid, msg, msgs)
    elif msg['type'] == 'RESPONSE':
      self.msg_response(sid, msg)

  def init_chorus(self):
    self.current_operation = False
    self.seq = 0
    self.answers = {}
    self.answered = []
    self.ans_count = 0
    self.view = 0
    self.hn = 'Initial'

  def do_operation(self, operation):
    msg = {'type': 'REQUEST',
    'operation': operation,
    'time': time.time(),
    'clientId': self.id}
    self.broadcast(msg)

  def msg_response(self, sid, msg):
    replica = msg['replica']
    thing = '' + str(replica['view']) + '|' + str(replica['seq']) + '|' + replica['hn'] + '|' + replica['hr'] + '|' + str(replica['clientId'])
    if thing in self.answered:
      #print "  -- Already answered."
      return
    if thing not in self.answers:
      #print "  -- New answer."
      self.answers[thing] = []
    self.answers.get(thing, []).append(msg)
    self.ans_count += 1
    #print "  -- Have ", `len(self.answers[thing])`, "of", `self.ans_count`
    if len(self.answers[thing]) >= (3 * fail_tolerance + 1):
      if replica['clientId'] == self.id:
        print "** Answer:: ", `msg['response']`
      else:
        print "** Push:: ", `msg['response']`
      self.answered.append(thing)
      self.answers = {}

  def msg_order(self, sid, msg):
    if sid != self.leader:
      print "Sender is not leader."
      return
    primary = msg['primary']
    if primary['view'] != self.view:
      print `self.__class__.__name__`, `self.id`, "ERROR:", "Incorrect view"
      return # Incorrect view
    if primary['seq'] != self.seq + 1:
      print `self.__class__.__name__`, `self.id`, "ERROR:", "Incorrect sequence"
      return # Incorrect sequence
    dh = hashlib.sha256()
    dh.update(msg['clientMessage'])
    d = dh.hexdigest()
    if primary['d'] != d:
      print `self.__class__.__name__`, `self.id`, "ERROR:", "Incorrect message hash"
      return # Message Hash
    hnh = hashlib.sha256()
    hnh.update(self.hn)
    hnh.update(d)
    hn = hnh.hexdigest()
    if primary['hn'] != hn:
      print `self.__class__.__name__`, `self.id`, "ERROR:", "Incorrect history hash"
      return
    self.seq += 1
    self.hn = hn
    client = json.loads(msg['clientMessage'])
    self.perform_operation(client)

  def perform_operation(self, msg):
    reply = self.handle_operation(msg['operation'])
    hrh = hashlib.sha256()
    hrh.update(reply)
    hr = hrh.hexdigest()
    replymsg = {
      'type': 'RESPONSE',
      'replica': {
        'view': self.view,
        'seq': self.seq,
        'hn': self.hn,
        'hr': hr,
        'clientId': msg['clientId']
      },
      'replicaId': self.id,
      'response': reply,
      'primary': self.leader
    }
    self.broadcast(replymsg)

  def msg_request(self, sid, msg, msgs):
    if self.leader != self.id:
      return
    if msg['clientId'] != sid:
      print self.id, "Spoofed client, ignoring"
      return
    self.seq += 1
    d = hashlib.sha256()
    d.update(msgs)
    x = d.hexdigest()
    hnh = hashlib.sha256()
    hnh.update(self.hn)
    hnh.update(x)
    self.hn = hnh.hexdigest()
    newmsg = {
      'type': 'ORDER',
      'primary': {
        'view': self.view,
        'seq': self.seq,
        'hn': self.hn,
        'd': x,
        'nd': {}
      },
      'clientMessage': msgs
    }
    self.broadcast(newmsg, True)
    self.perform_operation(msg)

  def handle_operation(self, op):
    if op == 'Hello':
      return 'World!'
    else:
      return 'Error.'

if __name__ == '__main__':
  for r in range(total_replicas):
    Replica(r)
  for rid, r in replicas.items():
    r.start()
  replicas[0].do_operation('Hello')
  replicas[1].do_operation('World')
