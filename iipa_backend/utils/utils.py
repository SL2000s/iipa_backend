import contextlib
import importlib.util
import io
import os
import shutil
import sys
# import traceback


def get_class(module_path, class_name):
    spec = importlib.util.spec_from_file_location(class_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    class_ = getattr(module, class_name)
    return class_


def instantiate_class(module_path, class_name):
    class_ = get_class(module_path, class_name)
    instance = class_()
    return instance


def execute_code_str(code):
    buffer = io.StringIO()
    error_str = None
    try:
        with contextlib.redirect_stdout(buffer):
            exec(code)
    except Exception as e:
        error_type = type(e).__name__
        error_message = str(e)
        error_str = f'{error_type}: {error_message}'
        # error = traceback.format_exc()
    output = error_str if error_str else buffer.getvalue()
    return output


async def a_capture_prints(method):
    buffer = io.StringIO()
    original_stdout = sys.stdout
    try:
        sys.stdout = buffer
        await method()
    finally:
        sys.stdout = original_stdout
    captured_prints = buffer.getvalue()
    buffer.close()
    return captured_prints


def find_all_occurrences(text, substring):
    indices = []
    start = 0
    while True:
        start = text.find(substring, start)
        if start == -1:
            break
        indices.append(start)
        start += len(substring)
    return indices


def str2md(text):
    """Makes sure two new lines are used everywhere outside code blocks"""
    def fix_newlines(text):
        while '\n\n' in text:
            text = text.replace('\n\n', '\n')
        text = text.replace('\n', '\n\n')
        return text
    code_block_indices = find_all_occurrences(text, '```')
    assert(len(code_block_indices) & 1 == 0)
    sb = []
    last_end = 0
    for i in range(0, len(code_block_indices), 2):
        start_ind, end_ind = code_block_indices[i:i+2]
        sb.append(fix_newlines(text[last_end:start_ind]))
        sb.append(text[start_ind:end_ind])
        last_end = end_ind
    sb.append(fix_newlines(text[last_end:]))
    md = ''.join(sb)
    return md


def delete_directory(directory_path: str):
    """
    Deletes the specified directory if it exists.
    
    Parameters:
        directory_path (str): The path of the directory to delete.
    """
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        shutil.rmtree(directory_path)
