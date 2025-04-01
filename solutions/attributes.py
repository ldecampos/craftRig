"""
This module provides functions for managing and manipulating attributes of nodes
"""

from maya import cmds


# VALIDATORS
def attribute_exists(node: str, attribute: str) -> bool:
    """Check if the attribute's name exists in the node

    Args:
        node (str): Name of the node
        attribute (str): Name of the attribute

    Returns:
        bool: True if the attribute exist

    Example:
        >>> attribute_exists('translateX')
        True
    """

    return cmds.attributeQuery(attribute, n=node, ex=True)


def is_attribute_locked(node: str, attribute: str) -> bool:
    """Check if the attribute is locked

    Args:
        node (str): Name of the node
        attribute (str): Name of the attribute

    Returns:
        bool: True if the attribute is locked

    Example:
        >>> is_attribute_locked('myAttribute')
        True
    """

    if not attribute_exists(node=node, attribute=attribute):
        return False

    return cmds.getAttr(f'{node}.{attribute}', l=True)


def is_attribute_keyable(node: str, attribute: str) -> bool:
    """Check if the attribute is keyable

    Args:
        node (str): Name of the node
        attribute (str): Name of the attribute

    Returns:
        bool: True if the attribute is keyable

    Example:
        >>> is_attribute_keyable('myAttribute')
        True
    """

    if not attribute_exists(node=node, attribute=attribute):
        return False

    if is_attribute_locked(node=node, attribute=attribute):
        return False

    return cmds.getAttr(f'{node}.{attribute}', k=True)


# GETTERS
def get_attr_value(node: str, attribute: str, **kwargs: any) -> any:
    """ Get the value of the attribute

    Args:
        node (str): Name of the node
        attribute (str): Name of the attribute

    Returns:
        any: value of the attribute

    Example:
        >>> get_attr_value('translateX')
        0.0
    """

    if not attribute_exists(node=node, attribute=attribute):
        return None

    return cmds.getAttr(f'{node}.{attribute}', **kwargs)


def get_user_defined_attrs(node: str) -> list[str]:
    """Get the user defined attributes

    Args:
        node (str): Name of the node

    Returns:
        list[str]: list of attributes

    Example:
        >>> get_user_defined_attrs()
        ['myAttribute']
    """

    return cmds.listAttr(node, ud=True, se=True) or []


def get_attribute_type(node: str, attribute: str) -> str:
    """Get the type of the attribute

    Args:
        node (str): Name of the node
        attribute (str): Name of the attribute

    Returns:
        str: type of the attribute

    Example:
        >>> get_attr_type('myAttribute')
        'float'

    """
    if not attribute_exists(node=node, attribute=attribute):
        return None

    return cmds.getAttr(f'{node}.{attribute}', typ=True)


def get_default_value(node: str, attribute: str) -> any:
    """Get the default value of the attribute

    Args:
        node (str): Name of the node
        attribute (str): Name of the attribute

    Returns:
        any: default value of the attribute

    Example:
        >>> get_default_value('translateX')
        0.0
    """

    if not attribute_exists(node=node, attribute=attribute):
        return None

    return cmds.attributeQuery(attribute, n=node, ld=True)


# SETTERS
def set_attribute_value(node: str, attribute: str, value: any, **kwargs: any) -> bool:
    """Set the value of the attribute

    Args:
        node (str): Name of the node
        attribute (str): Name of the attribute
        value (any): Value of the attribute

    Returns:
        bool: True if the attribute is set

    Example:
        >>> set_attr_value('translateX', 0)
        True
    """

    if not attribute_exists(node=node, attribute=attribute):
        return False

    cmds.setAttr(f'{node}.{attribute}', value, **kwargs)

    return True


