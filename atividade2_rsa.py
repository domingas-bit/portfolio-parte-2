"""
ATIVIDADE 2 - CRIPTOGRAFIA RSA

Programa desenvolvido para a Continuacao do Portfolio de Programacao
Matematica - Parte 2 (Estruturas Matematicas para Computacao).

Os procedimentos centrais sao implementados neste arquivo: teste de
primalidade, MDC, Euclides estendido, inverso modular e exponenciacao
modular por quadrados sucessivos. Nao utiliza math.gcd, sympy ou
pow(base, expoente, modulo).
"""


def ler_inteiro(mensagem):
    """Le uma entrada inteira, repetindo a solicitacao em caso de erro."""
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Entrada invalida. Digite um numero inteiro.")


def eh_primo(numero):
    """Testa primalidade por divisao experimental ate a raiz quadrada."""
    if numero <= 1:
        return False, None
    if numero == 2:
        return True, []
    if numero % 2 == 0:
        return False, [(2, numero % 2)]

    testes = []
    divisor = 3
    while divisor * divisor <= numero:
        resto = numero % divisor
        testes.append((divisor, resto))
        if resto == 0:
            return False, testes
        divisor += 2
    return True, testes


def mdc(a, b):
    """Calcula o maximo divisor comum pelo algoritmo de Euclides."""
    a, b = abs(a), abs(b)
    while b != 0:
        a, b = b, a % b
    return a


def euclides_estendido(a, b):
    """Retorna (g, x, y, passos), com a*x + b*y = g = MDC(a,b)."""
    sinal_a = 1 if a >= 0 else -1
    sinal_b = 1 if b >= 0 else -1
    r_anterior, r_atual = abs(a), abs(b)
    x_anterior, x_atual = 1, 0
    y_anterior, y_atual = 0, 1
    passos = []

    while r_atual != 0:
        quociente = r_anterior // r_atual
        resto = r_anterior - quociente * r_atual
        passos.append((r_anterior, r_atual, quociente, resto))
        r_anterior, r_atual = r_atual, resto
        x_anterior, x_atual = x_atual, x_anterior - quociente * x_atual
        y_anterior, y_atual = y_atual, y_anterior - quociente * y_atual

    return r_anterior, x_anterior * sinal_a, y_anterior * sinal_b, passos


def inverso_modular(a, modulo):
    """Encontra o inverso de a modulo modulo pelo Euclides estendido."""
    if modulo <= 1:
        raise ValueError("Para o RSA, o modulo do inverso deve ser maior que 1.")
    divisor, x, y, passos = euclides_estendido(a, modulo)
    if divisor != 1:
        raise ValueError(
            f"Nao existe inverso: MDC({a}, {modulo}) = {divisor}, diferente de 1."
        )
    return x % modulo, divisor, x, y, passos


def mostrar_euclides(a, b, passos):
    print(f"Aplicando Euclides a {a} e {b}:")
    for dividendo, divisor, quociente, resto in passos:
        print(f"  {dividendo} = {divisor} * {quociente} + {resto}")


def potencia_modular(base, expoente, modulo):
    """Calcula base**expoente modulo modulo por quadrados sucessivos."""
    if modulo <= 0:
        raise ValueError("O modulo deve ser positivo.")
    if expoente < 0:
        raise ValueError("O expoente deve ser nao negativo.")

    base_original = base
    expoente_original = expoente
    base_atual = base % modulo
    expoente_atual = expoente
    resultado = 1 % modulo
    passos = []

    while expoente_atual > 0:
        expoente_antes = expoente_atual
        base_antes = base_atual
        resultado_antes = resultado
        bit = expoente_atual % 2

        if bit == 1:
            resultado = (resultado * base_atual) % modulo
            operacao = (
                f"resultado = ({resultado_antes} * {base_antes}) mod {modulo} "
                f"= {resultado}"
            )
        else:
            operacao = "expoente par: resultado permanece igual"

        expoente_atual = expoente_atual // 2
        base_atual = (base_atual * base_atual) % modulo
        passos.append({
            "expoente": expoente_antes,
            "base": base_antes,
            "bit": bit,
            "resultado_antes": resultado_antes,
            "operacao": operacao,
            "resultado": resultado,
            "proximo_expoente": expoente_atual,
            "proxima_base": base_atual,
        })

    return resultado, passos, base_original, expoente_original


def mostrar_potencia(base, expoente, modulo, resultado, passos, titulo):
    print(f"\n{titulo}")
    print(f"Calcular {base}^{expoente} mod {modulo} por quadrados sucessivos:")
    if not passos:
        print(f"  Expoente zero: resultado = 1 mod {modulo} = {resultado}")
    for indice, passo in enumerate(passos, start=1):
        print(
            f"  Passo {indice}: expoente = {passo['expoente']}, "
            f"base reduzida = {passo['base']}, "
            f"expoente {'impar' if passo['bit'] else 'par'}"
        )
        print(f"    {passo['operacao']}")
        print(
            f"    Proxima etapa: expoente = {passo['proximo_expoente']}; "
            f"base ao quadrado mod {modulo} = {passo['proxima_base']}"
        )
    print(f"  Resultado final: {base}^{expoente} mod {modulo} = {resultado}")


