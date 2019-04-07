from poker_hands import play_poker
import unittest


data = [
    ('5H 5C 6S 7S KD 2C 3S 8S 8D TD', 2),
    ('5D 8C 9S JS AC 2C 5C 7D 8S QH', 1),
    ('2D 9C AS AH AC 3D 6D 7D TD QD', 2),
    ('4D 6S 9H QH QC 3D 6D 7H QD QS', 1),
    ('2H 2D 4C 4D 4S 3C 3D 3S 9S 9D', 1),
    ('6D 7C 5D 5H 3S 5C JC 2H 5S 3D', 2),
    ('6C 4D 7S 7H 5S JC 6S 9H 4H JH', 2),
    ('JH 7C 9H 7H TC 5H 3D 6D 5D 4D', 1),
    ('5D 4D 3H 4H 6S 7C 7S AH QD TD', 2),
    ('3H JS 8S QD JH 3C 4H 6D 5C 3S', 1),
    ('7D 6C 8D 8H 5C JH 8S QD TH JD', 2),
]


class TestPokerHands(unittest.TestCase):

    def test_poker_games(self):
        for line in data:
            cards = line[0].split()
            player_1 = cards[:5]
            player_2 = cards[5:]
            game = play_poker([player_1, player_2])
            self.assertEquals(line[1] - 1, game)

if __name__ == '__main__':
    unittest.main()