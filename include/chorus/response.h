//
// Created by dwd on 28/12/15.
//

#ifndef CHORUS_RESPONSE_H
#define CHORUS_RESPONSE_H

#include <chorus/message.h>

namespace Chorus {
    class Response : public Message {
    public:
        Response(id_t from, id_t leader);
        virtual ~Response();

    protected:
        void render(std::string &) const override;
    };
}


#endif //CHORUS_RESPONSE_H
