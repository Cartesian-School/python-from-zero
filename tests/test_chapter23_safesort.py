"""Интеграционная приёмка SafeSort (проект главы 23) на временном каталоге.

Проверяет полный жизненный цикл — scan, plan, apply, duplicates, undo — так,
как его описывает сама глава: явное подтверждение перед перемещением,
обнаружение дубликатов без удаления, отмену с восстановлением исходных
путей и отказ перезаписывать при конфликте имён. Ни один тест не касается
настоящих пользовательских каталогов вроде ~/Downloads — только tmp_path.
"""

from pathlib import Path

from safesort.classifier import classify
from safesort.config import Config
from safesort.duplicates import find_duplicates
from safesort.executor import apply_plan
from safesort.manifest import read_manifest, undo, write_manifest
from safesort.planner import build_plan
from safesort.scanner import scan


def _seed_files(root: Path) -> None:
    (root / "report.pdf").write_text("report content", encoding="utf-8")
    (root / "photo.jpg").write_text("fake image", encoding="utf-8")
    (root / "archive.zip").write_text("archive", encoding="utf-8")
    (root / "notes.txt").write_text("duplicate content here", encoding="utf-8")
    (root / "copy_of_notes.txt").write_text("duplicate content here", encoding="utf-8")


def test_full_lifecycle_scan_plan_apply_duplicates_undo(tmp_path):
    _seed_files(tmp_path)
    config = Config()

    # scan — только чтение
    files = scan(tmp_path, config)
    assert len(files) == 5

    # plan — только чтение, ничего на диске не меняется
    plan = build_plan(files, tmp_path, config)
    assert len(plan.operations) == 5
    for entry in tmp_path.iterdir():
        assert entry.is_file() or entry.name == config.destination

    # категории верны
    categories = {classify(f.extension, config.extensions) for f in files}
    assert categories == {"documents", "images", "archives"}

    # duplicates — тоже только чтение
    groups = find_duplicates(files)
    assert len(groups) == 1
    assert len(groups[0].files) == 2
    duplicate_names = {f.path.name for f in groups[0].files}
    assert duplicate_names == {"notes.txt", "copy_of_notes.txt"}
    for entry in tmp_path.iterdir():
        assert entry.is_file()

    # apply выполняет прямую сортировку; undo ниже выполняет обратное перемещение
    moves = apply_plan(plan)
    assert all(move.completed for move in moves)
    assert (tmp_path / "Sorted" / "documents" / "report.pdf").exists()
    assert (tmp_path / "Sorted" / "documents" / "notes.txt").exists()
    assert (tmp_path / "Sorted" / "documents" / "copy_of_notes.txt").exists()
    assert (tmp_path / "Sorted" / "images" / "photo.jpg").exists()
    assert (tmp_path / "Sorted" / "archives" / "archive.zip").exists()
    assert not (tmp_path / "report.pdf").exists()

    manifest, manifest_path = write_manifest(tmp_path, moves)
    assert manifest_path.exists()

    # повторный scan не должен снова находить уже отсортированные файлы
    rescanned = scan(tmp_path, config)
    assert rescanned == []

    # undo — восстанавливает исходные пути
    result = undo(read_manifest(manifest_path))
    assert result.conflicts == ()
    assert len(result.restored) == 5
    assert (tmp_path / "report.pdf").exists()
    assert (tmp_path / "notes.txt").exists()
    assert not (tmp_path / "Sorted" / "documents" / "report.pdf").exists()


def test_apply_never_overwrites_existing_destination(tmp_path):
    (tmp_path / "otchet.pdf").write_text("first", encoding="utf-8")
    config = Config()
    dest_dir = tmp_path / config.destination / "documents"
    dest_dir.mkdir(parents=True)
    (dest_dir / "otchet.pdf").write_text("already here", encoding="utf-8")

    files = scan(tmp_path, config)
    plan = build_plan(files, tmp_path, config)
    [operation] = plan.operations

    assert operation.destination.name == "otchet (1).pdf"

    apply_plan(plan)
    assert (dest_dir / "otchet.pdf").read_text(encoding="utf-8") == "already here"
    assert (dest_dir / "otchet (1).pdf").read_text(encoding="utf-8") == "first"


def test_undo_refuses_to_overwrite_a_file_that_reappeared(tmp_path):
    (tmp_path / "otchet.pdf").write_text("original", encoding="utf-8")
    config = Config()

    files = scan(tmp_path, config)
    plan = build_plan(files, tmp_path, config)
    moves = apply_plan(plan)
    manifest, manifest_path = write_manifest(tmp_path, moves)

    # пользователь создал новый файл на исходном месте, пока задача была применена
    (tmp_path / "otchet.pdf").write_text("new file, unrelated", encoding="utf-8")

    result = undo(read_manifest(manifest_path))

    assert len(result.conflicts) == 1
    assert result.conflicts[0].source == tmp_path / "otchet.pdf"
    assert (tmp_path / "otchet.pdf").read_text(encoding="utf-8") == "new file, unrelated"
