import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class DrawTriangle(Node):
    def __init__(self):
        super().__init__('draw_triangle')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

    def move_forward(self, speed, duration):
        msg = Twist()
        msg.linear.x = speed
        msg.angular.z = 0.0

        end_time = time.time() + duration
        while time.time() < end_time:
            self.publisher_.publish(msg)

        msg.linear.x = 0.0
        self.publisher_.publish(msg)

    def turn(self, angular_speed, duration):
        msg = Twist()
        msg.linear.x = 0.0
        msg.angular.z = angular_speed

        end_time = time.time() + duration
        while time.time() < end_time:
            self.publisher_.publish(msg)

        msg.angular.z = 0.0
        self.publisher_.publish(msg)

    def draw(self):
        for i in range(3):
            self.move_forward(2.0, 2.0)   
            self.turn(2.09, 1.0)          

def main():
    rclpy.init()
    node = DrawTriangle()
    time.sleep(2)   
    node.draw()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
