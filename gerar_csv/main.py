import random
import csv
from datetime import datetime, timedelta

# ---------- Listas base ----------
nomes_masc = ["Douglas","João","Pedro","Lucas","Gabriel","Rafael","Bruno","Felipe","Thiago","Matheus",
              "Carlos","Eduardo","Vinícius","Leonardo","Gustavo","Rodrigo","Marcelo","André","Fábio","Diego"]
nomes_fem = ["Ana","Maria","Juliana","Fernanda","Camila","Patrícia","Larissa","Beatriz","Amanda","Letícia",
             "Carolina","Bruna","Gabriela","Mariana","Vanessa","Aline","Tatiane","Renata","Débora","Priscila"]
sobrenomes = ["Silva","Santos","Oliveira","Souza","Lima","Pereira","Costa","Ferreira","Rodrigues","Almeida",
              "Nascimento","Carvalho","Araújo","Ribeiro","Gomes","Martins","Barbosa","Rocha","Dias","Monteiro"]

instituicoes = ["Itpro","Universidade Federal do Rio de Janeiro","USP","Unicamp","Petrobras","Embrapa",
                "Fiocruz","INPE","IBM Brasil","Google Brasil","Microsoft Brasil","SENAI","SESI","Sebrae",
                "Prefeitura de São Paulo","Governo do Estado","Ministério da Saúde","Hospital Sírio-Libanês",
                "Banco do Brasil","Caixa Econômica","Vale","Embraer","Ambev","Natura","Magazine Luiza"]

cargos = ["Analista de tecnologia","Professor","Pesquisador","Engenheiro","Coordenador","Gerente",
          "Diretor","Consultor","Desenvolvedor","Designer","Assistente","Estagiário","Supervisor",
          "Especialista","Técnico","Administrador","Cientista de Dados","Arquiteto de Software"]

departamentos = ["Tecnologia","Educação","Saúde","Engenharia","Administração","Marketing","Financeiro",
                 "Recursos Humanos","Operações","Pesquisa e Desenvolvimento","Comercial","Jurídico"]

categorias = ["Participante","Palestrante","Organizador","Expositor","Imprensa","Convidado","Staff"]

# Pares (País Residência, Nacionalidade) — sempre alinhados
paises_nacionalidades = [
    ("Brasil", "Brasileira"),
    ("Brasil", "Brasileira"),
    ("Brasil", "Brasileira"),
    ("Brasil", "Brasileira"),
    ("Brasil", "Brasileira"),
    ("Brasil", "Brasileira"),
    ("Brasil", "Brasileira"),
    ("Brasil", "Brasileira"),
    ("Portugal", "Portuguesa"),
    ("EUA", "Americana"),
    ("Argentina", "Argentina"),
    ("Chile", "Chilena"),
    ("Espanha", "Espanhola"),
    ("Canadá", "Canadense"),
    ("Alemanha", "Alemã"),
]

# Dias possíveis do evento
dias_evento = ["2026-11-30", "2026-12-01", "2026-12-02"]


# ---------- Gerador de CPF válido ----------
def gerar_cpf_valido():
    def dv(nums):
        soma = sum(n * peso for n, peso in zip(nums, range(len(nums) + 1, 1, -1)))
        resto = soma % 11
        return '0' if resto < 2 else str(11 - resto)

    base = [random.randint(0, 9) for _ in range(9)]
    d1 = dv(base)
    d2 = dv(base + [int(d1)])
    return ''.join(map(str, base)) + d1 + d2


# ---------- Geração dos dados ----------
random.seed(42)
rows = []
usados_email = set()
usados_cpf = set()

