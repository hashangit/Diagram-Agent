import os
import importlib.util
import config

def load_example(diagram_type):
    try:
        module_name = f"{diagram_type}_example"
        module_path = os.path.join(config.EXAMPLES_DIR, f"{module_name}.py")
        
        if not os.path.exists(module_path):
            raise FileNotFoundError(f"Example file for {diagram_type} not found")
        
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        example_var_name = diagram_type
        if hasattr(module, example_var_name):
            return getattr(module, example_var_name)
        else:
            raise AttributeError(f"Example variable '{example_var_name}' not found in {module_name}.py")
    except Exception as e:
        raise Exception(f"Error loading example for {diagram_type}: {str(e)}")

# Add more utility functions as needed