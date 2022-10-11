import os
import json
from pathlib import Path
import shutil
import subprocess
from inputs_from_user.config import inputs # noqa
from inputs_from_user.config import outputs # noqa

USER_INPUT_PATH = Path("inputs_from_user")
BASE_OUTPUT_PATH = Path("../harmony_interface/protos")
INPUT_PATH = Path("inputs_from_user")
INIT_FILE_NAME = "__init__.py"
KAFKA_MESSAGE_RECEIVER_FILE = "../harmony_interface/kafka_message_receiver.py"
KAFKA_MESSAGE_SENDER_FILE = "../harmony_interface/kafka_message_sender.py"

config = json.load(open(USER_INPUT_PATH / 'component.json'))[0]
model_id = config["modelId"]
proto_file_name = "start_{}.proto".format(model_id)
# Model id is expected to be separated by semicolon
model_id_title = "".join([name_part.title() for name_part in model_id.split("_")])
kafka_message_name = "Start{}".format(model_id_title)
start_class_package = "start_" + model_id + "_pb2"
start_class_full_name = start_class_package + "." + kafka_message_name


def check_equivalence_of_config_and_json():
    config_inputs = config["inputs"]
    config_inputs_keys = [config_input["key"]  for config_input in config_inputs]
    config_outputs = config["outputs"]
    config_outputs_keys = [config_output["key"]  for config_output in config_outputs]
    # Check that all inputs and outputs in config.py are present in component.json
    for input in inputs:
        try:
            assert input in config_inputs_keys
            if "_" in input:
                print("input in config.py {} has an underscore, this should be removed. Aborting.".format(input))
                exit(0)
        except AssertionError:
            print("input '{}' is in config.py but on in json file".format(input))
    for output in outputs:
        try:
            assert output in config_outputs_keys
            if "_" in output:
                print("output in config.py {} has an underscore, this should be removed. Aborting.".format(output))
                exit(0)
        except AssertionError:
            print("output '{}' is in config.py but on in json file".format(output))

    # Check that all inputs and outputs in component.json are present in config.py
    for input in config_inputs_keys:
        try:
            assert input in inputs
            if "_" in input:
                print("input in component.json {} has an underscore, this should be removed. Aborting.".format(input))
                exit(0)
        except AssertionError:
            print("input '{}' is in json file but not in config.py".format(input))
    for output in config_outputs_keys:
        try:
            assert output in outputs
            if "_" in output:
                print("output in component.json {} has an underscore, this should be removed. Aborting.".format(output))
                exit(0)
        except AssertionError:
            print("output '{}' is in json file but not in config.py".format(output))
    print("All checks passed.")


def generate_proto_file():
    proto_file_contents = "syntax = \"proto2\";\n"
    proto_file_contents += "\n"
    proto_file_contents += "package harmonyServer;\n"
    proto_file_contents += "\n"
    proto_file_contents += "message " + kafka_message_name + " {\n"
    proto_file_contents += "  required string scenarioId = 1;\n"
    proto_file_contents += "  required Inputs inputs = 2;\n"
    proto_file_contents += "  required Outputs outputs = 3;\n"
    proto_file_contents += "\n"
    proto_file_contents += "  message Inputs {\n"

    count = 1
    for input in config["inputs"]:
        pre = "    required string "
        post = " = " + str(count) + ";\n"
        line = pre + input["key"] + post
        proto_file_contents += line
        count = count + 1
    proto_file_contents += "  }\n"
    proto_file_contents += "\n"
    proto_file_contents += "  message Outputs {\n"

    count = 1
    for output in config["outputs"]:
        pre = "    required string "
        post = " = " + str(count) + ";\n"
        line = pre + output["key"] + post
        proto_file_contents += line
        count = count + 1
    proto_file_contents += "  }\n"
    proto_file_contents += "}"

    proto_file = open(proto_file_name, "w")
    proto_file.write(proto_file_contents)
    proto_file.close()

    print("Proto file generated and placed in the same folder as this script.")
    print("Proto file name: {}".format(proto_file_name))
    print("message name: {}".format(kafka_message_name))


def create_folder_and_interfaces():
    new_folder_path = BASE_OUTPUT_PATH / model_id

    if new_folder_path.exists():
        print("The folder already exists. Aborting.")
        exit(0)
    else:
        os.mkdir(new_folder_path)
        print("New folder created: {}".format(new_folder_path))

    open(new_folder_path / INIT_FILE_NAME, 'w').close()
    print("File {} copied into folder".format(INIT_FILE_NAME))

    shutil.move(proto_file_name, new_folder_path / proto_file_name)
    print("Proto file {} moved to folder".format(proto_file_name))

    subprocess.run(["protoc", "--python_out=" + str(new_folder_path), "--proto_path=" + str(new_folder_path), proto_file_name])
    print("Protoc command executed. A new python file should have been generated next to the proto file.")


def update_kafka_message_receiver():
    with open(KAFKA_MESSAGE_RECEIVER_FILE) as f:
        lines = f.readlines()

        new_lines = []
        for line in lines:
            if "from .config import Config" in line:
                new_lines.append("from .protos." + model_id + " import " + start_class_package + "\n")
            if "if protobuf_deserializer is None:" in line:
                new_lines.append("        elif self.topic == \"" + model_id +  "\":\n")
                new_lines.append("            protobuf_deserializer = ProtobufDeserializer(" + start_class_full_name + ")\n")
                new_lines.append("\n")
            new_lines.append(line)

        proto_file = open(KAFKA_MESSAGE_RECEIVER_FILE, "w")
        proto_file.writelines(new_lines)
        proto_file.close()
        print("kafka_message_receiver updated.")


def update_kafka_message_sender():
    with open(KAFKA_MESSAGE_SENDER_FILE) as f:
        lines = f.readlines()
        new_lines = []
        for line in lines:
            if "from .protos.common import progress_outputs_pb2" in line:
                new_lines.append("from .protos." + model_id + " import " + start_class_package + "\n")
            if "class ComponentKafkaMessageSender(KafkaMessageSender):" in line:
                new_lines.append("    def send_start_{}(self, params):\n".format(model_id))
                new_lines.append("        self.logger.warning('START {} params: %s', params)\n".format(model_id))
                new_lines.append("        inputs = {}.Inputs(**params[\"inputs\"])\n".format(start_class_full_name))
                new_lines.append("        outputs = {}.Outputs(**params[\"outputs\"])\n".format(start_class_full_name))
                new_lines.append("        serializer = ProtobufSerializer({}, schema_registry_client)\n".format(start_class_full_name))
                new_lines.append("        conf = self.__get_producer_config(serializer)\n")
                new_lines.append("        message = {}(scenarioId = params[\"scenarioId\"], inputs = inputs, outputs = outputs)\n".format(start_class_full_name))
                new_lines.append("        self.__send_anything(self.topic, message, conf)\n")
                new_lines.append("\n")
            new_lines.append(line)
        proto_file = open(KAFKA_MESSAGE_SENDER_FILE, "w")
        proto_file.writelines(new_lines)
        proto_file.close()
        print("kafka_message_sender updated.")


if __name__ == "__main__":
    # It expects two files in the "inputs_from_user" folder named "component.json" and "config.py"
    check_equivalence_of_config_and_json()
    generate_proto_file()
    create_folder_and_interfaces()
    update_kafka_message_receiver()
    update_kafka_message_sender()