def set_keyable_attribute(node: str, attribute: str, keyable: bool = True) -> bool:
    """Change the attribute property between keyable and not keyable

    Args:
        node (str): Name of the node
        attribute (str): Name of the attribute
        keyable (bool, optional): Defaults to True

    Returns:
        bool: True if the attribute is keyable

    Example:
        >>> set_keyable_attribute('myAttribute', keyable=True)
        True
    """

    if not attribute_exists(node=node, attribute=attribute):
        return False

    cmds.setAttr(f'{node}.{attribute}', k=keyable, cb=not keyable)
    return True


def set_default_value(node: str, attribute: str, value: any, **kwargs: any) -> bool:
    """Set the default value of the attribute

    Args:
        node (str): Name of the node
        attribute (str): Name of the attribute
        value (any): Value of the attribute

    Returns:
        bool: True if the attribute is set

    Example:
        >>> set_default_value('myAttribute', 0)
        True
    """

    if not attribute_exists(node=node, attribute=attribute):
        return False

    lock = False
    if is_attribute_locked(node=node, attribute=attribute):
        lock_attribute(node=node, attribute=attribute, lock=False)
        lock = True

    cmds.addAttr(f'{node}.{attribute}', e=True, dv=value, **kwargs)
    cmds.setAttr(f'{node}.{attribute}', value, **kwargs)

    lock_attribute(node=node, attribute=attribute, lock=lock)

    return True


def lock_attribute(node: str, attribute: str, lock: bool = True) -> bool:
    """Lock the attribute given

    Args:
        node (str): Name of the node
        attribute (str): name of the attribute
        lock (bool, optional): True to lock the attribute. Defaults to True.

    Returns:
        bool: True if the attribute is locked

    Example:
        >>> lock_attr('translateX')
        True
    """

    if not attribute_exists(node=node, attribute=attribute):
        return False

    cmds.setAttr(f'{node}.{attribute}', l=lock)

    return True


def lock_attributes(node: str, attributes: list[str], lock: bool = True) -> bool:
    """Lock the attributes given

    Args:
        node (str): Name of the node
        attributes (list[str]): List of attributes
        lock (bool, optional): True to lock the attributes. Defaults to True.

    Returns:
        bool: True if the attributes are locked

    Example:
        >>> lock_attrs(['translateX', 'translateY'])
        True
    """

    for attribute in attributes:
        lock_attribute(node=node, attribute=attribute, lock=lock)

    return True


def hide_attribute(node: str, attribute: str, hide: bool = True) -> bool:
    """Hide the attribute given

    Args:
        node (str): Name of the node
        attribute (str): Name of the attribute
        hide (bool, optional): True to hide the attribute. Defaults to True.

    Returns:
        bool: True if the attribute is hidden

    Example:
        >>> hide_attr('translateX')
        True
    """

    if not attribute_exists(node=node, attribute=attribute):
        return False

    cmds.setAttr(f'{node}.{attribute}', k=not hide, cb=not hide)

    return True


def hide_attributes(node: str, attributes: list[str], hide: bool = True) -> bool:
    """Hide the attributes given

    Args:
        node (str): Name of the node
        attributes (list[str]): List of attributes
        hide (bool, optional): True to hide the attributes. Defaults to True.

    Returns:
        bool: True if the attributes are hidden

    Example:
        >>> hide_attrs(['translateX', 'translateY'])
        True
    """

    for attribute in attributes:
        hide_attribute(node=node, attribute=attribute, hide=hide)

    return True


def lock_and_hide_attribute(node: str,
                            attribute: str,
                            lock: bool = True,
                            hide: bool = True) -> bool:
    """Lock and hide the attribute given

    Args:
        node (str): Name of the node
        attribute_name (str): Name of the attribute
        lock (bool, optional): True to lock the attribute. Defaults to True.
        hide (bool, optional): True to hide the attribute. Defaults to True.

    Returns:
        bool: True if the attribute is locked and hidden

    Example:
        >>> lock_and_hide_attr('translateX')
        True
    """

    lock_attribute(node=node, attribute=attribute, lock=lock)
    hide_attribute(node=node, attribute=attribute, hide=hide)

    return True


