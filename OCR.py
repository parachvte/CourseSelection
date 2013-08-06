__author__ = 'Ryan'
from PIL import Image
import json


class CaptchaHandler:
    __white = "O"
    __black = "v"

    def __init__(self):
        self.__ranges = ((4, 12), (14, 22), (24, 32), (34, 42))
        self.image = None
        self.records = self._get_records()

    def _get_records(self):
        res = {}
        with open("attribute_codes.txt", "r") as F:
            while True:
                line = F.readline()
                if not line.strip():
                    break
                data = json.loads(line)
                char, code = data.items()[0]
                res[tuple(code)] = char
        return res

    def _to_ascii_matrix(self, image):
        pixels = image.load()
        self.width, self.height = image.size

        matrix = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                r, g, b = pixels[x, y]
                m = self.__white if (0.299 * r + 0.587 * g + 0.114 * b) > 180 else self.__black
                row.append(m)
            matrix.append(row)
        return matrix

    def _get_attribute_codes(self, matrix):
        attribute_codes = []
        for start, end in self.__ranges:
            code = []
            for y in range(start, end):
                min_x, max_x = 1000, -1
                for x in range(self.height):
                    if matrix[x][y] == self.__black:
                        min_x = min(min_x, x)
                        max_x = max(max_x, x)
                max_x = min(max_x, min_x + 5)
                col = 0
                for x in range(min_x, max_x + 1):
                    col = col * 2 + (matrix[x][y] == self.__black)
                code.append(col)
            attribute_codes.append(code)
        return attribute_codes

    def captcha_from_image(self, image_file):
        image = Image.open(image_file)

        matrix = self._to_ascii_matrix(image)
        self.attribute_codes = self._get_attribute_codes(matrix)
        self.chars = ""
        for code in self.attribute_codes:
            if tuple(code) in self.records:
                self.chars += self.records[tuple(code)]
            else:
                print self.chars
                return "unknown"
        return self.chars

    def save_attribute_codes(self, correct_chars):
        if len(self.attribute_codes) != len(correct_chars):
            print "length not equal: attribute_codes and correct_chars"
            raise AttributeError()
        with open("attribute_codes.txt", "a") as F:
            for char, code in zip(correct_chars, self.attribute_codes):
                if not tuple(code) in self.records:
                    self.records[tuple(code)] = char
                    data = {char: code}
                    F.write(json.dumps(data) + "\n")
