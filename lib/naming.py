"""
Module providing string manipulation facilities.
"""
import re
from typing import Union


# VALIDATORS
def is_string(text: str) -> bool:
    """Validate if a variable is string

    Args:
        text (str): String to validate

    Returns:
         bool: True if successful, False otherwise

    Example:
        >>> is_string('nameOfVariable')
        True
        >>> is_string(1234)
        False
    """

    return isinstance(text, str)


def is_value(value: Union[int, float]) -> bool:
    """Validate if a variable is a number

    Args:
        value (int, float): Value to validate

    Returns:
         bool: True if successful, False otherwise

    Example:
        >>> is_value(1234)
        True
        >>> is_value('nameOfVariable')
        False
    """

    return isinstance(value, (int, float))


def is_camel_case(text: str) -> bool:
    """Validate if a text is in camelCase style

    Args:
        text (str): Text to valitate

    Returns:
        bool: True if the text is in camelCase style, False otherwise

    Note:
        Text must have only alphanumeric characters

    Example: 
        >>> is_camel_case('nameOfVariable')
        True
        >>> is_camel_case('nameOfVariable1')
        True
        >>> is_camel_case('NameOfVariable')
        False
        >>> is_camel_case('name_of_variable')
        False
    """

    return bool(re.fullmatch(r"^[a-z]+([A-Z][a-z0-9]*)*$", text))


def is_pascal_case(text: str) -> bool:
    """Validate if a text is in PascalCase style

    Args:
        text (str): String to validate

    Returns:
        bool: True if the text is in PascalCase style, False otherwise

    Note:
        Text must have only alphanumeric characters

    Example: 
        >>> is_pascal_case('NameOfVariable')
        True
        >>> is_pascal_case('NameOfVariable1')
        True
        >>> is_pascal_case('Name_of_variable')
        False
        >>> is_pascal_case('nameOfVariable')
        False
    """

    return bool(re.fullmatch(r"^[A-Z][a-z0-9]*([A-Z][a-z0-9]*)*$", text))


def is_snake_case(text: str) -> bool:
    """Validate if a text is in snake_case style

    Args:
        text (str): String to validate

    Returns:
        bool: True if the text is in snake_case style, False otherwise

    Note:
        Text must have only alphanumeric characters

    Example:
        >>> is_snake_case('name_of_variable')
        True
        >>> is_snake_case('name_of_variable1')
        True
        >>> is_snake_case('Name_of_variable')
        False
        >>> is_snake_case('nameOfVariable')
        False
    """

    return bool(re.fullmatch(r"^[a-z]+(_[a-z0-9]+)*$", text))


def is_kebab_case(text: str) -> bool:
    """Validate if a text is in kebab-case style

    Args:
        text (str): String to validate

    Returns:
        bool: True if the text is in kebab-case style, False otherwise

    Note:
        Text must have only alphanumeric characters

    Example:
        >>> is_kebab_case('name-of-variable')
        True
        >>> is_kebab_case('name-of-variable1')
        True
        >>> is_kebab_case('Name-of-variable')
        False
        >>> is_kebab_case('nameOfVariable')
        False
    """

    return bool(re.fullmatch(r"^[a-z]+(-[a-z0-9]+)*$", text))


def is_character_in(text: str, character: str = '_') -> bool:
    """Validate if a character is in a text

    Args:
        text (str): Text to look for
        character (str): Character to validate. Defaults to '_'

    Returns:
        bool: True if the character is in the text, False otherwise

    Example:
        >>> is_character_in('Name_of_variable', '_')
        True
        >>> is_character_in('NameOfVariable', '_')
        False
        >>> is_character_in('Name.Of-Variable', '_')
        False
        >>> is_character_in('name of variable', '_')
        False
    """

    return bool(character in text)


# GETTERS
def get_case_style(text: str) -> bool:
    """Determine the naming style of a given text.

    Args:
        text (str): The text to determinate style.

    Returns:
        str: The naming style of the text.Possible values are:            
             "camelCase",
             "PascalCase", 
             "snake_case", 
             "kebab-case",
             or "unknown".

    Note:
        Text must have only alphanumeric characters

    Example:
        >>> get_case_style('nameOfVariable')
        'camelCase'
        >>> get_case_style(NameOfVariable')
        'PascalCase'
        >>> get_case_style('name_of_variable')
        'snake_case'
        >>> get_case_style('name-of-variable')
        'kebab-case'
        >>> get_case_style('unknown Style')
        'unknown'
    """

    if is_camel_case(text):
        return "camelCase"
    if is_pascal_case(text):
        return "PascalCase"
    if is_snake_case(text):
        return "snake_case"
    if is_kebab_case(text):
        return "kebab-case"

    return "unknown"


