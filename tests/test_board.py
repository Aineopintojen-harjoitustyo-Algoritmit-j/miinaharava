import unittest
from board.board import Board

class TestBoardClass(unittest.TestCase):
    def test_init(self):
        b = Board()
        self.assertTrue(b.size>0)
    
    def test_init_with_size(self):
        b = Board(15)
        self.assertEqual(b.size, 15)
        
    def test_get_view_and_make_guess(self):
        b = Board(3)
        b.tiles=[[0,0,0],[0,1,1],[0,1,9]]

        v = b.get_view()
        t = [[10,10,10],[10,10,10],[10,10,10]]
        for i in range(3):
            self.assertEqual(v[i],t[i])
            
        self.assertTrue(b.make_guess(0,0))
        v = b.get_view()
        t = [[0,0,0],[0,1,1],[0,1,10]]
        for i in range(3):
            self.assertEqual(v[i],t[i])
            
        self.assertFalse(b.make_guess(2,2))
        
    