def contrato_schema(contrato: list) -> list:
    return {
        "id_contrato": contrato['id_contrato'],
        "fecha_inicio": contrato['fecha_inicio'],
        "fecha_termino": contrato['fecha_termino'],
        "vigente": contrato['vigente']
    }