def get_digits(text: str) -> list:
    """Get numbers inside a text

    Args:
        text (str): Text to extract numbers

    Returns:
        list: List of string numbers from the original text

    Note:
        If it doesn't have numbers return empty list

    Example:
        >>> get_digits('name_0_of_1_variable_2_')
        ['0', '1', '2']
        >>> get_digits('name123of456variable') 
        ['123', '456']
        >>> get_digits('0name12Of34Variable56') 
        ['0', '12', '34']
        >>> get_digits('nameOfVariable') 
        []
    """

    return re.findall(r'\d+', text)


def get_digit_by_index(text: str, index: int = 0) -> Union[str, list]:
    """Get the number inside a text at a specific index

    Args:
        text (str): Text to extract numbers
        index (int): Index of the number to extract. Defaults to 0

    Returns:
        str: Number from the original text

    Note:
        If it doesn't have numbers return empty list

    Example: 
        >>> get_digit_by_index('name_01_of_12_variable_34_', 2)
        '34'
        >>> get_digit_by_index('name123of456variable', 0)
        '123'
        >>> get_digit_by_index('0name12Of34Variable56', -1)
        56
        >>> get_digit_by_index('nameOfVariable', 2)
        []
    """

    number = get_digits(text)

    return number[index] if number else []


def get_first_number(text: str) -> Union[str, list]:
    """Get the first number inside a text

    Args:
        text (str): Text to extract numbers

    Returns:
        str: First number from the original string

    Note:
        If it does not have numbers return empty list

    Example:
        >>> get_first_number('name_01_of_12_variable_34_')
        '01'
        >>> get_first_number('name123of456variable')
        '123'
        >>> get_first_number('0name12Of34Variable56')
        '120'
        >>> get_first_number('nameOfVariable')
        []
    """

    number = get_digits(text)

    return number[0] if number else []


def get_last_number(text: str) -> Union[str, list]:
    """Get the last number inside a string

    Args:
        text (str): Test to extract numbers

    Returns:
        str: Last number from the original text

    Note:
        If it does not have numbers return empty list

    Example:
        >>> get_last_number('name_01_of_12_variable_34')
        '34'
        >>> get_last_number('name123of456variable')
        '456'
        >>> get_last_number('0name12Of34Variable56')
        '56'
        >>> get_last_number('nameOfVariable')
        []
    """

    number = get_digits(text=text)

    return number[-1] if number else []


def get_values_between_brackets(text: str) -> list:
    """Get all values between brackets inside a text

    Args:
        text (str): The text to extract values from.

    Returns:
        list: List of strings representing the numeric values found between square brackets.

    Note:
        If the text does not contain any values enclosed in square brackets,
        an empty list is returned.

    Example:
        >>> get_values_between_brackets('name_[01]_of_[12]_variable_34')
        ['01', '12']
        >>> get_values_between_brackets('name123of456[variable]')
        []
        >>> get_values_between_brackets('0name[12Of34]Variable56')
        ['12', '34']
        >>> get_values_between_brackets('nameOfVariable')
        []
    """

    results = re.findall(r"\[([^\]]+)\]", text)

    numeric_results = []
    for item in results:
        numbers = re.findall(r'\d+', item)
        numeric_results.extend(numbers)

    return numeric_results if numeric_results else []


# CONVERTERS
def replace_spaces(text: str, replacement: str) -> str:
    """Replace spaces in the given text with a specified character

    Args:
        text (str): The input text
        replacement (str): Specified character to replace with

    Returns:
        str: The input text with spaces replaced by the given replacement

    Example:
        >>> replace_spaces('name of Variable', '_')
        'name_of_Variable
        >>> replace_spaces('name.of variable', '_')
        'name.of_variable'
        >>> replace_spaces('name OfVariable', '_')
        'name_OfVariable'
        >>> replace_spaces('Name_of-variable', '_')
        'Name_of-variable' 
    """

    return text.replace(' ', replacement)


def normalize_text(text: str) -> str:
    """Normalize text by replacing non-alphanumeric characters with spaces

    Args:
        text (str): Text to normalize

    Returns:
        str: Normalized text

    Example:
        >>> normalize_text('name_of_Variable')
        'name of Variable'
        >>> normalize_text('name.of.variable')
        'name of variable'
        >>> normalize_text('nameOfVariable')
        'nameOfVariable'
        >>> normalize_text('name@of#variable!')
        'name of variable '
    """

    return re.sub(r'[^a-zA-Z0-9]+', ' ', text)


