import pathlib
import functools
import re
import heapq
import itertools
import collections


def get_filepath(file_name):
    """Returns the full path of the file_name"""
    return pathlib.Path(__file__).parent.joinpath(file_name).resolve()


def solve_day_22_part_ab():
    import copy
    import random

    CAST_ANY_TIME = -1

    def boss_turn(timer, player, boss):
      MINIMUM_DAMAGE = 1 
      player_damage = max(boss_damage - player['armor'], MINIMUM_DAMAGE)
      player['hit_points'] -= player_damage
      return CAST_ANY_TIME
 
    def magic_missle(timer, player, boss):
      boss['hit_points'] -= 4
      return CAST_ANY_TIME
      
    def drain(timer, player, boss):
      boss['hit_points'] -= 2
      player['hit_points'] += 2
      return CAST_ANY_TIME
      
    def shield(timer, player, boss):
      player['armor'] += 7
      until = timer + 5
      def apply_effect(timer, player, boss):
        should_continue= timer <= until
        if not should_continue:
          player['armor'] -= 7
        return should_continue 
      player['effects'].append(apply_effect)
      return until 

    def poison(timer, player, boss):
      until = timer + 5 
      def apply_effect(timer, player, boss):
        boss['hit_points'] -= 3
        return timer <= until
      player['effects'].append(apply_effect)
      return until 

    def recharge(timer, player, boss):
      until = timer + 4
      def apply_effect(timer, player, boss):
        player['mana'] += 101
        return timer <= until
      player['effects'].append(apply_effect)
      return until 

    boss_hit_points= 51
    boss_damage= 9

    default_spells = [(CAST_ANY_TIME, 53, magic_missle), (CAST_ANY_TIME, 73, drain),
                      (CAST_ANY_TIME, 113, shield), (CAST_ANY_TIME, 173, poison),
                      (CAST_ANY_TIME, 229, recharge) ]

    player = {'hit_points': 50, 'mana':500, 'spells': default_spells, 'effects': [], 'armor': 0}
    boss = {'hit_points': boss_hit_points}
    world = {"timer": 1, "player": player, "boss": boss}


    def apply_effects(world, effects) -> list:
        new_effects = []
        for effect in effects:
          result = effect(**world)
          if result:
            new_effects.append(effect)
        return new_effects

    def default_turn_effect(timer, player, boss):
      pass

    def hard_mode(timer, player, boss):
      #if timer % 2 == 1:
      player["hit_points"] -= 1

    def search(world, difficulty=default_turn_effect):
      moves = [(0 , world)]
      while moves:
        mana_cost, best_world = heapq.heappop(moves) 
        best_world = copy.deepcopy(best_world)
  
        
        difficulty(**best_world)

        if  best_world["player"]["hit_points"] <= 0:
          continue

        if  best_world["boss"]["hit_points"] < 0:
          return mana_cost



        best_world["player"]["effects"] = apply_effects(best_world, best_world["player"]["effects"])
  
        is_boss_turn = (best_world["timer"] % 2) == 0
        best_world["timer"] += 1
  
        if is_boss_turn:
          boss_turn(**best_world)
          if best_world["player"]["hit_points"] >= 0:
            heapq.heappush(moves, (mana_cost, best_world))
        else:
          for idx, (until, spell_cost, pick) in enumerate(best_world["player"]["spells"]):
            if until <= best_world["timer"] and spell_cost < best_world["player"]["mana"]:
              new_world = copy.deepcopy(best_world)
              new_until = pick(**new_world)
              new_world["player"]["spells"][idx] = (new_until, spell_cost, pick)
              new_world["player"]['mana'] -= spell_cost
  
              new_mana_cost = mana_cost + spell_cost
              new_mana_cost += random.random() / 1e3 # Make every value unique 
              if new_world["boss"]["hit_points"] <= 0:
                return new_mana_cost
              else:
                heapq.heappush(moves, (new_mana_cost, new_world))
       
    return search(world), search(world, hard_mode)
  

def solve():

    day22_a, day22_b = solve_day_22_part_ab()
    print(f"Day22a: Winning takes {int(day22_a)} mana")
    print(f"Day22b: On hard mode winning takes {int(day22_b)} mana")

if __name__ == "__main__":
    solve()