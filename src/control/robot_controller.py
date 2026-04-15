from ..communication.robot_api import WooshApi
from .gripper_controller import GripperController
from .arm_controller import ArmController
import logging

logger = logging.getLogger(__name__)

class RobotController:
    """机器人统一控制器"""
    
    def __init__(self, config: dict):
        """初始化控制器
        
        Args:
            config: 配置字典，包含 IP、端口等
        """
        self.config = config
        self.chassis = None   # WooshApi 实例
        self.gripper = None   # GripperController 实例
        self.arm = None       # ArmController 实例
        
    def initialize(self) -> bool:
        """初始化所有连接
        
        Returns:
            bool: 全部连接成功返回 True
        """
        try:
            # 初始化底盘控制
            websocket_config = self.config.get("robot", {}).get("websocket", {})
            ip = websocket_config.get("ip", "192.168.1.100")
            port = websocket_config.get("port", 8080)
            url = f"ws://{ip}:{port}/"
            
            self.chassis = WooshApi(url)
            if not self.chassis.connect():
                logger.error("Failed to connect to chassis")
                return False
            
            # 初始化夹爪控制器
            try:
                self.gripper = GripperController()
            except Exception as e:
                logger.warning(f"Failed to initialize gripper: {e}")
                self.gripper = None
            
            # 初始化机械臂控制器
            try:
                self.arm = ArmController()
            except Exception as e:
                logger.warning(f"Failed to initialize arm: {e}")
                self.arm = None
            
            logger.info("Robot controller initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Error initializing robot controller: {e}")
            return False
    
    def move_to(self, x: float, y: float) -> bool:
        """移动底盘到指定位置"""
        try:
            if not self.chassis:
                logger.error("Chassis not initialized")
                return False
            
            return self.chassis.robot_go_to(x, y)
        except Exception as e:
            logger.error(f"Error moving to position: {e}")
            return False
    
    def pick_object(self, x: float, y: float, z: float) -> bool:
        """在指定位置抓取物体
        
        Args:
            x, y, z: 物体在机器人坐标系下的位置
        
        Returns:
            bool: 抓取成功返回 True
        """
        try:
            # 1. 移动到物体附近
            if not self.move_to(x, y):
                logger.error("Failed to move to object")
                return False
            
            # 2. 张开夹爪准备抓取
            if self.gripper:
                if not self.gripper.open():
                    logger.error("Failed to open gripper")
                    return False
            
            # 3. 机械臂移动到抓取点
            if self.arm:
                if not self.arm.go_to_position(x, y, z):
                    logger.error("Failed to move arm to grasp position")
                    return False
            
            # 4. 闭合夹爪
            if self.gripper:
                if not self.gripper.close():
                    logger.error("Failed to close gripper")
                    return False
            
            # 5. 抬起机械臂
            if self.arm:
                if not self.arm.go_to_position(x, y, z + 0.2):
                    logger.error("Failed to lift arm")
                    return False
            
            logger.info(f"Object picked at position ({x}, {y}, {z})")
            return True
        except Exception as e:
            logger.error(f"Error picking object: {e}")
            return False
    
    def place_object(self, x: float, y: float, z: float) -> bool:
        """将物体放置到指定位置"""
        try:
            # 1. 移动到放置位置附近
            if not self.move_to(x, y):
                logger.error("Failed to move to place position")
                return False
            
            # 2. 机械臂移动到放置点
            if self.arm:
                if not self.arm.go_to_position(x, y, z + 0.2):
                    logger.error("Failed to move arm to place position")
                    return False
            
            # 3. 机械臂下降到放置高度
            if self.arm:
                if not self.arm.go_to_position(x, y, z):
                    logger.error("Failed to lower arm")
                    return False
            
            # 4. 张开夹爪释放物体
            if self.gripper:
                if not self.gripper.open():
                    logger.error("Failed to open gripper")
                    return False
            
            # 5. 抬起机械臂
            if self.arm:
                if not self.arm.go_to_position(x, y, z + 0.2):
                    logger.error("Failed to lift arm")
                    return False
            
            logger.info(f"Object placed at position ({x}, {y}, {z})")
            return True
        except Exception as e:
            logger.error(f"Error placing object: {e}")
            return False
    
    def get_status(self) -> dict:
        """获取机器人完整状态
        
        Returns:
            dict: 包含位置、电池、夹爪状态等
        """
        try:
            status = {}
            
            # 获取底盘状态
            if self.chassis:
                status["chassis"] = {
                    "state": self.chassis.robot_state(),
                    "pose": self.chassis.robot_pose_speed(),
                    "battery": self.chassis.robot_battery()
                }
            
            # 获取夹爪状态
            if self.gripper:
                status["gripper"] = self.gripper.get_state()
            
            # 获取机械臂状态
            if self.arm:
                status["arm"] = "initialized"
            
            return status
        except Exception as e:
            logger.error(f"Error getting robot status: {e}")
            return {}
