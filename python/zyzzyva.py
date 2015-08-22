import time
import json
import hashlib

msg_types = {}

class MessageType:
  def __init__(self, t):
    self.t = t
    msg_types[t] = self
  def __str__(self):
    return self.t
  def str(self):
    return self.t
  def __repr__(self):
    return 'MessageType(' + repr(self.t) + ')'
REQUEST = MessageType('REQUEST')
ORDER_REQ = MessageType('ORDER-REQ')
SPEC_RESPONSE = MessageType('SPEC-RESPONSE')
def MsgType(t):
  return msg_types[t]

class World:
  def __init__(self):
    self.clients = {}
    self.servers = {}
    self.primary = None
    self.max_failures = 1

world = World()

class Client:
  def __init__(self, id):
    self.id = id
    self.current_operation = False
    world.clients[id] = self
    self.seq = 0
    self.answers = {}
    self.answered = []
    self.ans_count = 0

  def rx_message(self, stuff):
    #print `self.__class__.__name__`, `self.id`, stuff
    msg = json.loads(stuff)
    if MsgType(msg['msgtype']) is SPEC_RESPONSE:
      replica = msg['replica']
      thing = '' + str(replica['view']) + '|' + str(replica['seq']) + '|' + replica['hn'] + '|' + replica['hr'] + '|' + replica['clientId']
      if thing in self.answered:
        return
      if thing not in self.answers:
        self.answers[thing] = []
      self.answers.get(thing, []).append(msg)
      self.ans_count += 1
      if len(self.answers[thing]) >= (3 * world.max_failures + 1):
        if replica['clientId'] == self.id:
          print "** Answer:: ", `msg['response']`
        else:
          print "** Push:: ", `msg['response']`
        self.answered.append(thing)


  def do_operation(self, operation):
    msg = {'msgtype': REQUEST.str(),
    'operation': operation,
    'time': time.time(),
    'clientId': self.id}
    world.primary.rx_message(json.dumps(msg))

class Server:
  def __init__(self, id, is_master):
    self.id = id
    self.view = 0
    self.seq = 0
    self.is_master = is_master
    self.hn = 'Initial'
    world.servers[id] = self
    if is_master:
      world.primary = self

  def rx_message(self, stuff):
    #print `self.__class__.__name__`, `self.id`, stuff
    msg = json.loads(stuff)
    if MsgType(msg['msgtype']) is REQUEST:
      if not self.is_master:
        world.primary.rx_message(stuff)
        return
      self.seq += 1
      d = hashlib.sha256()
      d.update(stuff)
      x = d.hexdigest()
      hnh = hashlib.sha256()
      hnh.update(self.hn)
      hnh.update(x)
      self.hn = hnh.hexdigest()
      newmsg = {
        'msgtype': ORDER_REQ.str(),
        'primary': {
          'view': self.view,
          'seq': self.seq,
          'hn': self.hn,
          'd': x,
          'nd': {}
        },
        'clientMessage': stuff
      }
      new_stuff = json.dumps(newmsg)
      for id, replica in world.servers.items():
        if id == self.id:
          continue
        replica.rx_message(new_stuff)
    elif MsgType(msg['msgtype']) is ORDER_REQ:
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
      client = json.loads(msg['clientMessage'])
      if client['operation'] != "Hello":
        reply = 'Error' ## Note that errors are successful in the sense of Zyzzyva
      else:
        reply = 'World'
      self.seq += 1
      self.hn = hn
      hrh = hashlib.sha256()
      hrh.update(reply)
      hr = hrh.hexdigest()
      replymsg = {
        'msgtype': SPEC_RESPONSE.str(),
        'replica': {
          'view': self.view,
          'seq': self.seq,
          'hn': self.hn,
          'hr': hr,
          'clientId': client['clientId']
        },
        'replicaId': self.id,
        'response': reply,
        'primary': primary
      }
      replydata = json.dumps(replymsg)
      for id, client in world.clients.items():
        client.rx_message(replydata)


c1 = Client('c1')
c2 = Client('c2')
servers = [Server('s%d' % x, x == 0) for x in range(7)]

c1.do_operation('Hello')
c2.do_operation('World!')
