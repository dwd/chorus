//
// Created by dwd on 28/12/15.
//

#include <chorus/vote.h>

using namespace Chorus;

Vote::Vote(unsigned around, id_t afrom, id_t aproposed)
        : Message(Type::VOTE, afrom), round(around), proposed(aproposed) {}
Vote::~Vote() {}

std::unique_ptr<Message> Vote::copy() const {
        return std::unique_ptr<Message>(new Vote(round, from, proposed));
}

void Vote::render(std::string &buffer) const {
}