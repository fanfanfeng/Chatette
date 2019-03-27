"""
Test module.
Tests the functions in module 'chatette_qiu.parsing.parser_utils'.
"""

import pytest

from chatette_qiu.parsing.parser_utils import *


class TestStripComments(object):
    def test_empty(self):
        assert strip_comments("") == ""

    def test_no_comment(self):
        strings = ["test", "%[intent]", "@[slot]\t", "~[alias]", "\t{}test"]
        for s in strings:
            assert strip_comments(s) == s.rstrip()

    def test_only_old_comments(self):
        strings = ["; comment", ";", "\t;", ";this is a comment",
                   "\t ;a comment", ";a comment ; still a comment"]
        for s in strings:
            assert strip_comments(s) == ""

    def test_old_comments(self):
        s = "%[intent] ; comment"
        assert strip_comments(s) == "%[intent]"
        s = "@[slot]\t;comment"
        assert strip_comments(s) == "@[slot]"
        s = "~[alias];comment"
        assert strip_comments(s) == "~[alias]"
        s = "other ;\tcomment"
        assert strip_comments(s) == "other"

    def test_old_comments_escaped(self):
        s = r"test \; not a comment"
        assert strip_comments(s) == s
        s = r"\;"+"not a comment\t;comment"
        assert strip_comments(s) == r"\;not a comment"
        s = "\ttest"+r"\; no comment; comment"
        assert strip_comments(s) == "\ttest"+r"\; no comment"

    def test_only_new_comments(self):
        strings = ["// comment", "//", "\t//", "//this is a comment",
                   "\t //a comment", "//a comment // still a comment"]
        for s in strings:
            assert strip_comments(s) == ""

    def test_new_comments(self):
        s = "%[intent] // comment"
        assert strip_comments(s) == "%[intent]"
        s = "@[slot]\t//comment"
        assert strip_comments(s) == "@[slot]"
        s = "~[alias]//comment"
        assert strip_comments(s) == "~[alias]"
        s = "other //\tcomment"
        assert strip_comments(s) == "other"

    def test_new_comments_escaped(self):
        s = r"test \// not a comment"
        assert strip_comments(s) == s
        s = r"\/\/"+"not a comment\t//comment"
        assert strip_comments(s) == r"\/\/not a comment"
        s = "\ttest"+r"\// no comment// comment"
        assert strip_comments(s) == "\ttest"+r"\// no comment"

    def test_old_and_new_comments(self):
        s = "test // new comment ; old comment"
        assert strip_comments(s) == "test"
        s = "test ; old comment // new comment"
        assert strip_comments(s) == "test"


class TestRemoveEscapement(object):
    def test_empty(self):
        assert remove_escapement("") == ""

    def test_no_escapement(self):
        strings = ["word", "several different words",
                   "sentence with a [word group].", "%[intent](1) // comment",
                   "sentence with ~[alias?/90] ans @[slot]!", "{choice/too}"]
        for s in strings:
            assert remove_escapement(s) == s

    def test_single_escaped_special_symbols(self):
        assert remove_escapement(r"\?") == "?"
        assert remove_escapement(r"\;") == ";"
        assert remove_escapement(r"\/") == "/"
        assert remove_escapement(r"\//") == "//"
        assert remove_escapement(r"\/\/") == "//"
        assert remove_escapement(r"\[") == "["
        assert remove_escapement(r"\]") == "]"
        assert remove_escapement(r"\{") == "{"
        assert remove_escapement(r"\}") == "}"
        assert remove_escapement(r"\~") == "~"
        assert remove_escapement(r"\@") == "@"
        assert remove_escapement(r"\%") == "%"
        assert remove_escapement(r"\#") == "#"
        assert remove_escapement(r"\&") == "&"
        assert remove_escapement(r"\|") == "|"
        assert remove_escapement(r"\=") == "="
        assert remove_escapement(r"\$") == "\$"

    def test_several_words_escaped(self):
        s = r"test\? with several \? escapements\|"
        assert remove_escapement(s) == "test? with several ? escapements|"
        s = r"\[another [test\?] with] escapement\$2"
        assert remove_escapement(s) == r"[another [test?] with] escapement\$2"


class TestAddEscapementBackForNotComments(object):
    def test(self):
        assert add_escapement_back_for_not_comments("") == ""
        assert add_escapement_back_for_not_comments("test") == "test"
        assert add_escapement_back_for_not_comments("test // not comment") == \
               r"test \// not comment"

