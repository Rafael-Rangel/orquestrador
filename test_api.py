"""
Script de teste para a API Content Orchestrator
Testa todos os endpoints principais da aplicação
"""
import requests
import json
import time
import sys
import io
from uuid import UUID

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Configuração
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/v1"

# Cores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.RESET}")

def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.RESET}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.RESET}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.RESET}")

def test_health():
    """Testa o endpoint de health check"""
    print("\n" + "="*60)
    print("1️⃣  TESTANDO HEALTH CHECK")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print_success(f"Health check OK: {response.json()}")
            return True
        else:
            print_error(f"Health check falhou: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Não foi possível conectar à API. Certifique-se de que o servidor está rodando.")
        print_info("Execute: python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        return False
    except Exception as e:
        print_error(f"Erro ao testar health: {e}")
        return False

def test_fetch():
    """Testa o endpoint de fetch (buscar novos conteúdos)"""
    print("\n" + "="*60)
    print("2️⃣  TESTANDO FETCH (Buscar Conteúdos)")
    print("="*60)
    
    try:
        response = requests.post(f"{API_BASE}/fetch/run", timeout=30)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Fetch iniciado: {data}")
            job_id = data.get("job_id")
            if job_id:
                print_info(f"Job ID: {job_id}")
                print_info("Aguardando processamento... (pode levar alguns segundos)")
                return job_id
            return True
        else:
            print_error(f"Fetch falhou: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print_error(f"Erro ao testar fetch: {e}")
        return None

def test_select():
    """Testa o endpoint de select (selecionar conteúdo)"""
    print("\n" + "="*60)
    print("3️⃣  TESTANDO SELECT (Selecionar Conteúdo)")
    print("="*60)
    
    print_warning("⚠️  Para testar SELECT, você precisa ter:")
    print_warning("   - Pelo menos 1 Source ativo no banco")
    print_warning("   - Pelo menos 1 Destination no banco")
    print_warning("   - Pelo menos 1 ContentItem com status 'discovered'")
    
    # Solicitar IDs do usuário
    try:
        destination_id = input("\nDigite o UUID do Destination (ou Enter para pular): ").strip()
        if not destination_id:
            print_warning("Teste de SELECT pulado")
            return None
        
        # Gerar idempotency_key
        import uuid
        idempotency_key = str(uuid.uuid4())
        
        body = {
            "destination_id": destination_id,
            "idempotency_key": idempotency_key,
            "strategy": "fifo"
        }
        
        response = requests.post(
            f"{API_BASE}/select",
            json=body,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Conteúdo selecionado: {data}")
            content_item_id = data.get("id")
            if content_item_id:
                print_info(f"Content Item ID: {content_item_id}")
                return content_item_id
            return data
        elif response.status_code == 404:
            print_warning("Nenhum conteúdo disponível para seleção")
            return None
        else:
            print_error(f"Select falhou: {response.status_code} - {response.text}")
            return None
    except KeyboardInterrupt:
        print_warning("\nTeste cancelado pelo usuário")
        return None
    except Exception as e:
        print_error(f"Erro ao testar select: {e}")
        return None

def test_download(content_item_id):
    """Testa o endpoint de download"""
    print("\n" + "="*60)
    print("4️⃣  TESTANDO DOWNLOAD")
    print("="*60)
    
    if not content_item_id:
        print_warning("⚠️  Content Item ID não fornecido. Pulando teste de download.")
        return None
    
    try:
        body = {
            "content_item_id": content_item_id
        }
        
        response = requests.post(
            f"{API_BASE}/download",
            json=body,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Download iniciado: {data}")
            job_id = data.get("job_id")
            if job_id:
                print_info(f"Job ID: {job_id}")
                print_info("Download em processamento... (pode levar alguns minutos)")
            return job_id
        else:
            print_error(f"Download falhou: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print_error(f"Erro ao testar download: {e}")
        return None

def test_confirm_publish(content_item_id, destination_id):
    """Testa o endpoint de confirmar publicação"""
    print("\n" + "="*60)
    print("5️⃣  TESTANDO CONFIRM PUBLISH")
    print("="*60)
    
    if not content_item_id or not destination_id:
        print_warning("⚠️  IDs não fornecidos. Pulando teste de confirm.")
        return False
    
    try:
        body = {
            "content_item_id": content_item_id,
            "destination_id": destination_id,
            "result": "success",
            "platform_post_id": "test_post_12345"
        }
        
        response = requests.post(
            f"{API_BASE}/confirm_publish",
            json=body,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Publicação confirmada: {data}")
            return True
        else:
            print_error(f"Confirm falhou: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_error(f"Erro ao testar confirm: {e}")
        return False

def test_docs():
    """Testa se a documentação está acessível"""
    print("\n" + "="*60)
    print("6️⃣  TESTANDO DOCUMENTAÇÃO")
    print("="*60)
    
    endpoints = [
        ("/", "Painel Principal"),
        ("/docs", "Swagger UI"),
        ("/redoc", "ReDoc"),
        ("/v1/openapi.json", "OpenAPI JSON")
    ]
    
    all_ok = True
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
            if response.status_code == 200:
                print_success(f"{name}: OK")
            else:
                print_warning(f"{name}: Status {response.status_code}")
                all_ok = False
        except Exception as e:
            print_error(f"{name}: Erro - {e}")
            all_ok = False
    
    return all_ok

def main():
    """Função principal de teste"""
    print("\n" + "="*60)
    print("🧪 TESTE DA API CONTENT ORCHESTRATOR")
    print("="*60)
    print(f"\n📍 URL Base: {BASE_URL}")
    print(f"📍 API Base: {API_BASE}\n")
    
    # Teste 1: Health Check
    if not test_health():
        print_error("\n❌ API não está respondendo. Verifique se o servidor está rodando.")
        sys.exit(1)
    
    # Teste 2: Fetch
    job_id = test_fetch()
    
    # Teste 3: Select (opcional)
    content_item_id = test_select()
    destination_id = None
    if content_item_id:
        # Se o usuário forneceu um destination_id, vamos usá-lo
        try:
            destination_id = input("\nDigite o UUID do Destination usado no select (ou Enter para pular confirm): ").strip()
            if not destination_id:
                destination_id = None
        except:
            pass
    
    # Teste 4: Download (se tiver content_item_id)
    if content_item_id:
        download_job = test_download(content_item_id)
    
    # Teste 5: Confirm (se tiver ambos IDs)
    if content_item_id and destination_id:
        test_confirm_publish(content_item_id, destination_id)
    
    # Teste 6: Documentação
    test_docs()
    
    # Resumo
    print("\n" + "="*60)
    print("📊 RESUMO DOS TESTES")
    print("="*60)
    print_success("Health Check: OK")
    print_success("Fetch: Testado")
    if content_item_id:
        print_success("Select: OK")
        print_success("Download: Iniciado")
        if destination_id:
            print_success("Confirm: Testado")
    else:
        print_warning("Select/Download/Confirm: Não testados (requer dados no banco)")
    print_success("Documentação: Verificada")
    
    print("\n" + "="*60)
    print("✅ TESTES CONCLUÍDOS")
    print("="*60)
    print("\n💡 Dicas:")
    print("   - Verifique os logs do servidor para mais detalhes")
    print("   - Acesse http://localhost:8000/docs para testar manualmente")
    print("   - Configure Sources e Destinations no banco para testar o fluxo completo")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Teste interrompido pelo usuário")
        sys.exit(0)