def lock_and_hide_attributes(node: str,
                             attributes: list[str],
                             lock: bool = True,
                             hide: bool = True) -> bool:
    """Lock and hide the attributes given

    Args:
        node (str): Name of the node
        attributes (list[str]): List of attributes
        lock (bool, optional): True to lock the attributes. Defaults to True.
        hide (bool, optional): True to hide the attributes. Defaults to True.

    Returns:
        bool: True if the attributes are locked and hidden

    Example:
        >>> lock_and_hide_attrs(['translateX', 'translateY'])
        True
    """

    for attribute in attributes:
        lock_and_hide_attribute(node=node,
                                attribute=attribute,
                                lock=lock,
                                hide=hide)

    return True


def lock_and_hide_all_attributes(node: str, lock: bool = True, hide: bool = True) -> bool:
    """
    Lock and hide all the attributes

    Args:
        node (str): Name of the node
        lock (bool, optional): True to lock the attributes. Defaults to True.
        hide (bool, optional): True to hide the attributes. Defaults to True.

    Returns:
        bool: True if the attributes are locked and hidden

    Example:
        >>> lock_and_hide_all()
        True
    """

    for attribute in cmds.listAttr(node, k=True):
        lock_and_hide_attribute(node=node,
                                attribute=attribute,
                                lock=lock,
                                hide=hide)

    return True


# ADDERS
def add_attribute(node: str, attribute: str, keyable: bool = True, **kwargs: any) -> str:
    """Add an attribute to the node

    Args:
        node (str): Name of the node
        attribute (str): Name of the attribute
        keyable (bool, optional): True == keyable. Defaults to True.

    Returns:
        str: name of the attribute

    Example:
        >>> add_attribute('myAttribute', keyable=True)
        'myAttribute'
    """

    if attribute_exists(node=node, attribute=attribute):
        raise ValueError(
            f'Attribute "{attribute}" already exists in "{node}" node')

    cmds.addAttr(node, ln=attribute, **kwargs)
    cmds.setAttr(f'{node}.{attribute}', k=keyable, cb=not keyable)

    return attribute


def add_separator(node: str, separator: str) -> str:
    """Add a attribute separator in the channel box

    Args:
        node (str): Name of the node
        separator (str): name of the separator

    Returns:
        str: name of the separator

    Example:
        >>> add_separator('attributes')
        'attributes'
    """

    add_attribute(node=node,
                  attribute=separator,
                  keyable=False,
                  niceName=' ',
                  attributeType='enum',
                  enumName=separator)
    lock_attribute(node=node, attribute=separator)

    return separator


def add_float_attribute(node: str, attribute: str, keyable: bool = True, **kwargs: any) -> str:
    """Add a float attribute to the node

    Args:
        node (str): Name of the node
        attribute (str): Name of the attribute
        keyable (bool, optional): True == keyable. Defaults to True.

    Returns:
        str: name of the attribute

    Example:
        >>> add_float_attribute('myAttribute', keyable=True)
        'myAttribute'
    """

    return add_attribute(node=node,
                         attribute=attribute,
                         keyable=keyable,
                         attributeType='float',
                         **kwargs)


def add_int_attribute(node: str, attribute: str, keyable: bool = True, **kwargs: any) -> str:
    """Add a int attribute to the node

    Args:
        node (str): Name of the node
        attribute (str): Name of the attribute
        keyable (bool, optional): True == keyable. Defaults to True.

    Returns:
        str: name of the attribute

    Example:
        >>> add_int_attribute('myAttribute', keyable=True)
        'myAttribute'
    """

    return add_attribute(node=node,
                         attribute=attribute,
                         keyable=keyable,
                         attributeType='long',
                         **kwargs)


