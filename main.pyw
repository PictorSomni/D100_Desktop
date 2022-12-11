# -*- coding: UTF-8 -*-

##########################################################################################
# IMPORTS
##########################################################################################
from PySide6 import QtCore, QtGui, QtWidgets
from random import randint as RNG
from random import choice
import sys
import csv
import os
import pygame.mixer as audio
import pygame

# import UI_D100_tabbed as UI
import UI_D100 as UI

import CONSTANT
from character import Character

# import qdarkstyle
from qt_material import apply_stylesheet

##########################################################################################
# MAIN CLASS
##########################################################################################
class Toolkit(UI.Ui_MainWindow, QtWidgets.QMainWindow) :

    def __init__(self):

        # Initialize the QT interface
        super(Toolkit, self).__init__()
        self.setupUi(self)

        # Characters containers
        battle_npc = {}
        story_npc = {}

        # Init pygame and pygame.mixer otherwise the sound will lag !
        #audio.pre_init()
        #audio.init()
        #pygame.init()
                
        # Set font size
        self.setStyleSheet(CONSTANT.FONT_SIZE)        

        # Init Timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timer_update)
        self.minutes = 0

        # Init labels
        self.label_general_info.setText("Infos générales")
        self.label_general_dice.setText("Lancez un dé")
        self.label_character_score.setText("Réussi / Raté\nScore = ")
        self.label_character_damage_score.setText("{}{}\nDégâts =".format(self.spinBox_character_damage_dice_number.text(), self.spinBox_character_damage_dice.text()))
        self.label_timer.setText("Timer prêt !")
        self.label_adventure_result.setText("Dé d'aventure")
        self.label_adventure_counter.setText("{} / {}".format(self.horizontalSlider_adventure_counter.value(), self.horizontalSlider_adventure_counter.maximum()))

        # Init buttons
        self.pushButton_general_dice.clicked.connect(lambda : self.label_general_dice.setText("D{} = {}".format(int(self.spinBox_general_dice.cleanText()), self.dice_roll(int(self.spinBox_general_dice.cleanText())))))
        self.pushButton_general_dice_negative.clicked.connect(lambda : self.spinBox_general_dice.setValue(int(self.spinBox_general_dice.value()) - 5))
        self.pushButton_general_dice_positive.clicked.connect(lambda : self.spinBox_general_dice.setValue(int(self.spinBox_general_dice.value()) + 5))
        self.pushButton_add_npc_combat.clicked.connect(lambda : self.generate_npc_wave(True, self.tableWidget_npc_combat, self.spinBox_max_npc_combat_spawn, battle_npc, CONSTANT.ADVENTURE_VOCATION, "combat"))
        self.pushButton_add_npc_story.clicked.connect(lambda : self.generate_npc_wave(True, self.tableWidget_npc_story, self.spinBox_max_npc_story_spawn, story_npc, CONSTANT.COMMON_VOCATION, "story"))
        self.pushButton_add_player.clicked.connect(lambda : self.add_player(self.tableWidget_players))
        self.pushButton_remove_player.clicked.connect(lambda : self.remove_player(self.tableWidget_players))
        self.pushButton_max_npc_combat_spawn_negative.clicked.connect(lambda : self.spinBox_max_npc_combat_spawn.setValue(int(self.spinBox_max_npc_combat_spawn.value()) - 1))
        self.pushButton_max_npc_combat_spawn_positive.clicked.connect(lambda : self.spinBox_max_npc_combat_spawn.setValue(int(self.spinBox_max_npc_combat_spawn.value()) + 1))
        self.pushButton_max_npc_story_spawn_negative.clicked.connect(lambda : self.spinBox_max_npc_story_spawn.setValue(int(self.spinBox_max_npc_story_spawn.value()) - 1))
        self.pushButton_max_npc_story_spawn_positive.clicked.connect(lambda : self.spinBox_max_npc_story_spawn.setValue(int(self.spinBox_max_npc_story_spawn.value()) + 1))
        self.pushButton_suppress_all_npc_combat.clicked.connect(lambda : self.clear_table(self.tableWidget_npc_combat))
        self.pushButton_suppress_all_npc_story.clicked.connect(lambda : self.clear_table(self.tableWidget_npc_story))
        self.pushButton_adventure_GM.clicked.connect(lambda : self.adventure(self.horizontalSlider_adventure_counter, self.label_adventure_result, self.label_adventure_counter, -1))
        self.pushButton_adventure_PC.clicked.connect(lambda : self.adventure(self.horizontalSlider_adventure_counter, self.label_adventure_result, self.label_adventure_counter, 1))
        self.pushButton_character_damage_dice_number_negative.clicked.connect(lambda : self.spinBox_character_damage_dice_number.setValue(int(self.spinBox_character_damage_dice_number.value()) - 1))
        self.pushButton_character_damage_dice_number_positive.clicked.connect(lambda : self.spinBox_character_damage_dice_number.setValue(int(self.spinBox_character_damage_dice_number.value()) + 1))
        self.pushButton_character_damage_dice_negative.clicked.connect(lambda : self.spinBox_character_damage_dice.setValue(int(self.spinBox_character_damage_dice.value()) - 1))
        self.pushButton_character_damage_dice_positive.clicked.connect(lambda : self.spinBox_character_damage_dice.setValue(int(self.spinBox_character_damage_dice.value()) + 1))
        self.pushButton_character_damage_dice_supplement_negative.clicked.connect(lambda : self.spinBox_character_damage_dice_supplement.setValue(int(self.spinBox_character_damage_dice_supplement.value()) - 1))
        self.pushButton_character_damage_dice_supplement_positive.clicked.connect(lambda : self.spinBox_character_damage_dice_supplement.setValue(int(self.spinBox_character_damage_dice_supplement.value()) + 1))
        self.pushButton_character_damage.clicked.connect(lambda : self.damage(False, self.tableWidget_players, self.tableWidget_npc_story, self.tableWidget_npc_combat))
        self.pushButton_character_damage_max.clicked.connect(lambda : self.damage(True, self.tableWidget_players, self.tableWidget_npc_story, self.tableWidget_npc_combat))        
        self.pushButton_bonus_malus_negative.clicked.connect(lambda : self.spinBox_character_bonus_malus.setValue(int(self.spinBox_character_bonus_malus.value()) - 5))
        self.pushButton_bonus_malus_positive.clicked.connect(lambda : self.spinBox_character_bonus_malus.setValue(int(self.spinBox_character_bonus_malus.value()) + 5))
        self.pushButton_physic.clicked.connect(lambda : self.use_skill("physique", self.tableWidget_players, self.tableWidget_npc_story, self.tableWidget_npc_combat))
        self.pushButton_social.clicked.connect(lambda : self.use_skill("social", self.tableWidget_players, self.tableWidget_npc_story, self.tableWidget_npc_combat))
        self.pushButton_mental.clicked.connect(lambda : self.use_skill("mental", self.tableWidget_players, self.tableWidget_npc_story, self.tableWidget_npc_combat))
        self.pushButton_timer_fixed.clicked.connect(lambda : self.timer_handler("fixe", self.horizontalSlider_timer_set_time.value()))
        self.pushButton_timer_random.clicked.connect(lambda : self.timer_handler("aléatoire", self.horizontalSlider_timer_set_time.value()))
        
        # Generate and assign the soundbox' buttons based on the sound files existing in the "audio" folder
        # If there is another folder inside the audio folder, it will randomly choose a sound inside this folder
        # Folders are colored in orange to differentiate them
        x_counter = 0
        y_counter = 0
        for sound in CONSTANT.AUDIO_FILES :
            button = QtWidgets.QPushButton(sound)
            button.setMinimumSize(128, 128)
            if sound in CONSTANT.AUDIO_DIRECTORIES :
                button.setStyleSheet('QPushButton {color: orange;}')

            if x_counter < CONSTANT.SOUNDBOX_BUTTONS_PER_ROW :
                self.gridLayout_soundbox.addWidget(button, y_counter, x_counter)
                x_counter += 1

            else :
                x_counter = 1
                y_counter += 1

            self.gridLayout_soundbox.addWidget(button, y_counter, x_counter)

            button.clicked.connect(lambda _, which_sound = sound : self.playing_sound(which_sound))

        # Import player list
        self.import_player(self.tableWidget_players)    

        # Init comboboxes
        self.comboBox_timer_events.addItems(CONSTANT.TIMER_EVENT)

        self.comboBox_generate_npc_combat.addItems(CONSTANT.RANDOM_NPC_WAVE)
        self.comboBox_generate_npc_story.addItems(CONSTANT.RANDOM_NPC_WAVE)

        self.comboBox_generate_npc_combat.addItem("-" * 7)
        self.comboBox_generate_npc_story.addItem("-" * 7)

        self.comboBox_generate_npc_combat.addItems(CONSTANT.ORIGIN)
        self.comboBox_generate_npc_story.addItems(CONSTANT.ORIGIN)

        self.comboBox_generate_npc_combat.activated.connect(lambda : self.generate_npc_wave(False, self.tableWidget_npc_combat, self.spinBox_max_npc_combat_spawn, battle_npc, CONSTANT.ADVENTURE_VOCATION, "combat"))
        self.comboBox_generate_npc_story.activated.connect(lambda : self.generate_npc_wave(False, self.tableWidget_npc_story, self.spinBox_max_npc_story_spawn, story_npc, CONSTANT.COMMON_VOCATION, "story"))

        # Init slider
        self.horizontalSlider_timer_set_time.valueChanged.connect(lambda : self.label_timer_set_time.setText("{} minutes".format(self.horizontalSlider_timer_set_time.value())))
 
        # Init the progress bar
        self.progressBar_timer.valueChanged.connect(lambda : self.progressBar_timer.text())

        # Sets the global dice to the number of players (used to pick which player is damaged by an NPC)
        self.spinBox_general_dice.setValue(self.tableWidget_players.rowCount())


