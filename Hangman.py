import os
import signal
import random
import time
from string import ascii_lowercase, ascii_uppercase
from enum import Enum
# import colorama
# colorama.init()


# # Call one latin lowercase letter
class ValidationError(BaseException):
    em = {4001: "Назовите !!ОДНУ!! латинскую букву в нижнем регистре.", \
          4002: "Назовите одну латинскую букву в !!НИЖНЕМ!! регистре.", \
          4003: "Назовите одну !!ЛАТИНСКУЮ!! букву в нижнем регистре.", \
          4004: "Эта !!БУКВА!! уже называлась в этой попытке."} # This !! LETTER !! already called in this attempt

WORDS = ['skillfactory', 'testing', 'blackbox', 'pytest', 'unittest', 'coverage']
MAX_WRONG = 4 # maximum number of errors - максимальное количество ошибок
used = []  # letters already guessed or self.spoken_letters = []. I will solve later on.

# result for hashing - результат для хеширования
class Result(Enum):
    FAIL = 0
    WIN = 1
    CONTINUE = -1

def random_new_word(words_list):
    return random.choice(words_list)

class Game():
    def __init__(self):
        self.guessed_word = random_new_word(WORDS)
        self.hidden_word = '_' * len(self.guessed_word)
        self.guess_count = 0
        self.spoken_letters = []

    def guess_letter(self, letter):
        if len(letter) != 1: #
            raise ValidationError(4001) # "Назовите одну букву."
        if letter in ascii_uppercase:
            raise ValidationError(4002) # нелатин
        if letter not in ascii_lowercase:
            raise ValidationError(4003) # Верхний
        if letter in self.spoken_letters:
            raise ValidationError(4004) # уже
        self.spoken_letters.append(letter)
        if letter in self.guessed_word:
            self.hidden_word = self.change_hidden_word()
            return True
        else:
            self.guess_count += 1
            return False

    def change_hidden_word(self):
        current_state = []
        for letter in self.guessed_word:
            if letter in self.spoken_letters:
                current_state.append(letter)##
            else:
                current_state.append('_')
        return ''.join(current_state)

    def get_game_result(self):
        if self.guess_count >= MAX_WRONG:
            return Result.FAIL
        elif self.guessed_word == self.change_hidden_word():##
            return Result.WIN
        else:
            return Result.CONTINUE

def make_rus(count):
    count = MAX_WRONG - count
    if count == 0:
        return f'{count} штрафных очков'
    elif count == 1:
        return f'{count} штрафное очко'
    else:
        return f'{count} штрафных очка'

def gameplay():
    game = Game()
    print('\033[4m\033[47m\033[46m{}\033[0m'.format('*' * 75))
    print('Угадайте слово из {} букв,'.format(len(game.guessed_word)), 'вводя в консоли по','\033[4m\033[33m\033[44m{}\033[0m'.format('ОДНОЙ'),'букве.')
    print('Загаданное слово содержит только','\033[4m\033[33m\033[44m{}\033[0m'.format('ЛАТИНСКИЕ'),'буквы в','\033[4m\033[33m\033[44m{}\033[0m'.format('НИЖНЕМ'),'регистре.')
    print('За каждую неправильную букву начисляется 1 штрафное очко. Если наберете',MAX_WRONG,'штрафных очка - проиграете.')
    print('\033[4m\033[47m\033[46m{}\033[0m'.format('*' * 75))
    print(game.hidden_word)

    while True:
        letter = str(input())

        try:
            result = game.guess_letter(letter)
            if result is True:
                print('Вы угадали букву в этом слове!!!')
            else:
                print('Неудачная попытка. У вас {}.'.format(make_rus(game.guess_count)))
        except ValidationError as e:
            print("Ошибка: %s" % e.em[e.args[0]])

        print(game.hidden_word.upper())

        result = game.get_game_result()
        if result == Result.WIN:
            print("\033[5m\033[34m\033[43m{}\033[0m".format('Вы угадали все буквы в этом слове!!!'))
            break
        elif result == Result.FAIL:
            print('Вы проиграли!?!')
            break
        else:
            time.sleep(0.1)

if __name__ == '__main__':
    print('*' * 75)
    print('Сочетание клавиш Ctrl+C для выхода...')
    signal.signal(signal.SIGINT, lambda *_: os._exit(1))
    while True:
        gameplay()
