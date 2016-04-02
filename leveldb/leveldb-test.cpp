#include <iostream>
#include <sstream>
#include <cassert>
#include <leveldb/db.h>

int main(int argc, char **argv)
{
    leveldb::DB* db;
    leveldb::Options options;
    options.create_if_missing = true;
    leveldb::Status status = leveldb::DB::Open(options,
            "./testdb", &db);
    assert(status.ok());

    leveldb::WriteOptions writeoptions;
    for (uint64_t i = 0; i < 1024; ++i)
    {
        std::ostringstream keystream;
        keystream << "Key" << i;

        std::ostringstream valuestream;
        valuestream << "Test data value: " << i;

        db->Put(writeoptions, keystream.str(), valuestream.str());
    }

    leveldb::Iterator* it = db->NewIterator(leveldb::ReadOptions());

    for (it->SeekToFirst(); it->Valid(); it->Next())
    {
        std::cout << it->key().ToString() << " : "
            << it->value().ToString() << std::endl;
    }
    assert(it->status().ok());

    delete it;

    delete db;

    return 0;
}
