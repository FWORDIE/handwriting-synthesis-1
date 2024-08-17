import numpy as np
import sys
from handwriting_synthesis import Hand
from timeit import default_timer as timer
import time
import random


GSBs = []


class GSB:
    def __init__(self, style: int, bais: int, risky=False, line_height=2, chars=60):
        self.style = style
        self.bais = bais
        self.risky = risky
        self.line_height = line_height
        self.chars = chars


GSBs.append(GSB(0, 0.4))
GSBs.append(GSB(0, 2))
GSBs.append(GSB(0, 12))
GSBs.append(GSB(1, 0.6))
GSBs.append(GSB(1, 12))
GSBs.append(GSB(2, 8, True))
# GSBs.append(GSB(2,12,True))
GSBs.append(GSB(3, 0.6))
GSBs.append(GSB(3, 12))
GSBs.append(GSB(4, 2, True))
# GSBs.append(GSB(4,12,True))
GSBs.append(GSB(5, 2))
GSBs.append(GSB(5, 7))
GSBs.append(GSB(6, 2))
GSBs.append(GSB(7, 1, True))
# GSBs.append(GSB(7,12,True))
GSBs.append(GSB(8, 0.4, True))
# GSBs.append(GSB(8,1,True))
GSBs.append(GSB(9, 0.8, True))
# GSBs.append(GSB(10,1,True))
GSBs.append(GSB(10, 2))
# GSBs.append(GSB(11,0.4,True))
GSBs.append(GSB(11, 12, True))
GSBs.append(GSB(12, 2))
GSBs.append(GSB(12, 12))


def formater(letter='testing letter', subject='test', chars=60, styleVar=0, baisVar=1, line_height=30, dither=0, noiseVal=0, line_break=1.2, margins=50):
    print(f'STARTING: {subject}')
    print(f'---PARAMS---')
    print(f'Chars: {chars}')
    print(f'Style: S{styleVar} B{baisVar}')
    print(f'Dither: {dither}')
    print(f'Line Height: {line_height}')
    print(f'Noise: {noiseVal}')
    print(f'Para Gap: {line_break}')
    print(f'Margins: {margins}')

    print('FORMATING')

    max_length = chars
    charsAllowed = {'\n', 'O', 'W', ';', 'j', 'r', 'R', 'n', 's', 'D', 'A', '\x00', '.', 'E', 'o', 'K', 't', 'p', 'N', 'w', '9', '3', 'l', 'T', 'f', 'G', 'v', 'a', '1', 'F', 'P', '#', 'V', ':', 'x',
                    'B', '(', '!', 'C', 'H', ')', '5', '4', 'L', 'S', 'y', "'", '0', 'c', 'J', 'U', 'd', 'h', 'e', 'k', '8', 'z', ' ', '2', ',', 'g', 'Y', 'q', '"', '?', '7', '-', '6', 'm', 'i', 'b', 'M', 'I', 'u'}
    hand = Hand()

    def replaceMissing(word: str):
        replacements = {'Q': 'q', 'Z': 'z', 'X': 'x', "—": "-", "ü": 'u', "é": 'e', "–": '-', 'ù': 'u', 'à': 'a', '&': 'and',
                        'ï': 'i', '[': '(', ']': ')', '¡': 'i', 'í': 'i', 'ñ': 'n', 'á': 'a', 'ó': 'o', 'ú': 'u', 'ú': 'u', '’': "'"}
        for old, new in replacements.items():
            word = word.replace(old, new)

        for char in word:
            if char not in charsAllowed:
                print(f"Unallowed character: {char}")
                word = word.replace(char, ' ')
        return word

    def splitter(text):
        parts = []
        temp = ''
        for char in text:
            if char == '\n':
                if temp:
                    parts.append(temp)
                    temp = ''
                parts.append('\n')
            elif char == ' ':
                if temp:
                    parts.append(temp)
                    temp = ''
            else:
                temp += char
        if temp:
            parts.append(temp)
        parts = [x for x in parts if x]
        return parts

    def splitText(text: str):
        lines = []
        words = splitter(text)
        # print(words)
        current_line: str = ''
        # print(words)
        for word in words:
            word = replaceMissing(word)
            if word == '\n':
                # print('newLine')
                lines.append(current_line)
                lines.append('\n')
                current_line = ""
            elif len(current_line) + len(word) + 1 <= max_length:
                current_line += (" " if current_line else "") + word
            else:
                lines.append(current_line)
                current_line = word

        lines.append(current_line)
        lines = [x for x in lines if x]
        newLines = []
        for line in lines:
            if line == '\n':
                newLines.append('')
            else:
                newLines.append(line)

        # print(newLines)
        return newLines

    def lines_adjust(lines):
        text = lines
        return splitText(text)

    lines = lines_adjust(letter)

    # usage demo
    biases = [baisVar for i in lines]
    styles = [styleVar for i in lines]
    stroke_colors = ['black' for i in lines]
    stroke_widths = [1 for i in lines]

    fileName = f'{subject}   S{styleVar}_B{baisVar}_L{line_height}_D{dither}_N{noiseVal}_G{line_break}_C{chars}_M{margins}'
    fileNameCleaned = fileName.replace(".", "-")
    hand.write(
        filename=f'letters/{fileNameCleaned}.svg',
        lines=lines,
        biases=biases,
        styles=styles,
        stroke_colors=stroke_colors,
        stroke_widths=stroke_widths,
        dither=0,
        line_height=line_height,
        margins=margins,
        noiseVal=noiseVal,
        line_break=line_break
    )

    print(f'FINISHED: {subject}')


