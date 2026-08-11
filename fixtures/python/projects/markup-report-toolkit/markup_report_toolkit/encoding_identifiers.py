# -*- coding: utf-8 -*-
"""Source encoding and Unicode identifiers (PY-CAN-SRC-001).

Demonstrates explicit UTF-8 encoding declaration, non-ASCII identifiers
across declarations, NFKC-equivalent spellings, and visually confusable
but distinct identifiers. A byte-order-mark module is provided separately
as ``bom_module.py`` encoded with UTF-8-SIG.
"""

# Non-ASCII identifiers across modules: report title, author, section
répport = "quarterly-overview"
# Use genuine non-ASCII bindings
titre = "Rapport trimestriel"
auteur_été = "Renée"
résumé = "Résumé du rendement"
Δtotal = 100
Ωμέга = "omega-value"

# Greek identifiers
κείμενο = "markup body"
παράγραφος = "paragraph-1"

# NFKC-equivalent spellings: Angstrom sign U+212B normalizes to Å U+00C5.
# Both spellings refer to the same identifier after NFKC normalization.
Å = "angstrom-normalized"
Å = Å  # same binding after normalization; assignment proves identity
nfkc_same_object = (Å is Å)

# Compatibility decomposition: "ﬁ" (U+FB01) is NFKC-equivalent to "fi".
# Both spellings normalize to the same identifier, so second assignment overwrites first.
ﬁ = "ligature surface"
fi = "ascii surface"  # overwrites same NFKC-normalized binding as ﬁ
nfkc_ligature_collides = (ﬁ == fi and fi == "ascii surface")
nfkc_ligature_equivalence = ("ﬁ".encode("utf-8"), "fi".encode("utf-8"))

# Café example: e-acute as single code point vs e + combining acute
café_single = "single-codepoint é U+00E9"
cafe_combining = "e + combining U+0065 U+0301"
# Identifiers using those spellings — NFKC normalizes combining to single.
café = "single"
café = "combining"  # second line contains U+0065 U+0301; normalized same as café
nfkc_cafe_identity = (café == café)  # same identifier, later assignment overwrites

# Visually confusable but distinct identifiers: Cyrillic 'а' U+0430 vs Latin 'a' U+0061
a_latin = "latin a"
а_cyrillic = "cyrillic a U+0430"  # first char is Cyrillic
# They are distinct objects and distinct bindings
confusable_distinct = (a_latin != а_cyrillic)
confusable_ids = {"latin": a_latin, "cyrillic": а_cyrillic}

# Second set of confusables: Greek omicron 'ο' U+03BF vs Latin 'o'
o_latin = "latin o"
ο_greek = "greek omicron U+03BF"
confusable_greek_distinct = (o_latin != ο_greek)

# Filesystem normalization note: Python source identity is NFKC-normalized,
# while filesystem may use NFC or NFD. This module's filename is NFC.
filesystem_normalization_note = "NFC filename vs NFKC identifier normalization"

# Explicit encoding cookie is valid only at top of file (first or second line).
encoding_cookie_valid = "utf-8 cookie present"

# Unicode identifiers across functions and classes
def résumé_section(titre: str, auteur_été: str) -> str:
    """Return a section header using non-ASCII parameter names."""
    return f"{titre} — {auteur_été}"

class RapportÉlément:
    """Document element with non-ASCII class and attribute names."""

    def __init__(self, κείμενο: str) -> None:
        self.κείμενο = κείμενο

    def παράγραφος_texte(self) -> str:
        return self.κείμενο


# Re-exported values demonstrating cross-module Unicode identifiers
__all__ = [
    "titre",
    "auteur_été",
    "résumé",
    "Δtotal",
    "κείμενο",
    "résumé_section",
    "RapportÉlément",
    "nfkc_same_object",
    "confusable_distinct",
    "filesystem_normalization_note",
]
