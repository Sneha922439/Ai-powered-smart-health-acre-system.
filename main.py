from pathlib import Path
import importlib.util

backend_main_path = Path(__file__).resolve().parent / "disease-predictor" / "backend" / "main.py"
if not backend_main_path.exists():
    raise FileNotFoundError(f"Backend entrypoint not found: {backend_main_path}")

spec = importlib.util.spec_from_file_location("backend_main", backend_main_path)
backend_main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(backend_main)

app = backend_main.app
