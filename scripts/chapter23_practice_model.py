"""Pedagogical task model for all 24 Chapter 23 notebooks.

The chapter builders still own examples and narrative.  This module turns the
final exercise into a consistent Example -> Starter -> Task -> Tests -> Hint ->
Solution sequence and assigns stable task cell IDs used by browser graders.
"""

from __future__ import annotations

from dataclasses import dataclass

import nbformat as nbf


@dataclass(frozen=True)
class PracticeSpec:
    task: str
    starter: str
    tests: str
    hint: str
    solution: str | None = None


SPECS: dict[str, PracticeSpec] = {
    "23-01": PracticeSpec(
        "Смоделируйте нажатия `1`, `2`, `+`, `8`, `=`. В task cell должен остаться объект `sostoyanie` с результатом `20`.",
        '''sostoyanie = c.SostoyanieKalkulyatora()

# TODO: передайте объекту четыре символа "12+8", затем нажмите равно.
''',
        '''assert sostoyanie.na_ekrane() == "20"

# Edge case: ошибка вычисления тоже должна стать состоянием экрана, а не падением.
kraj = c.SostoyanieKalkulyatora()
for simvol in "5/0":
    kraj.na_cifru_ili_znak_nazhali(simvol)
kraj.na_ravno_nazhali()
assert kraj.na_ekrane() == "Ошибка"
print("Tests passed")''',
        "Сначала вызывайте `na_cifru_ili_znak_nazhali()` для каждого символа, затем один раз `na_ravno_nazhali()`.",
    ),
    "23-02": PracticeSpec(
        "Напишите `poschitat_varianty(*gruppy)`: число комбинаций равно произведению длин. Пустая группа даёт ноль.",
        '''def poschitat_varianty(*gruppy):
    """Return the number of Cartesian-product combinations."""
    # TODO: multiply len(group) for every group.
    raise NotImplementedError


kolichestvo_variantov = poschitat_varianty(
    sg.PRILAGATELNYE, sg.SUSHESTVITELNYE, sg.MESTA, sg.GLAGOLY, sg.PREDMETY
)''',
        '''assert kolichestvo_variantov == 5 * 5 * 4 * 5 * 4
assert poschitat_varianty([1, 2], ["a", "b", "c"]) == 6
assert poschitat_varianty([], [1, 2]) == 0
print("Tests passed")''',
        "Начните с `result = 1` и умножайте его на `len(group)` в цикле.",
        '''def poschitat_varianty(*gruppy):
    result = 1
    for group in gruppy:
        result *= len(group)
    return result


kolichestvo_variantov = poschitat_varianty(
    sg.PRILAGATELNYE, sg.SUSHESTVITELNYE, sg.MESTA, sg.GLAGOLY, sg.PREDMETY
)''',
    ),
    "23-03": PracticeSpec(
        "Постройте словарь исходов всех девяти пар ходов через `rps.opredelit_pobeditelya()`.",
        '''def tablica_ishodov():
    """Map every (player, computer) pair to its outcome."""
    # TODO: use two nested loops over rps.VARIANTY.
    raise NotImplementedError


ishody_vseh_par = tablica_ishodov()''',
        '''assert len(ishody_vseh_par) == 9
assert ishody_vseh_par[("камень", "ножницы")] == "игрок"
assert ishody_vseh_par[("ножницы", "камень")] == "компьютер"
assert ishody_vseh_par[("бумага", "бумага")] == "ничья"
print("Tests passed")''',
        "Dictionary comprehension может содержать два `for`: один для хода игрока, другой для хода компьютера.",
        '''def tablica_ishodov():
    return {
        (player, computer): rps.opredelit_pobeditelya(player, computer)
        for player in rps.VARIANTY
        for computer in rps.VARIANTY
    }


ishody_vseh_par = tablica_ishodov()''',
    ),
    "23-04": PracticeSpec(
        "Создайте три мяча и выполните 300 шагов по 1/60 секунды. Сохраните список в `myachi`.",
        '''myachi = bb.sozdat_myachi(3)

# TODO: advance every ball for 300 time steps of 1/60 second.
''',
        '''assert len(myachi) == 3
for m in myachi:
    assert m.radius <= m.pos.x <= bb.SHIRINA - m.radius
    assert m.radius <= m.pos.y <= bb.VYSOTA - m.radius
    assert m.otskokov > 0
print("Tests passed")''',
        "Нужны два вложенных цикла: шаги времени снаружи, мячи внутри.",
    ),
    "23-05": PracticeSpec(
        "Проверьте границу шкалы: `0 K` допустим, `-0.01 K` вызывает `ValueError`. Запишите факт отказа в `otkloneno_nizhe_nulya`.",
        '''assert tc.preobrazovat(0, "K")["C"] == -273.15

otkloneno_nizhe_nulya = None
# TODO: call preobrazovat(-0.01, "K") inside try/except ValueError.
''',
        '''assert otkloneno_nizhe_nulya is True
assert tc.preobrazovat(0, "K")["K"] == 0
print("Tests passed")''',
        "Установите флаг в `False` перед вызовом и в `True` только внутри `except ValueError`.",
        '''assert tc.preobrazovat(0, "K")["C"] == -273.15

otkloneno_nizhe_nulya = False
try:
    tc.preobrazovat(-0.01, "K")
except ValueError:
    otkloneno_nizhe_nulya = True''',
    ),
    "23-06": PracticeSpec(
        "Сохраните многострочный UTF-8 текст с кириллицей и emoji в `put_k_zametke`, затем прочитайте его обратно.",
        '''novyj_tekst = """Список покупок:
- хлеб
- сыр
- яблоки 🍎"""

# TODO: save novyj_tekst through na.sohranit_v_fajl(...).
''',
        '''assert na.zagruzit_iz_fajla(put_k_zametke) == novyj_tekst
assert "🍎" in na.zagruzit_iz_fajla(put_k_zametke)
print("Tests passed")''',
        "Передайте путь первым аргументом, текст вторым.",
        '''novyj_tekst = """Список покупок:
- хлеб
- сыр
- яблоки 🍎"""
na.sohranit_v_fajl(put_k_zametke, novyj_tekst)''',
    ),
    "23-07": PracticeSpec(
        "Напишите функцию, разбирающую подкоманду `duplicates` для любого строкового пути.",
        '''def razobrat_duplicates(path_text: str):
    """Parse `safesort duplicates PATH` with the existing parser."""
    # TODO: return parser.parse_args([...]).
    raise NotImplementedError


zadanie_args = razobrat_duplicates("/home/anna/Photos")''',
        '''assert zadanie_args.command == "duplicates"
assert zadanie_args.root == Path("/home/anna/Photos")
assert razobrat_duplicates("/tmp/Photo Archive").root == Path("/tmp/Photo Archive")
print("Tests passed")''',
        "Список argv содержит ровно два элемента: имя подкоманды и путь.",
        '''def razobrat_duplicates(path_text: str):
    return parser.parse_args(["duplicates", path_text])


zadanie_args = razobrat_duplicates("/home/anna/Photos")''',
    ),
    "23-08": PracticeSpec(
        "Напишите `opisat_fajl(path, size)`, создающую `FileInfo` с lower-case suffix.",
        '''def opisat_fajl(path: Path, size: int) -> FileInfo:
    # TODO: construct and return FileInfo.
    raise NotImplementedError


zadanie_info = opisat_fajl(koren / "photo.JPG", 2048)''',
        '''assert zadanie_info.extension == ".jpg"
assert zadanie_info.size == 2048
assert zadanie_info.path.name == "photo.JPG"
assert opisat_fajl(Path("README"), 10).extension == ""
print("Tests passed")''',
        "Расширение находится в `path.suffix`; примените `.lower()`.",
        '''def opisat_fajl(path: Path, size: int) -> FileInfo:
    return FileInfo(path=path, size=size, extension=path.suffix.lower())


zadanie_info = opisat_fajl(koren / "photo.JPG", 2048)''',
    ),
    "23-09": PracticeSpec(
        "Напишите `proverit_propusk_ssylki(root)`: создайте target и symlink, затем верните `True`, если scan пропустил ссылку. При отсутствии поддержки верните `None`.",
        '''def proverit_propusk_ssylki(root: Path):
    # TODO: create photo.jpg and a symlink, call scan(), inspect names.
    raise NotImplementedError
''',
        '''with tempfile.TemporaryDirectory() as tmp:
    rezultat_ssylki = proverit_propusk_ssylki(Path(tmp))
assert rezultat_ssylki in (True, None)

# Edge case: an empty directory has no scan results.
with tempfile.TemporaryDirectory() as tmp:
    assert scan(Path(tmp), Config()) == []
print("Tests passed")''',
        "Перехватите `(OSError, NotImplementedError)` только вокруг `symlink_to()`.",
        '''def proverit_propusk_ssylki(root: Path):
    target = root / "photo.jpg"
    target.write_text("photo", encoding="utf-8")
    link = root / "ssylka_na_foto.jpg"
    try:
        link.symlink_to(target)
    except (OSError, NotImplementedError):
        return None

    names = {file.path.name for file in scan(root, Config())}
    return "photo.jpg" in names and "ssylka_na_foto.jpg" not in names''',
    ),
    "23-10": PracticeSpec(
        "Напишите функцию, добавляющую одно пользовательское имя к exclusions и сохраняющую обязательные исключения.",
        '''def config_s_isklyucheniem(name: str) -> Config:
    # TODO: return Config with DEFAULT_EXCLUDE plus name.
    raise NotImplementedError


svoi_nastrojki = config_s_isklyucheniem("node_modules")''',
        '''assert "node_modules" in svoi_nastrojki.excluded_names()
assert "Sorted" in svoi_nastrojki.excluded_names()
assert ".safesort" in svoi_nastrojki.excluded_names()
assert "build" in config_s_isklyucheniem("build").excluded_names()
print("Tests passed")''',
        "Создайте tuple через `(*DEFAULT_EXCLUDE, name)`.",
        '''def config_s_isklyucheniem(name: str) -> Config:
    return Config(exclude=(*DEFAULT_EXCLUDE, name))


svoi_nastrojki = config_s_isklyucheniem("node_modules")''',
    ),
    "23-11": PracticeSpec(
        "Верните новый mapping с категорией `presentations`, не изменяя DEFAULT_EXTENSIONS.",
        '''def dobavit_presentations(mapping):
    # TODO: return a new dictionary with .pptx and .key.
    raise NotImplementedError


svoi_kategorii = dobavit_presentations(DEFAULT_EXTENSIONS)''',
        '''assert classify(".pptx", svoi_kategorii) == "presentations"
assert classify(".KEY", svoi_kategorii) == "presentations"
assert classify(".pdf", svoi_kategorii) == "documents"
assert "presentations" not in DEFAULT_EXTENSIONS
print("Tests passed")''',
        "Распакуйте исходный словарь через `{**mapping, ...}`.",
        '''def dobavit_presentations(mapping):
    return {**mapping, "presentations": [".pptx", ".key"]}


svoi_kategorii = dobavit_presentations(DEFAULT_EXTENSIONS)''',
    ),
    "23-12": PracticeSpec(
        "Напишите функцию, добавляющую к исходным данным один файл и строящую для него plan.",
        '''def plan_s_dopolnitelnym_fajlom(filename: str):
    # TODO: create FileInfo, append it to fajly, then call build_plan().
    raise NotImplementedError


plan2 = plan_s_dopolnitelnym_fajlom("strannyj.xyz")''',
        '''destination = next(op.destination for op in plan2.operations if op.source.name == "strannyj.xyz")
assert destination == koren / "Sorted" / "other" / "strannyj.xyz"
plan_pdf = plan_s_dopolnitelnym_fajlom("REPORT.PDF")
dest_pdf = next(op.destination for op in plan_pdf.operations if op.source.name == "REPORT.PDF")
assert dest_pdf.parent.name == "documents"
print("Tests passed")''',
        "Расширение можно получить как `Path(filename).suffix`; для классификатора нормализация уже реализована.",
        '''def plan_s_dopolnitelnym_fajlom(filename: str):
    path = koren / filename
    extra = FileInfo(path=path, size=10, extension=path.suffix)
    return build_plan(fajly + [extra], koren, "Sorted", DEFAULT_EXTENSIONS)


plan2 = plan_s_dopolnitelnym_fajlom("strannyj.xyz")''',
    ),
    "23-13": PracticeSpec(
        "Напишите `peremestit_dva(root)`: создайте a.txt и b.txt, выполните один SortPlan и верните результаты.",
        '''def peremestit_dva(root: Path):
    # TODO: create two files, build one SortPlan, call apply_plan().
    raise NotImplementedError
''',
        '''with tempfile.TemporaryDirectory() as tmp:
    test_root = Path(tmp)
    rezultaty3 = peremestit_dva(test_root)
    assert len(rezultaty3) == 2 and all(r.completed for r in rezultaty3)
    assert (test_root / "Sorted/documents/a.txt").read_text() == "A"
    assert (test_root / "Sorted/documents/b.txt").read_text() == "B"
print("Tests passed")''',
        "Обе `MoveOperation` поместите в один tuple `SortPlan.operations`.",
        '''def peremestit_dva(root: Path):
    source_a = root / "a.txt"
    source_b = root / "b.txt"
    source_a.write_text("A", encoding="utf-8")
    source_b.write_text("B", encoding="utf-8")
    destination = root / "Sorted" / "documents"
    plan = SortPlan(
        root=root,
        operations=(
            MoveOperation(source_a, destination / "a.txt"),
            MoveOperation(source_b, destination / "b.txt"),
        ),
    )
    return apply_plan(plan)''',
    ),
    "23-14": PracticeSpec(
        "Напишите функцию, последовательно резервирующую `count` безопасных имён для одного кандидата.",
        '''def svobodnye_imena(candidate: Path, count: int) -> list[Path]:
    # TODO: maintain one reserved set and call _resolve_collision count times.
    raise NotImplementedError


imena2 = svobodnye_imena(papka.parent / "images/photo.jpg", 3)''',
        '''assert [p.name for p in imena2] == ["photo.jpg", "photo (1).jpg", "photo (2).jpg"]
assert svobodnye_imena(Path("README"), 1)[0].name == "README"
assert svobodnye_imena(Path("x.txt"), 0) == []
print("Tests passed")''',
        "После каждого результата добавляйте путь в `reserved` до следующего вызова.",
        '''def svobodnye_imena(candidate: Path, count: int) -> list[Path]:
    reserved = set()
    result = []
    for _ in range(count):
        path = _resolve_collision(candidate, reserved)
        reserved.add(path)
        result.append(path)
    return result


imena2 = svobodnye_imena(papka.parent / "images/photo.jpg", 3)''',
    ),
    "23-15": PracticeSpec(
        "Напишите функцию подсчёта записей с `completed=True`.",
        '''def poschitat_uspeshnye(moves):
    # TODO: count completed moves without changing the list.
    raise NotImplementedError


uspeshnyh = poschitat_uspeshnye(zagruzhennyj["moves"])''',
        '''assert uspeshnyh == 1
assert poschitat_uspeshnye([]) == 0
assert poschitat_uspeshnye([{"completed": True}, {"completed": True}]) == 2
print("Tests passed")''',
        "Подойдёт generator expression внутри `sum()`.",
        '''def poschitat_uspeshnye(moves):
    return sum(1 for move in moves if move["completed"])


uspeshnyh = poschitat_uspeshnye(zagruzhennyj["moves"])''',
    ),
    "23-16": PracticeSpec(
        "Напишите сценарий, где после apply на исходном пути появляется новый файл, а undo сообщает один конфликт и не перезаписывает его.",
        '''def proverit_konflikt_undo(root: Path):
    # TODO: apply one file, write a replacement at the source, then call undo.
    raise NotImplementedError
''',
        '''with tempfile.TemporaryDirectory() as tmp:
    test_root = Path(tmp)
    konflikt, content = proverit_konflikt_undo(test_root)
assert konflikt is True
assert content == "новый файл"
print("Tests passed")''',
        "Сохраните manifest после `apply_plan`, затем создайте новый source до `undo`.",
        '''def proverit_konflikt_undo(root: Path):
    source = root / "otchet.pdf"
    source.write_text("оригинал", encoding="utf-8")
    config = Config()
    plan = build_plan(scan(root, config), root, config)
    moves = apply_plan(plan)
    manifest, _ = write_manifest(root, moves)

    source.write_text("новый файл", encoding="utf-8")
    result = undo(manifest)
    return len(result.conflicts) == 1, source.read_text(encoding="utf-8")''',
    ),
    "23-17": PracticeSpec(
        "Напишите функцию, заменяющую один байт и возвращающую SHA-256 изменённых данных, не меняя исходный bytes.",
        '''def digest_posle_zameny(data: bytes, index: int, new_byte: int) -> str:
    # TODO: build changed bytes and return hashlib.sha256(...).hexdigest().
    raise NotImplementedError


digest_izmenennogo = digest_posle_zameny(soderzhimoe, 0, ord("x"))''',
        '''assert digest_izmenennogo != hashlib.sha256(soderzhimoe).hexdigest()
assert digest_posle_zameny(b"abc", 1, ord("b")) == hashlib.sha256(b"abc").hexdigest()
assert soderzhimoe[0] != ord("x")
print("Tests passed")''',
        "Преобразуйте bytes в `bytearray`, замените элемент, затем верните `bytes(changed)` в hashlib.",
        '''def digest_posle_zameny(data: bytes, index: int, new_byte: int) -> str:
    changed = bytearray(data)
    changed[index] = new_byte
    return hashlib.sha256(bytes(changed)).hexdigest()


digest_izmenennogo = digest_posle_zameny(soderzhimoe, 0, ord("x"))''',
    ),
    "23-18": PracticeSpec(
        "Добавьте к списку два пустых файла и верните результат `find_duplicates()`.",
        '''def gruppy_s_pustoj_paroj(files):
    # TODO: append two zero-byte FileInfo values, then find duplicates.
    raise NotImplementedError


gruppy2 = gruppy_s_pustoj_paroj(fajly)''',
        '''gruppa_pustyh = next(g for g in gruppy2 if g["size"] == 0)
assert {f.name for f in gruppa_pustyh["files"]} == {"pustoj_a.txt", "pustoj_b.txt"}
assert gruppa_pustyh["digest"] == hashlib.sha256(b"").hexdigest()
assert not any(g["size"] == 0 for g in find_duplicates(fajly + [FileInfo("one", 0, b"")]))
print("Tests passed")''',
        "Создайте два `FileInfo` с size 0 и content `b\"\"`.",
        '''def gruppy_s_pustoj_paroj(files):
    return find_duplicates(files + [
        FileInfo("pustoj_a.txt", 0, b""),
        FileInfo("pustoj_b.txt", 0, b""),
    ])


gruppy2 = gruppy_s_pustoj_paroj(fajly)''',
    ),
    "23-19": PracticeSpec(
        "Напишите `config_iz_toml(text)`. Новые категории должны добавляться поверх defaults, а названная встроенная категория должна заменяться.",
        '''def config_iz_toml(text: str) -> Config:
    # TODO: parse text and apply defaults + category-specific overrides.
    raise NotImplementedError


nastrojki_minimalnye = config_iz_toml('destination = "Sorted2"\\n')''',
        '''assert nastrojki_minimalnye.destination == "Sorted2"
assert nastrojki_minimalnye.extensions == DEFAULT_EXTENSIONS
with_books = config_iz_toml('[extensions]\\nbooks = [".epub"]\\n')
assert with_books.extensions["books"] == [".epub"]
assert with_books.extensions["documents"] == DEFAULT_EXTENSIONS["documents"]
overridden = config_iz_toml('[extensions]\\ndocuments = [".md"]\\n')
assert overridden.extensions["documents"] == [".md"]
print("Tests passed")''',
        "Сначала скопируйте каждый список DEFAULT_EXTENSIONS, затем вызовите `.update()` с пользовательской таблицей.",
        '''def config_iz_toml(text: str) -> Config:
    raw = tomllib.loads(text)
    extensions = {k: list(v) for k, v in DEFAULT_EXTENSIONS.items()}
    extensions.update(raw.get("extensions", {}))
    return Config(
        destination=raw.get("destination", DEFAULT_DESTINATION),
        exclude=tuple(raw.get("exclude", DEFAULT_EXCLUDE)),
        extensions=extensions,
    )


nastrojki_minimalnye = config_iz_toml('destination = "Sorted2"\\n')''',
    ),
    "23-20": PracticeSpec(
        "Допишите тест отсутствующего source: apply_plan должен вернуть completed=False и текст ошибки.",
        '''def test_apply_plan_reports_missing_source(tmp_path):
    # TODO: build a plan for a path that was never created and assert failure.
    raise NotImplementedError
''',
        '''with tempfile.TemporaryDirectory() as tmp:
    test_apply_plan_reports_missing_source(Path(tmp))

# Edge case: an empty plan is a no-op.
with tempfile.TemporaryDirectory() as tmp:
    empty_root = Path(tmp)
    assert apply_plan(SortPlan(root=empty_root, operations=())) == []
    assert list(empty_root.iterdir()) == []
print("Tests passed")''',
        "Создайте только объекты Path и SortPlan; сам source на диске создавать не нужно.",
    ),
    "23-21": PracticeSpec(
        "Допишите тест: реальный файл найден, symlink на него пропущен. Если symlink недоступен, тест может завершиться через return.",
        '''def test_scan_skips_symlinks(tmp_path):
    # TODO: create a file and symlink, call scan(), inspect returned names.
    raise NotImplementedError
''',
        '''with tempfile.TemporaryDirectory() as tmp:
    test_scan_skips_symlinks(Path(tmp))

# Edge cases for the same feature boundary.
with tempfile.TemporaryDirectory() as tmp:
    assert scan(Path(tmp), Config()) == []
assert classify(".unknown", DEFAULT_EXTENSIONS) == "other"
print("Tests passed")''',
        "Проверяйте `symlink_to()` отдельно; после scan сравните множество `f.path.name`.",
    ),
    "23-22": PracticeSpec(
        "Верните множества имён для всех найденных duplicate groups. Уникальные размеры не должны появиться.",
        '''def imena_duplicate_groups(files):
    # TODO: call find_duplicates and return a set of frozenset names.
    raise NotImplementedError


imena_grupp = imena_duplicate_groups([
    FileInfo("a1.txt", 5, b"AAAAA"),
    FileInfo("a2.txt", 5, b"AAAAA"),
    FileInfo("b1.txt", 7, b"BBBBBBB"),
    FileInfo("c1.txt", 9, b"CCCCCCCCC"),
])''',
        '''assert imena_grupp == {frozenset({"a1.txt", "a2.txt"})}
assert imena_duplicate_groups([]) == set()
assert imena_duplicate_groups([FileInfo("x", 1, b"x")]) == set()
print("Tests passed")''',
        "Преобразуйте каждую `group[\"files\"]` во `frozenset(file.name ...)`.",
        '''def imena_duplicate_groups(files):
    return {
        frozenset(file.name for file in group["files"])
        for group in find_duplicates(files)
    }


imena_grupp = imena_duplicate_groups([
    FileInfo("a1.txt", 5, b"AAAAA"),
    FileInfo("a2.txt", 5, b"AAAAA"),
    FileInfo("b1.txt", 7, b"BBBBBBB"),
    FileInfo("c1.txt", 9, b"CCCCCCCCC"),
])''',
    ),
    "23-23": PracticeSpec(
        "Напишите `kod_razbora(argv)`: верните 0 для успешного разбора или код SystemExit для help/ошибки.",
        '''def kod_razbora(argv: list[str]) -> int:
    # TODO: call build_parser().parse_args(argv), catch SystemExit.
    raise NotImplementedError
''',
        '''assert kod_razbora(["apply", "/tmp/x"]) == 0
assert kod_razbora(["--help"]) == 0
assert kod_razbora(["zip", "/tmp/x"]) != 0
assert kod_razbora([]) != 0
print("Tests passed")''',
        "Нормальный `parse_args` просто возвращает Namespace. `--help` и ошибка попадают в `except SystemExit as exc`.",
        '''def kod_razbora(argv: list[str]) -> int:
    try:
        build_parser().parse_args(argv)
    except SystemExit as exc:
        return int(exc.code)
    return 0''',
    ),
    "23-24": PracticeSpec(
        "Сформулируйте логическое commit message для изменения теста нулевых файлов. Не используйте `update` или `fix stuff`.",
        '''moe_commit_soobshenie = ""
# TODO: write a specific message with an accepted prefix.
''',
        '''dopustimye_prefiksy = ("feat:", "fix:", "test:", "docs:", "refactor:", "chore:")
assert moe_commit_soobshenie.startswith(dopustimye_prefiksy)
assert len(moe_commit_soobshenie.split()) >= 4
assert moe_commit_soobshenie.lower() not in {"update", "fix", "fix stuff"}
print("Tests passed")''',
        "Сообщите не факт редактирования, а проверяемое изменение поведения, например `test: ...`.",
    ),
}