def escolher_primos():
    while True:
        print("\n--- PARTE A: PARAMETROS RSA ---")
        p = ler_inteiro("Digite o primeiro primo p: ")
        q = ler_inteiro("Digite o segundo primo q: ")

        if p <= 1 or q <= 1:
            print("p e q devem ser inteiros maiores que 1. Tente novamente.")
            continue
        if p == q:
            print("Os primos precisam ser distintos. Tente novamente.")
            continue

        p_primo, testes_p = eh_primo(p)
        q_primo, testes_q = eh_primo(q)
        print("\nVerificacao de primalidade:")
        print(f"  p = {p}: {'primo' if p_primo else 'nao primo'}")
        if testes_p:
            for divisor, resto in testes_p:
                print(f"    Teste: {p} mod {divisor} = {resto}")
        print(f"  q = {q}: {'primo' if q_primo else 'nao primo'}")
        if testes_q:
            for divisor, resto in testes_q:
                print(f"    Teste: {q} mod {divisor} = {resto}")

        if not p_primo or not q_primo:
            print("Os dois valores devem ser primos. Informe outro par.")
            continue

        n = p * q
        phi = (p - 1) * (q - 1)
        print("\nCalculo dos parametros:")
        print(f"  n = p * q = {p} * {q} = {n}")
        print(f"  phi(n) = (p - 1) * (q - 1) = {p - 1} * {q - 1} = {phi}")

        if phi <= 2:
            print("Nao existe e com 1 < e < phi(n). Escolha outros primos.")
            continue
        return p, q, n, phi


def escolher_expoente_publico(phi):
    print("\n--- ESCOLHA DO EXPOENTE PUBLICO ---")
    while True:
        e = ler_inteiro(f"Digite e, com 1 < e < {phi}: ")
        if not (1 < e < phi):
            print("O expoente precisa estar estritamente entre 1 e phi(n).")
            continue
        divisor = mdc(e, phi)
        print(f"  MDC({e}, {phi}) = {divisor}")
        if divisor != 1:
            print("e e phi(n) nao sao coprimos. Escolha outro e.")
            continue
        print("  Condicao atendida: MDC(e, phi(n)) = 1.")
        return e


def construir_chaves(e, phi, n):
    print("\n--- PARTE B: CONSTRUCAO DAS CHAVES ---")
    d, divisor, coeficiente, coeficiente_phi, passos = inverso_modular(e, phi)
    mostrar_euclides(e, phi, passos)
    print(
        f"Identidade de Bezout: {e} * ({coeficiente}) + "
        f"{phi} * ({coeficiente_phi}) = {divisor}"
    )
    print(f"Inverso modular: d = {coeficiente} mod {phi} = {d}")
    verificacao = (e * d) % phi
    print(f"Conferencia: ({e} * {d}) mod {phi} = {verificacao}")
    if verificacao != 1:
        raise ArithmeticError("Falha ao verificar o inverso modular.")
    print(f"Chave publica: (e, n) = ({e}, {n})")
    print(f"Chave privada: (d, n) = ({d}, {n})")
    return d


def cifrar_decifrar(e, d, n):
    print("\n--- PARTE C: CIFRAGEM E DECIFRAGEM ---")
    mensagem = ler_inteiro(f"Digite M, com 0 <= M < {n}: ")
    while not (0 <= mensagem < n):
        print("Mensagem invalida: M deve estar entre 0 e n-1.")
        mensagem = ler_inteiro(f"Digite novamente M, com 0 <= M < {n}: ")

    cifrada, passos_c, _, _ = potencia_modular(mensagem, e, n)
    mostrar_potencia(mensagem, e, n, cifrada, passos_c, "CIFRAGEM")

    decifrada, passos_d, _, _ = potencia_modular(cifrada, d, n)
    mostrar_potencia(cifrada, d, n, decifrada, passos_d, "DECIFRAGEM")

    print("\nResumo da cifragem:")
    print(f"  Mensagem original: M = {mensagem}")
    print(f"  Mensagem cifrada: C = {cifrada}")
    print(f"  Mensagem decifrada: M' = {decifrada}")
    print(f"  Verificacao: M' == M? {'SIM' if decifrada == mensagem else 'NAO'}")
    if decifrada == mensagem:
        print("Conclusao: a decifragem recuperou o numero original.")
    else:
        print("Conclusao: a verificacao falhou; confira os parametros e os calculos.")

    return mensagem


