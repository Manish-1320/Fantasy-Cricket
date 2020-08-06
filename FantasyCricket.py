# All The Rquired Classes Have Been Copied In One File So That Objects Of Different Classes
# That Do Not Have Any Relation Can Share The Data Using Global Variables.

from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3

# Global Data For Evaluate Team Dialog Box.
matches_count = {}

# Class For Evaluate Team Dialog Box.
class Ui_evaluateTeamDialog(object):
    def setupUi(self, evaluateTeamDialog):
        evaluateTeamDialog.setObjectName("evaluateTeamDialog")
        evaluateTeamDialog.resize(480, 320)
        self.gridLayout_2 = QtWidgets.QGridLayout(evaluateTeamDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.titleLabel = QtWidgets.QLabel(evaluateTeamDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.titleLabel.setFont(font)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName("titleLabel")
        self.gridLayout_2.addWidget(self.titleLabel, 0, 0, 1, 4)
        self.horizontalLayout1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout1.setObjectName("horizontalLayout1")
        self.selectTeam = QtWidgets.QComboBox(evaluateTeamDialog)
        self.selectTeam.setObjectName("selectTeam")
        self.selectTeam.addItem("")
        self.horizontalLayout1.addWidget(self.selectTeam)
        self.selectMatch = QtWidgets.QComboBox(evaluateTeamDialog)
        self.selectMatch.setObjectName("selectMatch")
        self.selectMatch.addItem("")
        self.horizontalLayout1.addWidget(self.selectMatch)
        self.gridLayout_2.addLayout(self.horizontalLayout1, 1, 0, 1, 4)
        self.line0 = QtWidgets.QFrame(evaluateTeamDialog)
        self.line0.setFrameShape(QtWidgets.QFrame.HLine)
        self.line0.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line0.setObjectName("line0")
        self.gridLayout_2.addWidget(self.line0, 2, 0, 2, 4)
        self.horizontalLayout2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout2.setObjectName("horizontalLayout2")
        self.playerList = QtWidgets.QListWidget(evaluateTeamDialog)
        self.playerList.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.playerList.setObjectName("playerList")
        self.horizontalLayout2.addWidget(self.playerList)
        self.playerPoints = QtWidgets.QListWidget(evaluateTeamDialog)
        self.playerPoints.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.playerPoints.setObjectName("playerPoints")
        self.horizontalLayout2.addWidget(self.playerPoints)
        self.gridLayout_2.addLayout(self.horizontalLayout2, 5, 0, 1, 4)
        self.pointsLabel = QtWidgets.QLabel(evaluateTeamDialog)
        self.pointsLabel.setObjectName("pointsLabel")
        self.gridLayout_2.addWidget(self.pointsLabel, 4, 2, 1, 1)
        self.scoreLabel = QtWidgets.QLabel(evaluateTeamDialog)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.scoreLabel.setFont(font)
        self.scoreLabel.setText("")
        self.scoreLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.scoreLabel.setObjectName("scoreLabel")
        self.gridLayout_2.addWidget(self.scoreLabel, 4, 3, 1, 1)
        self.playersLabel = QtWidgets.QLabel(evaluateTeamDialog)
        self.playersLabel.setObjectName("playersLabel")
        self.gridLayout_2.addWidget(self.playersLabel, 4, 0, 1, 1)
        self.horizontalLayout0 = QtWidgets.QHBoxLayout()
        self.horizontalLayout0.setObjectName("horizontalLayout0")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout0.addItem(spacerItem)
        self.calculateScore = QtWidgets.QPushButton(evaluateTeamDialog)
        self.calculateScore.setObjectName("calculateScore")
        self.horizontalLayout0.addWidget(self.calculateScore)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout0.addItem(spacerItem1)
        self.gridLayout_2.addLayout(self.horizontalLayout0, 6, 0, 1, 4)
        self.retranslateUi(evaluateTeamDialog)
        QtCore.QMetaObject.connectSlotsByName(evaluateTeamDialog)

        # Filling The Select Team Combo Box.
        global matches_count

        connection = sqlite3.connect('FantasyCricket.db')
        cursor = connection.cursor()
        sql_query = '''select team_name, count(match_num) from teams group by team_name;'''
        result = cursor.execute(sql_query)
        team_names = result.fetchall()
        cursor.close()
        connection.close()

        for team, count in team_names:
            matches_count[team] = count
            self.selectTeam.addItem(team)

        # Adding Event Handling To The Select Team Combo Box.
        self.selectTeam.currentTextChanged.connect(self.fillNewValues)

        # Adding Event Handling To The Evaluate Score team
        self.calculateScore.clicked.connect(self.findPlayerScores)

        # Additional Functionality That Matches Player Name With Their Scores And Vice Versa.
        self.playerList.itemClicked.connect(lambda:self.playerPoints.setCurrentRow(
            self.playerList.currentRow()))
        self.playerPoints.itemClicked.connect(lambda: self.playerList.setCurrentRow(
            self.playerPoints.currentRow()))

    def findPlayerScores(self):
        self.playerList.clear()
        self.playerPoints.clear()
        team_name = self.selectTeam.currentText()
        if team_name == 'Select Team':
            alert = QtWidgets.QMessageBox()
            alert.setIcon(QtWidgets.QMessageBox.Critical)
            alert.setWindowTitle('Select Team')
            alert.setStandardButtons(QtWidgets.QMessageBox.Ok)
            alert.setText('No Team Was Selected.')
            alert.exec_()
        else:
            match_num = self.selectMatch.currentText()
            match_num = int(match_num[7:])

            #Connecting To Database To Find Out Players And Their Scores.
            connection = sqlite3.connect('FantasyCricket.db')
            cursor = connection.cursor()
            sql_query = '''select players from teams where team_name = ? and match_num = ?;'''
            result = cursor.execute(sql_query, (team_name, match_num))
            player_data = result.fetchall()
            player_data = player_data[0][0].strip().split(',')
            score = 0
            for player in player_data:
                sql_query = '''select * from match where player = ?;'''
                result = cursor.execute(sql_query, (player,))
                stats = result.fetchall()
                player_score = self.findScore(stats)
                score += player_score
                self.playerPoints.addItem(str(player_score))
                self.playerList.addItem(player)
            self.scoreLabel.setText(str(score))
            cursor.close()
            connection.close()

    def findScore(self, player_stats):
        # Extracting The Information From The Provided Stats
        player_stats = player_stats[0]
        player = player_stats[0]
        scored = int(player_stats[1])
        faced = int(player_stats[2])
        fours = int(player_stats[3])
        sixes = int(player_stats[4])
        bowled = int(player_stats[5])
        maiden = int(player_stats[6])
        given = int(player_stats[7])
        wickets = int(player_stats[8])
        catches = int(player_stats[9])
        stumping = int(player_stats[10])
        run_out = int(player_stats[11])

        # Evaluating Player Score.
        player_score = 0

        # Fielding Score.
        player_score += (catches + run_out + stumping) * 10

        # Bowling Score.
        player_score += wickets * 10
        if wickets >= 3:
            player_score += 5
        if wickets >= 5:
            player_score += 10

        try:
            economy_rate = (given/bowled) * 6
        except ZeroDivisionError:
            pass
        else:
            if economy_rate >= 3.5 and economy_rate <= 4.5:
                player_score += 4
            elif economy_rate >= 2:
                player_score += 7
            else:
                player_score += 10

        player_score += maiden * 10

        # Batting Score.
        player_score += scored // 2

        if scored >= 50:
            player_score += 5
        if scored >= 100:
            player_score += 10
        try:
            strike_rate = (scored/faced) * 100
        except ZeroDivisionError:
            pass
        else:
            if strike_rate >= 80 and strike_rate <= 100:
                player_score += 2
            if strike_rate > 100:
                player_score += 4

        player_score += fours
        player_score += sixes * 2

        return player_score

    def fillNewValues(self):
        global matches_count
        text = self.selectTeam.currentText()
        text.strip()
        if text != 'Select Team':
            limit = matches_count[text]
            self.selectMatch.clear()
            for i in range(1, limit + 1):
                self.selectMatch.addItem('Match: {}'.format(i))
        else:
            self.selectMatch.clear()
            self.selectMatch.addItem('Select Match')

    def retranslateUi(self, evaluateTeamDialog):
        _translate = QtCore.QCoreApplication.translate
        evaluateTeamDialog.setWindowTitle(_translate("evaluateTeamDialog", "Evaluate Team"))
        self.titleLabel.setText(_translate("evaluateTeamDialog", "EVALUATE THE PERFORMACE OF YOUR FANTASY TEAM"))
        self.selectTeam.setCurrentText(_translate("evaluateTeamDialog", "Select Team"))
        self.selectTeam.setItemText(0, _translate("evaluateTeamDialog", "Select Team"))
        self.selectMatch.setItemText(0, _translate("evaluateTeamDialog", "Select Match"))
        self.pointsLabel.setText(_translate("evaluateTeamDialog", "POINTS:"))
        self.playersLabel.setText(_translate("evaluateTeamDialog", "PLAYERS"))
        self.calculateScore.setText(_translate("evaluateTeamDialog", "CALCULATE SCORE"))


# Global Data For New Team Dialog Box.
teamName = None

# Class For New Team Dialog Box.
class Ui_newTeamDialog(object):
    def setupUi(self, newTeamDialog):
        newTeamDialog.setObjectName("newTeamDialog")
        newTeamDialog.resize(300, 70)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(newTeamDialog.sizePolicy().hasHeightForWidth())
        newTeamDialog.setSizePolicy(sizePolicy)
        self.buttonBox = QtWidgets.QDialogButtonBox(newTeamDialog)
        self.buttonBox.setGeometry(QtCore.QRect(220, 9, 75, 52))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.infoLabel = QtWidgets.QLabel(newTeamDialog)
        self.infoLabel.setGeometry(QtCore.QRect(10, 10, 201, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.infoLabel.setFont(font)
        self.infoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.infoLabel.setObjectName("infoLabel")
        self.nameText = QtWidgets.QLineEdit(newTeamDialog)
        self.nameText.setGeometry(QtCore.QRect(10, 40, 201, 20))
        self.nameText.setObjectName("nameText")

        self.retranslateUi(newTeamDialog)
        self.buttonBox.accepted.connect(lambda: self.setTeamName(newTeamDialog))
        self.buttonBox.rejected.connect(newTeamDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(newTeamDialog)

    def setTeamName(self, newTeamDialog):
        global teamName
        temp = self.nameText.text()
        if temp:
            teamName = temp
            newTeamDialog.accept()
        else:
            alert = QtWidgets.QMessageBox()
            alert.setIcon(QtWidgets.QMessageBox.Critical)
            alert.setText('Empty Team Name!')
            alert.setWindowTitle("Alert")
            alert.setStandardButtons(QtWidgets.QMessageBox.Ok)
            alert.exec_()

    def retranslateUi(self, newTeamDialog):
        _translate = QtCore.QCoreApplication.translate
        newTeamDialog.setWindowTitle(_translate("newTeamDialog", "New Team"))
        self.infoLabel.setText(_translate("newTeamDialog", "Enter Team Name In Provided Space"))


# Global Data For Open Team Dialog Box.
open_team_name = None
open_team_match = None

# Class For Open Team Dialog Box.
class Ui_openTeamDialog(object):
    def setupUi(self, openTeamDialog):
        openTeamDialog.setObjectName("openTeamDialog")
        openTeamDialog.resize(300, 70)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(openTeamDialog.sizePolicy().hasHeightForWidth())
        openTeamDialog.setSizePolicy(sizePolicy)
        self.buttonBox = QtWidgets.QDialogButtonBox(openTeamDialog)
        self.buttonBox.setGeometry(QtCore.QRect(220, 9, 75, 52))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.selectTeam = QtWidgets.QComboBox(openTeamDialog)
        self.selectTeam.setGeometry(QtCore.QRect(10, 40, 201, 20))
        self.selectTeam.setObjectName("selectTeam")
        self.selectTeam.addItem("")
        self.infoLabel = QtWidgets.QLabel(openTeamDialog)
        self.infoLabel.setGeometry(QtCore.QRect(10, 10, 201, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.infoLabel.setFont(font)
        self.infoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.infoLabel.setObjectName("infoLabel")

        self.retranslateUi(openTeamDialog)
        self.buttonBox.accepted.connect(lambda: self.acceptAction(openTeamDialog))
        self.buttonBox.rejected.connect(openTeamDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(openTeamDialog)

        # Adding Saved Team Data To The Combo Box.
        connection = sqlite3.connect('FantasyCricket.db')
        cursor = connection.cursor()
        sql_query = '''select * from teams;'''
        result = cursor.execute(sql_query)
        team_data = result.fetchall()
        cursor.close()
        connection.close()

        for match_id, team_name, players, match_num in team_data:
            item = team_name + ' | Match: ' + str(match_num).rjust(3, '0')
            self.selectTeam.addItem(item)

    def acceptAction(self, openTeamDialog):
        global open_team_name
        global open_team_match
        item = self.selectTeam.currentText()
        if item == 'Select Team':
            warn = QtWidgets.QMessageBox()
            warn.setIcon(QtWidgets.QMessageBox.Warning)
            warn.setText('No Team Was Selected.')
            warn.setWindowTitle("Team Error")
            warn.setStandardButtons(QtWidgets.QMessageBox.Ok)
            warn.exec_()
        else:
            open_team_name = item[0:-13]
            open_team_match = int(item[-3:])
            openTeamDialog.accept()

    def retranslateUi(self, openTeamDialog):
        _translate = QtCore.QCoreApplication.translate
        openTeamDialog.setWindowTitle(_translate("openTeamDialog", "Open Team"))
        self.selectTeam.setItemText(0, _translate("openTeamDialog", "Select Team"))
        self.infoLabel.setText(_translate("openTeamDialog", "Select Team From Dropdown List"))


# GLobal Data For Main Window.
available_players = {'BAT': [], 'BWL': [], 'WK': [], 'AR': []}
added_players = {'BAT': [], 'BWL': [], 'WK': [], 'AR': []}
left_points = 1000
used_points = 0
player_category = {}

# Class For Main Window.
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(False)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.teamNameLabel = QtWidgets.QLabel(self.centralwidget)
        self.teamNameLabel.setEnabled(False)
        self.teamNameLabel.setObjectName("teamNameLabel")
        self.gridLayout.addWidget(self.teamNameLabel, 3, 2, 1, 1)
        self.typeBox = QtWidgets.QGroupBox(self.centralwidget)
        self.typeBox.setEnabled(False)
        self.typeBox.setObjectName("typeBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.typeBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.typeGroup = QtWidgets.QButtonGroup(MainWindow)
        self.typeGroup.setObjectName("typeGroup")

        self.batRadio = QtWidgets.QRadioButton(self.typeBox)
        self.batRadio.setObjectName("batRadio")
        self.typeGroup.addButton(self.batRadio)
        self.horizontalLayout_2.addWidget(self.batRadio)

        self.bowRadio = QtWidgets.QRadioButton(self.typeBox)
        self.bowRadio.setObjectName("bowRadio")
        self.typeGroup.addButton(self.bowRadio)
        self.horizontalLayout_2.addWidget(self.bowRadio)

        self.arRadio = QtWidgets.QRadioButton(self.typeBox)
        self.arRadio.setObjectName("arRadio")
        self.typeGroup.addButton(self.arRadio)
        self.horizontalLayout_2.addWidget(self.arRadio)

        self.wkRadio = QtWidgets.QRadioButton(self.typeBox)
        self.wkRadio.setObjectName("wkRadio")
        self.typeGroup.addButton(self.wkRadio)
        self.horizontalLayout_2.addWidget(self.wkRadio)

        self.gridLayout.addWidget(self.typeBox, 3, 0, 3, 2)
        self.guideAddLabel = QtWidgets.QLabel(self.centralwidget)
        self.guideAddLabel.setObjectName("guideAddLabel")
        self.gridLayout.addWidget(self.guideAddLabel, 7, 0, 1, 2)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout.addWidget(self.line_3, 4, 2, 1, 2)
        self.playerAddedLabel = QtWidgets.QLabel(self.centralwidget)
        self.playerAddedLabel.setEnabled(False)
        self.playerAddedLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.playerAddedLabel.setObjectName("playerAddedLabel")
        self.gridLayout.addWidget(self.playerAddedLabel, 5, 2, 1, 2)
        self.addedPlayers = QtWidgets.QListWidget(self.centralwidget)
        self.addedPlayers.setEnabled(False)
        self.addedPlayers.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.addedPlayers.setObjectName("addedPlayers")
        self.gridLayout.addWidget(self.addedPlayers, 6, 2, 1, 2)
        self.guideRemoveLabel = QtWidgets.QLabel(self.centralwidget)
        self.guideRemoveLabel.setObjectName("guideRemoveLabel")
        self.gridLayout.addWidget(self.guideRemoveLabel, 7, 2, 1, 2)
        self.availablePlayers = QtWidgets.QListWidget(self.centralwidget)
        self.availablePlayers.setEnabled(False)
        self.availablePlayers.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.availablePlayers.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.availablePlayers.setObjectName("availablePlayers")
        self.gridLayout.addWidget(self.availablePlayers, 6, 0, 1, 2)
        self.pointsBox = QtWidgets.QGroupBox(self.centralwidget)
        self.pointsBox.setEnabled(False)
        self.pointsBox.setObjectName("pointsBox")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.pointsBox)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.leftPointLabel = QtWidgets.QLabel(self.pointsBox)
        self.leftPointLabel.setObjectName("leftPointLabel")
        self.horizontalLayout_3.addWidget(self.leftPointLabel)
        self.leftPointCount = QtWidgets.QLCDNumber(self.pointsBox)
        self.leftPointCount.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.leftPointCount.setLineWidth(0)
        self.leftPointCount.setDigitCount(4)
        self.leftPointCount.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.leftPointCount.setObjectName("leftPointCount")
        self.horizontalLayout_3.addWidget(self.leftPointCount)
        self.usedPointLabel = QtWidgets.QLabel(self.pointsBox)
        self.usedPointLabel.setObjectName("usedPointLabel")
        self.horizontalLayout_3.addWidget(self.usedPointLabel)
        self.usedPointCount = QtWidgets.QLCDNumber(self.pointsBox)
        self.usedPointCount.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.usedPointCount.setLineWidth(0)
        self.usedPointCount.setDigitCount(4)
        self.usedPointCount.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.usedPointCount.setObjectName("usedPointCount")
        self.horizontalLayout_3.addWidget(self.usedPointCount)
        self.gridLayout.addWidget(self.pointsBox, 2, 0, 1, 4)
        self.selectionBox = QtWidgets.QGroupBox(self.centralwidget)
        self.selectionBox.setEnabled(False)
        self.selectionBox.setObjectName("selectionBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.selectionBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelBat = QtWidgets.QLabel(self.selectionBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.labelBat.setFont(font)
        self.labelBat.setObjectName("labelBat")
        self.horizontalLayout.addWidget(self.labelBat)
        self.countBat = QtWidgets.QLCDNumber(self.selectionBox)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.countBat.setFont(font)
        self.countBat.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.countBat.setLineWidth(0)
        self.countBat.setSmallDecimalPoint(False)
        self.countBat.setDigitCount(2)
        self.countBat.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.countBat.setProperty("value", 0.0)
        self.countBat.setObjectName("countBat")
        self.horizontalLayout.addWidget(self.countBat)
        self.line_0 = QtWidgets.QFrame(self.selectionBox)
        self.line_0.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_0.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_0.setObjectName("line_0")
        self.horizontalLayout.addWidget(self.line_0)
        self.labelBow = QtWidgets.QLabel(self.selectionBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.labelBow.setFont(font)
        self.labelBow.setObjectName("labelBow")
        self.horizontalLayout.addWidget(self.labelBow)
        self.countBow = QtWidgets.QLCDNumber(self.selectionBox)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.countBow.setFont(font)
        self.countBow.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.countBow.setLineWidth(0)
        self.countBow.setSmallDecimalPoint(False)
        self.countBow.setDigitCount(2)
        self.countBow.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.countBow.setProperty("value", 0.0)
        self.countBow.setObjectName("countBow")
        self.horizontalLayout.addWidget(self.countBow)
        self.line_1 = QtWidgets.QFrame(self.selectionBox)
        self.line_1.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_1.setObjectName("line_1")
        self.horizontalLayout.addWidget(self.line_1)
        self.labelAr = QtWidgets.QLabel(self.selectionBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.labelAr.setFont(font)
        self.labelAr.setObjectName("labelAr")
        self.horizontalLayout.addWidget(self.labelAr)
        self.countAr = QtWidgets.QLCDNumber(self.selectionBox)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.countAr.setFont(font)
        self.countAr.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.countAr.setLineWidth(0)
        self.countAr.setSmallDecimalPoint(False)
        self.countAr.setDigitCount(2)
        self.countAr.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.countAr.setProperty("value", 0.0)
        self.countAr.setObjectName("countAr")
        self.horizontalLayout.addWidget(self.countAr)
        self.line_2 = QtWidgets.QFrame(self.selectionBox)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.line_2)
        self.labelWk = QtWidgets.QLabel(self.selectionBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.labelWk.setFont(font)
        self.labelWk.setObjectName("labelWk")
        self.horizontalLayout.addWidget(self.labelWk)
        self.countWk = QtWidgets.QLCDNumber(self.selectionBox)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.countWk.setFont(font)
        self.countWk.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.countWk.setLineWidth(0)
        self.countWk.setSmallDecimalPoint(False)
        self.countWk.setDigitCount(2)
        self.countWk.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.countWk.setProperty("value", 0.0)
        self.countWk.setObjectName("countWk")
        self.horizontalLayout.addWidget(self.countWk)
        self.gridLayout.addWidget(self.selectionBox, 1, 0, 1, 4)
        self.nameLabel = QtWidgets.QLabel(self.centralwidget)
        self.nameLabel.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.nameLabel.setFont(font)
        self.nameLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.nameLabel.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.nameLabel.setText("")
        self.nameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.nameLabel.setObjectName("nameLabel")
        self.gridLayout.addWidget(self.nameLabel, 3, 3, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 21))
        self.menubar.setObjectName("menubar")
        self.manageTeams = QtWidgets.QMenu(self.menubar)
        self.manageTeams.setObjectName("manageTeams")
        MainWindow.setMenuBar(self.menubar)
        self.newTeam = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.newTeam.setFont(font)
        self.newTeam.setObjectName("newTeam")
        self.openTeam = QtWidgets.QAction(MainWindow)
        self.openTeam.setObjectName("openTeam")
        self.saveTeam = QtWidgets.QAction(MainWindow)
        self.saveTeam.setObjectName("saveTeam")
        self.evaluateTeam = QtWidgets.QAction(MainWindow)
        self.evaluateTeam.setObjectName("evaluateTeam")
        self.manageTeams.addAction(self.newTeam)
        self.manageTeams.addAction(self.openTeam)
        self.manageTeams.addAction(self.saveTeam)
        self.manageTeams.addSeparator()
        self.manageTeams.addAction(self.evaluateTeam)
        self.menubar.addAction(self.manageTeams.menuAction())

        self.retranslateUi(MainWindow)

        self.batRadio.clicked.connect(lambda: self.fillAvailable('BAT'))
        self.bowRadio.clicked.connect(lambda: self.fillAvailable('BWL'))
        self.arRadio.clicked.connect(lambda: self.fillAvailable('AR'))
        self.wkRadio.clicked.connect(lambda: self.fillAvailable('WK'))

        self.evaluateTeam.triggered.connect(self.evaluateDialog)
        self.newTeam.triggered.connect(self.newDialog)
        self.openTeam.triggered.connect(self.openDialog)
        self.saveTeam.triggered.connect(self.saveInformation)

        self.availablePlayers.itemDoubleClicked.connect(self.addPlayer)
        self.addedPlayers.itemDoubleClicked.connect(self.removePlayer)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def saveInformation(self):
        bat_count = self.countBat.intValue()
        bwl_count = self.countBow.intValue()
        wk_count = self.countWk.intValue()
        ar_count = self.countAr.intValue()

        total_players = bat_count + bwl_count + wk_count + ar_count
        if total_players < 11:
            warn = QtWidgets.QMessageBox()
            warn.setIcon(QtWidgets.QMessageBox.Warning)
            warn.setText('Insufficient Players In Team.')
            warn.setWindowTitle("Team Error!")
            warn.setStandardButtons(QtWidgets.QMessageBox.Ok)
            warn.exec_()
        else:
            connection = sqlite3.connect('FantasyCricket.db')
            team_cursor = connection.cursor()
            sql_query = '''select * from teams where team_name = ?;'''
            result = team_cursor.execute(sql_query, (teamName,))
            data = result.fetchall()
            team_num = len(data) + 1
            team_players = []
            for key in added_players:
                team_players.extend(added_players[key])
            team_players = list(map(lambda x: x[0], team_players))
            team_players = ','.join(team_players)
            sql_query = '''insert into teams(team_name, players, match_num) values(?, ?, ?);'''
            result = team_cursor.execute(sql_query, (teamName, team_players, team_num))
            team_cursor.close()
            connection.commit()
            connection.close()
            info = QtWidgets.QMessageBox()
            info.setIcon(QtWidgets.QMessageBox.Information)
            if len(data) != 0:
                info.setText('A New Match Has Been Saved.')
                info.setWindowTitle('Match Saved!')
            else:
                info.setText('A New Team Has Been Saved.')
                info.setWindowTitle('Team Saved!')
            info.setStandardButtons(QtWidgets.QMessageBox.Ok)
            info.exec_()

    def evaluateDialog(self):
        evaluateTeamDialog = QtWidgets.QDialog()
        ui = Ui_evaluateTeamDialog()
        ui.setupUi(evaluateTeamDialog)
        evaluateTeamDialog.show()
        evaluateTeamDialog.exec_()

    def findAvailable(self):
        global available_players
        global player_category
        global added_players

        connection = sqlite3.connect('FantasyCricket.db')
        cursor = connection.cursor()
        sql_query = '''select player, value, category from stats;'''
        result = cursor.execute(sql_query)
        player_data = result.fetchall()

        # Cleaning Up The Data.
        for key in available_players:
            available_players[key] = []
        for key in added_players:
            added_players[key] = []
        player_category.clear()

        # Adding The Global Data From Database.
        for player, value, category in player_data:
            available_players[category].append((player, int(value)))
            player_category[player] = (category, int(value))
        cursor.close()
        connection.close()

    def fillAvailable(self, category):
        self.availablePlayers.clear()
        for player, value in available_players[category]:
            item = 'Value: ' + str(value).rjust(3, '0') + ' | Player: {}'.format(player)
            self.availablePlayers.addItem(item)

    def addPlayer(self):
        # Using Global Data Variables.
        global left_points
        global used_points
        global added_players
        global available_players

        # Currently Selected Item In The List.
        item = self.availablePlayers.currentItem()

        # Extracting List Item Information.
        text = item.text()
        value = int(text[7:10])
        player = text[21:]

        # Reading Flag Values.
        Ar_flag = self.arRadio.isChecked()
        Bat_flag = self.batRadio.isChecked()
        Bwl_flag = self.bowRadio.isChecked()
        Wk_flag = self.wkRadio.isChecked()

        # Added Players Type Count.
        bat_count = self.countBat.intValue()
        bwl_count = self.countBow.intValue()
        wk_count = self.countWk.intValue()
        ar_count = self.countAr.intValue()

        # Constraint On Available Points.
        if (used_points + value) > 1000:
            warn = QtWidgets.QMessageBox()
            warn.setIcon(QtWidgets.QMessageBox.Warning)
            warn.setText('Insufficient Points.')
            warn.setWindowTitle("Warning!")
            warn.setStandardButtons(QtWidgets.QMessageBox.Ok)
            warn.exec_()
        # If Maximum Players Have Been Already Added.
        elif (bat_count + bwl_count + wk_count + ar_count) == 11:
            critic = QtWidgets.QMessageBox()
            critic.setIcon(QtWidgets.QMessageBox.Critical)
            critic.setText('11 Players Already Added.')
            critic.setWindowTitle("Alert!")
            critic.setStandardButtons(QtWidgets.QMessageBox.Ok)
            critic.exec_()
        # If More Than One Wicket Keeper Is Added.
        elif Wk_flag and wk_count == 1:
            warn = QtWidgets.QMessageBox()
            warn.setIcon(QtWidgets.QMessageBox.Warning)
            warn.setText('Only One Wicket Keeper Allowed.')
            warn.setWindowTitle("Alert!")
            warn.setStandardButtons(QtWidgets.QMessageBox.Ok)
            warn.exec_()
        # Processing The Selected Items.
        else:
            left_points -= value
            used_points += value

            if Ar_flag:
                added_players['AR'].append((player, value))
                available_players['AR'].remove((player, value))
                self.countAr.display(str(self.countAr.intValue() + 1))

            elif Bat_flag:
                available_players['BAT'].remove((player, value))
                added_players['BAT'].append((player, value))
                self.countBat.display(str(self.countBat.intValue() + 1))

            elif Bwl_flag:
                available_players['BWL'].remove((player, value))
                added_players['BWL'].append((player, value))
                self.countBow.display(str(self.countBow.intValue() + 1))

            elif Wk_flag:
                available_players['WK'].remove((player, value))
                added_players['WK'].append((player, value))
                self.countWk.display(str(self.countWk.intValue() + 1))

            self.leftPointCount.display(str(left_points))
            self.usedPointCount.display(str(used_points))

            # Adding The Player To Added List Widget.
            self.addedPlayers.addItem(item.text())
            # Removing The Selected Player From Available Players.
            self.availablePlayers.takeItem(self.availablePlayers.currentRow())

    def removePlayer(self):
        # Using Global Data Variables.
        global left_points
        global used_points
        global added_players
        global available_players

        # Removing The Currently Selected Item In The List.
        item = self.addedPlayers.takeItem(self.addedPlayers.currentRow())

        # Extracting List Item Information.
        text = item.text()
        value = int(text[7:10])
        player = text[21:]

        # Reading Flag Values.
        Ar_flag = self.arRadio.isChecked()
        Bat_flag = self.batRadio.isChecked()
        Bwl_flag = self.bowRadio.isChecked()
        Wk_flag = self.wkRadio.isChecked()

        # Maintaining The Global Data.
        category = player_category[player][0]
        added_players[category].remove((player, value))
        available_players[category].append((player, value))

        # Updating Point Counts Global Data.
        left_points += value
        used_points -= value
        self.leftPointCount.display(str(left_points))
        self.usedPointCount.display(str(used_points))

        if category == 'BAT':
            self.countBat.display(self.countBat.intValue() - 1)
            if Bat_flag:
                self.availablePlayers.addItem(item.text())
        elif category == 'BWL':
            self.countBow.display(self.countBow.intValue() - 1)
            if Bwl_flag:
                self.availablePlayers.addItem(item.text())
        elif category == 'WK':
            self.countWk.display(self.countWk.intValue() - 1)
            if Wk_flag:
                self.availablePlayers.addItem(item.text())
        elif category == 'AR':
            self.countAr.display(self.countAr.intValue() - 1)
            if Ar_flag:
                self.availablePlayers.addItem(item.text())

    def activateUI(self):
        self.typeBox.setEnabled(True)
        self.pointsBox.setEnabled(True)
        self.selectionBox.setEnabled(True)

        self.nameLabel.setEnabled(True)
        self.teamNameLabel.setEnabled(True)
        self.playerAddedLabel.setEnabled(True)

        self.addedPlayers.setEnabled(True)
        self.availablePlayers.setEnabled(True)
        self.centralwidget.setEnabled(True)

    def clearStats(self):
        global left_points
        global used_points
        global available_players
        global added_players
        global player_category

        left_points = 1000
        used_points = 0

        self.addedPlayers.clear()
        self.availablePlayers.clear()
        self.countAr.display('0')
        self.countWk.display('0')
        self.countBat.display('0')
        self.countBow.display('0')
        self.leftPointCount.display(str(left_points))
        self.usedPointCount.display(str(used_points))

    def newDialog(self):
        newTeamDialog = QtWidgets.QDialog()
        ui = Ui_newTeamDialog()
        ui.setupUi(newTeamDialog)
        newTeamDialog.show()
        retval = newTeamDialog.exec_()
        if retval == 1:
            self.activateUI()
            self.clearStats()

            # Reset The Radio Button Group.
            self.typeGroup.setExclusive(False)
            self.batRadio.setChecked(False)
            self.bowRadio.setChecked(False)
            self.wkRadio.setChecked(False)
            self.arRadio.setChecked(False)
            self.typeGroup.setExclusive(True)

            self.findAvailable()
            self.nameLabel.setText(teamName)

    def openDialog(self):
        openTeamDialog = QtWidgets.QDialog()
        ui = Ui_openTeamDialog()
        ui.setupUi(openTeamDialog)
        openTeamDialog.show()
        flag = openTeamDialog.exec_()
        if flag == 1:
            self.activateUI()
            self.clearStats()

            # Reset The Radio Button Group.
            self.typeGroup.setExclusive(False)
            self.batRadio.setChecked(False)
            self.bowRadio.setChecked(False)
            self.wkRadio.setChecked(False)
            self.arRadio.setChecked(False)
            self.typeGroup.setExclusive(True)

            self.findAvailable()

            # Reading Team Players From Database.
            connection = sqlite3.connect('FantasyCricket.db')
            cursor = connection.cursor()
            sql_query = '''select players from teams where team_name = ? and match_num = ?;'''
            result = cursor.execute(sql_query, (open_team_name, open_team_match))
            players = result.fetchone()[0].strip().split(',')
            cursor.close()
            connection.close()

            global available_players
            global added_players
            global left_points
            global used_points

            #Setting Up The UI.
            bat, bowl, wk, ar = 0, 0, 0, 0
            left, used = 1000, 0
            for player in players:
                category, value = player_category[player]
                if category == 'BAT':
                    bat += 1
                elif category == 'BWL':
                    bowl += 1
                elif category == 'AR':
                    ar += 1
                elif category == 'WK':
                    wk += 1
                left -= value
                used += value
                available_players[category].remove((player, value))
                added_players[category].append((player, value))
                item = 'Value: ' + str(value).rjust(3, '0') + ' | Player: {}'.format(player)
                self.addedPlayers.addItem(item)
            left_points = left
            used_points = used

            # Updating The LCD Displays.
            self.leftPointCount.display(left_points)
            self.usedPointCount.display(used_points)
            self.countWk.display(wk)
            self.countAr.display(ar)
            self.countBow.display(bowl)
            self.countBat.display(bat)
            self.nameLabel.setText(open_team_name)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Fantasy Cricket"))
        self.teamNameLabel.setText(_translate("MainWindow", "Team Name:"))
        self.typeBox.setTitle(_translate("MainWindow", "Player Type"))
        self.batRadio.setText(_translate("MainWindow", "BAT"))
        self.bowRadio.setText(_translate("MainWindow", "BOW"))
        self.arRadio.setText(_translate("MainWindow", "AR"))
        self.wkRadio.setText(_translate("MainWindow", "WK"))
        self.guideAddLabel.setText(_translate("MainWindow", "Double Click Player Name To Add The Player."))
        self.playerAddedLabel.setText(_translate("MainWindow", "┏Players Added To The Team┓"))
        self.guideRemoveLabel.setText(_translate("MainWindow", "Double Click Player Name To Remove The Player."))
        self.pointsBox.setTitle(_translate("MainWindow", "Points"))
        self.leftPointLabel.setText(_translate("MainWindow", "Points Available:"))
        self.usedPointLabel.setText(_translate("MainWindow", "Points Used:"))
        self.selectionBox.setTitle(_translate("MainWindow", "Your Selections"))
        self.labelBat.setText(_translate("MainWindow", "Batsman (BAT):"))
        self.labelBow.setText(_translate("MainWindow", "Bowlers (BOW):"))
        self.labelAr.setText(_translate("MainWindow", "All Rounders (AR):"))
        self.labelWk.setText(_translate("MainWindow", "Wicket Keepers (WK):"))
        self.manageTeams.setTitle(_translate("MainWindow", "Manage Teams"))
        self.newTeam.setText(_translate("MainWindow", "New Team"))
        self.newTeam.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.openTeam.setText(_translate("MainWindow", "Open Team"))
        self.openTeam.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.saveTeam.setText(_translate("MainWindow", "Save Team"))
        self.saveTeam.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.evaluateTeam.setText(_translate("MainWindow", "Evaluate Team"))
        self.evaluateTeam.setShortcut(_translate("MainWindow", "F5"))

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

# The Project If Finally Completed.