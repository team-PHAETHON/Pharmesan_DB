class PillSchemaMapper:
    """
    약 정보 필드명 매핑 도구 (OOP로 캡슐화된 FP)
    """

    _search_mappings = {
        "entpName": "enterprise_name",
        "itemName": "item_name",
        "itemSeq": "item_no",
        "efcyQesitm": "efficacy",
        "useMethodQesitm": "method",
        "atpnWarnQesitm": "warning",
        "atpnQesitm": "attention",
        "intrcQesitm": "interaction",
        "seQesitm": "side_effect",
        "itemImage": "item_image",
        "CHART": "chart",
        "PRINT_FRONT": "print_front",
        "PRINT_BACK": "print_back",
        "DRUG_SHAPE": "drug_shape",
        "COLOR_CLASS1": "color_front",
        "COLOR_CLASS2": "color_back",
        "LINE_FRONT": "line_front",
        "LINE_BACK": "line_back",
        "LENG_LONG": "length_long",
        "LENG_SHORT": "length_short",
        "THICK": "thick",
        "CLASS_NO": "class_no",
        "CLASS_NAME": "class_name",
        "ETC_OTC_NAME": "etc_otc",
        "FORM_CODE_NAME": "form_code_name",
        "ITEM_ENG_NAME": "item_eng_name",
    }

    @classmethod
    def convert(cls, key: str) -> str:
        return cls._search_mappings.get(key, key)
