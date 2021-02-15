from codecs import BOM_UTF8, BOM_UTF16_BE, BOM_UTF16_LE, BOM_UTF32_BE, BOM_UTF32_LE

BOMS = (
    (BOM_UTF8, "UTF-8"),
    (BOM_UTF32_BE, "UTF-32-BE"),
    (BOM_UTF32_LE, "UTF-32-LE"),
    (BOM_UTF16_BE, "UTF-16-BE"),
    (BOM_UTF16_LE, "UTF-16-LE"),
)


def check_bom(data):
    return [encoding for bom, encoding in BOMS if data.startswith(bom)]


def is_utf8_without_bom(data):
    try:
        data.decode("UTF-8")
    except UnicodeDecodeError:
        return False
    else:
        if len(check_bom(data)) == 0:
            return True
        else:
            return False
