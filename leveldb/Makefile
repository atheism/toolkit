CXX = g++
SOURCE_LIST = leveldb-test.cpp
CXXFLAGS = -lleveldb -ggdb3

all: leveldb-test

leveldb-test: $(SOURCE_LIST)
	$(CXX) -o $@ $< $(CXXFLAGS)

clean:
	rm -rf leveldb-test ./testdb
