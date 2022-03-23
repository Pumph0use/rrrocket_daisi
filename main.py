import subprocess
import json
from rrrocket_retriever import get_latest_rrrocket_release
from rrrocket_processor import process_match_overview


def process_replay(file_path: str):
    bin_path = get_latest_rrrocket_release()

    result = subprocess.check_output([bin_path, '-n', r'41805C0A4C99046708C38B9C735919D4.replay'])
    result = json.loads(result.decode('utf-8'))

    blue, orange = process_match_overview(result['properties'])

    return [blue, orange]


# if __name__ == '__main__':
#     result = subprocess.check_output(['rrrocket.exe', '-n', r'41805C0A4C99046708C38B9C735919D4.replay'])
#     result = json.loads(result.decode('utf-8'))
#
#     blue, orange = process_match_overview(result['properties'])