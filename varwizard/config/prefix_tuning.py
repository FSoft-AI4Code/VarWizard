from peft import get_peft_config, get_peft_model, PrefixTuningConfig, TaskType

def get_prefix_tuning_config(dim_size: int = 1024,
                    prefix_projection: bool = True,
                    num_virtual_tokens: int = 30
                    ):

    peft_config = PrefixTuningConfig(
            task_type = TaskType.CAUSAL_LM,
            inference_mode = False, 
            encoder_hidden_size = dim_size,
            prefix_projection = prefix_projection,
            num_virtual_tokens = num_virtual_tokens
        )
    return peft_config