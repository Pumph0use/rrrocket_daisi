import subprocess

from rrrocket_retriever import get_latest_rrrocket_release


def process_replay(file_path: str):
    bin_path = get_latest_rrrocket_release()

    result = subprocess.check_output([bin_path, '-n', r'41805C0A4C99046708C38B9C735919D4.replay'])

    return [{'type': 'json', 'data': json.dumps(result.decode('utf-8'))}]

