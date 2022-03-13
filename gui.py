from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtGui import QTextCursor
from enigma import *
import sys
from ui_enigma import Ui_MainWindow


def find_rotor(list_rotors, name):
    for rotor in list_rotors:
        if rotor._name == name:
            wiring = rotor._wiring
            notch = rotor._notch
            ring_settings = rotor._ring_settings
            position = rotor._position
            name = rotor._name
            return Rotor(wiring, notch, ring_settings, position, name)


def find_reflector(list_reflector, name):
    for reflector in list_reflector:
        if reflector._name == name:
            return reflector


def was_already(text, letter):  # checks if last letter is not a duplicate (plugboard)
    cut_text = text[:-1]
    if letter in cut_text:
        return True
    return False


class EnigmaWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.enigma = Enigma()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # connect all buttons to fuctions they activate
        self.ui.Apply.clicked.connect(self.pressed_apply)
        self.ui.Reset.clicked.connect(self.reset_enigma)
        self.ui.writeText.textChanged.connect(self.encrypt)
        self.ui.Plug.setMaxLength(len_alphabet)
        self.ui.Plug.textEdited.connect(self.plug_action)
        self.ui.Plug.cursorPositionChanged.connect(self.plug_cursor)
        self.ui.writeText.cursorPositionChanged.connect(self.writeText_cursor)

    # prevents changing cursor (always at the end) thus deleting chars in the middle of text
    def writeText_cursor(self):
        end_cursor = QTextCursor(self.ui.writeText.document())
        end_cursor.movePosition(QTextCursor.End)
        self.ui.writeText.setTextCursor(end_cursor)

    def plug_cursor(self):  # cursor in plugboard always at the end
        self.ui.Plug.end(False)

    def plug_action(self):
        content = self.ui.Plug.text()
        if content == '':  # situation when user deletes chars to the very end
            pass
        elif content[-1] not in alphabet or was_already(content, content[-1]):
            text = content[:-1]
            self.ui.Plug.setText(text)

    def pressed_apply(self):
        rotor1 = self.ui.RotorI.currentText()  # get data that user set
        rotor2 = self.ui.RotorII.currentText()
        rotor3 = self.ui.RotorIII.currentText()
        ring1 = int(self.ui.RingSettingI.currentText())
        ring2 = int(self.ui.RingSettingII.currentText())
        ring3 = int(self.ui.RingSettingIII.currentText())
        pos1 = self.ui.PositionI.currentText()
        pos2 = self.ui.PositionII.currentText()
        pos3 = self.ui.PositionIII.currentText()

        if len(self.ui.Plug.text()) % 2 != 0:
            new_plugboard = self.ui.Plug.text()[:-1]
            self.ui.Plug.setText(new_plugboard)
        else:
            new_plugboard = self.ui.Plug.text()

        all_rotors = get_5ROTORS()
        rotorI = find_rotor(all_rotors, rotor1)
        rotorII = find_rotor(all_rotors, rotor2)
        rotorIII = find_rotor(all_rotors, rotor3)
        self.enigma.set_rotors([rotorI, rotorII, rotorIII])

        new_pos = pos1+pos2+pos3
        self.enigma.set_position(new_pos)
        self.enigma.set_ring_settings([ring1, ring2, ring3])
        self.enigma.set_plugboard(Plugboard(new_plugboard))
        all_reflectors = get_Reflectors()
        new_reflector_name = self.ui.Reflector.currentText()
        new_reflector = find_reflector(all_reflectors, new_reflector_name)
        self.enigma.set_reflector(new_reflector)
        self.encrypt()

    def encrypt(self):
        if self.ui.writeText.toPlainText() != '':
            if self.ui.writeText.toPlainText()[-1] not in alphabet:
                text = self.ui.writeText.toPlainText()[:-1]
                self.ui.writeText.setPlainText(text)
            else:
                temp_rotors = [rotor.get_same_rotor()
                               for rotor in self.enigma._rotors]
                temp_plugboard = self.enigma._plugboard.get_same_plugboard()
                temp_reflector = self.enigma._reflector.get_same_reflector()
                # makes temporary enigma not to change its settings
                temp_enigma = Enigma(
                    temp_rotors, temp_plugboard, temp_reflector)
                text = self.ui.writeText.toPlainText()
                encrypted_text = temp_enigma.encrypt_text(text)
                self.ui.readText.setPlainText(encrypted_text)
                self.ui.Plug.setText(temp_enigma._plugboard._wiring)
                indexRef = self.ui.Reflector.findText(
                    temp_enigma._reflector._name)
                self.ui.Reflector.setCurrentIndex(indexRef)

                rotors_positions = [rotor._position for rotor in temp_enigma._rotors]
                rotors_rings = [rotor._ring_settings for rotor in temp_enigma._rotors]
                rotor_names = [rotor._name for rotor in temp_enigma._rotors]

                # all below code makes unapplied data to vanish
                indexPosI = self.ui.PositionI.findText(rotors_positions[0])
                self.ui.PositionI.setCurrentIndex(indexPosI)
                indexPosII = self.ui.PositionII.findText(rotors_positions[1])
                self.ui.PositionII.setCurrentIndex(indexPosII)
                indexPosIII = self.ui.PositionIII.findText(rotors_positions[2])
                self.ui.PositionIII.setCurrentIndex(indexPosIII)

                indexRotorI = self.ui.RotorI.findText(rotor_names[0])
                self.ui.RotorI.setCurrentIndex(indexRotorI)
                indexRotorII = self.ui.RotorII.findText(rotor_names[1])
                self.ui.RotorII.setCurrentIndex(indexRotorII)
                indexRotorIII = self.ui.RotorIII.findText(rotor_names[2])
                self.ui.RotorIII.setCurrentIndex(indexRotorIII)

                indexRingI = self.ui.RingSettingI.findText(
                    str(rotors_rings[0]))
                self.ui.RingSettingI.setCurrentIndex(indexRingI)
                indexRingII = self.ui.RingSettingII.findText(
                    str(rotors_rings[1]))
                self.ui.RingSettingII.setCurrentIndex(indexRingII)
                indexRingIII = self.ui.RingSettingIII.findText(
                    str(rotors_rings[2]))
                self.ui.RingSettingIII.setCurrentIndex(indexRingIII)
        else:
            self.ui.readText.clear()

            rotors_positions = [rotor._position for rotor in self.enigma._rotors]
            rotors_rings = [rotor._ring_settings for rotor in self.enigma._rotors]
            rotor_names = [rotor._name for rotor in self.enigma._rotors]
            # all below code makes unapplied data to vanish
            indexPosI = self.ui.PositionI.findText(rotors_positions[0])
            self.ui.PositionI.setCurrentIndex(indexPosI)
            indexPosII = self.ui.PositionII.findText(rotors_positions[1])
            self.ui.PositionII.setCurrentIndex(indexPosII)
            indexPosIII = self.ui.PositionIII.findText(rotors_positions[2])
            self.ui.PositionIII.setCurrentIndex(indexPosIII)

            indexRotorI = self.ui.RotorI.findText(rotor_names[0])
            self.ui.RotorI.setCurrentIndex(indexRotorI)
            indexRotorII = self.ui.RotorII.findText(rotor_names[1])
            self.ui.RotorII.setCurrentIndex(indexRotorII)
            indexRotorIII = self.ui.RotorIII.findText(rotor_names[2])
            self.ui.RotorIII.setCurrentIndex(indexRotorIII)

            indexRingI = self.ui.RingSettingI.findText(
                str(rotors_rings[0]))
            self.ui.RingSettingI.setCurrentIndex(indexRingI)
            indexRingII = self.ui.RingSettingII.findText(
                str(rotors_rings[1]))
            self.ui.RingSettingII.setCurrentIndex(indexRingII)
            indexRingIII = self.ui.RingSettingIII.findText(
                str(rotors_rings[2]))
            self.ui.RingSettingIII.setCurrentIndex(indexRingIII)

    def reset_enigma(self):  # sets enigma to default settings
        self.ui.writeText.clear()
        self.ui.readText.clear()
        self.ui.Plug.clear()
        indexRotorI = self.ui.RotorI.findText('I')
        self.ui.RotorI.setCurrentIndex(indexRotorI)
        indexRotorII = self.ui.RotorII.findText('II')
        self.ui.RotorII.setCurrentIndex(indexRotorII)
        indexRotorIII = self.ui.RotorIII.findText('III')
        self.ui.RotorIII.setCurrentIndex(indexRotorIII)

        indexRingI = self.ui.RingSettingI.findText('0')
        self.ui.RingSettingI.setCurrentIndex(indexRingI)
        indexRingII = self.ui.RingSettingII.findText('0')
        self.ui.RingSettingII.setCurrentIndex(indexRingII)
        indexRingIII = self.ui.RingSettingIII.findText('0')
        self.ui.RingSettingIII.setCurrentIndex(indexRingIII)

        indexPosI = self.ui.PositionI.findText('A')
        self.ui.PositionI.setCurrentIndex(indexPosI)
        indexPosII = self.ui.PositionII.findText('A')
        self.ui.PositionII.setCurrentIndex(indexPosII)
        indexPosIII = self.ui.PositionIII.findText('A')
        self.ui.PositionIII.setCurrentIndex(indexPosIII)

        indexRef = self.ui.Reflector.findText('UKW-B')
        self.ui.Reflector.setCurrentIndex(indexRef)
        self.enigma = Enigma()


def guiMain(args):
    app = QApplication(args)
    window = EnigmaWindow()
    window.show()
    return app.exec_()


if __name__ == '__main__':
    guiMain(sys.argv)
