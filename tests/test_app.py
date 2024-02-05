"""test_app.py - Testaa pelin suoritusta"""
# pylint: disable = missing-class-docstring, too-few-public-methods

from io import StringIO
import unittest
from unittest.mock import patch

from app import App

from tui import Action


class KbdTest:
    # pylint: disable = unused-argument, missing-function-docstring
    def __init__(self, actions):
        self.actions = actions
    def read_action(self):
        if self.actions:
            action, _, _ = self.actions.pop(0)
        else:
            action = Action.NOOP
        return action
    def read_matrix_action(self, w, h, x, y):
        return self.actions.pop(0) if self.actions else (Action.NOOP,x,y)


class TestAppClass(unittest.TestCase):
    """ Testit itse appille """
    class default_args:
        autoplay = 2
        intermediate = None
        expert = None
        board = None
        mines = None
        size = None
        bot = None
        quiet = None
        delay = None

    sure_win_board = [
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,1,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0]
            ]

    sure_lose_board = [
                [1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1],
                [1,1,1,1,0,1,1,1,1],
                [1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1]
            ]

    dssp_win_board = [
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,1,1,0,1,1,0,1,0]
            ]

    mini_board = [
                [0,0],
                [0,1]
            ]


    def test_run(self):
        """ Testataan että edes pyörähtää """
        app = App(self.default_args)
        app.run()
        del app

    def test_quit(self):
        """ Testataan Quittaamista """
        app = App()
        app.ui.kbd=KbdTest([
            (Action.QUIT,0,0),
            (Action.OPEN,0,0)
        ])
        app.run()
        del app

    def test_many_games(self):
        """ Varman voiton lauta palauttaa true """
        class args(self.default_args):
            quiet = True
        for _ in range(50):
            app = App(args)
            app.run()
            del app
        args.intermediate = True
        for _ in range(20):
            app = App(args)
            app.run()
            del app
        args.expert = True
        for _ in range(10):
            app = App(args)
            app.run()
            del app

    def test_sure_win(self):
        """ Varman voiton lauta palauttaa true """
        class args(self.default_args):
            board = self.sure_win_board
            quiet = True
        app = App(args)
        self.assertTrue(app.run())
        del app

    def test_dssp_win(self):
        """ Varman voiton lauta palauttaa true """
        class args(self.default_args):
            board = self.dssp_win_board
        app = App(args)
        self.assertTrue(app.run())
        del app

    def test_no_dssp_win_with_simple(self):
        """ Varman voiton lauta palauttaa true """
        class args(self.default_args):
            board = self.dssp_win_board
            quiet = True
            bot = 1
        while True:
            app = App(args)
            if not app.run():
                break
            del app

    def test_sure_lose(self):
        """ Varman häviön lauta palauttaa false """
        class args(self.default_args):
            board = self.sure_lose_board
        app = App(args)
        self.assertFalse(app.run())
        del app

    def test_custom_size(self):
        """ Varman häviön lauta palauttaa false """
        class args(self.default_args):
            size = (4, 4)
        with patch('sys.stdout', new = StringIO()) as captured:
            app = App(args)
            app.run()
            self.assertIn("Mukautettu (4x4", captured.getvalue())
            del app

    def test_sure_win_with_actions(self):
        """ Varman voiton lauta palauttaa true """
        class args(self.default_args):
            board = self.sure_win_board
            autoplay = 0
            bot = 0
        app = App(args)
        app.ui.kbd=KbdTest([
            (Action.SAFE,0,0),
            (Action.OPEN,0,0)
        ])
        self.assertTrue(app.run())
        del app

    def test_sure_lose_with_actions(self):
        """ Varman voiton lauta palauttaa true """
        class args(self.default_args):
            board = self.sure_lose_board
            autoplay = 0
        app = App(args)
        app.ui.kbd=KbdTest([
            (Action.FLAG,0,0),
            (Action.MINE,0,0),
            (Action.OPEN,0,0)
        ])
        self.assertFalse(app.run())
        del app

    def test_auto_play_hints(self):
        """ Vihjeiden automaattipelaaminen toimii """
        class args(self.default_args):
            board = self.dssp_win_board
            autoplay = 1
        app = App(args)
        app.ui.kbd=KbdTest([
            (Action.OPEN,0,0),
            (Action.HINT,0,0),
        ])
        self.assertTrue(app.run())
        del app

    def test_delay(self):
        """ Hidastus toimii """
        class args(self.default_args):
            board = self.dssp_win_board
            delay = 5
        app = App(args)
        with patch('time.sleep') as patched_sleep:
            self.assertTrue(app.run())
        del app
        patched_sleep.assert_called()

    def test_delay_can_be_off(self):
        """ Hidastus ei ole aina päälle """
        class args(self.default_args):
            board = self.dssp_win_board
        app = App(args)
        with patch('time.sleep') as patched_sleep:
            self.assertTrue(app.run())
        del app
        patched_sleep.assert_not_called()

    def test_botless_play(self):
        """ Hidastus toimii """
        class args(self.default_args):
            board = self.mini_board
            autoplay = 0
            delay = 50000
        app = App(args)
        app.ui.kbd=KbdTest([
            (Action.OPEN,0,0),
            (Action.HINT,0,0),
            (Action.OPEN,1,0),
            (Action.HINT,0,0),
            (Action.OPEN,0,1)
        ])
        self.assertTrue(app.run())
        del app
