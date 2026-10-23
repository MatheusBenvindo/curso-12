def calcular_media(notas):
    if not isinstance(notas, list) or len(notas) != 3:
        raise ValueError('Informe exatamente três notas em uma lista.')
    for nota in notas:
        if isinstance(nota, bool) or not isinstance(nota, (int, float)):
            raise ValueError('Cada nota deve ser um número entre 0 e 10.')
        if not 0 <= nota <= 10:
            raise ValueError('Cada nota deve ser um número entre 0 e 10.')
    return round(sum(notas) / 3, 2)
