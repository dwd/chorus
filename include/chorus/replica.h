//
// Created by dwd on 28/12/15.
//

#ifndef CHORUS_REPLICA_H
#define CHORUS_REPLICA_H

#include <memory>
#include <set>
#include <functional>
#include <chorus/constants.h>
#include <chorus/message.h>
#include <chorus/election.h>

namespace Chorus {
    class Replica {
    public:
        Replica(id_t replica_id, std::function<void(id_t, Message const &)> sendfunc);
        id_t leader() const {
            return m_leader;
        }
        void leader(id_t leader, Election &);

        void broadcast(Message const & msg);
        void submit(Message const & msg);

        id_t id() const {
            return m_id;
        }
        void complain();
        void complain(Complain const &);
        void concur(Concur const &);

    private:
        // General
        id_t m_id;
        id_t m_leader;
        // Comms.
        std::function<void(id_t, Message const &)> m_sendfunc;
        // Election
        std::unique_ptr<Election> m_election;
        std::set<id_t> m_complaints;
        std::set<id_t> m_concurs;
        bool m_concurred;
    };
}


#endif //CHORUS_REPLICA_H
