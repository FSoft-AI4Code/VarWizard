import torch
from peft import get_peft_model
import functools
from pkg_resources import resource_filename

import varwizard
from varwizard.data.input_preparation import prepare_input
from varwizard.models.bloom import get_tokenizer_and_model
from varwizard.config.prefix_tuning import get_prefix_tuning_config
from varwizard.generation.gen import generate


def get_varwizard_model(varwizard_path = 'varwizard.tar', model_name = 'bigscience/bloom-560m'):
	tokenizer, model = get_tokenizer_and_model(model_name)
	peft_config = get_prefix_tuning_config()
	model = get_peft_model(model, peft_config)

	varwizard_path = resource_filename('varwizard', 'libs/varwizard/varwizard.tar')
	varwizard_data = torch.load(varwizard_path, map_location = 'cpu')
	model.load_state_dict(varwizard_data, strict = False)
	return tokenizer, model

class VarWizard:
	def __init__(self):
		tokenizer, model = get_varwizard_model()
		self.tokenizer = tokenizer
		self.model = model.eval()
		self.prepare_input = functools.partial(prepare_input, tokenizer = tokenizer)
		self.generate = functools.partial(generate, tokenizer = self.tokenizer, model = self.model)
	def make_new_code(self, input, lang, max_input_len: int = 400, device = None):
		input_ids = self.prepare_input(input, lang, max_input_len = max_input_len)
		if device is not None:
			input_ids = input_ids.to(device)
			self.model.to(device)
		input_ids = torch.tensor(input_ids)[None]
		predictions = self.generate(input_ids)
		return predictions
