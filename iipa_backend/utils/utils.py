import contextlib
import importlib.util
import io
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
