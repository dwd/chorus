//
// Created by dwd on 28/12/15.
//

#include <chorus/complain.h>

using namespace Chorus;

Complain::Complain(id_t froma, id_t leadera)
        : Message(Type::COMPLAIN, froma), leader(leadera) {
}

Complain::~Complain() {}

std::unique_ptr<Message> Complain::copy() const {
        return std::unique_ptr<Message>(new Complain(from, leader));
}


void Complain::render(std::string &buffer) const {
        buffer += "<foo/>";
}