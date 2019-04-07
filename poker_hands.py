import sys


FACE_CARDS = {
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14
}


def index_of(d, value):
    return list(d.keys())[list(d.values()).index(value)]


def score_hand(hand):
    straight = False
    sorted_hand = {
        'C': [],
        'D': [],
        'H': [],
        'S': [],
    }
    kinds = {}
    suites = set()
    raw_values = []
    for card in hand:
        face_value = card[0]
        if face_value in FACE_CARDS:
            value = FACE_CARDS[face_value]
        else:
            value = int(face_value)
        if value not in kinds:
            kinds[value] = 0
        kinds[value] += 1
        raw_values.append(value)
        suites.add(card[1])
        sorted_hand[card[1]].append(value)
    raw_values.sort()
    value_range = xrange(raw_values[0], raw_values[-1] + 1)
    gaps = sorted(set(value_range).difference(raw_values))
    if gaps and 14 in raw_values:
        aces_low = [v for v in raw_values]
        aces_low.remove(14)
        aces_low.insert(0, 1)
        value_range = xrange(1, aces_low[-1] + 1)
        gaps = sorted(set(value_range).difference(aces_low))
        if not gaps:
            raw_values = aces_low
    count_of_a_kind = max(kinds.values())
    if not gaps and count_of_a_kind == 1:
        straight = True
    multiplier = 10
    score = 0
    other_cards = []
    if len(suites) == 1:  # flush
        score = sum(kinds.keys())
        if straight and raw_values[0] == 10:
            multiplier = 5000000  # Royal Flush
        elif straight:
            # Straight flush score ranges from 60M - 180M
            multiplier = 3000000
        else:
            # Flush score ranges from 350k-1.05M
            multiplier = 17500
    elif straight:
        # Straight score ranges from 75k-300k (15-60)
        score = sum(kinds.keys())
        multiplier = 5000
    elif count_of_a_kind == 4:
        # Four of a kind score ranges from 8M - 56M
        high_card = index_of(kinds, 4)
        score = high_card * 4
        multiplier = 1000000
        other_cards = [v for v in raw_values if v != high_card]
    elif count_of_a_kind == 3:
        high_card = index_of(kinds, 3)
        score += high_card * 3
        if 2 in kinds.values():
            # Full house score ranges from 1.2M-6.8M
            multiplier = 100000
        else:
            # Three of a kind score ranges from 7200-50400 (6-42)
            multiplier = 1200
        other_cards = [v for v in raw_values if v != high_card]
    elif count_of_a_kind == 2:
        if kinds.values().count(2) == 2:
            score = 0
            for card, count in kinds.iteritems():
                if count == 2:
                    score += card * 2
                else:
                    other_cards = [card]
            # Two pair ranges score from 1200 - 6480 (10-54)
            multiplier = 120
        else:
            # Single pair ranges score from 160-1120 (4-28)
            high_card = index_of(kinds, 2)
            score = high_card * 2
            multiplier = 40
            other_cards = [v for v in raw_values if v != high_card]
    else:
        # High card score ranges from 70 - 140 (7-14)
        score = raw_values[-1]
        multiplier = 10
        other_cards = raw_values[:-1]
    return score * multiplier, other_cards


def play_poker(players):
    game = []
    winning_score = 0
    winner = None
    for p, hand in enumerate(players):
        score = score_hand(hand)
        if score[0] == winning_score:
            for c, other_card in enumerate(game[winner][1]):
                if score[1][c] > other_card:
                    winner = p
                    break
        if score[0] > winning_score:
            winning_score = score[0]
            winner = p
        game.append(score)
    return winner


def main(file_name):
    with open(file_name) as f:
        lines = f.readlines()
        for line in lines:
            cards = line.split()
            player_1 = cards[:5]
            player_2 = cards[5:]
            game = play_poker([player_1, player_2])
            if game == 0:
                print "Player 1 wins :: ", player_1, "vs", player_2
            if game == 1:
                print "Player 2 wins :: ", player_1, "vs", player_2


if __name__ == '__main__':
    file_name = sys.argv[1:][0]
    main(file_name)
