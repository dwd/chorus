//
// Created by dwd on 28/12/15.
//

#ifndef CHORUS_CONCUR_H
#define CHORUS_CONCUR_H


#include <chorus/message.h>

namespace Chorus {
    class Concur : public Message {
    public:
        Concur(id_t from, id_t leader);
        virtual ~Concur();
        std::unique_ptr<Message> copy() const override;

    protected:
        void render(std::string &) const override;

    public:
        id_t leader;
    };
}

#endif //CHORUS_CONCUR_H
