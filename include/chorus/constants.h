//
// Created by dwd on 28/12/15.
//

#ifndef CHORUS_CONSTANTS_H
#define CHORUS_CONSTANTS_H

#include <stddef.h>

namespace Chorus {
    typedef long id_t;
    class Election;
    class Message;
    class Replica;
    class Config {
    public:
        static size_t fail_tolerance;
        static size_t total_replicas;
    };
}


#endif //CHORUS_CONSTANTS_H
