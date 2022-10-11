# noinspection PyUnresolvedReferences
import logging
# noinspection PyUnresolvedReferences
import threading
# noinspection PyUnresolvedReferences
from abc import abstractmethod
from .protos.common import progress_outputs_pb2
from .protos.common import stop_pb2
from .protos.demoMultipleFiles import start_demo_multiple_files_pb2
from .protos.demoMultipleFiles2 import start_demo_multiple_files2_pb2
from .protos.demo3 import start_demo3_pb2
from .protos.demo2 import start_demo2_pb2
from .protos.demo import start_demo_pb2
from .protos.tfs import start_tfs_pb2
from .protos.sfs import start_sfs_pb2
from .protos.ops import start_ops_pb2
from .protos.onm import start_onm_pb2
from .protos.trt import start_trt_pb2
from .protos.rem import start_rem_pb2
from .protos.dfm_lite import start_dfm_lite_pb2
from .protos.dfm_lite_partial import start_dfm_lite_partial_pb2
from .protos.luti_ath import start_luti_ath_pb2
from .protos.luti_tur import start_luti_tur_pb2
from .protos.ldm_ath import start_ldm_ath_pb2
# noinspection PyUnresolvedReferences
from confluent_kafka import DeserializingConsumer
# noinspection PyUnresolvedReferences
from confluent_kafka.schema_registry.protobuf import ProtobufDeserializer
# noinspection PyUnresolvedReferences
from confluent_kafka.serialization import StringDeserializer
# noinspection PyUnresolvedReferences
from google.protobuf.json_format import MessageToJson
from .protos.ldm_tur import start_ldm_tur_pb2
from .protos.ldm_oxf import start_ldm_oxf_pb2
from .protos.luti_oxf import start_luti_oxf_pb2
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

        elif self.topic == "sfs":
            protobuf_deserializer = ProtobufDeserializer(start_sfs_pb2.StartSFS)

        elif self.topic == "ops":
            protobuf_deserializer = ProtobufDeserializer(start_ops_pb2.StartOPSModel)
            
        elif self.topic == "onm":
            protobuf_deserializer = ProtobufDeserializer(start_onm_pb2.StartONMModel)
            
        elif self.topic == "trt":
            protobuf_deserializer = ProtobufDeserializer(start_trt_pb2.StartTRTModel)
            
        elif self.topic == "demo":
            protobuf_deserializer = ProtobufDeserializer(start_demo_pb2.StartDemoComponent)
            
        elif self.topic == "demo2":
            protobuf_deserializer = ProtobufDeserializer(start_demo2_pb2.StartDemo2Component)
            
        elif self.topic == "demo3":
            protobuf_deserializer = ProtobufDeserializer(start_demo3_pb2.StartDemo3Component)
            
        elif self.topic == "demo-multiple-files-1":
            protobuf_deserializer = ProtobufDeserializer(start_demo_multiple_files_pb2.StartDemoMultipleFilesComponent)
            
        elif self.topic == "demo-multiple-files-2":
            protobuf_deserializer = ProtobufDeserializer(start_demo_multiple_files2_pb2.StartDemoMultipleFilesComponent2)

        elif self.topic == "rem":
            protobuf_deserializer = ProtobufDeserializer(start_rem_pb2.StartREM)

        elif self.topic == "dfm_lite":
            protobuf_deserializer = ProtobufDeserializer(start_dfm_lite_pb2.StartDFMLite)

        elif self.topic == "dfm_lite_partial":
            protobuf_deserializer = ProtobufDeserializer(start_dfm_lite_partial_pb2.StartDFMLitePartial)

        elif self.topic == "luti_ath":
            protobuf_deserializer = ProtobufDeserializer(start_luti_ath_pb2.StartLutiAth)

        elif self.topic == "luti_tur":
            protobuf_deserializer = ProtobufDeserializer(start_luti_tur_pb2.StartLutiTur)

        elif self.topic == "ldm_ath":
            protobuf_deserializer = ProtobufDeserializer(start_ldm_ath_pb2.StartLdmAth)

        elif self.topic == "ldm_tur":
            protobuf_deserializer = ProtobufDeserializer(start_ldm_tur_pb2.StartLdmTur)

        elif self.topic == "ldm_oxf":
            protobuf_deserializer = ProtobufDeserializer(start_ldm_oxf_pb2.StartLdmOxf)

        elif self.topic == "luti_oxf":
            protobuf_deserializer = ProtobufDeserializer(start_luti_oxf_pb2.StartLutiOxf)

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
