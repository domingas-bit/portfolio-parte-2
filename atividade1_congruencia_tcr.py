"""
ATIVIDADE 1 - CONGRUENCIA MODULAR E TEOREMA CHINES DO RESTO

Programa desenvolvido para a Continuacao do Portfolio de Programacao
Matematica - Parte 2 (Estruturas Matematicas para Computacao).

Nao utiliza math.gcd, pow(base, expoente, modulo) ou bibliotecas externas.
Os procedimentos de MDC e inverso modular sao implementados neste arquivo.
"""


def ler_inteiro(mensagem):
    """Le uma entrada inteira, repetindo a solicitacao em caso de erro."""
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Entrada invalida. Digite um numero inteiro.")


def mdc(a, b):
    """Calcula o maximo divisor comum pelo algoritmo de Euclides."""
    a, b = abs(a), abs(b)
    while b != 0:
        resto = a % b
        a, b = b, resto
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
    if modulo <= 0:
        raise ValueError("O modulo deve ser positivo.")
    if modulo == 1:
        # Em modulo 1, 0 e congruente a 1; o valor residual e 0.
        return 0, 1, 0, 0, []

    divisor, x, y, passos = euclides_estendido(a, modulo)
    if divisor != 1:
        raise ValueError(
            f"Nao existe inverso: MDC({a}, {modulo}) = {divisor}, diferente de 1."
        )
    return x % modulo, divisor, x, y, passos


def mostrar_euclides(a, b, passos):
    print(f"Aplicando o algoritmo de Euclides a {a} e {b}:")
    if not passos:
        print("Nao foram necessarias divisoes.")
    for dividendo, divisor, quociente, resto in passos:
        print(
            f"  {dividendo} = {divisor} * {quociente} + {resto}"
        )


def verificar_congruencia():
    print("\n--- PARTE A: VERIFICACAO DE CONGRUENCIA ---")
    a = ler_inteiro("Digite o valor de a: ")
    b = ler_inteiro("Digite o valor de b: ")
    n = ler_inteiro("Digite o modulo n (n deve ser positivo): ")
    while n <= 0:
        print("O modulo precisa ser maior que zero.")
        n = ler_inteiro("Digite novamente n: ")

    diferenca = a - b
    quociente = diferenca // n
    resto = diferenca % n

    print("\nCalculo:")
    print(f"  a - b = {a} - ({b}) = {diferenca}")
    print(f"  {diferenca} = {n} * ({quociente}) + {resto}")
    print(f"  Resto de ({a} - ({b})) por {n}: {resto}")

    if resto == 0:
        print(f"Conclusao: {a} e {b} SAO congruentes modulo {n}.")
        print(f"Portanto, {a} == {b} (mod {n}).")
    else:
        print(f"Conclusao: {a} e {b} NAO sao congruentes modulo {n}.")
        print("Justificativa: a diferenca nao possui resto zero nesse modulo.")


def resolver_tcr():
    print("\n--- PARTE B: TEOREMA CHINES DO RESTO ---")
    quantidade = ler_inteiro("Escolha a quantidade de congruencias (3 ou 4): ")
    while quantidade not in (3, 4):
        print("A quantidade deve ser 3 ou 4.")
        quantidade = ler_inteiro("Digite 3 ou 4: ")

    restos = []
    modulos = []
    for indice in range(quantidade):
        print(f"\nCongruencia {indice + 1}: x == a{indice + 1} (mod n{indice + 1})")
        a = ler_inteiro(f"  Digite a{indice + 1} (resto): ")
        n = ler_inteiro(f"  Digite n{indice + 1} (modulo positivo): ")
        while n <= 0:
            print("  O modulo deve ser positivo.")
            n = ler_inteiro(f"  Digite novamente n{indice + 1}: ")
        restos.append(a)
        modulos.append(n)

    print("\nVerificacao dos modulos, dois a dois:")
    coprimos = True
    for i in range(quantidade):
        for j in range(i + 1, quantidade):
            divisor = mdc(modulos[i], modulos[j])
            print(f"  MDC({modulos[i]}, {modulos[j]}) = {divisor}")
            if divisor != 1:
                coprimos = False

    if not coprimos:
        print("Sistema fora das condicoes desta atividade: os modulos nao sao")
        print("dois a dois coprimos. Nao e possivel aplicar o TCR nesta forma.")
        return

    produto_total = 1
    for n in modulos:
        produto_total *= n
    print("\nProduto dos modulos:")
    fatores = " * ".join(str(n) for n in modulos)
    print(f"  N = {fatores} = {produto_total}")

    soma = 0
    print("\nCalculo dos termos do Teorema Chines do Resto:")
    for indice in range(quantidade):
        a = restos[indice]
        n = modulos[indice]
        parcial = produto_total // n
        inverso, divisor, coeficiente, coeficiente_modulo, passos = inverso_modular(parcial, n)

        print(f"\nCongruencia {indice + 1}: x == {a} (mod {n})")
        print(f"  N{indice + 1} = N / n{indice + 1} = {produto_total} / {n} = {parcial}")
        print(f"  MDC({parcial}, {n}) = {divisor}")
        if n == 1:
            print("  Modulo 1: o representante residual do inverso e 0.")
        else:
            mostrar_euclides(parcial, n, passos)
            print(
                f"  Identidade de Bezout: {parcial} * ({coeficiente}) "
                f"+ {n} * ({coeficiente_modulo}) = 1"
            )
            print(f"  Inverso: {parcial}^(-1) mod {n} = {inverso}")
            print(f"  Conferencia: ({parcial} * {inverso}) mod {n} = {(parcial * inverso) % n}")

        termo = a * parcial * inverso
        soma += termo
        print(f"  Termo: a{indice + 1} * N{indice + 1} * inverso")
        print(f"       = {a} * {parcial} * {inverso} = {termo}")

    solucao = soma % produto_total
    print("\nSoma dos termos:")
    print(f"  S = {soma}")
    print(f"  x0 = S mod N = {soma} mod {produto_total} = {solucao}")

    print("\nVerificacao da solucao em todas as congruencias:")
    verificou = True
    for indice in range(quantidade):
        resto_obtido = solucao % modulos[indice]
        correto = resto_obtido == restos[indice] % modulos[indice]
        print(
            f"  {solucao} mod {modulos[indice]} = {resto_obtido}; "
            f"resto esperado = {restos[indice] % modulos[indice]} "
            f"-> {'OK' if correto else 'ERRO'}"
        )
        if not correto:
            verificou = False

    if verificou:
        print("\nConclusao: todas as congruencias foram satisfeitas.")
        print(f"Solucao principal: x == {solucao} (mod {produto_total}).")
        print(f"Solucao geral: x = {solucao} + t * {produto_total}, com t pertencente a Z.")
    else:
        print("Erro na verificacao. Confira os dados e os calculos.")


def menu():
    while True:
        print("\n===============================================")
        print(" ATIVIDADE 1 - CONGRUENCIA MODULAR E TCR")
        print("===============================================")
        print("1 - Verificar se a e b sao congruentes modulo n")
        print("2 - Resolver sistema pelo Teorema Chines do Resto")
        print("0 - Encerrar")
        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            verificar_congruencia()
        elif opcao == "2":
            resolver_tcr()
        elif opcao == "0":
            print("Programa encerrado.")
            break
        else:
            print("Opcao invalida. Escolha 1, 2 ou 0.")


if __name__ == "__main__":
    menu()
