import unittest
from unittest.mock import patch

from simplegrammar import SimpleGrammar
from simplegrammar import __main__ as simplegrammar_cli


class SimpleGrammarTest(unittest.TestCase):
    def test_parse_dict_expands_default_text_tag(self):
        grammar = {
            "text": ["Hello #name#!"],
            "name": ["Ada"],
        }

        self.assertEqual(SimpleGrammar.parse(grammar), "Hello Ada!")

    def test_parse_dict_can_target_non_default_tag(self):
        grammar = {
            "text": ["unused"],
            "title": ["#adjective# story"],
            "adjective": ["Short"],
        }

        self.assertEqual(SimpleGrammar().parse(grammar, target_tag="title"), "Short story")

    def test_parse_list_treats_list_as_text_choices(self):
        self.assertEqual(SimpleGrammar.parse(["one option"]), "one option")

    def test_builder_aliases_are_chainable(self):
        grammar = SimpleGrammar().st("#greeting#, #name#!").at("greeting", ["Hello"]).at("name", ["Grace"])

        self.assertEqual(str(grammar), "Hello, Grace!")

    def test_nested_tags_are_evaluated_recursively(self):
        grammar = SimpleGrammar()
        grammar.add_tag("text", ["#subject# #verb#"])
        grammar.add_tag("subject", ["#article# cat"])
        grammar.add_tag("article", ["The"])
        grammar.add_tag("verb", ["sleeps"])

        self.assertEqual(grammar.parse({"text": ["#subject# #verb#"]}), "The cat sleeps")

    def test_capitalize_text_function_transforms_nested_tag(self):
        grammar = {
            "text": ["#capitalize.animal#"],
            "animal": ["cat"],
        }

        self.assertEqual(SimpleGrammar.parse(grammar), "Cat")

    def test_numeric_prefix_static_tag_reuses_choice_within_grammar(self):
        grammar = SimpleGrammar().st("#1.name# #1.name# #2.name#").at("name", ["Ada", "Grace"])

        with patch("simplegrammar.grammar.randint", side_effect=[0, 1]):
            self.assertEqual(str(grammar), "Ada Ada Grace")

    def test_seeded_parse_is_deterministic(self):
        grammar = {
            "text": ["#greeting#, #name#! #emoji#"],
            "greeting": ["Hello", "Hi", "Bonjour"],
            "name": ["Ada", "Grace", "Linus"],
            "emoji": [":)", ":D", "<3"],
        }

        first_output = SimpleGrammar.parse(grammar, seed="daily")
        second_output = SimpleGrammar.parse(grammar, seed="daily")

        self.assertEqual(first_output, second_output)

    def test_seeded_instances_are_deterministic(self):
        first_grammar = SimpleGrammar(seed="story").st("#hero# finds #treasure#")
        first_grammar.at("hero", ["Ada", "Grace", "Linus"])
        first_grammar.at("treasure", ["a map", "a key", "a shell"])

        second_grammar = SimpleGrammar(seed="story").st("#hero# finds #treasure#")
        second_grammar.at("hero", ["Ada", "Grace", "Linus"])
        second_grammar.at("treasure", ["a map", "a key", "a shell"])

        self.assertEqual(str(first_grammar), str(second_grammar))

    def test_parse_seed_resets_existing_generator_state(self):
        grammar = {
            "text": ["#name# #name#"],
            "name": ["Ada", "Grace", "Linus"],
        }
        generator = SimpleGrammar()

        self.assertEqual(
            generator.parse(grammar, seed="stable"),
            generator.parse(grammar, seed="stable"),
        )

    def test_parse_tags_from_finds_hash_delimited_tags(self):
        grammar = SimpleGrammar()

        self.assertEqual(
            grammar.parse_tags_from("#greeting#, #name#!"),
            ["greeting", "name"],
        )

    def test_parse_tags_from_ignores_tags_interrupted_by_space_or_newline(self):
        grammar = SimpleGrammar()

        self.assertEqual(grammar.parse_tags_from("#bad tag# #ok# #bad\nagain#"), ["ok"])

    def test_evaluate_rejects_unresolved_direct_tag(self):
        grammar = SimpleGrammar().st("Hello #name#")

        with self.assertRaisesRegex(ValueError, "Unresolved grammar tag: #name#"):
            str(grammar)

    def test_parse_dict_rejects_unresolved_nested_tag(self):
        grammar = {
            "text": ["#greeting#"],
            "greeting": ["Hello #name#"],
        }

        with self.assertRaisesRegex(ValueError, "Unresolved grammar tag: #name#"):
            SimpleGrammar.parse(grammar)

    def test_text_function_rejects_unresolved_tag_argument(self):
        grammar = {
            "text": ["#capitalize.name#"],
        }

        with self.assertRaisesRegex(ValueError, "Unresolved grammar tag: #name#"):
            SimpleGrammar.parse(grammar)

    def test_static_tag_rejects_unresolved_tag_argument(self):
        grammar = SimpleGrammar().st("#1.name#")

        with self.assertRaisesRegex(ValueError, "Unresolved grammar tag: #name#"):
            str(grammar)

    def test_dotted_tag_with_unknown_prefix_is_rejected(self):
        grammar = SimpleGrammar().st("#unknown.name#").at("name", ["Ada"])

        with self.assertRaisesRegex(ValueError, "Unresolved grammar tag: #unknown.name#"):
            str(grammar)

    def test_reset_tags_clears_tags_and_static_cache(self):
        grammar = SimpleGrammar().st("#1.name#").at("name", ["Ada"])
        self.assertEqual(str(grammar), "Ada")

        grammar.reset_tags()

        self.assertEqual(grammar.tags, {})
        self.assertEqual(grammar.static_tags, {})
        self.assertIn("capitalize", grammar.text_functions)

    def test_cli_accepts_seeded_generation(self):
        grammar = '{"text":["#name#"],"name":["Ada","Grace","Linus"]}'

        with patch("builtins.print") as print_mock:
            exit_code = simplegrammar_cli.main([grammar, "--seed", "cli"])
        first_output = print_mock.call_args.args[0]

        with patch("builtins.print") as print_mock:
            second_exit_code = simplegrammar_cli.main([grammar, "--seed", "cli"])
        second_output = print_mock.call_args.args[0]

        self.assertEqual(exit_code, 0)
        self.assertEqual(second_exit_code, 0)
        self.assertEqual(first_output, second_output)


if __name__ == "__main__":
    unittest.main()
