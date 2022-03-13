alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
len_alphabet = len(alphabet)  # global constants describing alphabet
first_letter_ord = ord(alphabet[0])
last_letter_ord = ord(alphabet[-1])


class OddWiringLenError(Exception):
    pass


class DuplicatedCharsError(Exception):
    pass


class WrongLenError(Exception):
    pass


class NotAcceptableCharsError(Exception):
    pass


class WiringNecessaryError(Exception):
    pass


def find_index(chars, letter):
    for i in range(len(chars)):
        if chars[i] == letter:
            return i


def split(word):
    return [char for char in word]


def listToString(list):
    str = ""
    for element in list:
        str += element
    return str


def prev_letter(letter):  # returns previous letter in alphabet, also works with A->Z
    prev_letter_num = (ord(letter) - 1 - first_letter_ord +
                       len_alphabet) % len_alphabet + first_letter_ord
    return chr(prev_letter_num)


class Plugboard():
    def __init__(self, wiring=None):
        if wiring == None:
            self._wiring = ""
        elif len(wiring) % 2 != 0:
            raise OddWiringLenError
        elif not self.is_unique(wiring):
            raise DuplicatedCharsError
        elif not self.is_correct(wiring):
            raise NotAcceptableCharsError
        else:
            self._wiring = wiring

    def get_same_plugboard(self):  # will be used in GUI
        return Plugboard(self._wiring)

    def is_unique(self, wiring):  # checks if wiring has duplicated chars
        for char in wiring:
            if wiring.count(char) > 1:
                return False
        return True

    def is_correct(self, wiring):  # checks if wiring has eligible chars
        for char in wiring:
            if ord(char) < first_letter_ord or ord(char) > last_letter_ord:
                return False
        return True

    def set_wiring(self, new_wiring):
        self._wiring = new_wiring

    def reflect(self, letter):  # swaps letter with the one conneted to the letter in reflector's wiring
        if letter not in self._wiring:
            return letter
        i = find_index(self._wiring, letter)
        if i % 2 == 0:
            return self._wiring[i+1]
        else:
            return self._wiring[i-1]


class Reflector(Plugboard):
    def __init__(self, wiring=None, name=None):
        super().__init__(wiring)
        self._name = name

    def get_same_reflector(self):  # will be used in GUI
        return Reflector(self._wiring, self._name)


class Rotor(Reflector):
    def __init__(self, wiring=None, notch=None, ring_settings=None, position=None, name=None):
        super().__init__(wiring, name)
        if wiring == None:
            raise WiringNecessaryError
        elif len(wiring) != len_alphabet:
            raise WrongLenError
        elif wiring != None:
            self._wiring = wiring

        # this block sets atributes from constructor
        self._notch = self.set_notch(notch)
        self._ring_settings = self.set_ring_setting(
            ring_settings)  # adds atribute 'dict'
        # sets rotor's wiring depending on ring's settings
        self._position = self.set_position(position)
        self._dict = self.rotor_to_dict()
        self.rotor_in_position()

    def get_same_rotor(self):  # will be used in GUI
        wiring = self._wiring
        rotor = Rotor(self._wiring, self._notch,
                      self._ring_settings, self._position, self._name)
        rotor.set_wiring(wiring)
        rotor._dict = rotor.rotor_to_dict()
        return rotor

    def set_notch(self, new_notch):  # sets appropriate notch
        if new_notch == None:
            self._notch = "A"
        elif not self.is_correct(new_notch):
            raise NotAcceptableCharsError
        elif not self.is_unique(new_notch):
            raise DuplicatedCharsError
        else:
            self._notch = new_notch
        return self._notch

    def set_position(self, new_position):  # sets appropriate position
        if new_position == None:
            self._position = 'A'
        elif len(new_position) != 1:
            raise WrongLenError
        else:
            self._position = new_position
        return self._position

    # sets appropriate ring's settings thus changes rotor's wiring and dict
    def set_ring_setting(self, new_ring_setting):
        if new_ring_setting == None:
            self._ring_settings = 0
        elif new_ring_setting >= 0 and new_ring_setting <= len_alphabet - 1:
            self._ring_settings = new_ring_setting
        else:
            raise WrongLenError
        self.rotor_in_position()
        self._dict = self.rotor_to_dict()
        return self._ring_settings

    def rotor_in_position(self):  # rotates rotor's wiring 'ring's settings times'
        temp_wiring = split(self._wiring)
        for i in range(len(temp_wiring)):
            shifted_letter_num = (
                ord(temp_wiring[i]) - first_letter_ord + self._ring_settings) % len_alphabet + first_letter_ord
            temp_wiring[i] = chr(shifted_letter_num)
        self._wiring = listToString(temp_wiring)
        for i in range(self._ring_settings):
            self._wiring = self.rotate_wiring()

    def find_letter(self, letter):  # returns letter's index in wiring
        for i in range(len(self._wiring)):
            if self._wiring[i] == letter:
                return i

    def rotate_wiring(self):
        last = self._wiring[-1]
        shifted_wiring = self._wiring[:-1]
        self._wiring = last + shifted_wiring
        return self._wiring

    # changes current rotor's position for next letter, works with Z->A
    def rotate_position(self):
        next_position_num = (
            ord(self._position) - first_letter_ord + 1) % len_alphabet + first_letter_ord
        self._position = chr(next_position_num)

    def rotor_to_dict(self):  # return dictionary made from wiring
        rotor_dict = {}
        for i in range(len(self._wiring)):
            rotor_dict[chr(i+first_letter_ord)] = self._wiring[i]
        return rotor_dict


# global constants - no function changes these constants
PLUGBOARD_DEFAULT = Plugboard()
UKW_B = Reflector(wiring="BRCUDHEQFSGLIPJXKNMOTZVWAY", name="UKW-B")
UKW_C = Reflector(wiring="AFBVCPDJEIGOHYKRLZMXNWTQSU", name="UKW-C")

#using getters because rotors will be changed and we don't
#want to make them global constants


def get_ROTOR_I():
    return Rotor(wiring="EKMFLGDQVZNTOWYHXUSPAIBRCJ", notch="Q", name="I")


def get_ROTOR_II():
    return Rotor(wiring="AJDKSIRUXBLHWTMCQGZNPYFVOE", notch="E", name="II")


def get_ROTOR_III():
    return Rotor(wiring="BDFHJLCPRTXVZNYEIWGAKMUSQO", notch="V", name="III")


def get_ROTOR_IV():
    return Rotor(wiring="ESOVPZJAYQUIRHXLNFTGKDCMWB", notch="J", name="IV")


def get_ROTOR_V():
    return Rotor(wiring="VZBRGITYUPSDNHLXAWMJQOFECK", notch="Z", name="V")


def get_5ROTORS():
    return [get_ROTOR_I(), get_ROTOR_II(), get_ROTOR_III(), get_ROTOR_IV(), get_ROTOR_V()]


def get_3ROTORS():
    return [get_ROTOR_I(), get_ROTOR_II(), get_ROTOR_III()]


def get_Reflectors():
    return [UKW_B, UKW_C]
