"""test_board.py - Testit pelilaudalle"""
# Tämä tiedosto on jätettty pylint testien ulkopuolelle, koska tässä tehdään
# paljon "kiellettyjä asioita", kuten käydään lukemassa luokan "privaatteja"
# muuttujia

import unittest
from board import Board, Level, LevelSpecs

class TestBoardClass(unittest.TestCase):
    """ pelilauden testit kattava luokka """
    def test_init_works_and_defaults_beginner(self):
        """ pelilautaolion luominen onnistuu ja defaulttaa aloittelijaksi """
        b = Board()
        self.assertEqual(b.get_width(), LevelSpecs[Level.BEGINNER][0])
        self.assertEqual(b.get_height(), LevelSpecs[Level.BEGINNER][1])
        self.assertEqual(b.get_mines(), LevelSpecs[Level.BEGINNER][2])
        self.assertTrue(b.get_width()>0)

    def test_init_with_level(self):
        """ olion luominen onnistuu vaikeustasolla"""
        b = Board(level=Level.EXPERT)
        self.assertEqual(b.get_width(), LevelSpecs[Level.EXPERT][0])
        self.assertEqual(b.get_height(), LevelSpecs[Level.EXPERT][1])
        self.assertEqual(b.get_mines(), LevelSpecs[Level.EXPERT][2])

    def test_init_with_incorect_dimensions(self):
        """ luominen ei saa onnitua mahdottomilla mitoilla """
        b = Board(width=1, height=999)
        self.assertEqual(b.get_width(), LevelSpecs[Level.BEGINNER][0])
        self.assertEqual(b.get_height(), LevelSpecs[Level.BEGINNER][1])
        self.assertEqual(b.get_mines(), LevelSpecs[Level.BEGINNER][2])

    def matrixs_equals(self, m1, m2):
        """ apufunktio testaa onko matriisit samat """
        # onko edes samaa kokoa ?
        if len(m1)!=len(m2):
            return False
        for i in range(len(m1)):
            if m1[i] != m2[i]:
                return False
        return True
        
    
    def test_init_with_valid_board(self):
        """ Pelilaudan luominen onnistuu kelvollisella asettelulla """
        t = [
            [0,0,0,0],
            [0,0,0,1],
            [0,0,0,0]
        ]
        b = Board(board = t)
        self.assertEqual(b.get_width(), 4)
        self.assertEqual(b.get_height(), 3)
        self.assertEqual(b.get_mines(), 1)

    def test_init_board_is_masked_right(self):
        """ Luodun pelilaudan laatat ja peitteet on asetettu oikein """
        t = [
            [0,0,0,0],
            [0,0,0,1],
            [0,0,0,0]
        ]
        b = Board(board = t)
        self.assertEqual(b.get_width(), 4)
        self.assertEqual(b.get_height(), 3)
        self.assertEqual(b.get_mines(), 1)

        # testataan onko laatat tallennettu oikein luokkaan
        t = [
            [0,0,0],
            [0,0,0],
            [1,1,1],
            [1,9,1]
        ]
        self.assertTrue(self.matrixs_equals(b._Board__tiles, t))

        # onko maksit asetettu oikein
        t = [
            [12,12,12],
            [12,12,12],
            [12,12,12],
            [12,12,12]
        ]
        self.assertTrue(self.matrixs_equals(b._Board__masked, t))

    def test_get_view_and_guess(self):
        """ laudan näkymä on oikein senkin jälkeen kun on arvattu """
        
        t = [
            [0,0,1],
            [0,0,0],
            [0,0,0]
        ]
        b = Board(board=t)

        # Antaahan pelikenttä pelkkää maskia aluksi
        t = [
            [12,12,12],
            [12,12,12],
            [12,12,12]
        ]
        self.assertTrue(self.matrixs_equals(b.get_view(), t))

        # avataan yläkulma -> palatuu True
        self.assertTrue(b.guess(0,0))

        # onko näkymä nyt oikein
        t = [
            [0,0,0],
            [1,1,0],
            [12,1,0]
        ]
        self.assertTrue(self.matrixs_equals(b.get_view(), t))

        # avataan alakulma jossa miina -> palautuu False
        self.assertFalse(b.guess(2,0))

    def test_is_winning(self):
        """ toimiiko voittotilanteen tunnistus """
        b = Board(width=2, height=2)
        b._Board__tiles=[[1,9],[9,9]]
        b._Board__masked=[[12,12],[12,12]]
        self.assertFalse(b.is_winning())
        b._Board__masked=[[0,12],[12,12]]
        self.assertTrue(b.is_winning())
        b._Board__masked=[[0,0],[12,12]]
        self.assertFalse(b.is_winning())

    def test_error_conditions_in_guess(self):
        """ ruudun avaus alueen ulkopuolelta tai avatussa ruudussa ei onnistu"""
        b = Board(width=2, height=2)
        b._Board__tiles=[[1,9],[9,9]]
        self.assertFalse(b.guess(2,2))
        self.assertTrue(b.guess(0,0))
        self.assertFalse(b.guess(0,0))

    def test_get_mask(self):
        """ maski annetaan oikein """
        b = Board(width=2, height=2)
        b._Board__tiles=[[1,9],[9,9]]
        self.assertEqual(b.get_mask(0,0), 12)

    def test_flag(self):
        """ ruudun liputus toimii """
        b = Board(width=2, height=2)
        b._Board__tiles=[[1,9],[9,9]]
        self.assertEqual(b.get_mask(0,0), 12)
        self.assertTrue(b.flag(0,0))
        self.assertEqual(b.get_mask(0,0), 13)
        self.assertTrue(b.flag(0,0))
        self.assertEqual(b.get_mask(0,0), 10)
        self.assertTrue(b.flag(0,0))
        self.assertEqual(b.get_mask(0,0), 11)
        self.assertTrue(b.flag(0,0))
        self.assertEqual(b.get_mask(0,0), 12)
        self.assertTrue(b.flag(0,0,10))
        self.assertEqual(b.get_mask(0,0), 10)

    def test_flag_error_conditions(self):
        """ liputus ei onnistu jos avattu, alueen ulkopuolella, outo arvo """
        b = Board(width=2, height=2)
        b._Board__tiles=[[1,9],[9,9]]
        b._Board__masked[0][0]=6
        self.assertFalse(b.flag(0,0))
        b._Board__masked[0][0]=10
        self.assertFalse(b.flag(0,0,4))
        b._Board__masked[0][0]=0
        self.assertFalse(b.flag(0,0))
        self.assertFalse(b.flag(2,2))

    def test_reveal(self):
        """ paljastuksen jälkeen näkyy laatat sellaisenaan """
        b = Board(width=2, height=2)
        b.reveal()
        t = b._Board__tiles
        v = b.get_view()
        for i in range(2):
            self.assertEqual(v[i],t[i])

    def test_get_level(self):
        """ Testataan että nykyinen vaikeustaso palautuu oikein """
        b = Board(level=Level.INTERMEDIATE)
        self.assertIn(LevelSpecs[Level.INTERMEDIATE][3], b.get_level_name())
        b = Board(level=Level.INTERMEDIATE, width=25, mines=2)
        self.assertIn("Mukautettu", b.get_level_name())

    def test_board_invalid(self):
        """ Yritetään luoda peli kelvottomalla laudalla """
        b = Board(board=[[0,0,0,0,0],[0,0,0,1],[0,0,0,0,0]])
        self.assertIn(LevelSpecs[Level.BEGINNER][3], b.get_level_name())
        b = Board(board=[[0,0,0,0,0]])
        self.assertIn(LevelSpecs[Level.BEGINNER][3], b.get_level_name())
        b = Board(board=[[0,0,0,0],[0,0,0,0],[0,0,0,0]])
        self.assertIn(LevelSpecs[Level.BEGINNER][3], b.get_level_name())

