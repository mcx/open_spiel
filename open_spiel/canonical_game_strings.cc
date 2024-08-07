// Copyright 2021 DeepMind Technologies Limited
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include "open_spiel/canonical_game_strings.h"

#include <string>

#include "open_spiel/abseil-cpp/absl/strings/str_format.h"

namespace open_spiel {

std::string HunlGameString(const std::string &betting_abstraction) {
  return absl::StrFormat(
      "universal_poker(betting=nolimit,numPlayers=2,numRounds=4,blind=100 50,"
      "firstPlayer=2 1 1 1,numSuits=4,numRanks=13,numHoleCards=2,"
      "numBoardCards=0 3 1 1,stack=20000 20000,bettingAbstraction=%s)",
      betting_abstraction);
}

// Note: Limit games do not support the 'stack' input.
std::string HulhGameString(const std::string &betting_abstraction) {
  return absl::StrFormat(
      "universal_poker(betting=limit,numPlayers=2,numRounds=4,blind=10 5,"
      "firstPlayer=2 1,numSuits=4,numRanks=13,numHoleCards=2,"
      "numBoardCards=0 3 1 1,raiseSize=10 10 20 20,"
      "maxRaises=3 4 4 4,bettingAbstraction=%s)",
      betting_abstraction);
}

std::string Multiway3max_1_2GameString(const std::string &betting_abstraction,
                                       int sb_stack, int bb_stack,
                                       int dealer_stack) {
  return absl::StrFormat(
      "universal_poker(betting=nolimit,numPlayers=3,numRounds=4,blind=1 2 0,"
      // Standard turn order: D->SB->BB, then SB->BB->D
      "firstPlayer=3 1 1 1,numSuits=4,numRanks=13,numHoleCards=2,"
      "numBoardCards=0 3 1 1,stack=%i %i %i,bettingAbstraction=%s)",
      sb_stack, bb_stack, dealer_stack, betting_abstraction);
}

std::string Multiway6max_1_2GameString(const std::string &betting_abstraction,
                                       int buy_in) {
  return absl::StrFormat(
      "universal_poker(betting=nolimit,numPlayers=6,numRounds=4,"
      "blind=1 2 0 0 0 0,"
      // Standard turn order: UTG->...->D->SB->BB, then SB->BB->UTG->...->D
      "firstPlayer=3 1 1 1,numSuits=4,numRanks=13,numHoleCards=2,"
      "numBoardCards=0 3 1 1,stack=%i %i %i %i %i %i,bettingAbstraction=%s)",
      buy_in, buy_in, buy_in, buy_in, buy_in, buy_in, betting_abstraction);
}

std::string TurnBasedGoofspielGameString(int num_cards) {
  return absl::StrFormat(
      "turn_based_simultaneous_game(game=goofspiel("
      "imp_info=true,num_cards=%i,players=2,"
      "points_order=descending,returns_type=win_loss))",
      num_cards);
}

}  // namespace open_spiel
