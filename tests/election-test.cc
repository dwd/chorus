//
// Created by dwd on 13/01/16.
//

#include <vector>
#include <memory>

#include <iostream>

#include <chorus/replica.h>

class TestHarness {
public:
    std::vector<std::unique_ptr<Chorus::Replica>> m_replicas;
    std::vector<std::pair<id_t, std::unique_ptr<Chorus::Message>>> m_queue;

    TestHarness(size_t fails) {
        Chorus::Config::fail_tolerance = fails;
        Chorus::Config::total_replicas = (3 * fails) + 1;
        using std::placeholders::_1;
        using std::placeholders::_2;
        for (Chorus::id_t i{0}; i < Chorus::Config::total_replicas; ++i) {
            m_replicas.emplace_back(new Chorus::Replica(i, std::function<void(Chorus::id_t, Chorus::Message const &)>(std::bind(&TestHarness::send, this, _1, _2))));
        }
    }
    bool tick_tock() {
        if (m_queue.empty()) return false;
        std::cout << "Queue is " << m_queue.size() << " long., sending to " << m_queue[0].first << std::endl;
        m_replicas[m_queue[0].first]->submit(*m_queue[0].second);
        m_queue.erase(m_queue.begin());
    }
    void send(Chorus::id_t id, Chorus::Message const & msg) {
        m_queue.emplace_back(std::make_pair(id,msg.copy()));
    }
};

int main(int argc, char * argv[]) {
    try {
        TestHarness tests(2);
        while (tests.tick_tock());
        for (auto & i : tests.m_replicas) {
            std::cout << "Replica " << i->id() << " selected leader " << i->leader() << std::endl;
        }
    } catch(std::exception & e) {
        std::cout << "Exception, dude: " << e.what() << std::endl;
    }
}