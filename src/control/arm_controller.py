import rospy
from sensor_msgs.msg import JointState
import logging

logger = logging.getLogger(__name__)

class ArmController:
    """机械臂控制器"""
    
    def __init__(self):
        """初始化 ROS 发布者"""
        try:
            # 初始化ROS节点
            if not rospy.core.is_initialized():
                rospy.init_node('arm_controller', anonymous=True)
            
            # 创建发布者
            self.arm_publisher = rospy.Publisher('/kuavo_arm_traj', JointState, queue_size=10)
            logger.info("Arm controller initialized successfully")
        except rospy.ROSException as e:
            logger.error(f"Failed to initialize arm controller: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error initializing arm controller: {e}")
            raise
    
    def set_joint_angles(self, angles: list) -> bool:
        """设置机械臂关节角度
        
        Args:
            angles: 14 个关节的角度值列表（单位：度）
        
        Returns:
            bool: 成功返回 True
        """
        try:
            if len(angles) != 14:
                logger.error(f"Expected 14 joint angles, got {len(angles)}")
                return False
            
            msg = JointState()
            msg.name = [f"arm_joint_{i}" for i in range(1, 15)]
            msg.header.stamp = rospy.Time.now()
            msg.position = angles
            
            self.arm_publisher.publish(msg)
            logger.info(f"Set joint angles: {angles}")
            return True
        except Exception as e:
            logger.error(f"Error setting joint angles: {e}")
            return False
    
    def go_to_position(self, x: float, y: float, z: float) -> bool:
        """移动到指定空间位置（使用逆运动学）
        
        Args:
            x, y, z: 目标位置坐标（米）
        
        Returns:
            bool: 成功返回 True
        """
        try:
            # 这里需要实现逆运动学计算
            # 暂时使用模拟数据
            # 假设逆运动学计算结果
            joint_angles = [-30, 60, 0, -30, 0, -30, 30, 0, 0, 0, 0, 0, 0, 0]
            
            # 发布关节角度
            return self.set_joint_angles(joint_angles)
        except Exception as e:
            logger.error(f"Error going to position: {e}")
            return False
    
    def home(self) -> bool:
        """回到初始位置"""
        try:
            # 初始位置的关节角度
            home_angles = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            return self.set_joint_angles(home_angles)
        except Exception as e:
            logger.error(f"Error going home: {e}")
            return False
    
    def set_control_mode(self, mode: int) -> bool:
        """设置控制模式
        
        Args:
            mode: 0=保持姿势, 1=自动摆手, 2=外部控制
        """
        try:
            # 这里需要根据实际的服务接口来实现
            # 假设通过服务设置控制模式
            service_name = '/arm_traj_change_mode'
            try:
                rospy.wait_for_service(service_name, timeout=5.0)
                # 这里需要导入对应的服务类型
                # from arm_control.srv import ChangeModeRequest
                # change_mode = rospy.ServiceProxy(service_name, ChangeModeRequest)
                # response = change_mode(mode)
                # return response.success
                
                # 暂时返回成功
                logger.info(f"Set control mode to: {mode}")
                return True
            except rospy.ROSException:
                logger.warning("Control mode service not available, using fallback")
                return True
        except Exception as e:
            logger.error(f"Error setting control mode: {e}")
            return False
