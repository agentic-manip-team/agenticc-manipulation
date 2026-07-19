"""
AnyGrasp Client Wrapper
Provides a simple interface for computing grasp poses from a point cloud.

Input:  point cloud (numpy array) of the target object's surface,
        camera-to-world transform
Output: best grasp pose (position + orientation) and a quality score
"""

from dataclasses import dataclass

import numpy as np


@dataclass
class GraspPose:
    """Represents a single candidate grasp pose."""
    position: dict       # {"x": float, "y": float, "z": float}
    orientation: dict     # quaternion {"x": float, "y": float, "z": float, "w": float}
    score: float          # quality score between 0 and 1


class AnyGraspClient:
    """
    Wrapper around the AnyGrasp SDK.

    This is currently a placeholder implementation. The actual AnyGrasp
    model call will be added once running on the GPU machine (M1's setup),
    following license registration at:
    https://github.com/graspnet/anygrasp_sdk
    """

    def __init__(self, checkpoint_path: str = "checkpoints/anygrasp.pt"):
        self.checkpoint_path = checkpoint_path
        self._model_loaded = False

    def load_model(self):
        """Load the AnyGrasp model. Placeholder for now."""
        # TODO: load actual AnyGrasp model from self.checkpoint_path
        self._model_loaded = True

    def plan_grasps(self, point_cloud: np.ndarray, camera_to_world: np.ndarray) -> list[GraspPose]:
        """
        Compute candidate grasp poses for the given point cloud.

        Args:
            point_cloud: Nx3 array of 3D points on the object's surface.
            camera_to_world: 4x4 transform matrix from camera frame to world frame.

        Returns:
            A list of GraspPose candidates, sorted by score (best first).
        """
        if not self._model_loaded:
            raise RuntimeError("Model not loaded. Call load_model() first.")

        # Placeholder grasp — replace with real AnyGrasp inference call
        placeholder_grasp = GraspPose(
            position={"x": 0.0, "y": 0.0, "z": 0.0},
            orientation={"x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0},
            score=0.0,
        )
        return [placeholder_grasp]

    def get_best_grasp(self, point_cloud: np.ndarray, camera_to_world: np.ndarray) -> GraspPose:
        """Convenience method to return only the highest-scoring grasp."""
        grasps = self.plan_grasps(point_cloud, camera_to_world)
        return max(grasps, key=lambda g: g.score)