def demonstrar_euler(base, modulo, phi):
    print("\n--- PARTE D: TEOREMA DE EULER ---")
    divisor = mdc(base, modulo)
    print(f"MDC({base}, {modulo}) = {divisor}")
    if divisor == 1:
        print("Como a base e coprima com o modulo, podemos aplicar Euler:")
        print(f"  {base}^{phi} == 1 (mod {modulo})")
        resultado, passos, _, _ = potencia_modular(base, phi, modulo)
        mostrar_potencia(
            base, phi, modulo, resultado, passos,
            "VERIFICACAO DA IDENTIDADE DE EULER"
        )
        if resultado == 1 % modulo:
            print("  Identidade confirmada para os valores informados.")
        else:
            print("  Resultado inesperado; revise os parametros.")

        expoente = ler_inteiro("Digite um expoente K nao negativo para demonstrar a reducao: ")
        while expoente < 0:
            print("O expoente deve ser nao negativo.")
            expoente = ler_inteiro("Digite K novamente: ")
        expoente_reduzido = expoente % phi
        print(
            f"Pelo Teorema de Euler, como MDC({base}, {modulo}) = 1, "
            f"podemos reduzir K modulo phi(n): {expoente} mod {phi} = {expoente_reduzido}."
        )
        original, passos_original, _, _ = potencia_modular(base, expoente, modulo)
        reduzida, passos_reduzida, _, _ = potencia_modular(base, expoente_reduzido, modulo)
        mostrar_potencia(
            base, expoente, modulo, original, passos_original,
            "POTENCIA COM EXPOENTE ORIGINAL"
        )
        mostrar_potencia(
            base, expoente_reduzido, modulo, reduzida, passos_reduzida,
            "POTENCIA COM EXPOENTE REDUZIDO"
        )
        print(f"Comparacao: {original} == {reduzida}? {'SIM' if original == reduzida else 'NAO'}")
    else:
        print("Euler nao pode ser usado para reduzir expoentes desta base, pois o MDC nao e 1.")
        print("A potencia modular por quadrados sucessivos continua sendo valida.")
        expoente = ler_inteiro("Digite um expoente K nao negativo para calcular sem reduzir por Euler: ")
        while expoente < 0:
            print("O expoente deve ser nao negativo.")
            expoente = ler_inteiro("Digite K novamente: ")
        resultado, passos, _, _ = potencia_modular(base, expoente, modulo)
        mostrar_potencia(
            base, expoente, modulo, resultado, passos,
            "POTENCIACAO MODULAR SEM REDUCAO PELO TEOREMA DE EULER"
        )
        print("  O resultado foi obtido reduzindo a base e cada resultado intermediario modulo n.")


def demonstrar_fermat(primo):
    print("\n--- PARTE D: PEQUENO TEOREMA DE FERMAT ---")
    print(f"O modulo escolhido e p = {primo}, ja verificado como primo.")
    base = ler_inteiro(f"Digite a base a, que nao pode ser divisivel por {primo}: ")
    while base % primo == 0:
        print(f"A base nao pode ser divisivel por {primo}. Tente novamente.")
        base = ler_inteiro("Digite outra base a: ")

    expoente = primo - 1
    resultado, passos, _, _ = potencia_modular(base, expoente, primo)
    print(
        f"Como p = {primo} e primo e {base} nao e divisivel por {primo}, "
        "podemos aplicar Fermat:"
    )
    print(f"  {base}^{primo - 1} == 1 (mod {primo})")
    mostrar_potencia(
        base, expoente, primo, resultado, passos,
        "VERIFICACAO DO PEQUENO TEOREMA DE FERMAT"
    )
    if resultado == 1:
        print("  Identidade confirmada para os valores informados.")
    else:
        print("  Resultado inesperado; revise os parametros.")


def demonstrar_teoremas(base_mensagem, p, n, phi):
    print("\n===============================================")
    print(" PARTE D - TEOREMAS E POTENCIACAO MODULAR")
    print("===============================================")
    print("A potenciacao modular por quadrados sucessivos reduz")
    print("a base e os resultados intermediarios modulo o modulo.")
    demonstrar_euler(base_mensagem, n, phi)
    demonstrar_fermat(p)
    print("\nObservacao importante:")
    print("  O modulo RSA n = p * q e composto; por isso, nao aplicamos")
    print("  diretamente o Pequeno Teorema de Fermat modulo n.")
    print("  Fermat foi demonstrado usando o modulo primo p.")
    print("  Quando Euler nao pode ser aplicado por falta de coprimalidade,")
    print("  a potenciacao modular por quadrados sucessivos continua valida.")


def main():
    print("===============================================")
    print(" ATIVIDADE 2 - CRIPTOGRAFIA RSA")
    print("===============================================")
    p, q, n, phi = escolher_primos()
    e = escolher_expoente_publico(phi)
    d = construir_chaves(e, phi, n)
    mensagem = cifrar_decifrar(e, d, n)
    demonstrar_teoremas(mensagem, p, n, phi)
    print("\nPrograma concluido.")


if __name__ == "__main__":
    main()
