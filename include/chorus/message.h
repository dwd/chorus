//
// Created by dwd on 28/12/15.
//

#ifndef CHORUS_MESSAGE_H
#define CHORUS_MESSAGE_H

#include <string>
#include <memory>

#include <chorus/constants.h>

namespace Chorus {
    class Vote;

    class Complain;
    class Concur;

    class Request;
    class Order;
    class Response;

    class Message {
    public:
        enum class Type {
            VOTE,
            COMPLAIN,
            CONCUR,
            ORDER,
            REQUEST,
            RESPONSE
        };
        virtual ~Message();
        static std::unique_ptr<Message> parse(std::string const & buffer);
        std::string render() const;
        virtual std::unique_ptr<Message> copy() const = 0;
    protected:
        Message(Type, id_t);
        virtual void render(std::string &) const = 0;
    public:
        Type type;
        id_t from;
    };
}

#endif //CHORUS_MESSAGE_H
