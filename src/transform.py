import pandas as pd
import math

def validar_texto(valor):
    if pd.isna(valor):
        return None
    if isinstance(valor, str) and valor.strip() != "":
        return valor.strip()
    return None

def validar_id(valor):
    if pd.isna(valor):
        return None
    try:
        id_numerico = float(valor)
    except (ValueError, TypeError):
        return None
    if not id_numerico.is_integer() or id_numerico <= 0:
        return None
    return int(id_numerico)

def validar_numero(valor):
    if pd.isna(valor):
        return None
    try:
        numero = float(valor)
    except (ValueError, TypeError):
        return None
    if not math.isfinite(numero):
        return None
    return numero


def validar_usuarios(usuarios):
    
    usuarios_validos = []
    ids_vistos = set()
    for usuario in usuarios:
        if 'id' in usuario and 'name' in usuario:
            usuario_id = validar_id(usuario["id"])
            if usuario_id is None:
                print("ID do usuário ausente ou inválido")
                continue
            usuario["id"] = usuario_id
            
            if usuario_id in ids_vistos:
                print(f"ID duplicado encontrado: {usuario_id}")
            else:
                nome_limpo = validar_texto(usuario["name"])
                if nome_limpo is None:
                    print(f"Nome ausente ou inválido para o usuário com ID: {usuario['id']}")
                    continue
                usuario["name"] = nome_limpo

                if "account_limit" in usuario:
                    limite_conta = validar_numero(usuario["account_limit"])
                    if limite_conta is None or limite_conta < 0:
                        print(f"Limite da conta ausente ou inválido para o usuário {usuario_id}")
                        continue
                    usuario["account_limit"] = limite_conta
                else:
                    print("Campo account_limit ausente")
                    continue

                if "card_limit" in usuario:
                    limite_cartao = validar_numero(usuario["card_limit"])
                    if limite_cartao is None or limite_cartao < 0:
                        print(f"Limite do cartão ausente ou inválido para o usuário {usuario_id}")
                        continue
                    usuario["card_limit"] = limite_cartao
                else:
                    print("Campo card_limit ausente")
                    continue

                if "account_balance" in usuario:
                    saldo_conta = validar_numero(usuario["account_balance"])
                    if saldo_conta is None:
                        print(f"Saldo da conta ausente ou inválido para o usuário {usuario_id}")
                        continue
                    usuario["account_balance"] = saldo_conta
                else:
                    print("Campo account_balance ausente")
                    continue
                    

                if "account_number" in usuario:
                    numero_conta = validar_texto(usuario["account_number"])
                    if numero_conta is None:
                        print(f"Número da conta ausente ou inválido para o usuário {usuario_id}")
                        continue
                    usuario["account_number"] = numero_conta
                else:
                    print(f"Campo account_number ausente para o usuário {usuario_id}")
                    continue

                if "account_agency" in usuario:
                    numero_agencia = validar_texto(usuario["account_agency"])
                    if numero_agencia is None:
                        print(f"Número da agência ausente ou inválido para o usuário {usuario_id}")
                        continue
                    usuario["account_agency"] = numero_agencia
                else:
                    print(f"Campo account_agency ausente para o usuário {usuario_id}")
                    continue
                          
                if "card_number" in usuario:
                    numero_cartao = validar_texto(usuario["card_number"])
                    if numero_cartao is None:
                        print(f"Número do cartão ausente ou inválido para o usuário {usuario_id}")
                        continue
                    usuario["card_number"] = numero_cartao
                else:
                    print(f"Campo card_number ausente para o usuário {usuario_id}")
                    continue
                          
                if "account_id" in usuario:
                    id_conta = validar_id(usuario["account_id"])
                    if id_conta is None:
                        print(f"ID da conta ausente ou inválido para o usuário {usuario_id}")
                        continue
                    usuario["account_id"] = id_conta
                else:
                    print(f"Campo account_id ausente para o usuário {usuario_id}")
                    continue
                    
                
                if "card_id" in usuario:
                    id_cartao = validar_id(usuario["card_id"])
                    if id_cartao is None:
                        print(f"ID do cartão ausente ou inválido para o usuário {usuario_id}")
                        continue
                    usuario["card_id"] = id_cartao

                else:
                    print(f"Campo card_id ausente para o usuário {usuario_id}")
                    continue
                
                
                usuarios_validos.append(usuario)
                ids_vistos.add(usuario_id)
                        
                 
        else:
            print(f"Usuário inválido encontrado: {usuario}")
    return usuarios_validos

def gerar_mensagem(cliente, usuario):
    response = cliente.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"""Você é um consultor financeiro com vasta experiencia em produtos e serviços financeiros
              de instituições financeiras varejo. Sugira em mensagens de até 150 caracteres soluções financeiras para o 
              cliente {usuario['name']}. Siga as orientações: 
              1. Escrever em português e usar o nome do cliente. 
              2. Incentivar planejamento financeiro e o hábito de poupar. 
              3. Não inventar produtos, taxas ou prometer rendimentos.
              4. Retornar somente a mensagem, com até 150 caracteres, contando espaços."""}
        ]
    )
    #return response.choices[0].message.content
    mensagem = validar_texto(response.choices[0].message.content)
    if mensagem is None:
        print("Mensagem inválida ou ausente na resposta do modelo.")
        return ""
    if len(mensagem) > 150:
        print("Mensagem excede 150 caracteres. Truncando.")
        mensagem = mensagem[:150]
    return mensagem