def to_camel_case(text: str, delete_numbers: bool = False) -> str:
    """Convert a text to camelCase

    Args:
        text (str): Text to convert to camelCase
        delete_numbers (bool): Remove numbers from the text. Defaults to False

    Returns:
        str: camelCase string

    Example:
        >>> to_camel_case('name_of_variable')
        'nameOfVariable'
        >>> to_camel_case('name-of-variable_32', True)
        'nameOfVariable'
        >>> to_camel_case('name of.var12iable', True)
        'nameOfVarIable'
        >>> to_camel_case('NameOfVariable')
        'nameOfVariable'
    """

    splited_text = split_text(text)

    camel_case = splited_text[0].lower()

    for word in splited_text[1:]:
        camel_case += word.capitalize()

    if delete_numbers:
        camel_case = remove_numbers(camel_case)

    return camel_case


def to_pascal_case(text: str, delete_numbers: bool = False) -> str:
    """Convert a text to PascalCase

    Args:
        text (str): Text to convert to PascalCase
        delete_numbers (bool): Remove numbers from the text. Defaults to False

    Returns:
        str: PascalCase string

    Example: 
        >>> to_pascal_case('name_of_variable')
        'NameOfVariable'
        >>> to_pascal_case('name-of-variable_32', True)
        'NameOfVariable'
        >>> to_pascal_case('name of.var12iable', True)
        'NameOfVarIable'
        >>> to_pascal_case('nameOfVariable')
        'NameOfVariable'
    """

    splited_text = split_text(text)

    pascal_case = ''
    for word in splited_text:
        pascal_case += word.capitalize()

    if delete_numbers:
        pascal_case = remove_numbers(pascal_case)

    return pascal_case


def to_snake_case(text: str, delete_numbers: bool = False) -> str:
    """Convert a text to snake_case

    Args:
        text (str): Text to convert to snake_case
        delete_numbers(bool): Remove numbers from the text. Defaults to False

    Returns:
        str: snake_case string

    Example:
        >>> to_snake_case('name_ofVariable')
        'name_of_variable'
        >>> to_snake_case('name-of-variable_32', True)
        'name_of_variable'
        >>> to_snake_case('name of.var12iable', True)
        'name_of_var_iable'
        >>> to_snake_case('nameOfVariable')
        'name_of_variable'
    """

    splited_text = split_text(text)

    snake_case = []
    for word in splited_text:
        snake_case.append(word.lower())
    snake_case = '_'.join(snake_case)

    if delete_numbers:
        snake_case = remove_numbers(snake_case)
        snake_case = to_snake_case(snake_case)

    return snake_case


def to_kebab_case(text: str, delete_numbers: bool = False) -> str:
    """Convert a text to kebab-case.

    Args:
        text (str): Text to convert to kebab-case
        delete_numbers(bool): Remove numbers from the text. Defaults to False

    Raises:
        TypeError: If the input is not a string

    Returns:
        str: kebab-case string

    Example:
        >>> to_kebab_case('name_ofVariable')
        'name-of-variable'
        >>> to_kebab_case('name-of_variable_32', True)
        'name-of-variable'
        >>> to_kebab_case('name of.var12iable', True)
        'name-of-var-iable'
        >>> to_kebab_case('nameOfVariable')
        'name-of-variable'
    """

    splited_text = split_text(text)

    kebab_case = []
    for word in splited_text:
        kebab_case.append(word.lower())
    kebab_case = '-'.join(kebab_case)

    if delete_numbers:
        kebab_case = remove_numbers(kebab_case)
        kebab_case = to_kebab_case(kebab_case)

    return kebab_case


def convert_value_to_text(value: Union[int, float]) -> str:
    """Convert a number to a string with the following format: Mxdx

    Args:
        value(int, float): Value to convert to string

    Returns:
        str: Converted value

    Example:
        >>> convert_value_to_text(-5.3)
        M5d3
        >>> convert_value_to_text(-0.99)
        'M0d99'
        >>> convert_value_to_text(0)
        '0'
        >>> convert_value_to_text(12.75)
        '12d75'
    """

    sign = ''
    if value < 0:
        sign = 'M'
        value = abs(value)  # Convert value to positive

    return f'{sign}{value}'.replace('.', 'd')