##########################################################################################
# METHODS
##########################################################################################
 
 # Calculate the damages taken by the active character and subtract it from it's corresponding table cell                    
    def damage (self, offensive = False,  *table) :

        selected_character = self.comboBox_character_select.itemText(self.comboBox_character_select.currentIndex())

        if offensive == True :
            damage_points = (int(self.spinBox_character_damage_dice_number.text()) * int(self.spinBox_character_damage_dice.cleanText())) + int(self.spinBox_character_damage_dice_supplement.text())

        else :
            damage_points = self.dice_roll(int(self.spinBox_character_damage_dice.cleanText()),
                            int(self.spinBox_character_damage_dice_number.text()),
                            int(self.spinBox_character_damage_dice_supplement.text()))

        self.label_character_damage_score.setText("{} D{} + {}\nDégâts = {}".format(int(self.spinBox_character_damage_dice_number.text()),
        int(self.spinBox_character_damage_dice.cleanText()),
        int(self.spinBox_character_damage_dice_supplement.text()),
        damage_points))

        for table in table :
            for item in range(table.rowCount()) :

                # Repopulates the list when an NPC dies without crashing...
                try:
                    table.item(item, 0).text()

                except AttributeError :
                    self.populate_character_combobox(self.tableWidget_players, self.tableWidget_npc_story, self.tableWidget_npc_combat)
                    break

                else :
                    # Matches the selected character with the correct table widget's row
                    if table.item(item, 0).text() == selected_character :

                        # If the character is a player, add the damage to the 7th column
                        if table == self.tableWidget_players : 
                            damage_delta = int(table.item(item, 6).text()) + int(damage_points)                           
                            table.item(item, 6).setText("{}".format(damage_delta))
                            self.label_general_info.setText("{} s'est pris {} de dégâts".format(selected_character, damage_points))
                            self.health_color(table)

                        # If the character is an NPC, subtract damage from health
                        else :
                            table.item(item, 6).setText("{}".format(int(table.item(item, 6).text()) - int(damage_points)))
                            self.label_general_info.setText("{} s'est pris {} de dégâts".format(selected_character, damage_points))

                            # If the health of the NPC reach 0, remove the row from the tabke widget
                            if int(table.item(item, 6).text()) <= 0 :
                                table.removeRow(item)
                                self.label_general_info.setText("{} est mort(e)".format(selected_character))
                                self.populate_character_combobox(self.tableWidget_players, self.tableWidget_npc_story, self.tableWidget_npc_combat)


