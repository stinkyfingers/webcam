from movie import Movie
import unittest
import os


class MovieTest(unittest.TestCase):
    def test(self):
        self.assertTrue(True)

    def test_get_index(self):
        m = Movie()
        for i in range (1,4):
            file = os.path.join(m.dir, 'test.{}.jpg'.format(i))
            open(file).close()
        index = m.get_index()
        self.assertEqual(index, 3)

if __name__ == '__main__':
	unittest.main()