SAFESORT_LOCAL_IDS = {"23-09", "23-13", "23-16", "23-20", "23-21", "23-24"}
HOMEWORK_LOCAL_IDS = {"23-01", "23-04", "23-05", "23-06"}


def _local_setup_cells(lesson_id: str) -> list:
    if lesson_id in SAFESORT_LOCAL_IDS:
        setup = nbf.v4.new_markdown_cell(
            """## Reproducible local environment

```bash
git clone https://github.com/Cartesian-School/safesort.git
cd safesort
python3.14 -m venv .venv
source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
python -m pip install -U pip
python -m pip install -e ".[dev]"
python -m pip install jupyter ipykernel
python -m ipykernel install --user --name safesort-py314 --display-name "SafeSort Python 3.14"
jupyter lab
```

Select the **SafeSort Python 3.14** kernel. The diagnostic cell below must
point into this `.venv` and the cloned `src/safesort` tree."""
        )
        diagnostic = nbf.v4.new_code_cell(
            """import sys
import safesort

print(sys.executable)
print(safesort.__file__)"""
        )
    elif lesson_id in HOMEWORK_LOCAL_IDS:
        setup = nbf.v4.new_markdown_cell(
            """## Reproducible local environment

These appendix projects live in the course repository, not in SafeSort:

```bash
git clone https://github.com/Cartesian-School/python-from-zero.git
cd python-from-zero
python3.14 -m venv .venv
source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
python -m pip install -U pip
python -m pip install pytest pygame-ce jupyter ipykernel
python -m ipykernel install --user --name course-py314 --display-name "Course Python 3.14"
jupyter lab
```

Select **Course Python 3.14**. On Linux, Tkinter may also require the OS
package `python3-tk`."""
        )
        diagnostic = nbf.v4.new_code_cell(
            """import sys
from pathlib import Path

print(sys.executable)
print(Path.cwd())"""
        )
    else:
        return []
    setup["id"] = f"setup-{lesson_id}"
    diagnostic["id"] = f"diagnostic-{lesson_id}"
    return [setup, diagnostic]


