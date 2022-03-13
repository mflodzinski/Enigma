import pytest
from rotor import *
from enigma import *


def test_prev_letter_normal():
    letter = 'D'
    previous_letter = prev_letter(letter)
    assert previous_letter == 'C'


def test_prev_letter_first():
    letter = 'A'
    previous_letter = prev_letter(letter)
    assert previous_letter == 'Z'


def test_listToString():
    list = ['a', '34', '!V']
    string = listToString(list)
    assert string == 'a34!V'


def test_split():
    word = 'turing'
    list = split(word)
    assert list == ['t', 'u', 'r', 'i', 'n', 'g']


def test_find_index():
    chars = 'ABFHUWYRG'
    letter = 'W'
    assert find_index(chars, letter) == 5


def test_no_find_index():
    chars = 'ABFHUWYRG'
    letter = 'N'
    assert find_index(chars, letter) == None


def test_construct_plugboard():
    p1 = Plugboard()
    assert p1._wiring == ''

    p2 = Plugboard('QWEASDZXCVFRTG')
    assert p2._wiring == 'QWEASDZXCVFRTG'

    with pytest.raises(DuplicatedCharsError):
        Plugboard('QQWEAS')

    with pytest.raises(OddWiringLenError):
        Plugboard('CDF')

    with pytest.raises(NotAcceptableCharsError):
        Plugboard('A1FV')


def test_reflect():
    letter = 'V'
    p1 = Plugboard()
    ref_letter = p1.reflect(letter)
    assert ref_letter == 'V'

    p2 = Plugboard('ANHSGVFBIK')
    ref_letter = p2.reflect(letter)
    assert ref_letter == 'G'


def test_construct_reflector():
    r1 = Reflector(wiring='ASDFGHJKLZ', name='UKW-X')
    assert r1._name == 'UKW-X'
    assert r1._wiring == 'ASDFGHJKLZ'

    r2 = Reflector(wiring='BVNJ')
    assert r2._name == None
    assert r2._wiring == 'BVNJ'

    with pytest.raises(OddWiringLenError):
        Reflector('ASM')


def test_construct_rotor():
    r1 = Rotor(wiring='QWERTYUIOPASDFGHJKLZXCVBNM')
    assert r1._wiring == 'QWERTYUIOPASDFGHJKLZXCVBNM'
    assert r1._notch == 'A'
    assert r1._ring_settings == 0
    assert r1._position == 'A'

    r2 = Rotor(wiring="BRCUDHEQFSGLIPJXKNMOTZVWAY",
               notch='T', ring_settings=4, position='E')
    assert r2._wiring != 'BRCUDHEQFSGLIPJXKNMOTZVWAY'
    assert r2._notch == 'T'
    assert r2._ring_settings == 4
    assert r2._position == 'E'

    with pytest.raises(WrongLenError):
        Rotor(wiring='ASDF')

    with pytest.raises(WiringNecessaryError):
        Rotor(notch='H', ring_settings=3)

    with pytest.raises(NotAcceptableCharsError):
        Rotor(wiring='ABC$')


def test_set_atributes():
    r1 = Rotor(wiring='BDFHJLCPRTXVZNYEIWGAKMUSQO')
    r1.set_position('B')
    r1.set_notch('F')
    r1.set_ring_setting(1)
    assert r1._notch == 'F'
    assert r1._position == 'B'
    assert r1._ring_settings == 1
    assert r1._wiring == 'PCEGIKMDQSUYWAOZFJXHBLNVTR'
    dict = r1._dict
    bool = 1
    for i in range(len(r1._wiring)):
        key_letter = alphabet[i]
        value_letter = r1._wiring[i]
        bool *= (dict[key_letter] == value_letter)
    assert bool == 1

    with pytest.raises(NotAcceptableCharsError):
        r1.set_notch('#')


def test_rotor_in_position():
    r1 = Rotor(wiring='AJDKSIRUXBLHWTMCQGZNPYFVOE')
    r1.set_ring_setting(1)
    assert r1._wiring == 'FBKELTJSVYCMIXUNDRHAOQZGWP'


def test_find_letter():
    r1 = Rotor(wiring='AJDKSIRUXBLHWTMCQGZNPYFVOE')
    index = r1.find_letter('X')
    assert index == 8


def test_rotor_to_dict():
    r1 = Rotor(wiring='AJDKSIRUXBLHWTMCQGZNPYFVOE')
    dict = r1._dict
    bool = 1
    for i in range(len(r1._wiring)):
        key_letter = alphabet[i]
        value_letter = r1._wiring[i]
        bool *= (dict[key_letter] == value_letter)
    assert bool == 1


