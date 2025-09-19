from google_play_scraper import reviews_all
import pandas as pd
import re


APP_IDS = [
    "br.gov.serpro.cnhe",
    "br.gov.meugovbr",
    "br.gov.dataprev.meuinss"
]

# Lista de palavras-chave relacionadas à acessibilidade
KEYWORDS = [
    'consentimento', 'políticas', 'política', 'regulamento', 'regulamentos', 'regulatório', 'gps', 'localização',
    'localizações', 'mapa', 'comportamento', 'comportamental', 'dado', 'dados', 'informação', 'informações', 'pessoal',
    'pessoais', 'privado', 'compartilhando', 'compartilhamento', 'compartilha', 'segue', 'seguindo', 'localiza',
    'localizando', 'autorização', 'autorizar', 'autoriza', 'consentimento', 'consentir', 'consentindo', 'permissão',
    'permitir', 'permissões', 'propaganda', 'propagandas', 'anúncio', 'anúncios', 'publicidade', 'publicidades', 'adware',
    'criptografar', 'criptografa', 'criptografia', 'hackear', 'hackeando', 'hackeado', 'hackeada', 'hackeia', 'inseguro',
    'insegura', 'insegurança', 'seguro', 'segura', 'segurança', 'abusivo', 'abusiva', 'ético', 'ética', 'código aberto',
    'código livre', 'protegido', 'protegida', 'proteção', 'código-fonte', 'confiar', 'confia', 'confio', 'confiável',
    'antiético', 'desprotegida', 'desprotegido', 'desproteção', 'inseguro', 'insegura', 'insegurança', 'spyware', 'fraude',
    'fraudulento', 'engano', 'enganação', 'enganar', 'paga', 'pago', 'pagar', 'pagamento', 'pagamentos', 'comprar',
    'compra', 'compro', 'comprado', 'comprada', 'enganado', 'enganada', 'golpe', 'golpista', 'golpistas', 'engana',
    'assinar', 'assinatura', 'assinado', 'assinante'
]

def limpar_texto(texto):
    if texto is None:
        return ""
    return re.sub(r"[\x00-\x08\x0B-\x1F\x7F-\x9F]", "", texto)


def coletar_comentarios(app_ids, max_estrelas=None, filtrar_por_keywords=False):
    resultados = []

    for app_id in app_ids:
        print(f"\n🔍 Coletando comentarios do app: {app_id}")
        comentarios = reviews_all(
            app_id,
            lang='pt',
            country='br'
        )

        print(f"  → Total de comentarios encontrados: {len(comentarios)}")

        for idx, comentario in enumerate(comentarios, 1):
            nota = comentario['score']
            texto = comentario.get('content')

            if texto is None:
                continue

            texto_lower = texto.lower()

            if max_estrelas is not None and nota > max_estrelas:
                continue

            if filtrar_por_keywords:
                if not any(palavra in texto_lower for palavra in KEYWORDS):
                    continue

            resultados.append({
                "app_id": app_id,
                "estrelas": nota,
                "comentario": limpar_texto(texto)
            })

            if idx % 100 == 0:
                print(f"    → Processados {idx} comentarios...")

    return resultados


def salvar_em_xlsx_dividido(comentarios, nome_base="comentarios_apps"):
    max_linhas = 1_000_000
    total = len(comentarios)
    partes = (total // max_linhas) + (1 if total % max_linhas else 0)

    for i in range(partes):
        parte_df = pd.DataFrame(comentarios[i * max_linhas : (i + 1) * max_linhas])
        nome_arquivo = f"{nome_base}_parte_{i+1}.xlsx"
        parte_df.to_excel(nome_arquivo, index=False, columns=["app_id", "estrelas", "comentario"])
        print(f"✅ Arquivo salvo: {nome_arquivo} ({len(parte_df)} comentarios)")


try:
    estrelas_input = input("Numero maximo de estrelas (1 a 5) ou deixe vazio para todos: ").strip()
    max_estrelas = int(estrelas_input) if estrelas_input else None
    if max_estrelas not in [1, 2, 3, 4, 5, None]:
        raise ValueError()
except:
    print("Entrada invalida. Pegando todos os comentarios.")
    max_estrelas = None

filtro_kw_input = input("filtrar por palavras-chave de acessibilidade? (s/n): ").strip().lower()
filtrar_keywords = filtro_kw_input == 's'


comentarios_filtrados = coletar_comentarios(APP_IDS, max_estrelas, filtrar_keywords)
salvar_em_xlsx_dividido(comentarios_filtrados)