def convert_text_to_value(text: str) -> float:
    """Convert a formatted string (Mxdx) into a number

    Args:
        text (str): Formatted text to convert into a number

    Returns:
        float: The corresponding numerical value

    Note:
        The input string must follow the format 'Mxdx', where:
        - 'M' (optional) indicates a negative number
        - 'd' represents the decimal point

    Example:
        >>> convert_text_to_value('M5d3')
        -5.3
        >>> convert_text_to_value('M0d99')
        '-0.99'
        >>> convert_text_to_value('12d75')
        12.75
        >>> convert_text_to_value('M100d01')
        -100.01
    """

    sign = 1
    if text[0] == 'M':
        sign = -1
        text = text[1:]

    return float(text.replace('d', '.')) * sign


def remove_numbers(text: str) -> str:
    """Remove numbers from a text

    Args:
        text (str): Text to remove numbers from

    Returns:
        str: Text without numbers

    Example:
        >>> remove_numbers('name_01_of_12_variable_34')
        'name__of__variable_'
        >>> remove_numbers('name123of456variable')
        'nameofvariable'
        >>> remove_numbers('0name[12Of34]Variable56')
        'name[Of]Variable'
        >>> remove_numbers('nameOfVariable')
        'nameOfVariable'
    """

    return re.sub(r'\d+', '', text)


def split_text(text: str) -> list:
    """Split text into individual words, handling camelCase, PascalCase, and delimiters like _ and -

    Args:
        text (str): The text to split

    Returns:
        list: A list of words

    Example:
        >>> split_text('camelCaseExample')
        ['camel', 'Case', 'Example']
        >>> split_text('Pascal32CaseText')
        ['Pascal', '32', 'Case', 'Text']
        >>> split_text('singleword')
        ['singleword']
        >>> split_text('Another_Example-Here99')
        ['Another', 'Example', 'Here', '99']
    """
    return re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=\s|$)|[0-9]+|[a-z]+|[A-Za-z]+(?=[_-])', text)


def capitalize_first(text: str) -> str:
    """Capitalize the first letter of a text

    Args:
        text (str): Text to capitalize

    Returns:
        str: Text with the first letter capitalized

    Example:
        >>> capitalize_first('nameOfVariable')
        'NameOfVariable'
        >>> capitalize_first('NameOfVariable')
        'NameOfVariable'
        >>> capitalize_first('name of variable')
        'Name of variable'
        >>> capitalize_first('name-of-variable')
        'Name-of-variable'
    """
    if len(text) == 1:
        return text.upper()

    return text[0].upper() + text[1:]


# INCREMENTERS
def increment_character(text: str) -> str:
    """Increment a letter sequence in a manner similar to Excel column naming

    - Works for both uppercase and lowercase sequences
    - Handles cases like 'ZZ' → 'AAA' and 'zz' → 'aaa'

    Args:
        text (str): A text containing only letters ('A'-'Z' or 'a'-'z')

    Returns:
        str: The incremented letter sequence

    Examples:
        >>> increment_character('A')
        'B'
        >>> increment_character('Z')
        'AA'
        >>> increment_character('aa')
        'ab'
        >>> increment_character('AZ')
        'BA'
    """

    # Convert string to list for mutability
    text = list(text)
    # Check if the input is uppercase or lowercase
    is_upper = text[0].isupper()
    start_char = 'A' if is_upper else 'a'
    end_char = 'Z' if is_upper else 'z'
    # Start from the last character
    i = len(text) - 1
    while i >= 0:
        if text[i] != end_char:
            text[i] = chr(ord(text[i]) + 1)  # Increment character
            return ''.join(text)
        else:
            text[i] = start_char  # Reset current position to start character
            i -= 1
    # Prepend 'A' or 'a' if all characters were 'Z' or 'z'
    return start_char + ''.join(text)


def increment_digit(text: str, digits: int = None) -> str:
    """Increment the last number in a text

    Args:
        text (str): Text to increment
        digits (int, optional): Number of digits for the number to increment. Defaults to None, which pads with 2 digits

    Returns:
        str: Text with the last number incremented, or a number appended if none existed.

    Note:
        If the text does not contain numbers, it will append '01' to the text
        If digits is None, it will pad the number with 2 digits

    Example:
        >>> increment_digit('abc123')
        'abc124'
        >>> increment_digit('test', digits=4)
        'test0001'
        >>> increment_digit('abc99', digits=2)
        'abc100'
        >>> increment_digit('file4567', digits=5)
        'file04568'
    """

    if not digits:
        digits = 2
    # Get the last number in the string
    match = re.search(r'(\d+)$', text)
    if match:
        # Get the current number, increment it, and pad it
        current_number = match.group(1)
        incremented_number = str(int(current_number) + 1).zfill(digits)
        return text[:match.start()] + incremented_number

    return text + "1".zfill(digits)


