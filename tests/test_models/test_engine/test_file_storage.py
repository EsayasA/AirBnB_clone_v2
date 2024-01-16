#!/usr/bin/python3
""" test for stirage file"""
import unittest
from models.base_model import BaseModel
from models import storage
import os


class test_fileStorage(unittest.TestCase):
    """ Class for test the file """

    def setUp(self):
        """ Setup """
        del_list = []
        for key in storage._FileStorage__objects.keys():
            del_list.append(key)
        for key in del_list:
            del storage._FileStorage__objects[key]

    def tearDown(self):
        """ teardown """
        try:
            os.remove('file.json')
        except:
            pass

    def test_obj_list_empty(self):
        """ empyty object """
        self.assertEqual(len(storage.all()), 0)

    def test_new(self):
        """ add new object """
        new = BaseModel()
        for obj in storage.all().values():
            temp = obj
        self.assertTrue(temp is obj)

    def test_all(self):
        """ return object """
        new = BaseModel()
        temp = storage.all()
        self.assertIsInstance(temp, dict)

    def test_base_model_instantiation(self):
        """ if file not created """
        new = BaseModel()
        self.assertFalse(os.path.exists('file.json'))

    def test_empty(self):
        """ save file """
        new = BaseModel()
        thing = new.to_dict()
        new.save()
        new2 = BaseModel(**thing)
        self.assertNotEqual(os.path.getsize('file.json'), 0)

    def test_save(self):
        """ save file """
        new = BaseModel()
        storage.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_reload(self):
        """ load file """
        new = BaseModel()
        storage.save()
        storage.reload()
        for obj in storage.all().values():
            loaded = obj
        self.assertEqual(new.to_dict()['id'], loaded.to_dict()['id'])

    def test_reload_empty(self):
        """ empty file loaded """
        with open('file.json', 'w') as f:
            pass
        with self.assertRaises(ValueError):
            storage.reload()

    def test_reload_from_nonexistent(self):
        """ if file not exist """
        self.assertEqual(storage.reload(), None)

    def test_base_model_save(self):
        """ save basemodel """
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_type_path(self):
        """ Confirm path of the file"""
        self.assertEqual(type(storage._FileStorage__file_path), str)

    def test_type_objects(self):
        """ Confirm obj of the dic """
        self.assertEqual(type(storage.all()), dict)

    def test_key_format(self):
        """ key format """
        new = BaseModel()
        _id = new.to_dict()['id']
        for key in storage.all().keys():
            temp = key
        self.assertEqual(temp, 'BaseModel' + '.' + _id)

    def test_storage_var_created(self):
        """ store the file """
        from models.engine.file_storage import FileStorage
        print(type(storage))
        self.assertEqual(type(storage), FileStorage)