class TestAddEscapementBackInSubRule(object):
    def test_empty(self):
        assert add_escapement_back_in_sub_rule("") == ""

    def test_proper_sub_rules(self):
        assert add_escapement_back_in_sub_rule("word") == "word"
        assert add_escapement_back_in_sub_rule("word?") == r"word\?"
        assert add_escapement_back_in_sub_rule("s [test?;a") == r"s \[test\?\;a"

class TestAddEscapementBackInWord(object):
    def test_no_escapement(self):
        assert add_escapement_back_in_word("") == ""
        assert add_escapement_back_in_word("word") == "word"
        assert add_escapement_back_in_group("$arg") == "$arg"

    def test_escapement(self):
        assert add_escapement_back_in_word("word;") == r"word\;"
        assert add_escapement_back_in_word("tab[]") == r"tab\[\]"
        assert add_escapement_back_in_word(r"syms{@~%}") == r"syms\{\@\~\%\}"

class TestAddEscapementBackInGroup(object):
    def test_no_escapement(self):
        assert add_escapement_back_in_group("group") == "group"
        assert add_escapement_back_in_group("$arg") == "$arg"

    def test_escapement(self):
        assert add_escapement_back_in_group(r"syms[]{}~@%&?/$//") == \
               r"syms\[\]\{\}\~\@\%\&\?\/$\/\/"

class TestAddEscapementBackInUnitRef(object):
    def test_no_escapement(self):
        assert add_escapement_back_in_unit_ref("") == ""
        assert add_escapement_back_in_unit_ref("word") == "word"

    def test_escapement(self):
        assert add_escapement_back_in_unit_ref(r"syms[]{}~@%") == \
               r"syms\[\]\{\}\~\@\%"
        assert add_escapement_back_in_unit_ref(r"&?/#") == r"\&\?\/\#"

class TestAddEscapementBackInChoiceItem(object):
    def test_no_escapement(self):
        assert add_escapement_back_in_choice_item("") == ""
        assert add_escapement_back_in_choice_item(r"word \//") == r"word \/\/"

    def test_escapement(self):
        assert add_escapement_back_in_choice_item(r"choice\?/~[second#a]/a") == \
               r"choice\?\/~[second#a]\/a"

class TestAddEscapementBackInUnitDecl(object):
    def test_no_escapement(self):
        assert add_escapement_back_in_unit_decl("") == ""
        assert add_escapement_back_in_unit_decl("word") == "word"

    def test_escapement(self):
        assert add_escapement_back_in_unit_decl("name$arg") == r"name\$arg"
        assert add_escapement_back_in_unit_decl(r"~@%[]{}") == r"\~\@\%\[\]\{\}"
        assert add_escapement_back_in_unit_decl("&#?/") == r"\&\#?/"


class TestIsSpecialSym(object):
    def test_empty(self):
        assert not is_special_sym(None)
        assert not is_special_sym("")

    def test_long_text(self):
        assert not is_special_sym("text")
        assert not is_special_sym("/Another test/")

    def test_not_special_char(self):
        symbols = ['a', ' ', '\t', '!']
        for sym in symbols:
            assert not is_special_sym(sym)

    def test_special_char(self):
        symbols = ['~', '@', '%', '[', ']', '#', '?', '/', '&', '$']
        for sym in symbols:
            assert is_special_sym(sym)

class TestIsCommentSym(object):
    def test_not_comment_sym(self):
        assert not is_comment_sym("")
        assert not is_comment_sym("a")
        assert not is_comment_sym("test;")
        assert not is_comment_sym("@")

    def test_comment_sym(self):
        assert is_comment_sym(";")
        assert is_comment_sym("//")

class TestIsBoundarySym(object):
    def test_not_boundary_sym(self):
        assert not is_boundary_sym("")
        assert not is_boundary_sym("a")
        assert not is_boundary_sym("?")
        assert not is_boundary_sym("#")

    def test_boundary_sym(self):
        boundary_syms = ['~', '@', '%', '[', ']', '{', '}']
        for sym in boundary_syms:
            assert is_boundary_sym(sym)

class TestIsArgSym(object):
    def test(self):
        assert not is_arg_sym("")
        assert not is_arg_sym("@")
        assert is_arg_sym("$")