##########################################################################################
    # Rolls a D100 and tells back if the roll succeeded or not based on the character's skill points.
    def use_skill (self, skill, *table) :

        selected_character = self.comboBox_character_select.itemText(self.comboBox_character_select.currentIndex())
        variation = int(self.spinBox_character_bonus_malus.cleanText())

        for table in table :
            for item in range(table.rowCount()) :
                if table.item(item, 0).text() == selected_character :
                    score = self.dice_roll(100)
                    if skill == "physique" :
                        selected_row = 1

                    elif skill == "social" :
                        selected_row = 2
                    
                    else :
                        selected_row = 3

                    if table != self.tableWidget_players :
                        selected_row += 2

                    try :
                        upper_limit = (int(table.item(item, selected_row).text()) + variation)

                    except Exception :
                        self.label_general_info.setText("LE PERSONNAGE N'A PAS DE POINTS DE COMPETENCE !")

                    else :
                        if score <= upper_limit :
                                self.label_character_score.setText("{} : réussite\nscore = {} / {}".format(skill, score, upper_limit))
                                self.label_general_info.setText("{} réussi son jet de {}".format(selected_character, skill))

                        else :
                            self.label_character_score.setText("{} : échec\nscore = {} / {}".format(skill, score, upper_limit))
                            self.label_general_info.setText("{} rate son jet de {}".format(selected_character, skill))


