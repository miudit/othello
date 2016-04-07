# -*- coding:utf-8 -*-

import sys,os
sys.path.append(os.pardir)
import board
import AI
import random
import time

class Test:
  STAGES      = 60/4
  FEATURES    = 11
  PATTARNS    = [3**8]*3 + [3**4, 3**5, 3**6, 3**7, 3**8] + [3**10]*2 + [3**9]
  
  MIDTREEHEIGHT = 6
  LASTPHASE     = 44

  def __init__(self):
    self.__weight    = self.__loadWeights() # Logistelloパターン重み
    self.__board     = board.Board(False)
    self.__player    = [  AI.AI(  self.__board,
                                  0,
                                  None,
                                  self.__weight,
                                  Test.MIDTREEHEIGHT,
                                  Test.LASTPHASE,
                                  True
                                ),
                          AI.AI(  self.__board,
                                  1,
                                  None,
                                  self.__weight,
                                  Test.MIDTREEHEIGHT,
                                  Test.LASTPHASE,
                                  True
                                )
                        ]

  def init(self):
    self.__board.init()
    self.__turn         = 0
    self.__turnCounter  = 0
    self.__passedFlag   = False

  # <概要> AI同士で一試合プレイする
  def run(self):
    while 1:
      if self.__turnCounter == Test.LASTPHASE:
        break
      if self.__player[self.__turn%2].canPut():  # 置ける場所があればTrue
        self.__player[self.__turn%2].takeTurn(self.__turnCounter)
        self.__passedFlag = False
        self.__turnCounter += 1
      else:
        if self.__passedFlag:  # 二人ともパス->終了
          return
        self.__passedFlag = True
      self.__turn += 1

  # <概要> 重みをロードする
  def __loadWeights(self):
    weight = [[[0 for i in range(Test.PATTARNS[j])] for j in range(Test.FEATURES)] for k in range(Test.STAGES)]
    for stage in range(Test.STAGES):
      f = open("../wei/w"+str(stage)+".txt", "r")
      for feature, line in enumerate(f):
        value = line.split(' ')
        for pattern in range(Test.PATTARNS[feature]):
          weight[stage][feature][pattern] = float(value[pattern])
      f.close()
    return weight

def main():
  start = time.time()
  test = Test()
  test.init()
  test.run()
  t = time.time()-start
  print ("total: {0}".format(t)+"[sec]")

if __name__ == "__main__":
  main()