def add_suffix(text: str, suffix: str, separator: str = '_') -> str:
    """Add a suffix to a text using a separator

    Args:
        text (str): Text to add the suffix to
        suffix (str): The suffix to add
        separator (str): The separator to use. Defaults to '_'

    Returns:
        str: Text with the suffix added

    Example:
        >>> add_suffix('name', 'Suffix')
        'name_suffix'
        >>> add_suffix('name_', '_suffix')
        'name_suffix'
        >>> add_suffix('name', '123')
        'name_123'
        >>> add_suffix('name', '')
        'name_'
    """

    text = to_camel_case(text=text)
    suffix = to_camel_case(text=suffix)

    return f"{text}{separator}{suffix}"


def add_prefix(text: str, prefix: str, separator: str = '_') -> str:
    """Add a prefix to a text using a separator

    Args:
        text (str): Text to add the prefix to
        prefix (str): The prefix to add
        separator (str): The separator to use. Defaults to '_'

    Returns:
        str: Text with the prefix added

    Example:
        >>> add_prefix('name', 'Prefix')
        'prefix_name'
        >>> add_prefix('name_', '_prefix')
        'prefix_name'
        >>> add_prefix('name', '123')
        '123_name'
        >>> add_prefix('name', '')
        '_name'
    """

    text = to_camel_case(text=text)
    prefix = to_camel_case(text=prefix)

    return f"{prefix}{separator}{text}"


def add_text(text: str, text_to_add: str = '') -> str:
    """Add a text to another text in PascalCase

    Args:
        text (str): The text to add to
        text_to_add (str): The text to add. Defaults to ''

    Returns:
        str: The text with the text_to_add added

    Example:
        >>> add_text('name', 'suffix')
        'nameSuffix'
        >>> add_text('name_', '_suffix')
        'nameSuffix'
        >>> add_text('name', 'suffix_prefix')
        'nameSuffixPrefix'
        >>> add_text('name', '123')
        'name123'
    """
    if text_to_add:
        text_to_add = to_pascal_case(text=text_to_add)

    return f'{text}{text_to_add}'


# DECREMENTERS
def decrement_character(text: str) -> str:
    """Decrement a letter sequence in a manner similar to Excel column naming

    - Works for both uppercase and lowercase sequences
    - Handles cases like 'AAA' → 'ZZ' and 'aaa' → 'zz'

    Args:
        text (str): A text containing only letters ('A'-'Z' or 'a'-'z')

    Returns:
        str: The decremented letter sequence

    Examples:
        >>> decrement_character('B')
        'A'
        >>> decrement_character('AA')
        'Z'
        >>> decrement_character('a')
        ''
        >>> decrement_character('BA')
        'AZ'
        >>> decrement_character('aaa')
        'zz'
    """

    # Convert string to list for mutability
    text = list(text)
    # Check if the input is uppercase or lowercase
    is_upper = text[0].isupper()
    start_char = 'A' if is_upper else 'a'
    end_char = 'Z' if is_upper else 'z'
    # Start from the last character
    i = len(text) - 1
    while i >= 0:
        if text[i] != start_char:
            text[i] = chr(ord(text[i]) - 1)  # Decrement character
            return ''.join(text)
        else:
            text[i] = end_char  # Reset current position to end character
            i -= 1
    # Remove one character from the start if all were 'A' or 'a'
    return ''.join(text[1:])


def decrement_digit(text: str) -> str:
    """ Decrement the last number in a text

    Args:
        string (str): Text to decrement

    Returns:
        str: Text with the decremented number, or the original text if no number is found

    Note:
        If the text does not contain numbers, it will return the original text
        If the number is 0 or 1, it will remove it

    Example:
        >>> decrement_digit("item123")
        'item122'
        >>> decrement_digit("file1")
        'file'
        >>> decrement_digit("data0")
        'data'
        >>> decrement_digit("hello")
        'hello'
    """

    # Get the last number in the string
    match = re.search(r'(\d+)$', text)
    if match:
        # Get the current number, decrement it, and pad it
        current_number = match.group(1)
        if int(current_number) == 0 or int(current_number) == 1:
            return text[:match.start()]
        digits = len(current_number)
        decremented_number = str(int(current_number) - 1).zfill(digits)

        return text[:match.start()] + decremented_number

    return text