for i in range(1, 501):
    # Nome
    genero = random.choice(['M', 'F'])
    nome = random.choice(nomes_masc if genero == 'M' else nomes_fem)
    nome += " " + random.choice(sobrenomes)
    if random.random() < 0.6:
        nome += " " + random.choice(sobrenomes)

    # Email único
    base_email = (nome.lower()
                  .replace(" ", ".")
                  .replace("á", "a").replace("ã", "a").replace("â", "a").replace("à", "a")
                  .replace("é", "e").replace("ê", "e")
                  .replace("í", "i")
                  .replace("ó", "o").replace("ô", "o").replace("õ", "o")
                  .replace("ú", "u")
                  .replace("ç", "c"))
    email = f"{base_email}{random.randint(1, 999)}@{random.choice(['gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.com.br', 'empresa.com.br'])}"
    while email in usados_email:
        email = f"{base_email}{random.randint(1000, 9999)}@gmail.com"
    usados_email.add(email)

    # Celular
    ddd = random.choice(['11', '21', '31', '41', '51', '61', '71', '81', '85', '62'])
    celular = ddd + '9' + ''.join(str(random.randint(0, 9)) for _ in range(8))

    # Nascimento
    ano = random.randint(1960, 2004)
    mes = random.randint(1, 12)
    dia = random.randint(1, 28)
    nascimento = f"{dia:02d}/{mes:02d}/{ano}"

    # País residência e nacionalidade (par sempre coerente)
    pais_res, nacionalidade = random.choice(paises_nacionalidades)

    # Documento: brasileiro → CPF | estrangeiro → passaporte
    if pais_res == "Brasil":
        tipo_doc = "cpf"
        passaporte = ""
        cpf = gerar_cpf_valido()
        while cpf in usados_cpf:
            cpf = gerar_cpf_valido()
        usados_cpf.add(cpf)
    else:
        tipo_doc = "passaporte"
        cpf = ""
        passaporte = f"{random.choice(['AB', 'CD', 'EF', 'GH'])}{random.randint(100000, 999999)}"

    # Instituição
    inst = random.choice(instituicoes)
    cargo = random.choice(cargos)
    depto = random.choice(departamentos)
    pais_inst = "Brasil" if random.random() < 0.9 else random.choice([p for p, _ in paises_nacionalidades])

    # Categoria
    categoria = random.choices(categorias, weights=[70, 8, 5, 5, 3, 5, 4])[0]

    # Credenciado / Bloqueado / Pagamento
    credenciado = random.choices(["Sim", "Não"], weights=[85, 15])[0]
    bloqueado = random.choices(["Não", "Sim"], weights=[95, 5])[0]
    pagamento = random.choices(["free", "pago", "pendente", "cancelado"], weights=[70, 20, 7, 3])[0]

    # Consentimentos
    politica = random.choices(["Sim", "Não"], weights=[95, 5])[0]
    termos = random.choices(["Sim", "Não"], weights=[97, 3])[0]
    imagem = random.choices(["Sim", "Não"], weights=[80, 20])[0]

    # Dias inscritos (1 a 3 dias)
    qtd_dias = random.choices([1, 2, 3], weights=[25, 35, 40])[0]
    dias_escolhidos = sorted(random.sample(dias_evento, qtd_dias))
    dias_str = "".join(f"{d} -  |  " for d in dias_escolhidos)

    # Data de cadastro entre 01/09/2026 e 15/10/2026
    inicio = datetime(2026, 9, 1)
    data_cad = inicio + timedelta(days=random.randint(0, 44),
                                  hours=random.randint(0, 23),
                                  minutes=random.randint(0, 59),
                                  seconds=random.randint(0, 59))
    data_cad_str = data_cad.strftime("%d/%m/%Y, %H:%M:%S")

    row = [
        str(i),
        nome,
        nome,
        email,
        celular,
        nascimento,
        nacionalidade,
        pais_res,
        tipo_doc,
        cpf,
        passaporte,
        inst,
        cargo,
        depto,
        pais_inst,
        categoria,
        credenciado,
        bloqueado,
        pagamento,
        politica,
        termos,
        imagem,
        dias_str,
        data_cad_str,
    ]
    rows.append(row)


# ---------- Salvar CSV ----------
header = ["ID", "Nome Completo", "Nome Crachá", "Email", "Celular", "Nascimento", "Nacionalidade",
          "País Residência", "Tipo Documento", "CPF", "Passaporte", "Instituição", "Cargo",
          "Departamento", "País Instituição", "Categoria", "Credenciado", "Bloqueado",
          "Status Pagamento", "Política Privacidade", "Termos Participação", "Uso Imagem",
          "Dias Inscritos", "Data Cadastro"]

with open("participantes_evento.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, quoting=csv.QUOTE_ALL)
    w.writerow(header)
    w.writerows(rows)

print("Arquivo 'participantes_evento.csv' gerado com 500 participantes.")
print("\n--- Amostra (5 primeiros) ---")
for r in rows[:5]:
    print(r)