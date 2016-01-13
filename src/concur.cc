//
// Created by dwd on 28/12/15.
//

#include <chorus/concur.h>

using namespace Chorus;

Concur::Concur(id_t froma, id_t leadera)
        : Message(Type::CONCUR, froma), leader(leadera) {
}

Concur::~Concur() {}

std::unique_ptr<Message> Concur::copy() const {
        return std::unique_ptr<Message>(new Concur(from, leader));
}


void Concur::render(std::string &buffer) const {
}