import ast
from rules.PY001_numpy_array import NumpyArrayRule
from rules.PY002_string_concat_in_loop import StringConcatInLoopRule
from rules.PY003_exessive_global_variable import ExcessiveGlobalRule
from rules.PY004_parellel_list_iteration import ParallelListIteration
from rules.PY005_prefer_explicit_typing import ExplicitTypingRule
from rules.PY006_list_slicing import ListSlicingRule
from rules.PY007_dict_items import DictItemsRule
from rules.PY008_dict_get_setdefault import DictGetSetdefaultRule
from rules.PY009_defaultdict import DefaultDictRule
from rules.PY010_mutable_default import MutableDefaultRule
from rules.PY011_return_none_conditionally import ConditionalNoneReturnRule
from rules.PY012_anonymous_tuple_return import AnonymousTupleReturnRule
from rules.PY013_value_equality_with_is import IsForValueComparisonRule
from rules.PY014_membership_on_list import MembershipOnListRule
from rules.PY015_string_join import StringJoinRule
from rules.PY016_shadow_builtin import ShadowBuiltinRule
from rules.PY017_any_all import AnyAllRule
from rules.PY023_WildcardImport import WildcardImportRule
from rules.PY024_OpenWithoutWith import UseWithOpenRule
from rules.PY025_TypeComparisonInsteadOfIsInstance import IsInstanceRule
from rules.PY026_DictInsteadOfDictComprehension import DictComprehensionRule
from rules.PY027_NoTupleUnpacking import MultipleAssignmentUnpackingRule
from rules.PY028_TypeInVariableName import TypeInVariableNameRule
from rules.PY029_BadExceptOrder import ExceptOrderRule
from rules.PY030_MutableDefaultArgument import MutableDefaultArgumentRule
from rules.PY031_LBYLInsteadOfEAFP import EAFPInsteadOfLBYLRule
from rules.PY032_MapFilterInsteadOfListComprehension import ListComprehensionInsteadOfMapFilterRule
from rules.PY033_set_membership import SetMembershipRule




def analyze_code(code: str):
    tree = ast.parse(code)

    rules = [
        NumpyArrayRule(),
        StringConcatInLoopRule(),
        ExcessiveGlobalRule(), 
        ListSlicingRule(),
        ExplicitTypingRule(),
        DictItemsRule(),
        DictGetSetdefaultRule(),
        DefaultDictRule(),
        MutableDefaultRule(),
        ParallelListIteration(),
        ConditionalNoneReturnRule(),
        AnonymousTupleReturnRule(),
        IsForValueComparisonRule(),
        MembershipOnListRule(),
        StringJoinRule(),
        ShadowBuiltinRule(),
        AnyAllRule(),
        WildcardImportRule(),
        UseWithOpenRule(),
        IsInstanceRule(),
        DictComprehensionRule(),
        MultipleAssignmentUnpackingRule(),
        TypeInVariableNameRule(),
        ExceptOrderRule(),
        MutableDefaultArgumentRule(),
        EAFPInsteadOfLBYLRule(),
        ListComprehensionInsteadOfMapFilterRule(),
        SetMembershipRule()
    ]

    diagnostics = []

    for rule in rules:
        rule.visit(tree)
        diagnostics.extend(rule.diagnostics)

    return diagnostics