def apply_practice_model(cells: list, lesson_id: str) -> list:
    """Return cells with one non-prefilled, testable task and hidden solution."""
    spec = SPECS[lesson_id]
    cells = list(cells)

    for cell in cells:
        if cell["cell_type"] == "markdown":
            source = cell["source"]
            source = source.replace("## Рабочий пример", "## Example", 1)
            source = source.replace("## Пример", "## Example", 1)
            cell["source"] = source

    if len(cells) > 1:
        cells[1:1] = _local_setup_cells(lesson_id)

    task_index = next(
        (
            index
            for index, cell in enumerate(cells)
            if cell["cell_type"] == "markdown" and "## Задание" in cell["source"]
        ),
        None,
    )

    existing_solution = spec.solution
    if task_index is not None:
        solution_index = next(
            index
            for index in range(task_index + 1, len(cells))
            if cells[index]["cell_type"] == "code"
        )
        if existing_solution is None:
            existing_solution = cells[solution_index]["source"]
        del cells[solution_index]
        del cells[task_index]
        insert_at = task_index
    else:
        if existing_solution is None:
            raise ValueError(f"{lesson_id}: task and explicit solution are both missing")
        insert_at = len(cells)

    starter_heading = nbf.v4.new_markdown_cell(
        "## Starter\n\nЗаполните отмеченное место. Неизменённый starter не проходит tests."
    )
    starter = nbf.v4.new_code_cell(spec.starter)
    starter["id"] = f"task-{lesson_id}"
    starter["metadata"]["tags"] = ["exercise", "starter"]
    task = nbf.v4.new_markdown_cell(f"## Task\n\n{spec.task}")
    tests_heading = nbf.v4.new_markdown_cell(
        "## Tests\n\nЗапустите после task cell: есть основной пример и хотя бы один крайний случай."
    )
    tests = nbf.v4.new_code_cell(spec.tests)
    tests["id"] = f"tests-{lesson_id}"
    tests["metadata"]["tags"] = ["exercise-tests"]
    hint = nbf.v4.new_markdown_cell(f"## Hint\n\n{spec.hint}")
    solution = nbf.v4.new_markdown_cell(
        "## Solution\n\n"
        "<details><summary>Показать решение после собственной попытки</summary>\n\n"
        f"```python\n{existing_solution.rstrip()}\n```\n\n</details>"
    )

    cells[insert_at:insert_at] = [
        starter_heading,
        starter,
        task,
        tests_heading,
        tests,
        hint,
        solution,
    ]
    return cells
