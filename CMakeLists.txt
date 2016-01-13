cmake_minimum_required(VERSION 3.3)
project(chorus)

include_directories(include)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES
        src/replica.cc include/chorus/replica.h src/election.cc include/chorus/election.h src/constants.cc include/chorus/constants.h src/vote.cc include/chorus/vote.h src/message.cc include/chorus/message.h src/complain.cc include/chorus/complain.h src/concur.cc include/chorus/concur.h src/order.cc include/chorus/order.h src/request.cc include/chorus/request.h src/response.cc include/chorus/response.h election.cc.cc election.cc.h election-test.cc.cc)

add_executable(zyzzyva ${SOURCE_FILES})