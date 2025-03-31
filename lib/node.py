"""
This module provides a 'Node' class that represents a node in a Maya scene.
It includes methods for creating, querying, modifying, and deleting nodes
"""

from maya import cmds
from craftRig.lib import naming
from craftRig.solutions import connections


class Node(object):
    """
    Node class
    """

    def __init__(self, name: str, node_type: str = '') -> None:
        """Node class constructor

        Args:
            name (str): The name of the node
            node_type (str): The type of the node
        """

        self.name = name
        self.node_type = node_type

    @classmethod
    def from_string(cls, text: str) -> 'Node':
        """Create a Node object from a string

        Args:
            text (str): Name of the node

        Returns:
            Node: Node object

        Example:
        >>> node = Node.from_string('pCube1')
        >>> node.name
        'pCube1'
        """

        return Node(name=text, node_type=cmds.nodeType(text))

    @classmethod
    def from_selection(cls) -> 'Node':
        """Create a Node object from the selection

        Returns:
            Node: Node object

        Example:
        >>> node = Node.from_selection()
        >>> node.name
        'pCube1'
        """

        selection = cmds.ls(sl=True) or []

        if not selection:
            return None

        return Node.from_string(text=selection[0])

    # VALIDATORS
    def node_exists(self) -> bool:
        """Check if the node exists in the scene

        Returns:
            bool: True if the node exists, False otherwise

        Example:
        >>> node = Node('pCube1')
        >>> node.node_exists()
        True
        """

        if not cmds.objExists(self.name):
            return False

        return True

    def is_intermediate(self) -> bool:
        """Check if the node is an intermediate object.

        Returns:
            bool: True if the node is intermediate, False otherwise.

        Example:
            >>> node = Node("pCube1")
            >>> node.is_intermediate()
            False
        """

        if not self.node_exists():
            return False

        return cmds.getAttr(f'{self.name}.intermediateObject')

    def is_node_locked(self) -> bool:
        """Check if the node is locked.

        Returns:
            bool: True if the node is locked, False otherwise.

        Example:
            >>> node = Node("pCube1")
            >>> node.is_locked()
            True
        """

        if not self.node_exists():
            return False

        return cmds.lockNode(self.name, True, l=True)[0]

    def is_reference(self) -> bool:
        """Check if the node is part of a reference.

        Returns:
            bool: True if the node is referenced, False otherwise.

        Example:
            >>> node = Node("pCube1")
            >>> node.is_referenced()
            False
        """

        if not self.node_exists():
            return False

        return cmds.referenceQuery(self.name, inr=True)

    # GETTERS
    def get_full_path(self) -> str:
        """Get the full path of the node.

        Returns:
            str: The full path of the node.

        Example:
        >>> node = Node('pCube1')
        >>> node.get_full_path()
        '|pCube1'
        """

        if not self.node_exists():
            return False

        return cmds.ls(self.name, l=True)[0]

    def get_node_type(self) -> str:
        """Get the node type of the node

        Returns:
            str: The node type of the node

        Example:
        >>> node = Node('pCube1')
        >>> node.get_node_type()
        'transform'
        """

        if self.node_exists():
            return cmds.nodeType(self.name)

        return None

    def get_history(self, **kwargs) -> list[str]:
        """Get the history of the node.

        Returns:
            List[str]: A list of history node names.

        Example:
            >>> node = Node("pCube1")
            >>> node.get_history()
        """

        if not self.node_exists():
            return []

        return [x for x in cmds.listHistory(self.name, **kwargs) if not self.name in x] or []

    def get_input_connection(self, attribute_name: str) -> list:
        """Get the source connection of an attribute.

        Args:
            attribute (str): Name of the attribute to check.

        Returns:
            str: Source connection.

        Example:
            >>> node = Node("pCube1")
            >>> node.get_input_connection('translateX')
            []
        """

        return connections.get_input_connection(node=self.name, attribute_name=attribute_name)

    # SETTERS
    def lock_node(self, lock: bool = True) -> bool:
        """Lock or unlock the node.

        Args:
            lock (bool, optional): True to lock the node, False to unlock. Defaults to True.

        Returns:
            bool: True if the node was locked or unlocked successfully, False otherwise.

        Example:
            >>> node = Node("pCube1")
            >>> node.lock_node(False)
            True
        """

        if not self.node_exists():
            return False

        cmds.lockNode(self.name, l=lock)
        return True

    def set_intermediate(self, value: bool = True) -> bool:
        """Set or unset the intermediate state of the node.

        Args:
            value (bool, optional): True to set intermediate, False to unset. Defaults to True.

        Returns:
            bool: True if the intermediate state was set or unset successfully, False otherwise.

        Example:
            >>> node = Node("pCube1")
            >>> node.set_intermediate(False)
            True
        """

        if not self.node_exists():
            return False

        cmds.setAttr(f'{self.name}.intermediateObject', value)
        return True

    def duplicate_node(self, new_name: str = "", children: bool = True, **kwargs) -> str:
        """Duplicate the current node.

        Args:
            new_name (str, optional): The new name of the node. Defaults to None.
            children (bool, optional): 	Duplicate only the specified DAG node
                                        and not any of its children.

        Returns:
            str: The name of the new node.

        Example:
            >>> node = Node("pCube1")
            >>> node.duplicate_node()
            'pCube2'
        """

        if not self.node_exists():
            return False

        if not new_name:
            new_name = self.name

        new_node = cmds.duplicate(
            self.name, n=new_name, po=not children, rc=True, **kwargs)

        return new_node[0]

    # DELETTERS
    def delete_node(self) -> bool:
        """Delete the node from the scene

        Returns:
            bool: True if the node was deleted, False otherwise

        Example:
        >>> node = Node('pCube1')
        >>> node.delete_node()
        True
        """

        if self.node_exists():

            if self.is_node_locked():
                self.lock_node(lock=False)

            cmds.delete(self.name)
            return True

        return False

    def delete_history(self) -> bool:
        """Delete the history of the node.

        Returns:
            bool: True if the history was deleted, False otherwise.

        Example:
            >>> node = Node("pCube1")
            >>> node.delete_history()
        """

        if not self.node_exists():
            return False
        cmds.delete(self.get_history())

        return True

    # METHODS
    def create_node(self, node_type: str, **kwargs) -> str:
        """Create node in the scene

        Args:
            node_type (str): The type of the node

        Returns:
            str: The name of the created node

        Example:
            >>> node = Node('test')
            >>> node.create_node('transform')
            'test'
        """

        if not self.node_exists():
            return cmds.createNode(node_type, self.name, **kwargs)

        return None

    # NAMING UTILITIES
    def rename_node(self, new_name: str) -> bool:
        """Renames the node to a new name.

        Args:
            new_name (str): The new name for the node.

        Returns:
            bool: True if the node was renamed successfully, False otherwise.

        Example:
            >>> node = Node("pCube1")
            >>> node.rename_node("myNewCube")
            True
        """

        if not self.node_exists():
            return None

        cmds.rename(self.name, new_name)
        self.name = new_name
        return new_name

    def add_prefix(self, prefix: str, separator: str = '_') -> str:
        """Add a prefix to the node name using a separator

        Args:
            prefix (str): The prefix to add.
            separator (str, optional): The separator to use. Defaults to '_'.

        Returns:
            str: The new name of the node.

        Example:
            >>> node = Node("pCube1")
            >>> node.add_prefix("myPrefix")
            'myPrefix_pCube1'
        """

        new_name = naming.add_prefix(
            text=self.name, prefix=prefix, separator=separator)

        return self.rename_node(new_name)

    def add_suffix(self, suffix: str, separator: str = '_') -> str:
        """Add a suffix to the node name using a separator

        Args:
            suffix (str): The suffix to add.
            separator (str, optional): The separator to use. Defaults to '_'.

        Returns:
            str: The new name of the node.

        Example:
            >>> node = Node("pCube1")
            >>> node.add_suffix("mySuffix")
            'pCube1_mySuffix'
        """

        new_name = naming.add_suffix(self.name, suffix, separator)

        return self.rename_node(new_name)

    def add_text(self, text: str) -> str:
        """Add text to the node name in PascalCase

        Args:
            text (str): The text to add.

        Returns:
            str: The new name of the node.

        Example:
            >>> node = Node("pCube1")
            >>> node.add_text("test")
            'pCube1Test'
        """

        new_name = naming.add_text(text=self.name, text_to_add=text)

        return self.rename_node(new_name)

    def increment_digit(self, digits: int = None) -> str:
        """Increment the last number in the node.

        Args:
            digits(int, optional): Number of digits for the number to increment.
                                    Defaults to None

        Returns:
            str: The new name of the node.

        Example:
            >>> node = Node("pCube1")
            >>> node.rename_with_increment_digit(3)
            'pCube002'
        """

        new_name = naming.increment_digit(self.name, digits=digits)

        return self.rename_node(new_name)

    def decrement_digit(self) -> str:
        """Decrement the last number in the node.

        Returns:
            str: The new name of the node.

        Note:
            If the text does not contain numbers, it will return the original text
            If the number is 0 or 1, it will remove it

        Example:
            >>> node = Node("pCube1")
            >>> node.rename_with_decrement_digit()
            'pCube'
        """

        new_name = naming.decrement_digit(text=self.name)

        return self.rename_node(new_name)

    def increment_character(self):
        """
        Rename the node with an incremented character.

        Returns:
            str: The new name of the node.

        Example:
            >>> node = Node("test")
            >>> node.rename_with_increment_character()
            'tess'
        """

        new_name = naming.increment_character(text=self.name)

        return self.rename_node(new_name)

    def decrement_character(self):
        """Decrement a letter sequence in a manner similar to Excel column naming

        Returns:
            str: The new name of the node.

        Example:
            >>> node = Node("pCube1")
            >>> node.rename_with_decrement_character()
        """

        new_name = naming.decrement_character(text=self.name)

        return self.rename_node(new_name)