##########################################################################################
    # Generates an adventure dice and changes the UI accordingly                 
    def adventure (self, slider, text, counter, direction) :

        value = slider.value()
        slider.setValue(value + direction)
        index = self.dice_roll(3) -1

        if (value != slider.value()) :
            if direction == 1 :
                text.setText("PJ : {}".format(CONSTANT.BONUS_MALUS[index]))

            else :
                text.setText("MJ : {}".format(CONSTANT.BONUS_MALUS[index]))

        counter.setText("{} / {}".format(slider.value(), slider.maximum()))


##########################################################################################
    # Dice handler
    def dice_roll (self, dice, dice_number = 1, dice_supplement = 0):

        result = []

        for i in range(dice_number) :
            result.append(RNG(1, dice))

        return sum(result, dice_supplement)


##########################################################################################
    # Populates the character selection box based on table widgets
    def populate_character_combobox (self, *table) :

        self.comboBox_character_select.clear()

        for table in table :
            if table.rowCount() > 0 :
                if table.objectName() == "tableWidget_players" :
                    self.comboBox_character_select.addItem("---=[    JOUEURS    ]=---")

                elif table.objectName() == "tableWidget_npc_story" :
                    self.comboBox_character_select.addItem("---=[    PNJs HISTOIRE    ]=---")

                else :
                    self.comboBox_character_select.addItem("---=[    PNJs COMBAT    ]=---")

                
            for item in range(table.rowCount()) :
                 # Repopulates the list when an NPC dies without crashing...
                try:
                    table.item(item, 0).text()

                except AttributeError :
                    pass

                else :
                    self.comboBox_character_select.addItem(table.item(item, 0).text())   
    
   
##########################################################################################
    # Generates a wave of NPCs and fills the corresponding table widget
    def generate_npc_wave (self, solo, table, spinbox, which_character, vocation_list, npc) :

        if solo == False :
            how_many = RNG(0, spinbox.value())
            if how_many == 0 :
                self.label_general_info.setText("Il n'y a personne...")


        else :
            how_many = 1

        if npc == "combat" :
            combobox = self.comboBox_generate_npc_combat
        
        else :
            combobox = self.comboBox_generate_npc_story

        current = table.rowCount()
        total = current + how_many
        table.setRowCount(total)

        origin = choice(CONSTANT.ORIGIN[:-1])

        for index in range(current, total) :
            if combobox.currentText() == CONSTANT.RANDOM_NPC_WAVE[0] :
                origin = choice(CONSTANT.ORIGIN[:-1])
                self.label_general_info.setText("{} PNJ(s) apparait/ssent !".format(how_many))

            
            elif combobox.currentText() == CONSTANT.RANDOM_NPC_WAVE[1] :
                # pass
                self.label_general_info.setText("{} {}(s) apparait/ssent !".format(how_many, origin))


            else :
                if not combobox.currentText() == ("-" * 7) :
                    origin = combobox.currentText()
                    self.label_general_info.setText("{} {}(s) apparait/ssent !".format(how_many, origin))

            which_character[index]= Character(origin = origin, vocation = choice(vocation_list)).get_character()
            table.setColumnCount(len(which_character[index]))

            for key, value in enumerate(which_character[index]) :
                table.setHorizontalHeaderLabels(Character.get_key(self))
                table.setItem(index, key, QtWidgets.QTableWidgetItem(str(value)))
 
        self.populate_character_combobox(self.tableWidget_players, self.tableWidget_npc_story, self.tableWidget_npc_combat)
        self.add_postures(table)
        table.resizeColumnsToContents()
        table.resizeRowsToContents()


##########################################################################################
    # Clears the content of a defined table widget
    def clear_table (self, table) :
        
        table.setRowCount(0)
        self.populate_character_combobox(self.tableWidget_players, self.tableWidget_npc_story, self.tableWidget_npc_combat)


##########################################################################################
    # Does something every tick of the timer
    def timer_update (self) :
        
        if self.minutes <= 0 :
            self.timer.stop()
            self.label_general_info.setText(self.comboBox_timer_events.currentText())
            QtWidgets.QMessageBox.about(self.parent(), "TIMER OUT", "{}".format(self.comboBox_timer_events.currentText()))
            
        else :
            self.minutes -= 1
            self.progressBar_timer.setValue(self.minutes)
            self.label_timer.setText("{}".format(self.minutes))
        

