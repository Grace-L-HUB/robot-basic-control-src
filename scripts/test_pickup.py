#!/usr/bin/env python3
"""
测试完整抓取流程
1. 移动到目标位置
2. 识别并抓取物体
3. 移动到放置位置
4. 释放物体
"""
import sys
import os
import time
import logging

# 添加src目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from control.robot_controller import RobotController
from utils.config_manager import ConfigManager

def setup_logging():
    """设置日志"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def test_pickup_place():
    """测试抓取和放置流程"""
    logger = logging.getLogger('test_pickup')
    logger.info("Testing pickup and place流程...")
    
    try:
        # 加载配置
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'robot_config.yaml')
        config = ConfigManager(config_path)
        
        # 初始化机器人控制器
        robot = RobotController(config.config)
        if not robot.initialize():
            logger.error("Failed to initialize robot controller")
            return False
        
        # 获取机器人状态
        logger.info("Getting robot status...")
        status = robot.get_status()
        if status:
            logger.info(f"Robot status: {status}")
        else:
            logger.warning("Failed to get robot status")
        
        # 定义抓取和放置位置
        # 注意：这里需要根据实际环境设置合适的坐标
        pickup_x, pickup_y, pickup_z = 1.0, 1.0, 0.1
        place_x, place_y, place_z = 2.0, 1.0, 0.1
        
        # 1. 移动到抓取位置
        logger.info(f"Moving to pickup position ({pickup_x}, {pickup_y})...")
        if not robot.move_to(pickup_x, pickup_y):
            logger.error("Failed to move to pickup position")
            return False
        
        time.sleep(2)
        
        # 2. 抓取物体
        logger.info(f"Picking up object at ({pickup_x}, {pickup_y}, {pickup_z})...")
        if not robot.pick_object(pickup_x, pickup_y, pickup_z):
            logger.error("Failed to pick up object")
            return False
        
        time.sleep(3)
        
        # 3. 移动到放置位置
        logger.info(f"Moving to place position ({place_x}, {place_y})...")
        if not robot.move_to(place_x, place_y):
            logger.error("Failed to move to place position")
            return False
        
        time.sleep(2)
        
        # 4. 放置物体
        logger.info(f"Placing object at ({place_x}, {place_y}, {place_z})...")
        if not robot.place_object(place_x, place_y, place_z):
            logger.error("Failed to place object")
            return False
        
        time.sleep(3)
        
        # 获取最终状态
        logger.info("Getting final robot status...")
        final_status = robot.get_status()
        if final_status:
            logger.info(f"Final robot status: {final_status}")
        else:
            logger.warning("Failed to get final robot status")
        
        logger.info("Pickup and place流程 completed successfully!")
        return True
    except Exception as e:
        logger.error(f"Error in pickup and place测试: {e}")
        return False

def main():
    """主函数"""
    setup_logging()
    logger = logging.getLogger('test_pickup')
    
    try:
        logger.info("Starting pickup and place tests...")
        
        # 测试抓取和放置流程
        test_pickup_place()
        
        logger.info("All pickup and place tests completed!")
        return 0
    except Exception as e:
        logger.error(f"Error in pickup and place tests: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
