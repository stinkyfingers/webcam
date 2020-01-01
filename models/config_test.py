from config import Config
import unittest
import os


class ConfigTest(unittest.TestCase):

    def test_write(self):
        c = Config()
        c.data = {
            'foo': 'bar'
        }
        c.write()

        c2 = Config()
        c2.read()
        self.assertEqual(c.data, c2.data)

        c.upsert({'poo': 'par'})
        c.data['poo'] = 'par'
        c2.read()
        self.assertEqual(c.data, c2.data)

        os.remove('config.json')

if __name__ == '__main__':
	unittest.main()