# letterText = {
#     'name': 'Its-Only-Been-6-Months',
#     'lang': 'eng',
#     'body': """
#         My dearest Irene,

# I don't think I can accurately put into words the joy that fills my heart each time I see your beautiful face. The past six months that I have known you have been filled with an indescribable happiness and love that I never thought I would find.

# Thank you for being the ray of sunshine in my life, Irene. You are my everything, and I love you more than words can express.

# Forever yours,
# Matteus
#         """
# }

thisOne = {
    'name': 'My-Anchor-For-12-Years',
    'lang': 'eng',
    'body': """
        Dear Amirr,

I hope this letter finds you surrounded by the same love and warmth that you have blessed my life with for the past 12.5 years. As we celebrate yet another milestone together, I can't help but reflect on the incredible journey we have embarked on since our clueless 20-year-old selves met.

These past years have been a whirlwind of joy, happiness, and growth. We have experienced the highest of highs and navigated through the toughest challenges hand in hand. From carefree youngsters to responsible and nurturing parents-to-be, every step we took together has further deepened my love and admiration for you.

With all my love,
Nura
        """
}

if __name__ == '__main__':

    # print(sys.argv)
    # if len(sys.argv) > 1 and sys.argv[1] == 'formater':
    # Parse additional arguments if necessary
    # print(letterText['body'], subject='test', chars=60, styleVar=0, baisVar=1, line_height=5, dither=0, noiseVal=20)
    total = len(GSBs)
    x = 0
    totalTime = 0
    average = 0
    GSB = GSBs[random.randint(0, len(GSBs))]
    # start = time.time()
    formater(
        letter=thisOne["body"],
        subject=thisOne["name"],
        chars=random.randint(45, 70),
        styleVar=GSB.style,
        baisVar=GSB.bais,
        line_height=random.randint(25, 70),
        dither=(random.randint(1, 50)/10),
        noiseVal=(random.randint(1, 20)/10),
        line_break=(random.randint(0, 15)/10),
        margins=random.randint(40, 70)
    )
    
    
    # x += 1

    # end = time.time()
    # thistime = end - start
    # totalTime += thistime
    # elapsedStr = time.strftime('%H:%M:%S', time.gmtime(thistime))
    # totalStr = time.strftime('%H:%M:%S', time.gmtime(totalTime))
    # averageStr = time.strftime('%H:%M:%S', time.gmtime(totalTime/x))
    # timeLeft = (total - x ) * (totalTime/x)
    # timeLeftStr = time.strftime('%H:%M:%S', time.gmtime(timeLeft))
    # print(f'Progress:{x}/{total}')
    # print(f'Time Taken:{elapsedStr}')
    # print(f'Time Total:{totalStr}')
    # print(f'Time Left:{timeLeftStr}')
