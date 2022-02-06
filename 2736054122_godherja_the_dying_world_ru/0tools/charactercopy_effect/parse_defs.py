from typing import Any, Dict, Final, Generator, List, Optional, Union

from pathlib import Path
import tokenize

JominiDef = Dict[str, Any]

def _printable_stack_item(x):
    if isinstance(x, tokenize.TokenInfo):
        return x.string
    elif isinstance(x, dict):
        return "DICT"
    else: return x

def transform_tokens(
    token_generator: Generator[tokenize.TokenInfo, Any, Any]
) -> Generator[tokenize.TokenInfo, Any, Any]:
    """
    This primarily exists to fuse `@` and NAME tokens together into a single
    NAME token, as this is the main divergence between python and jomini tokens.
    """
    last_at: Optional[tokenize.TokenInfo] = None
    for token in token_generator:
        if last_at is not None:
            assert(token.type == tokenize.NAME)
            yield tokenize.TokenInfo(
                tokenize.NAME, last_at.string + token.string,
                last_at.start, token.end, token.line
                )
            last_at = None
        elif token.type == tokenize.OP and token.string == '@':
            last_at = token
        else:
            yield token


def tokens_to_values(
    token_obj : Any
) -> Any:
    if isinstance(token_obj, tokenize.TokenInfo):
        if token_obj.type == tokenize.STRING:
            return token_obj.string[1:-1] # strip quotes
        elif token_obj.type == tokenize.NUMBER:
            return float(token_obj.string)
        elif token_obj.type == tokenize.NAME:
            return token_obj.string
        else:
            print("Unknown token: " + token_obj)
            return token_obj
    elif isinstance(token_obj, dict):
        ret = {
            k: tokens_to_values(v) for k,v in token_obj.items()
        }
        return ret
    else:
        return token_obj


def tokens_to_dict(
    token_generator: Generator[tokenize.TokenInfo, Any, Any]
) -> Dict[str, JominiDef]:
    """
    Parse a tokenized file into a dictionary of dictionaries.
    """
    # we reduce NAME types to strings, and leave literals as tokens
    tokens_stack: List[Union[str, tokenize.TokenInfo, JominiDef]] = [
    ]

    def _stack_top_is_lbrace():
        return (
            isinstance(tokens_stack[-1], tokenize.TokenInfo) and
            tokens_stack[-1].exact_type == tokenize.LBRACE
        )

    def _stack_top_is_eq(idx:int = -1):
        return (
            isinstance(tokens_stack[idx], tokenize.TokenInfo) and
            tokens_stack[idx].exact_type == tokenize.EQUAL
        )

    # convert name to str and append it (assume it's a key)
    def _append_name_token(token: tokenize.TokenInfo) -> None:
        assert(token.type == tokenize.NAME)

        # if top of stack is `=` token, then this is a value, so we append it
        # as-is without string casting
        if len(tokens_stack) > 0 and _stack_top_is_eq():
            tokens_stack.append(token)
        # otherwise this is a key, so append it as a string
        else:
            tokens_stack.append(token.string)

    def _append_value_token(token: tokenize.TokenInfo) -> None:
        assert(token.exact_type in {tokenize.NAME, tokenize.NUMBER, tokenize.LBRACE, tokenize.STRING})
        tokens_stack.append(token)

    # called when a } is seen; remove tokens from the top until we see a {, then
    # create a dictionary with those tokens and push that back on as a value
    def _complete_block() -> None:
        tmp: Dict[str, tokenize.TokenInfo] = {}
        while len(tokens_stack) > 0 and not _stack_top_is_lbrace():
            if _stack_top_is_eq(-2):
                value = tokens_stack.pop()
                assert(tokens_stack.pop().string == '=')
                key = tokens_stack.pop()
            else:
                value = True
                key = tokens_stack.pop()
            tmp[key] = value
        if len(tokens_stack) > 0: # remove the `{` if we stopped on one
            tokens_stack.pop()
        tokens_stack.append(tmp)

    for token in transform_tokens(token_generator):
        if token.type == tokenize.NAME:
            _append_name_token(token)
        elif token.type == tokenize.OP:
            # @s can be in keys, so we don't want to use _append_value_token
            if token.string == '{':
                _append_value_token(token)
            elif token.string == '}':
                _complete_block()
            elif token.string == '=':
                assert(isinstance(tokens_stack[-1], str))
                tokens_stack.append(token)
        elif token.type in {tokenize.STRING, tokenize.NUMBER}:
            _append_value_token(token)
        elif token.type in {tokenize.NL, tokenize.NEWLINE, tokenize.DEDENT, tokenize.ENDMARKER}:
            # ignore whitespace
            pass
        elif token.type == tokenize.COMMENT:
            # ignore comments
            pass
        else:
            # might as well tell us what's up with these other tokens
            print("Unknown token: " + token.__repr__())

    _complete_block()
    return tokens_to_values(tokens_stack[0])
            

def read_defs_from_file(path: str) -> Dict[str, JominiDef]:
    # technically tokenize is for python source but tokens in jomini are very
    # similar (although the grammar is very different)
    with tokenize.open(path) as f:
        return tokens_to_dict(tokenize.generate_tokens(f.readline))


def read_all_defs_from_files(folder_path: str = "../../common/traits") -> Dict[str, JominiDef]:
    pathlist = Path(folder_path).glob('*.txt')
    ret: Dict[str, JominiDef] = {}
    for path in pathlist:
        for k,v in read_defs_from_file(path).items():
            assert(k not in ret)
            ret[k] = v
    return ret
