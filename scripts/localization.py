"""RU/PL localization contracts. No browser detection or URL rewriting."""
from __future__ import annotations

import hashlib
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_DIR = ROOT / 'manifest/i18n'
STATES = frozenset({'untranslated', 'translated', 'reviewed', 'approved', 'stale'})


def read_json(path: Path) -> dict:
    """Reject duplicate JSON keys rather than silently losing route entries."""
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f'Duplicate JSON key: {key}')
            result[key] = value
        return result
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique)


REGISTRY = read_json(MANIFEST_DIR / 'locales.json')
LOCALES = REGISTRY['locales']
DEFAULT_LOCALE = REGISTRY['default_locale']
UI_STRINGS = read_json(MANIFEST_DIR / 'ui_strings.json')
TERMINOLOGY = read_json(MANIFEST_DIR / 'pl_terminology.json')


def polish_count(count: int, forms: tuple[str, str, str] | list[str]) -> str:
    """Format nonnegative integral UI counts using Polish one/few/many forms."""
    if type(count) is not int or count < 0 or len(forms) != 3:
        raise ValueError('Expected a nonnegative integer and three noun forms')
    index = 0 if count == 1 else 1 if 2 <= count % 10 <= 4 and not 12 <= count % 100 <= 14 else 2
    return f'{count} {forms[index]}'


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_hash(source: dict, root: Path = ROOT) -> str:
    """Bind all declared canonical inputs, including imported content resources."""
    dependencies = source.get('dependencies', [])
    if not dependencies:
        return sha256(root / source['path'])
    inputs = {path: sha256(root / path) for path in sorted([source['path'], *dependencies])}
    return hashlib.sha256(json.dumps(inputs, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()


def effective_status(page: dict, locale: str, root: Path = ROOT) -> str:
    variant = page['variants'][locale]
    if locale == page['source']['locale']:
        return variant['status']
    if variant['status'] == 'untranslated':
        return 'untranslated'
    try:
        current_hash = source_hash(page['source'], root)
    except OSError:
        return 'stale'
    if variant['source_sha256'] != current_hash:
        return 'stale'
    return variant['status']


def validate_routes(data: dict, root: Path = ROOT) -> None:
    """Validate the versioned route schema and fail closed on unsafe artifacts."""
    if data.get('schema_version') != 1 or not isinstance(data.get('pages'), dict):
        raise ValueError('Invalid route manifest version or pages')
    seen = set()
    for page_id, page in data['pages'].items():
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', page_id):
            raise ValueError(f'Invalid page ID: {page_id}')
        source = page['source']
        if source['locale'] != DEFAULT_LOCALE or not re.fullmatch(r'[0-9a-f]{64}', source['sha256']):
            raise ValueError(f'Invalid source binding: {page_id}')
        if not (root / source['path']).resolve().is_relative_to(root.resolve()) or not (root / source['path']).is_file():
            raise ValueError(f'Invalid canonical source: {page_id}')
        dependencies = source.get('dependencies', [])
        if not isinstance(dependencies, list) or len(set(dependencies)) != len(dependencies):
            raise ValueError(f'Invalid source dependencies: {page_id}')
        for dependency in dependencies:
            if not (root / dependency).resolve().is_relative_to(root.resolve()) or not (root / dependency).is_file():
                raise ValueError(f'Invalid source dependency: {page_id}')
        variants = page['variants']
        if DEFAULT_LOCALE not in variants or not variants.keys() <= LOCALES.keys():
            raise ValueError(f'Invalid locales: {page_id}')
        for locale, variant in variants.items():
            path = variant['path']
            prefix = LOCALES[locale]['prefix']
            if (not re.fullmatch(r'/[a-zA-Z0-9/_-]+\.html', path)
                    or '//' in path or path in seen
                    or (prefix and not path.startswith(prefix + '/'))
                    or (not prefix and any(path.startswith(x['prefix'] + '/') for x in LOCALES.values() if x['prefix']))
                    or path.startswith('/ru/')):
                raise ValueError(f'Invalid or colliding route: {path}')
            seen.add(path)
            if variant['status'] not in STATES:
                raise ValueError(f'Invalid translation state: {page_id}')
            if 'practice_id' in page:
                practice_id = page['practice_id']
                if not re.fullmatch(r'\d{2}-\d{2}', practice_id) or path != f'{prefix}/practice/{practice_id}/index.html':
                    raise ValueError(f'Practice identity changed: {page_id}')
            if locale != DEFAULT_LOCALE:
                if not re.fullmatch(r'[0-9a-f]{64}', variant.get('source_sha256', '')):
                    raise ValueError(f'Missing translation source hash: {page_id}')
                if variant['status'] == 'approved':
                    for key in ('source_path', 'evidence_path'):
                        artifact = variant.get(key)
                        if not artifact or not (root / artifact).resolve().is_relative_to(root.resolve()) or not (root / artifact).is_file():
                            raise ValueError(f'Approved translation missing {key}: {page_id}')
                    if effective_status(page, locale, root) != 'approved':
                        raise ValueError(f'Stale approved translation: {page_id}')


class Routes:
    """Exact page-ID lookup with approval, source freshness and file-existence gates."""
    def __init__(self, data: dict | None = None, *, site_dir: Path | None = None, root: Path = ROOT):
        self.root = root
        self.site_dir = site_dir if site_dir is not None else root / 'site'
        self.data = data if data is not None else read_json(MANIFEST_DIR / 'routes.json')
        validate_routes(self.data, root)
        self.pages = self.data['pages']
        self.by_path = {v['path']: pid for pid, p in self.pages.items() for v in p['variants'].values()}

    def available(self, page_id: str) -> dict[str, str]:
        page = self.pages[page_id]
        return {locale: v['path'] for locale, v in page['variants'].items()
                if effective_status(page, locale, self.root) == 'approved'
                and (self.site_dir / v['path'].lstrip('/')).is_file()}

    def publishable_path(self, path: str) -> bool:
        """Preserve existing default routes; gate every added locale route."""
        if not any(meta['prefix'] and path.startswith(meta['prefix'] + '/')
                   for meta in LOCALES.values()):
            return not path.startswith('/ru/')
        page_id = self.by_path.get(path)
        return page_id is not None and path in self.available(page_id).values()

    def alternates(self, path: str) -> dict[str, str]:
        page_id = self.by_path.get(path)
        if page_id is None:
            return {}
        variants = self.available(page_id)
        if path not in variants.values() or len(variants) < 2 or DEFAULT_LOCALE not in variants:
            return {}
        return {**variants, 'x-default': variants[DEFAULT_LOCALE]}

    def switcher(self, page_id: str, locale: str) -> str:
        page = self.pages[page_id]
        if locale not in page['variants']:
            raise ValueError('Current locale has no page variant')
        available = self.available(page_id)
        parts = []
        for code, meta in LOCALES.items():
            label = html.escape(meta['label'])
            if code == locale:
                parts.append(f'<span lang="{code}" aria-current="true">{label}</span>')
            elif code in available:
                parts.append(f'<a lang="{code}" hreflang="{code}" href="{html.escape(available[code])}">{label}</a>')
            else:
                title = html.escape(UI_STRINGS[locale]['unavailable'])
                parts.append(f'<span lang="{code}" aria-disabled="true" title="{title}">{label}</span>')
        return f'<nav class="language-switcher" aria-label="{UI_STRINGS[locale]["language"]}">' + '<span aria-hidden="true"> | </span>'.join(parts) + '</nav>'


def alternate_links(path: str, origin: str, routes: Routes) -> list[str]:
    return [f'<link rel="alternate" hreflang="{locale}" href="{html.escape(origin + url)}" />'
            for locale, url in routes.alternates(path).items()]
