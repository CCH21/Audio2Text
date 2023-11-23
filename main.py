# @author  : Chen Chunhan
# @time    : 2023-11-22 22:07
# @function: The script is used to convert wav format audio into a text file.
# @version : 1.0.0
import argparse
import glob
import logging
import os
import shutil

from pydub import AudioSegment
from pydub.utils import make_chunks
import speech_recognition as sr


logging.basicConfig(format='[%(levelname)8s]  %(asctime)13s  %(message)s', level=logging.DEBUG)


def split_audio(input_file: str, tmp_path: str = './tmp/') -> None:
    logging.info('Initialize the temporary folder...')
    if os.path.exists(tmp_path):
        shutil.rmtree(tmp_path)
        logging.warning('Deleted the existing temporary folder.')
    os.mkdir(tmp_path)
    logging.info('Created the temporary folder.')
    audio = AudioSegment.from_file(input_file, 'wav')
    _size = 60000
    _max_chunk_num = 120
    chunks = make_chunks(audio, _size)
    if len(chunks) > _max_chunk_num:
        logging.error('The audio file is too long. Make sure that the audio file does not last more than 2 hours.')
        return
    logging.info('Split the audio file...')
    for i, chunk in enumerate(chunks):
        chunk_name = 'tmp_{:02d}.wav'.format(i + 1)
        chunk_path = os.path.join(tmp_path, chunk_name)
        chunk.export(chunk_path, 'wav')
    logging.info('Completed.')


def recognition(output_file: str, lang: str, tmp_path: str = './tmp/') -> None:
    recognizer = sr.Recognizer()
    chunk_names = glob.glob(os.path.join(tmp_path, '*.wav'))
    chunk_names.sort()
    total = len(chunk_names)
    res = ''
    for i, chunk_name in enumerate(chunk_names):
        with sr.AudioFile(chunk_name) as source:
            audio = recognizer.record(source)
            try:
                cur = recognizer.recognize_google(audio, language=lang)
                res += cur
                logging.info('{:.2f}% completed.'.format((i + 1) / total * 100))
            except sr.UnknownValueError:
                cur = '<Unknown Value Time: {}:00>'.format(i)
                res += cur
                logging.warning('Google Speech Recognition could not understand audio.')
            except sr.RequestError:
                logging.error('Could not request results from Google Speech Recognition Service.')
                return
    with open(output_file, mode='w', encoding='utf-8') as f:
        f.write(res)
        logging.info('Audio to text completed.')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='input audio file (*.wav)', required=True)
    parser.add_argument('-o', '--output', help='output text file (*.txt)', required=True)
    parser.add_argument('-l', '--lang', help='language type (en-US or zh-CN)', required=True)
    args = parser.parse_args()
    if not args.input.endswith('.wav'):
        logging.error('Unsupported input audio file.')
        return
    if not args.output.endswith('.txt'):
        logging.error('Unsupported output text file.')
        return
    if args.lang not in ('en-US', 'zh-CN'):
        logging.error('Unsupported language. Please set the argument -l/--lang to "en-US" or "zh-CN".')
        return
    split_audio(args.input)
    recognition(args.output, args.lang)


if __name__ == '__main__':
    main()
