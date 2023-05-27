import torch
from peft import get_peft_model
import functools
import os
import json
from huggingface_hub import hf_hub_download

from varwizard.config import get_prefix_tuning_config
from varwizard.data.input_preparation import prepare_input
from varwizard.models.bloom import get_tokenizer_and_model
from varwizard.generation.gen import generate


def get_varwizard_model(varwizard_path = 'Fsoft-AIC/VarWizard', model_name = 'bigscience/bloom-560m'):
	if 'bloom' in model_name:
		from varwizard.models.bloom import get_tokenizer_and_model
	else:
		from varwizard.models.codet5 import get_tokenizer_and_model
	base_model_name = model_name.split('/')[1].replace('-', '_')
	tokenizer, model = get_tokenizer_and_model(model_name)
	peft_config = get_prefix_tuning_config(base_model_name)
	model = get_peft_model(model, peft_config)
	base_model_name = model_name.split('/')[1].replace('-', '_')
	cp_path = hf_hub_download(repo_id = varwizard_path, filename = f"varwizard_{base_model_name}.tar")
	cp_data = torch.load(cp_path, map_location = 'cpu')
	model.load_state_dict(cp_data, strict = False)
	return tokenizer, model

class VarWizard:
	__supported_models__ = ['bloom-560m', 'codet5-base']
	def __init__(self, model_name = 'bloom-560m'):
		assert model_name in VarWizard.__supported_models__, f"this model: {model_name} isn't supported"
		if model_name == 'bloom-560m':
			model_name = f'bigscience/{model_name}'
		elif model_name == 'codet5-base':
			model_name = 'Salesforce/codet5-base'
		tokenizer, model = get_varwizard_model(model_name = model_name)
		self.tokenizer = tokenizer
		self.model = model.eval()
		self.base_model_name = model_name
		self.prepare_input = functools.partial(prepare_input, tokenizer = tokenizer)
		self.generate = functools.partial(generate, base_model_name = self.base_model_name, tokenizer = self.tokenizer, model = self.model)
	@torch.inference_mode()
	def make_new_code(self, input, lang, output_path = None, max_input_len: int = 400, max_new_tokens: int = 100, penalty_alpha: float = 0.6, top_k: int = 4, device = 'cpu'):
		if os.path.exists(input):
			with open(input) as f:
				input = f.read()
		input = input.strip()
		all_predictions = []
		for input_ids, vmap, before_context, after_context in self.prepare_input(input, lang, base_model_name = self.base_model_name, max_input_len = max_input_len):
			input_ids = torch.tensor(input_ids)
			input_ids = input_ids.to(device)
			self.model.device = device
			self.model.to(device)
			input_ids = input_ids.unsqueeze(0)
			prediction = self.generate(input_ids, vmap, max_new_tokens = max_new_tokens, penalty_alpha = penalty_alpha, top_k = top_k)
			all_predictions.extend([before_context, prediction])
			if after_context is not None:
				all_predictions.append(after_context)
		prediction = ''.join(all_predictions)
		if output_path is not None:
			with open(output_path, 'w') as f:
				f.write(prediction)
		return prediction
	
