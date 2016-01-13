//
// Created by dwd on 28/12/15.
//

#ifndef CHORUS_ORDER_H
#define CHORUS_ORDER_H

#include <chorus/message.h>

namespace Chorus {
    class Order : public Message {
    public:
        Order(id_t from, size_t view, size_t seq, std::string const & hn, std::string const & d, Request const & request);
        virtual ~Order();
        std::unique_ptr<Message> copy() const override;

    protected:
        void render(std::string &) const override;
    };
}

#endif //CHORUS_ORDER_H
