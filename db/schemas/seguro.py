def seguro_schema(seguro: list) -> list:
    return {
        "id_seguro": seguro["id_seguro"],
        "id_transporte_extranjero": seguro["id_transporte_extranjero"],
        "cobertura": seguro["cobertura"],
        "fecha_inicio": seguro["fecha_inicio"],
        "fecha_fin": seguro["fecha_fin"],
        "costo": seguro["costo"]
    }