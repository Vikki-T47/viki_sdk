import torch
from transformers import LogitsProcessor

class DNAWeightProcessor(LogitsProcessor):
    def __init__(self, tokenizer, mandatory_terms: list, weight: float = 40.0):
        self.tokenizer = tokenizer
        self.term_tokens = []
        for term in mandatory_terms:
            # Превращаем слова в токены. Берем первый токен слова.
            token_ids = tokenizer.encode(term, add_special_tokens=False)
            if token_ids:
                self.term_tokens.append(token_ids[0])
        self.weight = weight

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor) -> torch.FloatTensor:
        # Мы находим вероятности наших слов и "выкручиваем" их вверх
        for token_id in self.term_tokens:
            scores[:, token_id] += self.weight
        return scores