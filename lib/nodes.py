"""
This module provides a `Node` class that represents a node in a Maya scene.
It includes methods for creating, querying, modifying, and deleting nodes
"""

# Maya imports
from maya import cmds

# Local imports
from craftRig.lib.scene import Scene


class Node(Scene):
    """
    Node class
    """

    def __init__(self, name, node_type=''):
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
        selection = cmds.ls(selection=True)

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

        return cmds.lockNode(self.name, query=True, lock=True)[0]

    # GETTERS
    def get_full_path(self) -> str:
        """Get the full path of the node.

        Returns:
            str: The full path of the node.
        """

        if not self.node_exists():
            return False

        return cmds.ls(self.name, long=True)[0]

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

        cmds.lockNode(self.name, lock=lock)
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
        """
        if not self.node_exists():
            return False

        if not new_name:
            new_name = self.name

        new_node = cmds.duplicate(
            self.name,
            name=new_name,
            parentOnly=not children,
            renameChildren=True,
            **kwargs)

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
            return cmds.createNode(node_type, name=self.name, **kwargs)

        return None

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
