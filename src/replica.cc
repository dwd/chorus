//
// Created by dwd on 28/12/15.
//

#include <chorus/replica.h>
#include <chorus/election.h>

// Message types
#include <chorus/vote.h>
#include <chorus/concur.h>
#include <chorus/complain.h>

using namespace Chorus;

Replica::Replica(id_t replica_id, std::function<void(id_t, Message const &)> & fn)
    : m_id(replica_id), m_election(new Election(*this)), m_leader(-1), m_sendfunc(fn) {
}

void Replica::leader(id_t leader, Election & election) {
    if (&election == m_election.get()) {
        m_leader = leader;
        m_election.reset(nullptr);
        m_complaints.clear();
        m_concurred = false;
        m_concurs.clear();
    }
}

void Replica::submit(Message const & msg) {
    switch (msg.type) {
        case Message::Type::VOTE:
            if (!m_election) {
                return;
            }
            m_election->vote(dynamic_cast<Vote const &>(msg));
            break;
        case Message::Type::CONCUR:
            concur(dynamic_cast<Concur const &>(msg));
            break;
        case Message::Type::COMPLAIN:
            complain(dynamic_cast<Complain const &>(msg));
            break;
    }
}

void Replica::complain() {
    broadcast(Complain(m_id, m_leader));
}

void Replica::complain(Complain const & complaint) {
    if (m_concurred) return;
    if (complaint.leader != m_leader) return;
    if (m_complaints.insert(complaint.from).second) {
        if (m_complaints.size() > Config::fail_tolerance) {
            // At least one complaint must be valid.
            broadcast(Concur(m_id, m_leader));
            m_concurred = true;
        }
    }
}

void Replica::concur(Concur const & msg) {
    if (msg.leader != m_leader) return;
    if (m_concurs.insert(msg.from).second) {
        if (m_concurs.size() > Config::fail_tolerance) {
            // At least one concur must be valid.
            m_election.reset(new Election(*this));
        }
    }
}

void Replica::broadcast(Message const &msg) {
    for (id_t replica{0}; replica < Config::total_replicas; ++replica) {
        m_sendfunc(replica, msg);
    }
}