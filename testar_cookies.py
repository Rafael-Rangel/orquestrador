"""
Teste rápido para verificar se os cookies funcionam
"""
import yt_dlp
import os

cookies_file = os.path.join(os.path.dirname(__file__), 'cookies.txt')
video_url = "https://www.youtube.com/shorts/qlIKbXlFkiE"
output_file = "teste_cookies.mp4"

print("=" * 60)
print("Testando cookies do YouTube")
print("=" * 60)
print()

if not os.path.exists(cookies_file):
    print(f"ERRO: Arquivo {cookies_file} nao encontrado!")
    exit(1)

print(f"Usando cookies de: {cookies_file}")
print(f"Testando URL: {video_url}")
print()

ydl_opts = {
    'format': 'best[ext=mp4]/best',
    'outtmpl': output_file.replace('.mp4', '.%(ext)s'),
    'quiet': False,
    'cookiefile': cookies_file,
    'extractor_args': {
        'youtube': {
            'player_client': ['android'],
        }
    },
}

try:
    print("Iniciando download de teste...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    
    if os.path.exists(output_file) or os.path.exists(output_file.replace('.mp4', '.webm')):
        print()
        print("=" * 60)
        print("SUCCESS: Cookies funcionam corretamente!")
        print("=" * 60)
        print()
        print("Agora voce pode enviar o arquivo cookies.txt para a VPS")
        print("Veja INSTRUCOES_ENVIAR_COOKIES.txt para detalhes")
        
        # Limpar arquivo de teste
        for ext in ['.mp4', '.webm']:
            test_file = output_file.replace('.mp4', ext)
            if os.path.exists(test_file):
                os.remove(test_file)
                print(f"Arquivo de teste removido: {test_file}")
    else:
        print()
        print("ERRO: Download nao completou")
        
except Exception as e:
    print()
    print("=" * 60)
    print(f"ERRO: {e}")
    print("=" * 60)
    print()
    print("Os cookies podem estar expirados ou invalidos")
    print("Tente exportar novamente do navegador")

