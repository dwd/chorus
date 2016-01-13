//
// Created by dwd on 28/12/15.
//

#ifndef CHORUS_REQUEST_H
#define CHORUS_REQUEST_H

#include <chorus/message.h>

namespace Chorus {
    class Request : public Message {
    public:
        Request(id_t from, id_t leader);
        virtual ~Request();
        std::unique_ptr<Message> copy() const override;

    protected:
        void render(std::string &) const override;
    };
}


#endif //CHORUS_REQUEST_H
