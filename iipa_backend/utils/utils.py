import importlib.util


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
