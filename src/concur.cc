//
// Created by dwd on 28/12/15.
//

#include <chorus/concur.h>

using namespace Chorus;

Concur::Concur(id_t froma, id_t leadera)
        : Message(Type::CONCUR, froma), leader(leadera) {
}

Concur::~Concur() {}


void Concur::render(std::string &buffer) const {
}