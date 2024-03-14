class SoundexEncoding:
    def __init__(self, file):
        self.__data = self.sanitize_file(file)
        self.__first_letter = ""
        self.__first_letter_code = ""
        self.__digit_code = ""

    '''
    Sanitize data in the file. Remove whitespaces, removes duplicates, converts to lower case
    '''

    def sanitize_file(self, file):
        sanitized_data = []
        file = open(file, 'r')  # Read the file
        # Read lines
        done_reading = False
        while not done_reading:
            line = file.readline().strip()  # read current line and trim whitespaces
            if line not in sanitized_data and line != "":
                sanitized_data.append(line.lower())
            if not line:
                done_reading = True

        return sanitized_data

    """
    Converts letter to digit
    """

    def convert_letter_to_digit(self, name):
        self.__first_letter = name[0]
        code = ""
        for letter in name:
            if letter in ['a', 'e', 'i', 'o', 'u', 'y', 'h', 'w']:
                code += "0"
            elif letter in ['b', 'v', 'f', 'p']:
                code += "1"
            elif letter in ['c', 'g', 'j', 'k', 'q', 'x', 's', 'z']:
                code += "2"
            elif letter in ['d', 't']:
                code += "3"
            elif letter in ['l']:
                code += "4"
            elif letter in ['m', 'n']:
                code += "5"
            elif letter in ['r']:
                code += "6"
        self.__first_letter_code = code[0]
        self.__digit_code = code

    '''
    Remove duplicated digits
    '''

    def remove_duplicate(self):
        non_duplicate_code = self.__digit_code[0]

        for digit in self.__digit_code:
            if digit != non_duplicate_code[-1]:
                non_duplicate_code += digit
        self.__digit_code = non_duplicate_code

    '''
    Remove zeros
    '''

    def remove_zero(self):
        non_zero_code = ""
        for digit in self.__digit_code:
            if digit != "0":
                non_zero_code += digit
        self.__digit_code = non_zero_code

    def final_digit_code(self):
        if self.__digit_code[0] == self.__first_letter_code:
            final_code = self.__first_letter + self.__digit_code[1:]
        else:
            final_code = self.__first_letter + self.__digit_code

        if len(final_code) > 4:
            self.__digit_code = final_code[:4]
        elif len(final_code) < 4:
            final_code += "0000"
            self.__digit_code = final_code[:4]
        else:
            self.__digit_code = final_code

    def get_soundex(self):
        soundex = {}
        for name in self.__data:
            self.convert_letter_to_digit(name)
            self.remove_duplicate()
            self.remove_zero()
            self.final_digit_code()
            if self.__digit_code not in soundex:
                soundex[self.__digit_code] = [name]
            else:
                soundex[self.__digit_code].append(name)

        return soundex

    '''
    Get names with same soundex
    '''

    def same_soundex(self):
        same_soundex = {}
        soundex = self.get_soundex()
        for code in sorted(soundex):
            if len(soundex[code]) != 1:
                same_soundex[code] = sorted(soundex[code])
        return same_soundex

    def __str__(self):
        same_soundex = self.same_soundex()
        for soundex in same_soundex:
            size = len(same_soundex[soundex])
            for i in range(size - 1):
                for j in range(i, size - 1):
                    print(f"{same_soundex[soundex][j].capitalize()} and {same_soundex[soundex][j+1].capitalize()} "
                          f"have the same Soundex encoding.")


if __name__ == '__main__':
    input_file = input("Enter the file name: ")
    soudex_encoding = SoundexEncoding(input_file)
    soudex_encoding.__str__()

