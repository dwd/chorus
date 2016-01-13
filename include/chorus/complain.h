//
// Created by dwd on 28/12/15.
//

#ifndef CHORUS_COMPLAIN_H
#define CHORUS_COMPLAIN_H

#include <chorus/message.h>

namespace Chorus {
    class Complain : public Message {
    public:
        Complain(id_t froma, id_t leadera);
        virtual ~Complain();

    protected:
        void render(std::string &) const override;

    public:
        id_t leader;
    };
}


#endif //CHORUS_COMPLAIN_H
