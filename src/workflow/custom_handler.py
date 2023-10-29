import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from ts.torch_handler.base_handler import BaseHandler


class CausalLMHandler(BaseHandler):

    def __init__(self):
        self.tokenizer = GPT2Tokenizer.from_pretrained('distilgpt2')
        # self.model = GPT2LMHeadModel.from_pretrained(
        #     'path/to/your/fine-tuned/model')
        self.model = GPT2LMHeadModel.from_pretrained('distilgpt2')
        self.model.eval()

    def preprocess(self, data):
        text = data[0]['data']
        if isinstance(text, bytes):
            text = text.decode('utf-8')
        inputs = self.tokenizer.encode_plus(text, return_tensors="pt")
        return inputs

    def inference(self, inputs):
        with torch.no_grad():
            outputs = self.model.generate(**inputs)
        return outputs

    def postprocess(self, outputs):
        generated_text = self.tokenizer.decode(
            outputs[0], skip_special_tokens=True)
        return [generated_text]
