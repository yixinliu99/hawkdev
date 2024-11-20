import pytest
from src.Auction.dao.mongoDAO import MongoDao
import mongomock
import uuid


class TestMongoDBManager:
    @pytest.fixture
    def mongo_dao(self):
        yield MongoDao()

    @pytest.fixture
    def client_mock(self):
        yield mongomock.MongoClient()

    @pytest.fixture
    def mock_db(self, client_mock):
        yield client_mock.db

    def test_write_to_db_one(self, mongo_dao, mock_db):
        data = {'arctic': 'monkeys' + str(uuid.uuid4())}
        result = mongo_dao.write_to_db('test_collection', data)
        assert result

        written_data = mock_db['test_collection'].find(data)
        assert written_data

    def test_write_to_db_list(self, mongo_dao, mock_db):
        data = [{'arctic': 'monkeys' + str(uuid.uuid4())}, {'arctic': 'monkeys' + str(uuid.uuid4())}]
        result = mongo_dao.write_to_db('test_collection', data)
        assert len(result) == 2

        for d in data:
            written_data = mock_db['test_collection'].find(d)
            assert written_data


    def test_read_from_db(self, mongo_dao, mock_db):
        data = {'arctic': 'monkeys' + str(uuid.uuid4())}
        mongo_dao.write_to_db('test_collection', data)

        # read
        written_data = mongo_dao.read_from_db('test_collection', data)
        assert written_data

    def test_update_db(self, mongo_dao, mock_db):
        data = {'arctic': 'monkeys' + str(uuid.uuid4())}
        mongo_dao.write_to_db('test_collection', data)

        update = {'$set': {'arctic': 'monkeys' + str(uuid.uuid4())}}
        result = mongo_dao.update_db('test_collection', data, update)
        assert result == 1

        updated_data = mock_db['test_collection'].find(data)
        assert updated_data

    def test_delete_from_db_one(self, mongo_dao, mock_db):
        # write
        data = {'arctic': 'monkeys' + str(uuid.uuid4())}
        mongo_dao.write_to_db('test_collection', data)

        # delete
        result = mongo_dao.delete_from_db('test_collection', data)
        assert result == 1
        deleted_data = mongo_dao.read_from_db('test_collection', data)
        assert not deleted_data


    def test_delete_from_db_many(self, mongo_dao, mock_db):
        # write
        data = [{'arctic': 'monkeys' + str(uuid.uuid4())}, {'arctic': 'monkeys' + str(uuid.uuid4())}]
        mongo_dao.write_to_db('test_collection', data)

        # delete
        result = mongo_dao.delete_from_db('test_collection', {'arctic': {'$regex': 'monkeys'}}, many=True)
        assert result > 1

        deleted_data = mongo_dao.read_from_db('test_collection', {'arctic': {'$regex': 'monkeys'}})
        assert not deleted_data