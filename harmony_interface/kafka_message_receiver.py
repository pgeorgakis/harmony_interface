# noinspection PyUnresolvedReferences
import logging
# noinspection PyUnresolvedReferences
import threading
# noinspection PyUnresolvedReferences
from abc import abstractmethod
from .protos.common import progress_outputs_pb2
from .protos.common import stop_pb2
from .protos.tfs import start_tfs_pb2
from .protos.tfs_ofs_data_transform import start_tfs_ofs_data_transform_pb2
from .protos.ofs import start_ofs_pb2
# noinspection PyUnresolvedReferences
from confluent_kafka import DeserializingConsumer
# noinspection PyUnresolvedReferences
from confluent_kafka.schema_registry.protobuf import ProtobufDeserializer
# noinspection PyUnresolvedReferences
from confluent_kafka.serialization import StringDeserializer
# noinspection PyUnresolvedReferences
from google.protobuf.json_format import MessageToJson
from .config import Config

config = Config()

class KafkaMessageReceiver(object):
    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.warning('KafkaMessageReceiver initialized !')

    def initialize_receiver(self, model_id):
        self.topic = model_id
        self.check_for_start_messages()

    def initialize_progress_output(self, topic_name):
        self.topic = topic_name
        self.check_for_progress_output_messages(topic_name + '_progress_output')

    def check_for_any_messages(self, kafka_topic, protobuf_deserializer):
        string_deserializer = StringDeserializer('utf_8')
        consumer_conf = {
            'session.timeout.ms': config.KAFKA_SESSION_TIME_OUT,
            'max.poll.interval.ms': config.KAFKA_MAX_POLL,
            'bootstrap.servers': config.KAFKA_BOOTSTRAP_SERVERS,
            'key.deserializer': string_deserializer,
            'value.deserializer': protobuf_deserializer,
            'group.id': config.KAFKA_GROUP_ID,
            'auto.offset.reset': config.KAFKA_OFFSET_RESET,
            "enable.auto.commit": config.KAFKA_AUTO_COMMIT_ENABLE
        }
        consumer = None
        try:
            consumer = DeserializingConsumer(consumer_conf)
            consumer.subscribe([kafka_topic])
            self.logger.warning('Received: Consumer created with topic %s', kafka_topic)
        except Exception as ex:
            self.logger.warning('Exception while connecting Kafka with Consumer: %s %s', kafka_topic, str(ex))

        while True:
            # try:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            elif msg.error():
                self.logger.warning("Consumer error: {}".format(msg.error()))
                continue
            else:
                json_obj = MessageToJson(msg.value())
                self.logger.warning("Topic and received Proto: %s %s", msg.topic(), json_obj)
                if str(msg.topic()).endswith('_progress_output'):
                    self.logger.warning("Progress message received: %s", msg.topic())
                    self.progress_output_message_received(json_obj)
                else:
                    self.logger.warning("Start message received. msg.topic(): %s | self.topic: %s", msg.topic(), self.topic)
                    threading.Thread(target=self.start_message_received, args=[json_obj]).start()
            # except Exception as ex:
            #     self.logger.warning('Exception occured in receiver: %s with topic: %s', ex, kafka_topic)

    def check_for_stop_messages(self):
        protobuf_deserializer = ProtobufDeserializer(stop_pb2.StopModel)
        self.check_for_any_messages(
            (self.topic + '_stop'), protobuf_deserializer)

    def check_for_progress_output_messages(self, topic_name):
        protobuf_deserializer = ProtobufDeserializer(progress_outputs_pb2.UpdateServerWithProgressAndOutputs)
        self.check_for_any_messages(topic_name, protobuf_deserializer)

    def check_for_start_messages(self):
        self.logger.warning('check_for_start_messages modelId: %s', self.topic)

        protobuf_deserializer = None
        if self.topic == "tfs":
            protobuf_deserializer = ProtobufDeserializer(start_tfs_pb2.StartTFS)

        elif self.topic == "tfs_ofs_data_transform":
            protobuf_deserializer = ProtobufDeserializer(start_tfs_ofs_data_transform_pb2.StartTFSOFSDataTransform)

        elif self.topic == "ofs":
            protobuf_deserializer = ProtobufDeserializer(start_ofs_pb2.StartOFS)

        if protobuf_deserializer is None:
            self.logger.warning('protobuf_deserializer: checking message not possible !')
        else:
            self.check_for_any_messages(self.topic, protobuf_deserializer)

    @abstractmethod
    def start_message_received(self):
        pass

    @abstractmethod
    def progress_output_message_received(self, json_obj):
        pass

    @abstractmethod
    def stop_message_received(self):
        pass