def add_bool_attribute(node: str, attribute: str, keyable: bool = True, **kwargs: any) -> str:
    """Add a bool attribute to the node

    Args:
        node (str): Name of the node
        attribute_name (str): Name of the attribute
        keyable (bool, optional): True == keyable. Defaults to True.

    Returns:
        str: name of the attribute

    Example:
        >>> add_bool_attribute('myAttribute', keyable=True)
        'myAttribute'
    """

    return add_attribute(node=node,
                         attribute=attribute,
                         keyable=keyable,
                         attributeType='bool',
                         **kwargs)


def add_enum_attribute(node: str,
                       attribute: str,
                       states: list,
                       keyable: bool = True,
                       **kwargs: any) -> str:
    """Add a enum attributes to the node

    Args:
        node (str): Name of the node
        attribute (str): Name of the attribute
        states (list): List of the enum values
        keyable (bool, optional): True == keyable. Defaults to True.

    Returns:
        str: name of the attribute

    Example:
        >>> add_enum_attribute('myAttribute', ['one', 'two'], keyable=True)
        'myAttribute'
    """

    return add_attribute(node=node,
                         attribute=attribute,
                         keyable=keyable,
                         attributeType='enum',
                         enumName=':'.join(states),
                         **kwargs)


def add_matrix_attribute(node: str, attribute: str, keyable: bool = True, **kwargs: any) -> str:
    """Add a matrix attribute to the node

    Args:
        node (str): Name of the node
        attribute (str): Name of the attribute
        keyable (bool, optional): True == keyable. Defaults to True.

    Returns:
        str: name of the attribute

    Example:
        >>> add_matrix_attribute('myAttribute', keyable=True)
        'myAttribute'
    """

    return add_attribute(node=node,
                         attribute=attribute,
                         keyable=keyable,
                         attributeType='matrix',
                         **kwargs)


def add_string_attribute(node: str, attribute: str, keyable: bool = True, **kwargs: any) -> str:
    """Add a string attribute to the node

    Args:
        node (str): Name of the node
        attribute (str): Name of the attribute
        keyable (bool, optional): True == keyable. Defaults to True.

    Returns:
        str: name of the attribute

    Example:
        >>> add_string_attribute('myAttribute', keyable=True)
        'myAttribute'
    """

    return add_attribute(node=node,
                         attribute=attribute,
                         keyable=keyable,
                         dataType='string',
                         **kwargs)


def add_message_attribute(node: str, attribute: str, keyable: bool = True, **kwargs: any) -> str:
    """Add a message attribute to the node

    Args:
        node (str): Name of the node
        attribute (str): Name of the attribute
        keyable (bool, optional): True == keyable. Defaults to True.

    Returns:
        str: name of the attribute

    Example:
        >>> add_message_attribute('myAttribute', keyable=True)
        'myAttribute'
    """

    return add_attribute(node=node,
                         attribute=attribute,
                         keyable=keyable,
                         attributeType='message',
                         **kwargs)


# DELETERS
def delete_attribute(node: str, attribute: str, **kwargs) -> bool:
    """Delete the attribute given

    Args:
        node (str): Name of the node
        attribute (str): Name of the attribute

    Returns:
        bool: True if the attribute is deleted

    Example:
        >>> delete_attr('myAttribute')
        True
    """

    if not attribute_exists(node=node, attribute=attribute):
        return False

    if is_attribute_locked(node=node, attribute=attribute):
        lock_attribute(node=node, attribute=attribute, lock=False)

    cmds.deleteAttr(node, at=attribute, **kwargs)

    return True


def delete_attributes(node: str, attributes: list, **kwargs) -> bool:
    """Delete the attributes given

    Args:
        node (str): Name of the node
        attributes (list): list of attributes

    Returns:
        bool: True if the attributes are deleted

    Example:
        >>> delete_attrs(['myAttribute', 'myAttribute2'])
        True
    """

    for attribute in attributes:
        delete_attribute(node=node, attribute=attribute, **kwargs)

    return True
