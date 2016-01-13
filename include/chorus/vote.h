//
// Created by dwd on 28/12/15.
//

#ifndef CHORUS_VOTE_H
#define CHORUS_VOTE_H

#include <chorus/constants.h>
#include <chorus/message.h>

namespace Chorus {
    class Vote : public Message {
    public:
        Vote(unsigned around, id_t afrom, id_t aproposed);
        virtual ~Vote();
    protected:
        virtual void render(std::string &) const override;

    public:
        unsigned round;
        id_t proposed;
    };
}


#endif //CHORUS_VOTE_H
