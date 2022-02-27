import re


class TableGenerator:
    TABLE_OF_CONTENT_HEADER = '## SPIS TREŚCI'

    def __init__(self, file_path):
        self.file_path = file_path
        self.file_lines = self.get_file_lines()
        self.sections = self.get_sections()
        self.file_header = self.file_lines[0].replace('\n', '').strip()
        self.table_of_contents = self.generate_table_of_contents()

    def get_file_lines(self):
        with open(self.file_path, 'r', encoding='UTF-8') as f:
            return f.readlines()

    @staticmethod
    def get_level(line):
        hash_count = 0
        for sign in line:
            if sign == '#':
                hash_count += 1
            else:
                return hash_count - 2

    def get_sections(self):
        sections = []
        for line in self.file_lines:
            if line.startswith('##') and line != self.TABLE_OF_CONTENT_HEADER:
                line = line.strip()
                level = self.get_level(line)
                line = line.replace('#', '').strip()
                sections.append((level, line))
        return sections

    def generate_table_of_contents(self):
        table = f'{self.TABLE_OF_CONTENT_HEADER}\n'
        for level, section in self.sections:
            indent = level * "\t"
            table += f'{indent}* [{section}](#{section.replace(" ", "-")})\n'
        return table

    def generate(self):
        with open(self.file_path, 'w', encoding='UTF-8') as f:
            f.write(self.file_header)
            f.write('\n')
            f.write(self.table_of_contents)
            f.write('\n')
            for line in self.file_lines:
                cleaned_line = line.replace('\n', '').strip()
                if cleaned_line not in [self.file_header, self.TABLE_OF_CONTENT_HEADER] and not re.match('\* \[.*]\(#.*\)$', cleaned_line):
                    f.write(line)


if __name__ == '__main__':
    file_path = 'GIT.md'
    TableGenerator(file_path).generate()