class TestIsGroupModifierSym(object):
    def test_not_group_modifier(self):
        assert not is_group_modifier_sym("")
        assert not is_group_modifier_sym("#")

    def test_group_modifier(self):
        group_modifiers_syms = ['&', '?', '/']
        for sym in group_modifiers_syms:
            assert is_group_modifier_sym(sym)

class TestIsUnitRefModifierSym(object):
    def test_not_unit_ref_modifier(self):
        assert not is_unit_ref_modifier_sym("")
        assert not is_unit_ref_modifier_sym("a")
        assert not is_unit_ref_modifier_sym("}")

    def test_unit_ref_modifier(self):
        unit_ref_modifiers_syms = ['&', '?', '/', '#']
        for sym in unit_ref_modifiers_syms:
            assert is_unit_ref_modifier_sym(sym)

class TestIsUnitDeclModifierSym(object):
    def test_not_unit_decl_modifier(self):
        assert not is_unit_decl_modifier_sym("")
        assert not is_unit_decl_modifier_sym("a")
        assert not is_unit_decl_modifier_sym("?")

    def test_unit_decl_modifier(self):
        unit_decl_modifier_syms = ['&', '#']
        for sym in unit_decl_modifier_syms:
            assert is_unit_decl_modifier_sym(sym)

class TestIsChoiceSpecialSym(object):
    def test_no_choice_sym(self):
        assert not is_choice_special_sym("")
        assert not is_choice_special_sym("a")
        assert not is_choice_special_sym("&")

    def test_chocie_sep(self):
        assert is_choice_special_sym("/")


class TestIsUnitTypeSym(object):
    def test_empty(self):
        assert not is_unit_type_sym("")

    def test_long_text(self):
        assert not is_unit_type_sym("text")
        assert not is_unit_type_sym("~long test")

    def test_not_special_char(self):
        symbols = ['a', ' ', '\\', '!', '?']
        for sym in symbols:
            assert not is_unit_type_sym(sym)

    def test_special_char(self):
        symbols = ['~', '@', '%']
        for sym in symbols:
            assert is_unit_type_sym(sym)


class TestIsStartUnitSym(object):
    def test_not_unit_start_sym(self):
        symbols = ['', ' ', '\t', 'a', '0', '/', ';', '|', '{', ']', '}',
                   '(', ')']
        for sym in symbols:
            assert not is_start_unit_sym(sym)

    def test_not_char(self):
        objects = ["word", 0, False, str, ['a', '['], {1: 0}, None]
        for o in objects:
            assert not is_start_unit_sym(o)

    def test_unit_start_sym(self):
        unit_open_sym = '['
        assert is_start_unit_sym(unit_open_sym)
        alias_sym = '~'
        assert is_start_unit_sym(alias_sym)
        slot_sym = '@'
        assert is_start_unit_sym(slot_sym)
        intent_sym = '%'
        assert is_start_unit_sym(intent_sym)

    def test_unit_start_word(self):
        words = ["[unit]", "~[alias]", "@[slot]", "%[intent]"]
        for w in words:
            assert not is_start_unit_sym(w)


class TestGetUnitTypeFromSym(object):
    def test_empty(self):
        assert get_unit_type_from_sym("") is None

    def test_long_text(self):
        assert get_unit_type_from_sym("text") is None
        assert get_unit_type_from_sym("~long test") is None

    def test_not_unit_start_sym(self):
        symbols = ['a', ' ', '\t', '?', '#', '[', '}']
        for sym in symbols:
            assert get_unit_type_from_sym(sym) is None

    def test_special_sym(self):
        assert get_unit_type_from_sym('~') == UnitType.alias
        assert get_unit_type_from_sym('@') == UnitType.slot
        assert get_unit_type_from_sym('%') == UnitType.intent


class TestGetDeclarationInterior(object):
    def test_empty(self):
        assert get_declaration_interior([""]) is None

    def test_normal_decl(self):
        assert get_declaration_interior(["~", "[", "name", "]"]) == ["name"]
        assert get_declaration_interior(["%", "[", "n", "#", "var", "?", "]"]) == \
               ["n", "#", "var", "?"]
        assert get_declaration_interior(["@", "[", "slot", "?", "n", "/", "5", "]"]) == \
               ["slot", "?", "n", "/", "5"]

    def test_invalid_decl(self):
        assert get_declaration_interior(["~", "[", "name"]) is None
        assert get_declaration_interior(["%", "[", "["]) is None


