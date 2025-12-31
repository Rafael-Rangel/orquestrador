"""
Teste simples do pytube
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from pytube import YouTube

def test_download():
    url = "https://www.youtube.com/shorts/qlIKbXlFkiE"
    output_dir = "downloads/teste/@shortspodcuts"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Testando download de: {url}")
    print(f"Salvando em: {output_dir}")
    print()
    
    try:
        yt = YouTube(url)
        print(f"Título: {yt.title}")
        print(f"Duração: {yt.length} segundos")
        print()
        
        # Pegar melhor stream
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        if not stream:
            stream = yt.streams.filter(file_extension='mp4').first()
        
        if stream:
            print(f"Stream encontrado: {stream.resolution}, {stream.filesize} bytes")
            print("Iniciando download...")
            stream.download(output_path=output_dir, filename="qlIKbXlFkiE.mp4")
            print("✅ Download concluído!")
            return True
        else:
            print("❌ Nenhum stream encontrado")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_download()

