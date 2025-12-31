"""Teste da função de sanitização de nome de arquivo"""
import re
import unicodedata

def _sanitize_filename(filename: str, max_length: int = 200) -> str:
    """Limpa o nome do arquivo criando um slug: minúsculo, sem acentos, sem emojis, espaços viram underscores"""
    # Remover emojis e caracteres especiais
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE
    )
    filename = emoji_pattern.sub('', filename)
    
    # Normalizar Unicode (NFD = Normalized Form Decomposed)
    filename = unicodedata.normalize('NFD', filename)
    
    # Remover acentos
    filename = ''.join(char for char in filename if unicodedata.category(char) != 'Mn')
    
    # Converter para minúsculas
    filename = filename.lower()
    
    # Remover caracteres inválidos
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    
    # Substituir espaços e caracteres especiais por underscore
    filename = re.sub(r'[\s\-_\.]+', '_', filename)
    
    # Remover underscores múltiplos
    filename = re.sub(r'_+', '_', filename)
    
    # Remover underscores no início e fim
    filename = filename.strip('_')
    
    # Limitar tamanho
    if len(filename) > max_length:
        filename = filename[:max_length].rstrip('_')
    
    # Se ficar vazio, usar um nome padrão
    if not filename:
        filename = "video"
    
    return filename

# Testes
test_cases = [
    ("F1 🤝 5ª série", "f1_5a_serie"),
    ("GRINGOS x PALAVRÕES...", "gringos_x_palavroes"),
    ("Esquece Esse Cara - Final", "esquece_esse_cara_final"),
    ("Vídeo com Acentos: ção", "video_com_acentos_cao"),
]

print("Testando função de sanitização:")
for original, expected in test_cases:
    result = _sanitize_filename(original)
    status = "✅" if result == expected else "❌"
    print(f"{status} '{original}' → '{result}' (esperado: '{expected}')")

