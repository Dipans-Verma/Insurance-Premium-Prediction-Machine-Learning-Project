from insurance.logger import logging
from insurance.exception import InsuranceException
import os
import sys
from insurance.utils import get_collection_As_dataframe
from insurance.entity.config_entity import DataIngestionconfig
from insurance.components.data_transformation import DataTransformation
from insurance.entity import config_entity
from insurance.components.data_ingestion import DataIngestion
from insurance.components.data_validation import DataValidation
from insurance.components.model_trainer import ModelTrainer
from insurance.components.model_evaluation import ModelEvaluation
from insurance.components.model_pusher import ModelPusher

# def test_logger_and_exception():
# try:
#logging.info("starting the test_logger_and_exception")
#result = 3 / 0
# print(result)
#logging.info("ending point of the test_logger_and_exception")
# except Exception as e:
# logging.debug(str(e))
#raise InsuranceException(e,sys)


if __name__ == "__main__":
    try:
        # get_collection_As_dataframe(database_name = "INSURANCE", collection_name = "INSURANCE_PROJECT")
        training_pipeline_config = config_entity.TrainingPipelineConfig()
        data_ingestion_config = config_entity.DataIngestionconfig(
            training_pipeline_config=training_pipeline_config)
        print(data_ingestion_config.to_Dict())

        data_ingestion = DataIngestion(
            data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

        # data validation

        data_validation_config = config_entity.DataValidationConfig(
            training_pipeline_config=training_pipeline_config)
        data_validation = DataValidation(
            data_validation_config=data_validation_config, data_ingestion_artifact=data_ingestion_artifact)
        data_validation_artifact = data_validation.initiate_data_validation()

        # data transformation

        data_transformation_config = config_entity.DataTransformationConfig(
            training_pipeline_config=training_pipeline_config)
        data_transformation = DataTransformation(
            data_transformation_config=data_transformation_config, data_ingestion_artifact=data_ingestion_artifact)
        data_transformation_artifact = data_transformation.initiate_data_transformation()

        # model trainer

        model_trainer_config = config_entity.ModelTrainerConfig(
            training_pipeline_config=training_pipeline_config)
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config,
                                     data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()

        # model evaluation

        model_evaluation_config = config_entity.ModelEvaluationConfig(
            training_pipeline_config=training_pipeline_config)
        modle_eval = ModelEvaluation(model_evaluation_config=model_evaluation_config,
                                     data_ingestion_artifact=data_ingestion_artifact,
                                     data_transformation_artifact=data_transformation_artifact,
                                     model_trainer_artifact=model_trainer_artifact)
        model_eval_artifact = modle_eval.initiate_model_evaluation()

        # model pusher

        model_pusher_config = config_entity.ModelPusherConfig(
            training_pipeline_config=training_pipeline_config)
        model_pusher = ModelPusher(model_pusher_config=model_pusher_config,
                                   data_transformation_artifact=data_transformation_artifact,
                                   model_trainer_artifact=model_trainer_artifact)

        model_pusher_artifact = model_pusher.inititate_model_pusher()

    except Exception as e:
        print(e)
