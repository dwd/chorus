//
// Created by dwd on 28/12/15.
//

#include <chorus/election.h>

using namespace Chorus;

Election::Election(Replica & replica)
        : m_replica(replica) {
    vote();
}

void Election::vote(Vote const & vote) {
    if (m_voted.find(vote.from) == m_voted.end()) {
        // Duplicate vote, toss.
        return;
    }
    if (m_round != vote.round) {
        // Wrong round, toss.
        return;
    }
    m_voted.insert(vote.from);
    ++m_votes[vote.proposed];
    if (m_votes[vote.proposed] > (2 * Config::fail_tolerance)) {
        // Winner.
        m_replica.leader(vote.proposed, *this);
        // Destroyed.
    } else if (m_voted.size() > (2 * Config::fail_tolerance)) {
        ++m_round;
        m_votes.clear();
        m_voted.clear();
        this->vote();
    }
}

void Election::vote() {
    id_t leader = m_round % Config::total_replicas;
    if (leader == m_replica.leader()) {
        leader = (leader + 1) % Config::total_replicas;
    }
    Vote v(m_round, m_replica.id(), leader);
    m_replica.broadcast(v);
}