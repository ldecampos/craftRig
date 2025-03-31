"""
This module provides a 'DagNode' class that represents a dag Node in a Maya scene.
"""

from maya import cmds
from craftRig.lib import node


class DagNode(node.Node):
    """
    DagNode class
    """

    def __init__(self, name: str, node_type: str = '') -> None:
        """DagNode class constructor

        Args:
            name (str): The name of the node
            node_type (str): The type of the node
        """

        super().__init__(name=name, node_type=node_type)
        self.name = name
        self.node_type = node_type

    @classmethod
    def from_string(cls, text: str) -> 'DagNode':
        """Create a DagNode object from a string

        Args:
            text (str): Name of the node

        Returns:
            DagNode: DagNode object

        Example:
        >>> dag_node = DagNode.from_string('test')
        >>> dag_node.name
        'test'
        """

        return DagNode(name=text, node_type=cmds.nodeType(text))

    @classmethod
    def from_selection(cls) -> 'DagNode':
        """Create a DagNode object from the selection

        Returns:
            DagNode: DagNode object

        Example:
        >>> dag_node = DagNode.from_selection()
        >>> dag_node.name
        'pCube1'
        """

        selection = cmds.ls(sl=True) or []

        if not selection:
            return None

        return DagNode.from_string(text=selection[0])

    # VALIDATORS
    def is_template(self) -> bool:
        """Check if the DagNode is set to template.

        Returns:
            bool: True if the DagNode is template, False otherwise.

        Example:
            >>> dag_node = DagNode("pCube1")
            >>> dag_node.is_template()
            False
        """

        if not self.node_exists():
            return False

        return cmds.getAttr(f'{self.name}.template')

    def is_visible(self) -> bool:
        """Check if the DagNode is visible.

        Returns:
            bool: True if the DagNode is visible, False otherwise.

        Example:
            >>> dag_node = DagNode("pCube1")
            >>> dag_node.is_visible()
        """

        if not self.node_exists():
            return False

        return cmds.getAttr(f'{self.name}.visibility')

    def is_in_hierarchy(self) -> bool:
        """Check if the node is in the hierarchy.

        Returns:
            bool: True if the node is in the hierarchy, False otherwise.

        Example:
            >>> dag_node = DagNode("pCube1")
            >>> dag_node.is_in_hierarchy()
            True
        """

        if not self.node_exists():
            return False

        return True if self.get_parent() else False

    # GETTERS
    def get_parent(self) -> str:
        """Gets the parent of the node.

        Returns:
            str or None: The name of the parent node, or None if it has no parent.

        Example:
            >>> node = Node('transform')
            >>> node.get_parent()
            []
        """

        if not self.node_exists():
            return []

        return cmds.listRelatives(self.name, p=True) or []

    def get_parents(self) -> list[str]:
        """Get all parents of the node.

        Returns:
            list[str]: A list of the names of all parents nodes.

        Example:
            >>> node = DagNode('pCube4')
            >>> node.get_parents()
            ['pCube2', 'pCube1']
        """

        if not self.node_exists():
            return []

        return cmds.listRelatives(self.name, ap=True) or []

    def get_child(self) -> str:
        """Gets the child of the node.

        Returns:
            list: A list of the names of the child nodes.

        Example:
        >>> node = Node('pCube1')
        >>> node.get_children()
        ['pCube2','pCube3']
        """
        if not self.node_exists():
            return []

        return cmds.listRelatives(self.name, c=True) or []

    def get_children(self) -> list[str]:
        """Get all children of the node.

        Returns:
            list[str]: A list of the names of all descendant nodes.

        Example:
            >>> node = DagNode('pCube1')
            >>> node.get_descendants()
            ['pCube2', 'pCube3', 'pCube4']
        """

        if not self.node_exists():
            return []

        return cmds.listRelatives(self.name, True) or []

    def get_translation(self, world_space: bool = True) -> list[float]:
        """Get the translation of the node.

        Args:
            world_space (bool, optional): The space to get the translation. Defaults to Trie

        Returns:
            list[float]: A list of the x, y, and z translation values.

        Example:
            >>> node = DagNode('pCube1')
            >>> node.get_translation()
            [1.0, 2.0, 3.0]
        """

        if not self.node_exists():
            return []

        return cmds.xform(self.name, True, t=True, ws=world_space)

    def get_rotation(self, world_space: bool = True) -> list[float]:
        """Get the rotation of the node.

        Args:
            world_space (bool, optional): The space to get the rotation. Defaults to True

        Returns:
            list[float]: A list of the x, y, and z rotation values.

        Example:
            >>> node = DagNode('pCube1')
            >>> node.get_rotation()
            [0.0, 45.0, 0.0]
        """

        if not self.node_exists():
            return []

        return cmds.xform(self.name, True, r=True, ws=world_space)

    def get_scale(self) -> list[float]:
        """Get the scale of the node.

        Returns:
            list[float]: A list of the x, y, and z scale values.

        Example:
            >>> node = DagNode('pCube1')
            >>> node.get_scale()
            [1.0, 1.0, 1.0]
        """

        if not self.node_exists():
            return []

        return cmds.xform(self.name, True, s=True)

    def get_matrix(self, world_space: bool = True) -> list[float]:
        """Get the world matrix of the node.

        Args:
            world_space (bool, optional): The space to get the matrix. Defaults to True

        Returns:
            list[float]: A list representing the 4x4 world matrix.

        Example:
            >>> node = DagNode('pCube1')
            >>> node.get_world_matrix()
            [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0,
                0.0, 0.0, 1.0, 0.0, 1.0, 2.0, 3.0, 1.0]
        """

        if not self.node_exists():
            return []

        return cmds.xform(self.name, q=True, m=True, ws=world_space, os=not world_space)

    def get_shapes(self) -> list[str]:
        """Get the shapes of the node.

        Returns:
            list[str]: A list of the names of the shape nodes.

        Example:
            >>> node = DagNode('pCube1')
            >>> node.get_shapes()
            ['pCubeShape1']
        """

        if not self.node_exists():
            return []

        return cmds.listRelatives(self.name, s=True, f=True) or []

    # SETTERS
    def set_template(self, value: bool = True) -> bool:
        """Set or unset the template state of the node.

        Args:
            value (bool, optional): True to set template, False to unset. Defaults to True.

        Returns:
            bool: True if the template state was set or unset successfully, False otherwise.

        Example:
        >>> node = Node('pCube1')
        >>> node.set_template(True)
        True
        """
        if not self.node_exists():
            return False

        cmds.setAttr(f'{self.name}.template', value)
        return True

    def set_visible(self, value: bool = True) -> bool:
        """Set or unset the visible state of the node.

        Args:
            value (bool, optional): True to set visible, False to unset. Defaults to True.

        Returns:
            bool: True if the visible state was set or unset successfully, False otherwise.

        Example:
        >>> node = Node('pCube1')
        >>> node.set_visible(True)
        True
        """
        if not self.node_exists():
            return False

        cmds.setAttr(f'{self.name}.visibility', value)
        return True

    def set_translation(self, x: float, y: float, z: float, world_space: bool = True) -> bool:
        """Set the translation of the node.

        Args:
            x (float): The x translation value.
            y (float): The y translation value.
            z (float): The z translation value.
            world_space (str, optional): The space to set the translation in. Defaults to True.

        Returns:
            bool: True if the translation was set successfully, False otherwise.

        Example:
            >>> node = DagNode('pCube1')
            >>> node.set_translation(1.0, 2.0, 3.0)
            True
        """

        if not self.node_exists():
            return False

        cmds.xform(self.name, t=[x, y, z], ws=world_space, os=not world_space)
        return True

    def set_rotation(self, x: float, y: float, z: float, world_space: bool = True) -> bool:
        """Set the rotation of the node.

        Args:
            x (float): The x rotation value.
            y (float): The y rotation value.
            z (float): The z rotation value.
            world_space (str, optional): The space to set the rotation in. Defaults to True.

        Returns:
            bool: True if the rotation was set successfully, False otherwise.

        Example:
            >>> node = DagNode('pCube1')
            >>> node.set_rotation(0.0, 45.0, 0.0)
            True
        """

        if not self.node_exists():
            return False

        cmds.xform(self.name, r=[x, y, z], ws=world_space, os=not world_space)
        return True

    def set_scale(self, x: float, y: float, z: float) -> bool:
        """Set the scale of the node.

        Args:
            x (float): The x scale value.
            y (float): The y scale value.
            z (float): The z scale value.

        Returns:
            bool: True if the scale was set successfully, False otherwise.

        Example:
            >>> node = DagNode('pCube1')
            >>> node.set_scale(2.0, 2.0, 2.0)
            True
        """

        if not self.node_exists():
            return False

        cmds.xform(self.name, s=[x, y, z])
        return True

    def set_matrix(self, matrix: list[float], world_space: bool = True) -> bool:
        """Set the world matrix of the node.

        Args:
            matrix (list[float]): A list representing the 4x4 world matrix.
            world_space (bool, optional): The space to get the matrix. Defaults to True

        Returns:
            bool: True if the world matrix was set successfully, False otherwise.

        Example:
            >>> node = DagNode('pCube1')
            >>> node.set_world_matrix(
            [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 2.0, 3.0, 1.0])
            True
        """

        if not self.node_exists():
            return False

        if len(matrix) != 16:
            return False

        cmds.xform(self.name, m=matrix, ws=world_space, os=not world_space)
        return True

    # METHODS
    def parent_to(self, parent_node: str, **kwargs: any) -> bool:
        """Parent the node to another node

        Args:
            parent_node (str): the node to parent to

        Returns:
            bool: True if successfull, False otherwise

        Example:
        >>> node = Node('pCube1')
        >>> node.parent_node('pCube2')
        True
        """

        if not self.node_exists():
            return False

        cmds.parent(self.name, parent_node, **kwargs)
        return True

    def parent_to_world(self):
        """Parent the node to world

        Returns:
            bool: rue if successfull, False otherwise

        Example:
        >>> node = Node('pCube1')
        >>> node.unparent_node()
        True
        """

        if not self.node_exists():
            return False

        if self.get_parent():
            cmds.parent(self.name, w=True)
            return True

        return False
