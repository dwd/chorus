//
// Created by dwd on 28/12/15.
//

#ifndef CHORUS_ELECTION_H
#define CHORUS_ELECTION_H

#include <map>
#include <set>
#include <memory>
#include <chorus/vote.h>
#include <chorus/replica.h>

namespace Chorus {
    class Election {
    public:
        Election(Replica & replica);
        void vote(Vote const & vote);
    private:
        void vote();

    private:
        Replica & m_replica;
        id_t m_id;
        unsigned m_round;
        std::set<id_t> m_voted;
        std::map<id_t,size_t> m_votes;
    };
}


#endif //CHORUS_ELECTION_H