class TestGetAnnotationInterior(object):
    def test_empty(self):
        assert get_annotation_interior([""]) is None

    def test_normal_annotation(self):
        assert get_annotation_interior(["(", "5", ")"]) == ["5"]
        assert get_annotation_interior(["(", "train", ":", "10", ")"]) == \
               ["train", ":", "10"]
        assert get_annotation_interior(["(", "training", ":", "5", ",", "test", ":", "0", ")"]) == \
               ["training", ":", "5", ",", "test", ":", "0"]

    def test_incorrect_annotation(self):
        assert get_annotation_interior(["(", "("]) is None
        assert get_annotation_interior(["(", "train"]) is None
        assert get_annotation_interior(["train", ":", ")"]) is None


class TestCheckDeclarationValidity(object):
    def test_valid(self):
        valid_decl_tokens = [["name"], ["name", "$", "arg", "1"],
                             ["name", "#", "var"], ["&", "name", "#", "var"]]
        for tokens in valid_decl_tokens:
            try:
                check_declaration_validity(tokens)
            except SyntaxError:
                pytest.fail("Unexpected 'SyntaxError' when calling " +
                            "'check_declaration_validity' with valid input.")

    def test_invalid(self):
        invalid_decl_tokens = [["&", "&", "name"], ["name", "&"], ["#"],
                               ["&", "$"], ["&"], ["name", "#", "#"],
                               ["name", "#"], ["name", "#", "$", "arg"],
                               ["name", "#", "arg"], ["name", "$", "$"],
                               ["name", "$"], ["name", "$", "#", "var"],
                               ["name", "?"], ["name", "/"]]
        for tokens in invalid_decl_tokens:
            with pytest.raises(SyntaxError):
                check_declaration_validity(tokens)


class TestCheckReferenceValidity(object):
    def test_valid(self):
        valid_ref_tokens = [["name"], ["&", "name"], ["name", "?"],
                            ["name", "?", "rand"], ["name", "?", "/", "5"],
                            ["&", "name", "?", "rand", "/", "20"],
                            ["name", "#", "var"], ["name", "$", "arg"],
                            ["name", "#", "var", "$", "arg"]]
        for tokens in valid_ref_tokens:
            try:
                check_reference_validity(tokens)
            except SyntaxError:
                pytest.fail("Unexpected 'SyntaxError' when calling " +
                            "'checck_reference_validity' with valid input.")

    def test_invalid(self):
        invalid_ref_tokens = [["&", "&"], ["name", "&"], ["?"], ["&"],
                              ["&", "#"], ["name", "#", "var", "#"],
                              ["name", "#"], ["&", "name", "#", "?"],
                              ["name", "#", "arg"], ["name", "$", "$"],
                              ["name", "?", "?"], ["name", "/", "/"],
                              ["name", "/", "50"], ["name", "/", "80", "?"],
                              ["name", "?", "/"], ["name", "?", "/", "0%"],
                              ["name", "?", "/", "200"]]
        for tokens in invalid_ref_tokens:
            with pytest.raises(SyntaxError):
                check_reference_validity(tokens)


class TestCheckChoiceValidity(object):
    def test_valid(self):
        valid_choice_tokens = [["word"], ["~", "[", "alias", "?", "]"],
                               ["[", "word", " ", "group", "]", "/", "@", "[",
                                "&", "slot", "]", " ", "word", "?"]]
        for tokens in valid_choice_tokens:
            try:
                check_choice_validity(tokens)
            except SyntaxError as e:
                pytest.fail("Unexpected 'SyntaxError' when calling "+
                            "'check_choice_validity' with valid input.")

    def test_invalid(self):
        invalid_choice_tokens = [["word", "/"],
                                 ["[", "word", " ", "group", "]", "/", "?"]]
        for tokens in invalid_choice_tokens:
            with pytest.raises(SyntaxError):
                check_choice_validity(tokens)


class TestCheckWordGroupValidity(object):
    def test_valid(self):
        valid_group_tokens = [["word"], ["word", " ", "group"]]
        for tokens in valid_group_tokens:
            try:
                check_word_group_validity(tokens)
            except SyntaxError:
                pytest.fail("Unexpected 'SyntaxError' when calling "+
                            "'check_word_group_validity' with valid input.")

    def test_invalid(self):
        invalid_group_tokens = [["&", "&"], ["name", "&"], ["name", "#", "#"],
                                ["name", "$", "$"], ["name", "?", "?"],
                                ["name", "/", "/"], ["name", "/"],
                                ["name", "/", "?"], ["name", "?", "/"],
                                ["name", "?", "/", "20%"],
                                ["name", "?", "/", "200"]]
        for tokens in invalid_group_tokens:
            with pytest.raises(SyntaxError):
                check_word_group_validity(tokens)


