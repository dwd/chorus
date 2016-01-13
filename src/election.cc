//
// Created by dwd on 28/12/15.
//

#include <chorus/election.h>

#include <iostream>

using namespace Chorus;

Election::Election(Replica & replica)
        : m_replica(replica), m_round(0) {
    vote();
}

void Election::vote(Vote const & vote) {
    if (m_voted.find(vote.from) != m_voted.end()) {
        // Duplicate vote, toss.
        std::cout << "Election " << m_replica.id() << " received duplicate vote from " << vote.from << std::endl;
        return;
    }
    if (m_round != vote.round) {
        // Wrong round, toss.
        std::cout << "Election " << m_replica.id() << " received wrong round vote from " << vote.from << std::endl;
        return;
    }
    m_voted.insert(vote.from);
    ++m_votes[vote.proposed];
    if (m_votes[vote.proposed] > (2 * Config::fail_tolerance)) {
        // Winner.
        std::cout << m_replica.id() << " believes there is a winner: " << vote.proposed << std::endl;
        m_replica.leader(vote.proposed, *this);
        // Destroyed.
    } else if (m_voted.size() > (2 * Config::fail_tolerance)) {
        std::cout << "Too many votes cast for " << m_replica.id() << ", new round." << std::endl;
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