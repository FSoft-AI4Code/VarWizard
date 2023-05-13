import torch
from peft import get_peft_model
import functools
from huggingface_hub import hf_hub_download

from varwizard.config import get_prefix_tuning_config
from varwizard.data.input_preparation import prepare_input
from varwizard.models.bloom import get_tokenizer_and_model
from varwizard.generation.gen import generate


def get_varwizard_model(varwizard_path = 'Fsoft-AIC/VarWizard', model_name = 'bigscience/bloom-560m'):
	tokenizer, model = get_tokenizer_and_model(model_name)
	peft_config = get_prefix_tuning_config()
	model = get_peft_model(model, peft_config)
	cp_path = hf_hub_download(repo_id = varwizard_path, filename = "varwizard.tar")
	cp_data = torch.load(cp_path, map_location = 'cpu')
	model.load_state_dict(cp_data, strict = False)
	return tokenizer, model

class VarWizard:
	def __init__(self):
		tokenizer, model = get_varwizard_model()
		self.tokenizer = tokenizer
		self.model = model.eval()
		self.prepare_input = functools.partial(prepare_input, tokenizer = tokenizer)
		self.generate = functools.partial(generate, tokenizer = self.tokenizer, model = self.model)
	def make_new_code(self, input, lang, max_input_len: int = 400, device = 'cpu'):
		input_ids = torch.tensor(self.prepare_input(input, lang, max_input_len = max_input_len))
		input_ids = input_ids.to(device)
		self.model.to(device)
		input_ids = input_ids.unsqueeze(0)
		predictions = self.generate(input_ids)
		return predictions
