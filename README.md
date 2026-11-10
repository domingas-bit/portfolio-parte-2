# Portfólio de Programação Matemática – Parte 2

**Disciplina:** Estruturas Matemáticas para Computação – Matemática Discreta  
**Linguagem:** Python  


## Arquivos

- `atividade1_congruencia_tcr.py` — verificação de congruência e resolução de sistemas com 3 ou 4 congruências pelo Teorema Chinês do Resto.
- `documento_explicativo_atividade1.docx` — explicação dos métodos, cálculos e testes da Atividade 1.
- `atividade2_rsa.py` — primalidade, parâmetros RSA, chaves, cifragem, decifragem, Euler, Fermat e exponenciação modular.
- `documento_explicativo_atividade2.docx` — explicação dos métodos, cálculos e testes da Atividade 2.

## Como executar

Abra o terminal na pasta dos arquivos e execute:

```bash
python atividade1_congruencia_tcr.py
```

ou

```bash
python atividade2_rsa.py
```

## Procedimentos implementados no código

Os procedimentos matemáticos centrais foram programados nos próprios arquivos:

- MDC pelo algoritmo de Euclides;
- inverso multiplicativo pelo algoritmo estendido de Euclides;
- teste de primalidade por tentativa de divisores até a raiz quadrada;
- exponenciação modular por quadrados sucessivos;
- composição e verificação da solução do Teorema Chinês do Resto.


## Casos de teste conferidos

### Atividade 1

1. Congruência: `a = 23`, `b = 8`, `n = 5` → diferença 15, resto 0.
2. TCR: `x ≡ 2 (mod 3)`, `x ≡ 3 (mod 5)`, `x ≡ 2 (mod 7)` → `x₀ = 23`, `N = 105`.
3. TCR com quatro congruências: `x ≡ 1 (mod 3)`, `x ≡ 2 (mod 5)`, `x ≡ 3 (mod 7)`, `x ≡ 4 (mod 11)` → `x₀ = 367`, `N = 1155`.
4. Módulos não coprimos → o sistema é recusado, conforme as condições do enunciado.

### Atividade 2

Com `p = 17`, `q = 5`, `e = 11` e `M = 19`:

- `n = 85` e `φ(n) = 64`;
- `d = 35`, pois `11 · 35 ≡ 1 (mod 64)`;
- cifragem: `19¹¹ mod 85 = 59`;
- decifragem: `59³⁵ mod 85 = 19`;
- demonstração de Euler: `19⁶⁴ mod 85 = 1`;
- demonstração de Fermat: `19¹⁶ mod 17 = 1`.