class TestIsSubRuleWord(object):
    def test_empty(self):
        assert not is_sub_rule_word("")

    def test_not_words(self):
        tokens_list = [["~", "[", "alias", "]"],
                       ["%", "[", "intent", "?", "rand", "]"],
                       ["[", "word", "group", "?", "]"],
                       ["{", "choice", "/", "2", "}"]]
        for tokens in tokens_list:
            assert not is_sub_rule_word(tokens)

    def test_words(self):
        tokens_list = [["word"], ["other"], [r"\?"]]
        for tokens in tokens_list:
            assert is_sub_rule_word(tokens)


class TestIsSubRuleWordGroup(object):
    def test_not_word_groups(self):
        tokens_list = [["word"],
                       ["~", "[", "alias", "]"],
                       ["%", "[", "intent", "?", "rand", "]"],
                       ["{", "choice", "/", "2", "}"]]
        for tokens in tokens_list:
            assert not is_sub_rule_word_group(tokens)

    def test_word_groups(self):
        tokens_list = [["[", "word", "]"], ["[", "word", "group", "]"],
                       ["[", "&", "word", "group", r"\?", "?", "rand", "]"]]
        for tokens in tokens_list:
            assert is_sub_rule_word_group(tokens)


class TestIsSubRuleChoice(object):
    def test_not_choices(self):
        tokens_list = [["word"],
                       ["~", "[", "alias", "]"],
                       ["%", "[", "intent", "?", "rand", "]"],
                       ["[", "word", "group", "?", "]"]]
        for tokens in tokens_list:
            assert not is_sub_rule_choice(tokens)

    def test_choices(self):
        tokens_list = [["{", "choice", "}"], ["{", "choice", "/", "2", "}"],
                       ["{", "choice", "word", "/", "[", "word", "group", "]", "}"],
                       ["{", "choice", "/", "choice", "?", "}"]]
        for tokens in tokens_list:
            assert is_sub_rule_choice(tokens)


class TestIsSubRuleAliasRef(object):
    def test_not_aliases(self):
        tokens_list = [["word"],
                       ["%", "[", "intent", "?", "rand", "]"],
                       ["[", "word", "group", "?", "]"],
                       ["{", "choice", "/", "2", "}"]]
        for tokens in tokens_list:
            assert not is_sub_rule_alias_ref(tokens)

    def test_aliases(self):
        tokens_list = [["~", "[", "alias", "]"], ["~", "[", "&", "a", "?", "]"],
                       ["~", "[", "alias", "?", "rand", "gen", "]"]]
        for tokens in tokens_list:
            assert is_sub_rule_alias_ref(tokens)


class TestIsSubRuleSlotRef(object):
    def test_not_slots(self):
        tokens_list = [["word"],
                       ["~", "[", "alias", "]"],
                       ["%", "[", "intent", "?", "rand", "]"],
                       ["[", "word", "group", "?", "]"],
                       ["{", "choice", "/", "2", "}"]]
        for tokens in tokens_list:
            assert not is_sub_rule_slot_ref(tokens)

    def test_slots(self):
        tokens_list = [["@", "[", "slot", "]"], ["@", "[", "s", "?", "r", "]"],
                       ["@", "[", "&", "slot", "?", "rand", "gen", "]"]]
        for tokens in tokens_list:
            assert is_sub_rule_slot_ref(tokens)


class TestIsSubRuleIntentRef(object):
    def test_not_intents(self):
        tokens_list = [["word"],
                       ["~", "[", "alias", "]"],
                       ["@", "[", "slot", "?", "rand", "]"],
                       ["[", "word", "group", "?", "]"],
                       ["{", "choice", "/", "2", "}"]]
        for tokens in tokens_list:
            assert not is_sub_rule_intent_ref(tokens)

    def test_intents(self):
        tokens_list = [["%", "[", "intent", "]"], ["%", "[", "i", "?", "r", "]"],
                       ["%", "[", "intent", "?", "rand", " ", "gen", "/", "1", "]"]]
        for tokens in tokens_list:
            assert is_sub_rule_intent_ref(tokens)
