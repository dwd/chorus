//
// Created by dwd on 28/12/15.
//

#include <chorus/complain.h>

using namespace Chorus;

Complain::Complain(id_t froma, id_t leadera)
        : Message(Type::COMPLAIN, froma), leader(leadera) {
}

Complain::~Complain() {}

void Complain::render(std::string &buffer) const {
        buffer += "<foo/>";
}