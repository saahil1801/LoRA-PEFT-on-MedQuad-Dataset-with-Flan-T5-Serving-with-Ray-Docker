from ray import serve
import ray
import sentencepiece
from transformers import T5Tokenizer, T5ForConditionalGeneration
from peft import PeftModel
import torch

ray.init(ignore_reinit_error=True, include_dashboard=True, dashboard_host='0.0.0.0')
serve.start()


@serve.deployment
class AnswerGenerator:
    def __init__(self):
        self.device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
        self.tokenizer = T5Tokenizer.from_pretrained("./biotokenizer")
        self.base_model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-large", device_map=self.device)
        self.model = PeftModel.from_pretrained(self.base_model, "./biomrcmodel")
        self.model.to(self.device)
        
        

    def generate_answer(self, question: str, max_length: int = 512):
        input_text = "Assuming you are working as a Doctor. Please answer this question: " + question
        inputs = self.tokenizer(input_text, return_tensors="pt").to(self.device)
        outputs = self.model.generate(
            input_ids=inputs["input_ids"], 
            max_length=max_length, 
            num_beams=5, 
            early_stopping=True
        )
        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return answer

    async def __call__(self, request):
        question = await request.json()
        answer = self.generate_answer(question["question"])
        return {"answer": answer}

biomedical= AnswerGenerator.bind()