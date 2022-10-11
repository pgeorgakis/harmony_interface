from inputs_from_user.config import inputs # noqa
from pathlib import Path
import shutil

DATA_PATH = Path("inputs_from_user/data")
NEW_DATA_PATH = Path("inputs_from_user/new_data")

for input in inputs:
    file_name = inputs[input].split("/")[-1]
    file_extension = file_name.split(".")[1]
    new_file_name = "{}.{}".format(input, file_extension)
    shutil.copy(DATA_PATH / file_name, NEW_DATA_PATH / new_file_name)
