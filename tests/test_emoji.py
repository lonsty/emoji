#!/usr/bin/env python

"""Tests for `emoji` package."""


import unittest

from click.testing import CliRunner

from emoji import cli, emoji


class TestEmoji(unittest.TestCase):
    """Tests for `emoji` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'ValueError: keyword must be provided for search.' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert 'Show this message and exit.' in help_result.output

    def test_searching_emoji(self):
        """Test the searching function."""
        runner = CliRunner()
        result = runner.invoke(cli.main, ['bug', '-c'])
        assert result.exit_code == 0
        assert ":bug:" in result.output
