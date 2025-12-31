"""
Script para exportar cookies do YouTube usando yt-dlp
"""
import subprocess
import sys
import os

def export_cookies(browser='chrome'):
    """
    Exporta cookies do navegador para cookies.txt
    
    Args:
        browser: 'chrome', 'firefox', 'edge', 'brave', 'opera', 'vivaldi'
    """
    browsers = ['chrome', 'firefox', 'edge', 'brave', 'opera', 'vivaldi']
    
    if browser not in browsers:
        print(f"Browser '{browser}' não suportado.")
        print(f"Browsers suportados: {', '.join(browsers)}")
        return False
    
    cookies_file = os.path.join(os.path.dirname(__file__), 'cookies.txt')
    
    print(f"Exportando cookies do {browser}...")
    print(f"Arquivo será salvo em: {cookies_file}")
    print()
    
    try:
        # Tentar diferentes formas de chamar yt-dlp
        cmd_options = [
            ['yt-dlp', '--cookies-from-browser', browser, '--cookies', cookies_file, 'https://www.youtube.com'],
            ['python', '-m', 'yt_dlp', '--cookies-from-browser', browser, '--cookies', cookies_file, 'https://www.youtube.com'],
            ['py', '-m', 'yt_dlp', '--cookies-from-browser', browser, '--cookies', cookies_file, 'https://www.youtube.com'],
        ]
        
        result = None
        for cmd in cmd_options:
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    break
            except FileNotFoundError:
                continue
            except Exception:
                continue
        
        if result and result.returncode == 0:
            if os.path.exists(cookies_file):
                file_size = os.path.getsize(cookies_file)
                print(f"SUCCESS: Cookies exportados com sucesso!")
                print(f"Arquivo: {cookies_file}")
                print(f"Tamanho: {file_size} bytes")
                print()
                print("Proximo passo: Envie este arquivo para a VPS:")
                print(f"  scp cookies.txt root@srv1011759:/root/content-orchestrator/data/cookies.txt")
                return True
            else:
                print("ERROR: Arquivo nao foi criado")
                return False
        else:
            print("ERROR: Erro ao exportar cookies")
            if result:
                print(result.stderr)
            return False
            
    except FileNotFoundError:
        print("ERROR: yt-dlp nao encontrado!")
        print("Instale o yt-dlp primeiro:")
        print("  pip install yt-dlp")
        print()
        print("OU use o metodo da extensao do navegador (veja CONFIGURAR_COOKIES.md)")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Exportador de Cookies do YouTube")
    print("=" * 60)
    print()
    
    # Tentar detectar navegador ou pedir ao usuário
    browser = 'chrome'  # Padrão
    
    if len(sys.argv) > 1:
        browser = sys.argv[1].lower()
    else:
        print("Navegadores disponíveis:")
        print("  1. Chrome")
        print("  2. Firefox")
        print("  3. Edge")
        print("  4. Brave")
        print()
        choice = input("Escolha o navegador (1-4) ou pressione Enter para Chrome: ").strip()
        
        browser_map = {
            '1': 'chrome',
            '2': 'firefox',
            '3': 'edge',
            '4': 'brave'
        }
        
        if choice in browser_map:
            browser = browser_map[choice]
    
    print(f"Usando navegador: {browser}")
    print()
    
    success = export_cookies(browser)
    
    if success:
        print()
        print("=" * 60)
        print("SUCCESS: Processo concluido!")
        print("=" * 60)
        sys.exit(0)
    else:
        print()
        print("=" * 60)
        print("ERROR: Falha ao exportar cookies")
        print("=" * 60)
        print()
        print("Alternativa: Use a extensao do navegador")
        print("Veja o arquivo CONFIGURAR_COOKIES.md para instrucoes detalhadas")
        sys.exit(1)

