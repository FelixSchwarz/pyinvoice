# -*- coding: UTF-8 -*-

from importlib.metadata import version

import pytest

from schwarz.pyinvoice.cli import build_parser


def test_parse_minimal_arguments():
    args = build_parser().parse_args(['invoice.xml'])
    assert args.invoice == 'invoice.xml'
    assert args.pdf is None
    assert args.config is None
    assert args.ignore == []
    assert not args.without_logo


def test_parse_all_arguments():
    cli_args = [
        '--config=foo.ini', '--without-logo', '--ignore=bogus-date', '--ignore', 'other',
        'invoice.xml', 'invoice.pdf',
    ]
    args = build_parser().parse_args(cli_args)
    assert args.invoice == 'invoice.xml'
    assert args.pdf == 'invoice.pdf'
    assert args.config == 'foo.ini'
    assert args.ignore == ['bogus-date', 'other']
    assert args.without_logo


def test_show_version_without_invoice(capsys):
    with pytest.raises(SystemExit) as exc_info:
        build_parser().parse_args(['--version'])
    assert exc_info.value.code == 0
    assert capsys.readouterr().out.strip() == version('pyinvoice')
