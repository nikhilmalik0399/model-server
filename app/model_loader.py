from ctransformers import AutoModelForCausalLM

model = None

def load_model(model_path, threads):
    global model
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        model_type="llama",
        threads=threads
    )
    return model
