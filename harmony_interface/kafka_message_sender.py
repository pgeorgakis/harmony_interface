# noinspection PyUnresolvedReferences
import logging
from .config import Config
from .protos.common import progress_outputs_pb2
from .protos.common import stop_pb2
from .protos.tfs import start_tfs_pb2
from .protos.tfs_ofs_data_transform import start_tfs_ofs_data_transform_pb2

# noinspection PyUnresolvedReferences
from uuid import uuid4
# noinspection PyUnresolvedReferences
from confluent_kafka import SerializingProducer
# noinspection PyUnresolvedReferences
from confluent_kafka.serialization import StringSerializer
# noinspection PyUnresolvedReferences
from confluent_kafka.schema_registry import SchemaRegistryClient
# noinspection PyUnresolvedReferences
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer

schema_registry_client = SchemaRegistryClient({'url': 'http://schema-registry:8081'})
config = Config()

class KafkaMessageSender(object):
    def __init__(self, model_id):
        logger = logging.getLogger()
        logger.setLevel(logging.WARNING)
        self.logger = logger
        self.topic = model_id

    def __get_producer_config(self, proto_serializer):
        return {'bootstrap.servers':  config.KAFKA_BOOTSTRAP_SERVERS,
                'key.serializer': StringSerializer('utf_8'),
                'value.serializer': proto_serializer}

    def __delivery_report(self, err, msg):
        if err is not None:
            self.logger.warning('Sender message delivery failed: {}'.format(err))
        else:
            self.logger.warning('Sender message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    def __send_anything(self, kafka_topic, message, conf):
        kp = None
        try:
            kp = SerializingProducer(conf)
        except Exception as ex:
            self.logger.warning('Exception while connecting Kafka with Producer : %s', str(ex))
        try:
            self.logger.warning('PRODUCER MSGS: %s with topic : %s', message, kafka_topic)
            kp.produce(topic=kafka_topic, value=message, key=str(uuid4()), on_delivery=self.__delivery_report)
            kp.poll(0)
        except Exception as ex:
            self.logger.warning('Exception in publishing message %s', str(ex))
        kp.flush()

    def send_progress_and_outputs(self, scenarioId, percent, outputList):
        serializer = ProtobufSerializer(progress_outputs_pb2.UpdateServerWithProgressAndOutputs, schema_registry_client)
        progress_output_conf = self.__get_producer_config(serializer)
        message = progress_outputs_pb2.UpdateServerWithProgressAndOutputs(
            scenarioId = scenarioId,
            percentage = int(percent),
            outputs = outputList
        )
        self.logger.warning('PROGRESS AND OUTPUTS: %s', message)
        self.__send_anything((self.topic + '_progress_output'), message, progress_output_conf)

    def send_stop(self, experiment_id):
        self.logger.warning('MESSAGE: STOP ')
        message = stop_pb2.StopModel(experiment_id=experiment_id)
        self.__send_anything(message)

    def send_start_tfs(self, params):
        self.logger.warning('START TFS params: %s', params)
        inputs = start_tfs_pb2.StartTFS.Inputs(**params["inputs"])
        outputs = start_tfs_pb2.StartTFS.Outputs(**params["outputs"])
        serializer = ProtobufSerializer(start_tfs_pb2.StartTFS, schema_registry_client)
        conf = self.__get_producer_config(serializer)
        message = start_tfs_pb2.StartTFS(scenarioId = params["scenarioId"], inputs = inputs, outputs = outputs)
        self.__send_anything(self.topic, message, conf)

    def send_start_tfs_ofs_data_transform(self, params):
        self.logger.warning('START TFS_OFS_DATA_TRANSFORM: %s', params)
        inputs = start_tfs_ofs_data_transform_pb2.StartTFSOFSDataTransform.Inputs(**params["inputs"])
        outputs = start_tfs_ofs_data_transform_pb2.StartTFSOFSDataTransform.Outputs(**params["inputs"])
        serializer = ProtobufSerializer(start_tfs_ofs_data_transform_pb2, schema_registry_client)
        conf = self.__get_producer_config(serializer)
        message = start_tfs_ofs_data_transform_pb2.StartTFSOFSDataTransform(scenarioID = params["scenarioID"], inputs = inputs, outputs = outputs)
        self.__send_anything(self.topic, message, conf)

class ComponentKafkaMessageSender(KafkaMessageSender):
    def send_progress(self, experiment_id, percentage):
        super().send_progress()