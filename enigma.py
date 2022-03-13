from rotor import *
import argparse


class Enigma:
    def __init__(self, rotors=None, plugboard=None, reflector=None):
        if rotors != None:
            self._rotors = rotors
        else:
            self._rotors = [get_ROTOR_I(), get_ROTOR_II(), get_ROTOR_III()]

        if plugboard != None:
            self._plugboard = plugboard
        else:
            self._plugboard = PLUGBOARD_DEFAULT

        if reflector != None:
            self._reflector = reflector
        else:
            self._reflector = UKW_B

    def get_position(self):  # returns all enigma's rotors' positions
        position = ''
        for rotor in self._rotors:
            position += rotor._position
        return position

    # sets atributes - without exceptions because the were included in constructors
    def set_rotors(self, new_rotors):
        self._rotors = new_rotors

    def set_reflector(self, new_reflector):
        self._reflector = new_reflector

    def set_position(self, new_position):
        if len(new_position) != len(self._rotors):
            raise WrongLenError
        else:
            for i in range(len(self._rotors)):
                self._rotors[i]._position = self._rotors[i].set_position(
                    new_position[i])

    def set_ring_settings(self, new_ring_settings):
        if len(new_ring_settings) != len(self._rotors):
            raise WrongLenError
        else:
            for i in range(len(self._rotors)):
                self._rotors[i]._ring_settings = self._rotors[i].set_ring_setting(
                    new_ring_settings[i])

    def set_plugboard(self, new_plugboard):
        self._plugboard = new_plugboard

    def rotate_enigma(self):  # rotates whole enigma every one letter
        if self._rotors[1]._position == self._rotors[1]._notch:
            self._rotors[0].rotate_position()
        self._rotors[-1].rotate_position()
        index = len(self._rotors) - 2
        while index > 0:
            prev_rotor_position = self._rotors[index + 1]._position
            prev_rotor_notch = self._rotors[index + 1]._notch
            condition1 = prev_letter(prev_rotor_position) == prev_rotor_notch
            condition2 = self._rotors[index]._position == self._rotors[index]._notch
            if condition1 or condition2:
                self._rotors[index].rotate_position()
            index -= 1

    def encrypt_letter(self, letter):
        letter = letter.upper()
        if letter not in alphabet:
            raise NotAcceptableCharsError
        self.rotate_enigma()
        letter = self._plugboard.reflect(letter)  # plugboard swap
        letter_index = find_index(alphabet, letter)

        for rotor in reversed(self._rotors):  # one way encryption
            shift = ord(rotor._position) - first_letter_ord
            letter = chr((letter_index + shift) %
                         len_alphabet + first_letter_ord)
            letter = rotor._dict[letter]
            letter_index = (ord(letter) - ord(rotor._position) +
                            len_alphabet) % len_alphabet

        letter = alphabet[letter_index]  # reflector reflect
        letter = self._reflector.reflect(letter)
        letter_index = find_index(alphabet, letter)

        for rotor in self._rotors:  # second way encryption
            shift = ord(rotor._position) - first_letter_ord
            letter = chr((letter_index + shift) %
                         len_alphabet + first_letter_ord)
            rotor_second_path = rotor.find_letter(letter)
            letter = alphabet[rotor_second_path]
            letter_index = (ord(letter) - ord(rotor._position) +
                            len_alphabet) % len_alphabet

        letter = alphabet[letter_index]  # second plugboard swap
        letter = self._plugboard.reflect(letter)
        return letter

    def encrypt_text(self, text):
        encrypted_text = ""
        for char in text:
            if char != ' ':
                encrypted_char = self.encrypt_letter(char)
            else:
                encrypted_char = ' '
            encrypted_text += encrypted_char
        return encrypted_text

    # encrypt text to file using terminal
    def encrypt_text_to_file(self, write_path):
        text = input('Enter message here-> ')
        encrypted_text = self.encrypt_text(text)
        with open(write_path, 'w') as file_handle:
            file_handle.write(encrypted_text)

    def encrypt_file_to_file(self, write_path, read_path):  # encrypt file to file
        with open(write_path, 'w') as write_path_handle:
            with open(read_path, 'r') as read_file_handle:
                for line in read_file_handle:
                    line = line.rstrip()
                    encrypted_line = self.encrypt_text(line)
                    write_path_handle.write(encrypted_line)
                    write_path_handle.write('\n')


if __name__ == "__main__":
    e1 = Enigma()
    e1.set_ring_settings([1, 1, 1])  # set enigma's settings here

    parser = argparse.ArgumentParser(  # call of function either encrypt_file_to_file or encrypt_text_to_file
        description='Encrypts text in enigma cipher')
    parser.add_argument('-w', '--write_path', type=str, metavar='',
                        required=True, help='Path to write encrypted text')
    parser.add_argument('-r', '--read_path', type=str, metavar='',
                        required=False, help='Path from which read text to encrypt')
    args = parser.parse_args()
    if args.read_path:
        e1.encrypt_file_to_file(args.write_path, args.read_path)
    else:
        e1.encrypt_text_to_file(args.write_path)
