from .hand import Hand
from .strategy import Strategy

class BasicStrategy(Strategy):

     def __init__(self):
          super().__init__()
          self.hard_totals = {
               21: {'2': 'stand', '3': 'stand', '4': 'stand', '5': 'stand', '6': 'stand',
                    '7': 'stand', '8': 'stand', '9': 'stand', '10': 'stand', 'Ace': 'stand'},
               20: {'2': 'stand', '3': 'stand', '4': 'stand', '5': 'stand', '6': 'stand',
                    '7': 'stand', '8': 'stand', '9': 'stand', '10': 'stand', 'Ace': 'stand'},
               19: {'2': 'stand', '3': 'stand', '4': 'stand', '5': 'stand', '6': 'stand',
                    '7': 'stand', '8': 'stand', '9': 'stand', '10': 'stand', 'Ace': 'stand'},
               18: {'2': 'stand', '3': 'stand', '4': 'stand', '5': 'stand', '6': 'stand',
                    '7': 'stand', '8': 'stand', '9': 'stand', '10': 'stand', 'Ace': 'stand'},
               17: {'2': 'stand', '3': 'stand', '4': 'stand', '5': 'stand', '6': 'stand',
                    '7': 'stand', '8': 'stand', '9': 'stand', '10': 'stand', 'Ace': 'stand'},
               16: {'2': 'stand', '3': 'stand', '4': 'stand', '5': 'stand', '6': 'stand',
                    '7': 'hit', '8': 'hit', '9': 'hit', '10': 'hit', 'Ace': 'hit'},
               15: {'2': 'stand', '3': 'stand', '4': 'stand', '5': 'stand', '6': 'stand',
                    '7': 'hit', '8': 'hit', '9': 'hit', '10': 'hit', 'Ace': 'hit'},
               14: {'2': 'stand', '3': 'stand', '4': 'stand', '5': 'stand', '6': 'stand',
                    '7': 'hit', '8': 'hit', '9': 'hit', '10': 'hit', 'Ace': 'hit'},
               13: {'2': 'stand', '3': 'stand', '4': 'stand', '5': 'stand', '6': 'stand',
                    '7': 'hit', '8': 'hit', '9': 'hit', '10': 'hit', 'Ace': 'hit'},
               12: {'2': 'hit', '3': 'hit', '4': 'stand', '5': 'stand', '6': 'stand',
                    '7': 'hit', '8': 'hit', '9': 'hit', '10': 'hit', 'Ace': 'hit'},
               11: {'2': 'double', '3': 'double', '4': 'double', '5': 'double', '6': 'double',
                    '7': 'double', '8': 'double', '9': 'double', '10': 'double', 'Ace': 'double'},
               10: {'2': 'double', '3': 'double', '4': 'double', '5': 'double', '6': 'double',
                    '7': 'double', '8': 'double', '9': 'double', '10': 'hit', 'Ace': 'hit'},
               9: {'2': 'hit', '3': 'double', '4': 'double', '5': 'double', '6': 'double',
                    '7': 'hit', '8': 'hit', '9': 'hit', '10': 'hit', 'Ace': 'hit'},
               8: {'2': 'hit', '3': 'hit', '4': 'hit', '5': 'hit', '6': 'hit',
                    '7': 'hit', '8': 'hit', '9': 'hit', '10': 'hit', 'Ace': 'hit'},
               7: {'2': 'hit', '3': 'hit', '4': 'hit', '5': 'hit', '6': 'hit',
                    '7': 'hit', '8': 'hit', '9': 'hit', '10': 'hit', 'Ace': 'hit'},
               6: {'2': 'hit', '3': 'hit', '4': 'hit', '5': 'hit', '6': 'hit',
                    '7': 'hit', '8': 'hit', '9': 'hit', '10': 'hit', 'Ace': 'hit'},
               5: {'2': 'hit', '3': 'hit', '4': 'hit', '5': 'hit', '6': 'hit',
                    '7': 'hit', '8': 'hit', '9': 'hit', '10': 'hit', 'Ace': 'hit'},
          }
          
          # Soft totals (with ace counted as 11)
          # Key: total value, Value: dict of dealer upcard -> action
          self.soft_totals = {
               21: {'2': 'stand', '3': 'stand', '4': 'stand', '5': 'stand', '6': 'stand',
                    '7': 'stand', '8': 'stand', '9': 'stand', '10': 'stand', 'Ace': 'stand'},
               20: {'2': 'stand', '3': 'stand', '4': 'stand', '5': 'stand', '6': 'stand',
                    '7': 'stand', '8': 'stand', '9': 'stand', '10': 'stand', 'Ace': 'stand'},
               19: {'2': 'stand', '3': 'stand', '4': 'stand', '5': 'stand', '6': 'double',
                    '7': 'stand', '8': 'stand', '9': 'stand', '10': 'stand', 'Ace': 'stand'},
               18: {'2': 'double', '3': 'double', '4': 'double', '5': 'double', '6': 'double',
                    '7': 'stand', '8': 'stand', '9': 'hit', '10': 'hit', 'Ace': 'hit'},
               17: {'2': 'hit', '3': 'double', '4': 'double', '5': 'double', '6': 'double',
                    '7': 'hit', '8': 'hit', '9': 'hit', '10': 'hit', 'Ace': 'hit'},
               16: {'2': 'hit', '3': 'hit', '4': 'double', '5': 'double', '6': 'double',
                    '7': 'hit', '8': 'hit', '9': 'hit', '10': 'hit', 'Ace': 'hit'},
               15: {'2': 'hit', '3': 'hit', '4': 'double', '5': 'double', '6': 'double',
                    '7': 'hit', '8': 'hit', '9': 'hit', '10': 'hit', 'Ace': 'hit'},
               14: {'2': 'hit', '3': 'hit', '4': 'double', '5': 'double', '6': 'double',
                    '7': 'hit', '8': 'hit', '9': 'hit', '10': 'hit', 'Ace': 'hit'},
               13: {'2': 'hit', '3': 'hit', '4': 'double', '5': 'double', '6': 'double',
                    '7': 'hit', '8': 'hit', '9': 'hit', '10': 'hit', 'Ace': 'hit'},
          }
          
          # Pair splitting
          # Key: card rank, Value: dict of dealer upcard -> action
          self.pairs = {
               'Ace': {'2': 'split', '3': 'split', '4': 'split', '5': 'split', '6': 'split',
                         '7': 'split', '8': 'split', '9': 'split', '10': 'split', 'Ace': 'split'},
               '10': {'2': 'stand', '3': 'stand', '4': 'stand', '5': 'stand', '6': 'stand',
                    '7': 'stand', '8': 'stand', '9': 'stand', '10': 'stand', 'Ace': 'stand'},
               '9': {'2': 'split', '3': 'split', '4': 'split', '5': 'split', '6': 'split',
                    '7': 'stand', '8': 'split', '9': 'split', '10': 'stand', 'Ace': 'stand'},
               '8': {'2': 'split', '3': 'split', '4': 'split', '5': 'split', '6': 'split',
                    '7': 'split', '8': 'split', '9': 'split', '10': 'split', 'Ace': 'split'},
               '7': {'2': 'split', '3': 'split', '4': 'split', '5': 'split', '6': 'split',
                    '7': 'split', '8': 'hit', '9': 'hit', '10': 'hit', 'Ace': 'hit'},
               '6': {'2': 'split', '3': 'split', '4': 'split', '5': 'split', '6': 'split',
                    '7': 'hit', '8': 'hit', '9': 'hit', '10': 'hit', 'Ace': 'hit'},
               '5': {'2': 'double', '3': 'double', '4': 'double', '5': 'double', '6': 'double',
                    '7': 'double', '8': 'double', '9': 'double', '10': 'hit', 'Ace': 'hit'},
               '4': {'2': 'hit', '3': 'hit', '4': 'hit', '5': 'split', '6': 'split',
                    '7': 'hit', '8': 'hit', '9': 'hit', '10': 'hit', 'Ace': 'hit'},
               '3': {'2': 'split', '3': 'split', '4': 'split', '5': 'split', '6': 'split',
                    '7': 'split', '8': 'hit', '9': 'hit', '10': 'hit', 'Ace': 'hit'},
               '2': {'2': 'split', '3': 'split', '4': 'split', '5': 'split', '6': 'split',
                    '7': 'split', '8': 'hit', '9': 'hit', '10': 'hit', 'Ace': 'hit'},
          }


     def get_action(self, hand: Hand, dealer_up_card_rank: str, can_split_or_double: bool) -> str:
          dealer_up_card_rank = self._normalize_rank(dealer_up_card_rank)

          if can_split_or_double and hand.is_pair(): 
               return self.pairs[self._normalize_rank(hand.cards[0].rank)][dealer_up_card_rank]
          
          
          if hand.is_soft_hand():
               #Soft hand
               #Address the possibilt of can't split aces
               if hand.get_value() == 12:
                    return 'hit'
               action = self.soft_totals[hand.get_value()][dealer_up_card_rank]
          
          else:
               #Address the possibility of can't split 2's
               if hand.get_value() == 4:
                    return 'hit'
               action = self.hard_totals[hand.get_value()][dealer_up_card_rank]

          if action == 'double' and not can_split_or_double:
               action = 'hit'
     
          return action
     
     def _normalize_rank(self, card_rank) -> str:
          if card_rank in ['Jack', 'Queen', 'King']:
               return '10'
          else:
               return card_rank


            

