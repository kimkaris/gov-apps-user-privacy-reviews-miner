#include <iostream>
#include <fstream>
#include <set>
#include <string>
#include <sstream>
#include <vector>
#include <cctype>

using namespace std;

// Função para dividir uma linha em partes usando a tabulação como delimitador.
vector<string> splitTab(const string &linha)
{
    vector<string> partes;
    string parte;
    stringstream ss(linha);
    while (getline(ss, parte, '\t'))
    {
        partes.push_back(parte);
    }
    return partes;
}

// Função para filtrar comentários por palavras-chave exatas.
bool contemPalavraChave(const string &comentario, const set<string> &KeyWords)
{
    stringstream ss(comentario);
    string palavraComentario;
    while (ss >> palavraComentario)
    {
        string palavraLimpa = "";
        for (char c : palavraComentario)
        {
            if (isalnum(c))
            {
                palavraLimpa += tolower(c);
            }
        }
        if (KeyWords.count(palavraLimpa))
        {
            return true;
        }
    }
    return false;
}

int main()
{
    ifstream leitor("entrada.txt");
    if (!leitor.is_open())
    {
        cerr << "Erro ao abrir o arquivo de entrada." << endl;
        return 1;
    }

    ofstream escritor("saida.txt");
    if (!escritor.is_open())
    {
        cerr << "Erro ao criar arquivo de saída." << endl;
        return 1;
    }
    
    set<string> KeyWords = {"consentimento", "políticas", "política", "regulamento", "regulamentos", "regulatório", "gps", "localização", "localizações", "mapa", "comportamento", "comportamental", "dado", "dados", "informação", "informações", "pessoal", "pessoais", "privado", "compartilhando", "compartilhamento", "compartilha", "segue", "seguindo", "localiza", "localizando", "autorização", "autorizar", "autoriza", "consentimento", "consentir", "consentindo", "permissão", "permitir", "permissões", "propaganda", "propagandas", "anúncio", "anúncios", "publicidade", "publicidades", "adware", "criptografar", "criptografa", "criptografia", "hackear", "hackeando", "hackeado", "hackeada", "hackeia", "inseguro", "insegura", "insegurança", "seguro", "segura", "segurança", "abusivo", "abusiva", "ético", "ética", "código aberto", "código livre", "protegido", "protegida", "proteção", "código-fonte", "confiar", "confia", "confio", "confiável", "antiético", "desprotegida", "desprotegido", "desproteção", "spyware", "fraude", "fraudulento", "engano", "enganação", "enganar", "paga", "pago", "pagar", "pagamento", "pagamentos", "comprar", "compra", "compro", "comprado", "comprada", "enganado", "enganada", "golpe", "golpista", "golpistas", "engana", "assinar", "assinatura", "assinado", "assinante"};

    string linha;
    getline(leitor, linha);
    escritor << linha << endl;

    set<string> comentariosUnicos;
    while (getline(leitor, linha))
    {
        vector<string> partes = splitTab(linha);

        if (partes.size() >= 3)
        {
            string numero = partes[1];
            string comentario = partes[2];
            
            // Verifica se a classificação é de 1 a 5 estrelas
            set<string> numeros = {"1", "2", "3", "4", "5"};
            if (numeros.count(numero))
            {
                // Usa a função de filtro
                if (contemPalavraChave(comentario, KeyWords))
                {
                    if (comentariosUnicos.insert(comentario).second)
                    {
                        escritor << linha << endl;
                    }
                }
            }
        }
    }

    leitor.close();
    escritor.close();

    cout << "Filtragem concluída. Verifique o arquivo 'saida.txt'." << endl;
    return 0;
}