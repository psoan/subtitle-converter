import re
import os

class SubtitleConverter:
    def __init__(self, subtitle) -> None:
        self.subtitle = subtitle

    def get_subtitle(self) -> str:
        with open(self.subtitle, 'r') as subtitle_file:
            subtitle_contents = subtitle_file.read()
            subtitle_file.close()
        return subtitle_contents

    def to_srt(self) -> str:
        subtitle_contents = self.get_subtitle()
        subtitle_contents = '\n'.join(subtitle_contents.split('\n')[1:])
        srt = ''
        line_number = 1
        lines = subtitle_contents.splitlines()
        for line in lines:
            pattern = r'(\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}\.\d{3})'
            replacement = r'00:\1 --> 00:\2'
            line = re.sub(pattern, replacement, line)
            if not line.strip():
                if line_number == 1:
                    srt += str(line_number) + '\n'
                else:
                    srt += '\n' + str(line_number) + '\n'
                line_number += 1 
            else:
                srt += line + '\n'
        file_name = os.path.splitext(self.subtitle)[0]
        new_file_name = f'{file_name}.srt'
        with open(f'{new_file_name}', 'w') as new_file:
            new_file.write(srt)
            new_file.close()
        return new_file_name
    
    def to_vtt(self) -> str:
        subtitle_contents = self.get_subtitle()
        pattern = r"\n(\d+)\n(?:00:)?(\d{2}:\d{2}:\d{2})\.(\d{3}) --> (?:00:)?(\d{2}:\d{2}:\d{2})\.(\d{3})\n"
        replacement = r"\1\n\2.\3 --> \4.\5\n"
        vtt = re.sub(pattern, replacement, subtitle_contents)
        vtt += 'WEBVTT' + '\n' + vtt
        file_name = os.path.splitext(self.subtitle)[0]
        new_file_name = f'{file_name}.vtt'
        with open(f'{new_file_name}', 'w') as new_file:
            new_file.write(vtt)
            new_file.close()
        return new_file_name
