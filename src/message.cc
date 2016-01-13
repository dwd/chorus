//
// Created by dwd on 28/12/15.
//

#include <chorus/message.h>

using namespace Chorus;

Message::Message(Type t, id_t froma)
    : type(t), from(froma) {
}

Message::~Message() {
}

std::unique_ptr<Message> Message::parse(std::string const &buffer) {

}