"""
Scene module
"""


# Maya imports
from maya import cmds


class Scene(object):
    """
    Scene class
    """

    @staticmethod
    def get_scene_namespaces() -> list:
        """Get a list of namespaces in the Maya scene, excluding default namespaces "UI", "shared".

        Returns:
            list: A list of namespaces in the Maya scene, 
        """

        namespaces = cmds.namespaceInfo(listOnlyNamespaces=True, recurse=True)

        filtered_namespaces = [
            ns for ns in namespaces if ns not in ["UI", "shared"]]

        return filtered_namespaces or []
