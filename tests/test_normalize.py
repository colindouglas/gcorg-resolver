import pytest

from gc_org_resolver.normalize import normalize


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (
            "Innovation, Science and Economic Development Canada",
            "innovation science economic development",
        ),
        (
            "Bibliothèque et Archives Canada",
            "bibliotheque archives",
        ),
        (
            "Femmes et Égalité des genres Canada",
            "femmes egalite genres",
        ),
        (
            "Canada Revenue Agency / Agence du revenu du Canada",
            "canada revenue agency agence revenu",
        ),
    ],
)
def test_r_docstring_examples(raw: str, expected: str):
    assert normalize(raw) == expected


def test_lowercases_and_strips_diacritics():
    assert normalize("Ministère de l'Emploi") == "ministere emploi"


def test_strips_trailing_canada_variants():
    assert normalize("Department of Finance Canada") == "department finance"
    assert normalize("Finances Canada") == "finances"
    assert normalize("Ministère des Finances du Canada") == "ministere finances"


def test_office_prefix_is_stripped():
    assert normalize("Office of the Auditor General of Canada") == "auditor general"


def test_agency_typos_are_fixed():
    assert normalize("Canada Revenue Agnecy") == "canada revenue agency"
    assert normalize("Canadian Space Ageny") == "canadian space agency"


def test_department_typos_are_fixed():
    assert normalize("Deprtment of Finance") == "department finance"


def test_punctuation_collapses():
    assert normalize("Foo & Bar (Baz)") == "foo bar baz"


def test_whitespace_is_squished():
    assert normalize("  Foo   Bar  ") == "foo bar"


def test_empty_string():
    assert normalize("") == ""


def test_bare_canada_is_not_stripped():
    assert normalize("Canada") == "canada"


def test_trailing_inc_is_stripped():
    assert normalize("Marine Atlantic Inc.") == "marine atlantic"
    assert normalize("Marine Atlantic Inc") == "marine atlantic"


def test_non_trailing_inc_is_preserved():
    assert normalize("Inc Holdings Ltd") == "inc holdings ltd"


def test_email_is_stripped_to_domain():
    assert normalize("user@agr.gc.ca") == "agr.gc.ca"
    assert normalize("first.last@inspection.gc.ca") == "inspection.gc.ca"


def test_email_subdomains_are_stripped():
    assert normalize("user@mail.agr.gc.ca") == "agr.gc.ca"
    assert normalize("user@a.b.cra-arc.gc.ca") == "cra-arc.gc.ca"


def test_email_canada_ca_suffix():
    assert normalize("user@sub.fintrac-canafe.canada.ca") == "fintrac-canafe.canada.ca"


def test_email_generic_tld():
    assert normalize("user@sub.example.ca") == "example.ca"


def test_non_email_unchanged():
    assert normalize("Folding @ Home") == "folding @ home"


def test_abbreviation_dots_are_stripped():
    assert normalize("St. John's") == "st john s"
    assert normalize("Intl. Trade") == "intl trade"


def test_domain_dots_are_preserved():
    assert normalize("agr.gc.ca") == "agr.gc.ca"