import rospy
from controlLejuClaw.srv import controlLejuClawRequest, controlLejuClawResponse
import logging

logger = logging.getLogger(__name__)

class GripperController:
    """机器人夹爪控制器"""
    
    def __init__(self):
        """初始化 ROS 节点和服务代理"""
        try:
            # 初始化ROS节点
            if not rospy.core.is_initialized():
                rospy.init_node('gripper_controller', anonymous=True)
            
            # 等待服务可用
            service_name = '/control_robot_leju_claw'
            rospy.wait_for_service(service_name, timeout=10.0)
            self.gripper_service = rospy.ServiceProxy(service_name, controlLejuClawRequest)
            logger.info("Gripper controller initialized successfully")
        except rospy.ROSException as e:
            logger.error(f"Failed to initialize gripper controller: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error initializing gripper controller: {e}")
            raise
    
    def close(self, position: int = 90) -> bool:
        """闭合夹爪
        
        Args:
            position: 闭合程度 0-100，90 表示闭合 90%
        
        Returns:
            bool: 成功返回 True
        """
        try:
            req = controlLejuClawRequest()
            req.data.name = ['left_claw', 'right_claw']
            req.data.position = [position, position]   # 0=张开, 100=闭合
            req.data.velocity = [50, 50]   # 速度 0-100
            req.data.effort = [1.0, 1.0]   # 力矩 1-2A
            
            response = self.gripper_service(req)
            if response.ok:
                logger.info(f"Gripper closed to position {position}")
                return True
            else:
                logger.error("Failed to close gripper")
                return False
        except Exception as e:
            logger.error(f"Error closing gripper: {e}")
            return False
    
    def open(self) -> bool:
        """完全张开夹爪"""
        try:
            return self.close(0)
        except Exception as e:
            logger.error(f"Error opening gripper: {e}")
            return False
    
    def get_state(self) -> dict:
        """获取夹爪状态
        
        Returns:
            dict: 包含位置、速度、是否抓取到物体等信息
        """
        try:
            # 这里需要根据实际的服务接口来实现
            # 假设服务返回夹爪状态
            # 暂时返回模拟数据
            return {
                "position": 0,
                "velocity": 0,
                "grasped": False,
                "status": "ok"
            }
        except Exception as e:
            logger.error(f"Error getting gripper state: {e}")
            return {}
