import tempfile
from contextlib import ExitStack
from typing import Text, Optional, Dict

from rasa.importers.importer import TrainingDataImporter
from rasa.train import DEFAULT_MODELS_PATH
from rasa.train import _train_async_internal, handle_domain_if_not_exists
from rasa.utils.common import TempDirectoryPath
import os
from bot_trainer.data_processor.importer import MongoDataImporter


async def train_model(
    data_importer: TrainingDataImporter,
    output_path: Text,
    force_training: bool = False,
    fixed_model_name: Optional[Text] = None,
    persist_nlu_training_data: bool = False,
    additional_arguments: Optional[Dict] = None,
):

    with ExitStack() as stack:
        train_path = stack.enter_context(TempDirectoryPath(tempfile.mkdtemp()))

        domain = await data_importer.get_domain()
        if domain.is_empty():
            return await handle_domain_if_not_exists(
                data_importer, output_path, fixed_model_name
            )

        return await _train_async_internal(
            data_importer,
            train_path,
            output_path,
            force_training,
            fixed_model_name,
            persist_nlu_training_data,
            additional_arguments,
        )


async def train_model_from_mongo(
    bot: str,
    force_training: bool = False,
    fixed_model_name: Optional[Text] = None,
    persist_nlu_training_data: bool = False,
    additional_arguments: Optional[Dict] = None,
):
    data_importer = MongoDataImporter(bot)
    output = os.path.join(DEFAULT_MODELS_PATH, bot)
    return await train_model(
        data_importer,
        output,
        force_training,
        fixed_model_name,
        persist_nlu_training_data,
        additional_arguments,
    )