##########################################################################################
    # Handles the duration of the timer (*60 to get secondes in minutes, which corresponds to the timer GUI)
    def timer_handler (self, state, duration) :

        if state == "fixe" :
            self.minutes = duration * 60

        else :
            self.minutes = RNG(1, (duration * 60))

        self.progressBar_timer.setMaximum(self.minutes)
        self.progressBar_timer.setValue(self.minutes)
        self.label_timer.setText("{}".format(self.minutes))

        self.timer.start(1000)


##########################################################################################
    # Import players.csv content and parse it to the players 'table
    def import_player (self, table) :

        with open("{}/players.csv".format(CONSTANT.PATH), "r") as player_list :
            player_reader = csv.DictReader(player_list)

            for row, player in enumerate(player_reader) :
                table.setColumnCount(len(player))
                table.setHorizontalHeaderLabels(player)
                table.insertRow(table.rowCount())
                for column, value in enumerate(player.values()) :
                    table.setItem(row, column, QtWidgets.QTableWidgetItem(value))

        self.add_postures(table)
        self.populate_character_combobox(self.tableWidget_players, self.tableWidget_npc_story, self.tableWidget_npc_combat)
        self.health_color(table)
        table.resizeColumnsToContents()
        table.resizeRowsToContents()


#########################################################################################
    # Adds a player
    def add_player (self, table) :

        table.insertRow(table.rowCount())
        table.setItem(table.rowCount() -1, 0, QtWidgets.QTableWidgetItem("Joueur {}".format(table.rowCount())))
        self.add_postures(table)
        self.populate_character_combobox(self.tableWidget_players, self.tableWidget_npc_story, self.tableWidget_npc_combat)


#########################################################################################
    # removes a player
    def remove_player (self, table) :
    
        deleteconfirmation = QtWidgets.QMessageBox.question(self.parent(), "Supprimer joueur ?", "Confirmation de la suppression de {} ?".format(table.item(table.currentRow(), 0).text()), QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
        
        if deleteconfirmation == QtWidgets.QMessageBox.Yes:
            table.removeRow(table.currentRow())
            self.populate_character_combobox(self.tableWidget_players, self.tableWidget_npc_story, self.tableWidget_npc_combat)


##########################################################################################
    # Add postures comboBox to the players'table
    def add_postures (self, table) :
        
        for item in range(table.rowCount()) :
            comboBox_posture = QtWidgets.QComboBox()
            for posture in CONSTANT.POSTURES :
                comboBox_posture.addItem(posture)
                table.setCellWidget(item, 8, comboBox_posture)


##########################################################################################
    # Change the player's row color according to his / her health
    def health_color (self, table) :
        
        for item in range(table.rowCount()) :
            damage_delta = int(table.item(item, 6).text())
            total_health = (int(table.item(item, 4).text()) + int(table.item(item, 5).text()))

            # Change the row's color depending on the character's health
            if damage_delta >= round(total_health / 4) * 3 :
                for cell in range(table.columnCount()):
                    table.item(item, cell).setBackground(QtGui.QColor(128, 32, 32))

            elif damage_delta >= (total_health / 2) :
                for cell in range(table.columnCount()):
                    table.item(item, cell).setBackground(QtGui.QColor(128, 110, 32))

            else :
                for cell in range(table.columnCount()) :
                    table.item(item, cell).setBackground(QtGui.QColor(32, 128, 32))


##########################################################################################
    # Play a sound
    def playing_sound (self, which_sound) :
        
        # If "which_sound" is a folder, chose randomly a wav file inside
        if which_sound in CONSTANT.AUDIO_DIRECTORIES :
            chosen_sound = [file for file in os.listdir("{}{}".format(CONSTANT.AUDIO_PATH, which_sound)) if os.path.splitext(file)[-1].lower() == ".wav"]
            sound = audio.Sound("{}{}/{}".format(CONSTANT.AUDIO_PATH, which_sound, choice(chosen_sound)))

        else :
            sound = audio.Sound("{}{}.wav".format(CONSTANT.AUDIO_PATH, which_sound))
        
        sound.play()


##########################################################################################
# EXECUTE THE PROGRAM
##########################################################################################

if __name__ == "__main__" :
    app = QtWidgets.QApplication(sys.argv)

    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    # setup stylesheet
    apply_stylesheet(app, theme='dark_blue.xml')

    toolkit = Toolkit()
    toolkit.show()
    sys.exit(app.exec())
