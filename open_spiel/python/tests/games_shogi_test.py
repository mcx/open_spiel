# Copyright 2026 DeepMind Technologies Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for the game-specific functions for shogi."""
import sys
from absl import flags
from absl.testing import absltest
from absl.testing import parameterized

import numpy as np
import pyspiel
shogi = pyspiel.shogi

def apply_legal(state, move):
    action = state.parse_move_to_action(move)
    if action in state.legal_actions():
        state.apply_action(action)
    else:
        raise ValueError()

class GamesShogiTest(parameterized.TestCase):
  def dtest_bindings_sim(self):
    game = pyspiel.load_game("shogi")
    state = game.new_initial_state()
    board = None
    count = 0

    while count < 200 and not state.is_terminal():
      # print(state)
      count += 1
      legal_actions = state.legal_actions()
      board = state.board()
      for action in legal_actions:
        move = shogi.action_to_move(action, board)
        # print("move", move.to_string())
        sys.stdout.flush()
        # Now do the reverse mapping from both string representations to check
        # that they correspond to this action.
        #print(move.to_string())
        action_from_move = state.parse_move_to_action(move.to_string())
        self.assertEqual(action, action_from_move)
      action = np.random.choice(legal_actions)
      board = state.board()
      move = shogi.action_to_move(action, board)
      print(move.to_string())
      state.apply_action(action)
      print(state)

    #print(board.to_unicode_string())
    #print(board.debug_string())
    print("Moves history:")
    print(" ".join([move.to_string() for move in state.moves_history()]))
    if count < 200:
      self.assertTrue(state.is_terminal())
    print("terminal?", state.is_terminal())

  def dtest_kma(self):
    game = pyspiel.load_game("shogi")
    state = game.new_initial_state()
    board = state.board()
    for action in state.legal_actions():
       move = shogi.action_to_move(action, board)
       print(move.to_string())

  def test_repeat(self):
      """Repeat without perpetual check is a draw."""
      game = pyspiel.load_game("shogi")
      state = game.new_initial_state()
      for ii in range(4):
          apply_legal(state, '2h1h')
          if state.is_terminal():
              break
          apply_legal(state, '8b9b')
          if state.is_terminal():
              break
          apply_legal(state, '1h2h')
          if state.is_terminal():
              break
          apply_legal(state, '9b8b')
          if state.is_terminal():
              break
      self.assertTrue(state.is_terminal())
      self.assertEqual(state.returns(), [0, 0])
      "Repeat with perpetual check is a loss for the checking player." 
      state = game.new_initial_state("lnsg2+R+Pl/4k4/p1ppppp1p/9/9/9/P1PPPPP1P/+R8/+pNSGKGSNL b PNSGBplb 14")
      for ii in range(4):
          apply_legal(state, '3a3b')
          if state.is_terminal():
              break
          apply_legal(state, '5b5a')
          if state.is_terminal():
              break
          apply_legal(state, '3b3a')
          if state.is_terminal():
              break
          apply_legal(state, '5a5b')
          if state.is_terminal():
              break
      self.assertTrue(state.is_terminal())
      self.assertEqual(state.returns(), [-1.0, 1.0])

if __name__ == "__main__":
  absltest.main()