def test_rotate_wiring():
    r1 = Rotor(wiring='FBKELTJSVYCMIXUNDRHAOQZGWP')
    r1.rotate_wiring()
    wiring = r1._wiring
    assert wiring == 'PFBKELTJSVYCMIXUNDRHAOQZGW'


def test_rotate_position():
    r1 = Rotor(wiring='FBKELTJSVYCMIXUNDRHAOQZGWP', position='G')
    r1.rotate_position()
    position = r1._position
    assert position == 'H'

    r2 = Rotor(wiring='FBKELTJSVYCMIXUNDRHAOQZGWP', position='Z')
    r2.rotate_position()
    position = r2._position
    assert position == 'A'


def test_construct_enigma():
    e1 = Enigma()
    rotor_names = [rotor._name for rotor in e1._rotors]
    assert rotor_names == ['I', 'II', 'III']
    assert e1._plugboard == PLUGBOARD_DEFAULT
    assert e1._reflector == UKW_B


def test_set_rotors():
    e1 = Enigma()
    rotorII = get_ROTOR_II()
    rotorIII = get_ROTOR_III()
    rotorI = get_ROTOR_I()
    new_rotors = [rotorII, rotorIII, rotorI]
    e1.set_rotors(new_rotors)
    rotor_names = [rotor._name for rotor in e1._rotors]
    assert rotor_names == ['II', 'III', 'I']


def test_set_position():
    e1 = Enigma()
    new_position = 'UJR'
    e1.set_position(new_position)
    rotors = e1._rotors
    assert rotors[0]._position == 'U'
    assert rotors[1]._position == 'J'
    assert rotors[2]._position == 'R'


def test_set_ring_settings():
    e1 = Enigma()
    new_ring_settings = [23, 6, 2]
    e1.set_ring_settings(new_ring_settings)
    rotors = e1._rotors
    assert rotors[0]._ring_settings == 23
    assert rotors[1]._ring_settings == 6
    assert rotors[2]._ring_settings == 2
    assert rotors[0]._wiring == 'CIDANSWKQLTVEURPMXFYOZGBHJ'
    assert rotors[1]._wiring == 'VELBUKGPJQYOXADHRNCZSIWMFT'
    assert rotors[2]._wiring == 'SQDFHJLNERTVZXBPAGKYICMOWU'

    bool = 1
    for i in range(len(e1._rotors)):
        rotor = e1._rotors[i]
        dict = rotor._dict
        for j in range(len(rotor._wiring)):
            key_letter = alphabet[j]
            value_letter = rotor._wiring[j]
            bool *= (dict[key_letter] == value_letter)
    assert bool == 1


def test_set_ring_settings_same_rotors():
    e1 = Enigma()
    new_rotors = [get_ROTOR_I(), get_ROTOR_III(), get_ROTOR_III()]
    e1.set_rotors(new_rotors)
    e1.set_ring_settings([2, 3, 6])
    rotors = e1._rotors
    assert rotors[0]._ring_settings == 2
    assert rotors[1]._ring_settings == 3
    assert rotors[2]._ring_settings == 6


def test_set_wrong_ring_settings():
    e1 = Enigma()
    with pytest.raises(WrongLenError):
        e1.set_ring_settings([2, 3])

    with pytest.raises(WrongLenError):
        e1.set_ring_settings([3, 5, 27])


def test_rotate_enigma_normal():
    e1 = Enigma()
    e1.set_position('FBN')
    e1.rotate_enigma()
    assert e1.get_position() == 'FBO'


def test_rotate_enigma_notch():
    e1 = Enigma()
    e1.set_position('BTV')
    e1.rotate_enigma()
    assert e1.get_position() == 'BUW'


def test_encrypt_text():
    p1 = Plugboard(wiring='BGHYEDOP')
    e1 = Enigma(rotors=get_3ROTORS(), plugboard=p1, reflector=UKW_C)
    e1.set_position('HBY')
    e1.set_ring_settings([2, 2, 1])
    text = 'DOBRA ROBOTA'
    encoded_text = e1.encrypt_text(text)
    assert encoded_text == 'EHFOQ NWALCK'


def test_encrypt_letter():
    p1 = Plugboard(wiring='BGHYEDOP')
    e1 = Enigma(rotors=get_3ROTORS(), plugboard=p1, reflector=UKW_C)
    e1.set_position('HBY')
    e1.set_ring_settings([2, 2, 1])
    letter = 'D'
    encoded_letter = e1.encrypt_letter(letter)
    assert encoded_letter == 'E'









    
