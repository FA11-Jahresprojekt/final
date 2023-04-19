import sqlite3
from Database import Database

testDataBase = Database.getInstance()

# testDataBase.registerNewPerson()
# testDataBase.registerNewGame()
# testDataBase.getPersonByUserName()
# testDataBase.getTopPlayersForGameAndDifficulty()
# testDataBase.getGameHistoryForChosenPlayer()
# testDataBase.getGamesSummaryForGameAndDifficultyAndPlayerID()



# print(testDataBase.registerNewPerson("Tester4", 123))

# (pid, gameName, difficulty, outcome, destroyedPawns):
# Bauernschach difficulty 1
testDataBase.registerNewGame(1, "Bauernschach", 1, "won", 3)
testDataBase.registerNewGame(1, "Bauernschach", 1, "cancelled", 5)
testDataBase.registerNewGame(1, "Bauernschach", 1, "lost", 1)
# difficulty 2
testDataBase.registerNewGame(1, "Bauernschach", 2, "cancelled", 3)
testDataBase.registerNewGame(1, "Bauernschach", 2, "won", 5)
testDataBase.registerNewGame(1, "Bauernschach", 2, "lost", 1)
# difficulty 3
testDataBase.registerNewGame(1, "Bauernschach", 3, "lost", 3)
testDataBase.registerNewGame(1, "Bauernschach", 3, "won", 5)
testDataBase.registerNewGame(1, "Bauernschach", 3, "cancelled", 1)
# difficulty 4
testDataBase.registerNewGame(1, "Bauernschach", 4, "cancelled", 3)
testDataBase.registerNewGame(1, "Bauernschach", 4, "lost", 5)
testDataBase.registerNewGame(1, "Bauernschach", 4, "won", 1)
# difficulty 5
testDataBase.registerNewGame(1, "Bauernschach", 5, "cancelled", 3)
testDataBase.registerNewGame(1, "Bauernschach", 5, "won", 5)
testDataBase.registerNewGame(1, "Bauernschach", 5, "lost", 1)

# Dame difficulty 1
testDataBase.registerNewGame(1, "Dame", 1, "won", 1)
testDataBase.registerNewGame(1, "Dame", 1, "cancelled", 2)
testDataBase.registerNewGame(1, "Dame", 1, "lost", 3)

# difficulty 2
testDataBase.registerNewGame(1, "Dame", 2, "cancelled", 3)
testDataBase.registerNewGame(1, "Dame", 2, "won", 5)
testDataBase.registerNewGame(1, "Dame", 2, "lost", 1)

# difficulty 3
testDataBase.registerNewGame(1, "Dame", 3, "lost", 4)
testDataBase.registerNewGame(1, "Dame", 3, "won", 6)
testDataBase.registerNewGame(1, "Dame", 3, "cancelled", 5)

# difficulty 4
testDataBase.registerNewGame(1, "Dame", 4, "cancelled", 0)
testDataBase.registerNewGame(1, "Dame", 4, "lost", 1)
testDataBase.registerNewGame(1, "Dame", 4, "won", 2)

# difficulty 5
testDataBase.registerNewGame(1, "Dame", 5, "cancelled", 3)
testDataBase.registerNewGame(1, "Dame", 5, "won", 2)
testDataBase.registerNewGame(1, "Dame", 5, "lost", 1)

testDataBase.registerNewGame(1, "Bauernschach", 4, "cancelled", 3)
testDataBase.registerNewGame(1, "Bauernschach", 3, "cancelled", 3)
testDataBase.registerNewGame(1, "Bauernschach", 2, "won", 3)
testDataBase.registerNewGame(1, "Bauernschach", 1, "lost", 3)
# print(testDataBase.testSelectRankingData())
# print(testDataBase.getTopPlayersForGameAndDifficulty("Bauernschach", 5, 2))
# print(testDataBase.getTopPlayersForGameAndDifficulty("Bauernschach", 3, 5))
# print(testDataBase.getTopPlayersForGameAndDifficulty("Dame", 5, 2))
# print(testDataBase.getTopPlayersForGameAndDifficulty("Dame", 3, 2))
#
# print(testDataBase.getGamesSummaryForGameAndDifficultyAndPlayerID("Bauernschach", 3, 1))
#
# print(testDataBase.getGameHistoryForChosenPlayer(1))
#
# print(hash(1))
# print(hash(str(1)))
# print(hash(int(str(1))))
# print(hash("Hallo"))
# print(hash(20))
# print(hash(str(20)))
# print(hash(int(str(20))))