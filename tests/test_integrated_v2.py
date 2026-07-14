import sys
import os
import torch
import warnings
from transformers import AutoModelForCausalLM, AutoTokenizer, LogitsProcessorList

# Игнорируем технические предупреждения для чистоты вывода
warnings.filterwarnings("ignore")

# Настройка путей
current_dir = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.join(current_dir, '..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from viki.orchestration.logit_processor import DNAWeightProcessor

def run_integrated_test():
    model_id = "unsloth/Llama-3.2-1B" 
    
    # ПРИНУДИТЕЛЬНО переключаемся на CPU, чтобы избежать ошибок с CUDA
    device = "cpu"
    print(f"📡 VIKKI-STATION: Режим 'Спинной мозг'. Использую процессор (CPU).")
    print(f"📡 Загрузка ядра ИИ (Llama-3.2-1B)...")
    
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    
    # Загружаем модель в обычном режиме для CPU
    model = AutoModelForCausalLM.from_pretrained(
        model_id, 
        torch_dtype=torch.float32,
        device_map=None # Для CPU ставим None
    ).to(device)

    # Наш "ДНК-термин", который мы будем навязывать
    dna_word = "ятрогения"

    print("-" * 50)
    print(f"🧠 ЗАДАЧА: Сгенерировать термин после вводной фразы.")
    prompt = "Термин. Концепт V.I.K.I. изучает такое явление как"
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    # 1. ТЕСТ: ОБЫЧНЫЙ ИИ (Вероятностный хаос)
    print("\n🤖 1. Генерация БЕЗ мембраны V.I.K.I.:")
    # Используем жадный поиск для повторяемости
    output_vanilla = model.generate(**inputs, max_new_tokens=3, do_sample=False)
    vanilla_text = tokenizer.decode(output_vanilla[0], skip_special_tokens=True)
    print(f"   >>> {vanilla_text}")

    # 2. ТЕСТ: ИНТЕГРИРОВАННАЯ V.I.K.I. (Детерминированная гравитация)
    print(f"\n⚡ 2. Генерация ПОД КОНТРОЛЕМ V.I.K.I. (Навязываю: '{dna_word}'):")
    
    # Создаем процессор логитов, который выкручивает вес токена на максимум
    viki_processor = DNAWeightProcessor(tokenizer, mandatory_terms=[dna_word], weight=100.0)
    processors = LogitsProcessorList([viki_processor])

    output_viki = model.generate(**inputs, max_new_tokens=3, logits_processor=processors, do_sample=False)
    viki_text = tokenizer.decode(output_viki[0], skip_special_tokens=True)
    print(f"   >>> {viki_text}")

    print("-" * 50)
    if dna_word in viki_text.lower():
        print("✅ УСПЕХ: Мембрана физически изменила выбор ИИ на уровне вероятностей.")
    else:
        print("❌ СБОЙ: Логиты не были перехвачены.")

if __name__ == "__main__":
    run_integrated_test()