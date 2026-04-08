import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time

class NavigateTurtle(Node):
    def __init__(self):
        super().__init__('navigate_turtle')

        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.subscription = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)

        self.current_pose = None

    def pose_callback(self, msg):
        self.current_pose = msg

    def move_to_goal(self, x_goal, y_goal):
        msg = Twist()

        while self.current_pose is None:
            rclpy.spin_once(self)

        while True:
            dx = x_goal - self.current_pose.x
            dy = y_goal - self.current_pose.y
            distance = math.sqrt(dx*dx + dy*dy)

            if distance < 0.1:
                break

            angle_to_goal = math.atan2(dy, dx)
            angle_diff = angle_to_goal - self.current_pose.theta

            msg.linear.x = 1.5 * distance
            msg.angular.z = 4.0 * angle_diff

            self.publisher_.publish(msg)
            rclpy.spin_once(self)

        msg.linear.x = 0.0
        msg.angular.z = 0.0
        self.publisher_.publish(msg)

def main():
    rclpy.init()
    node = NavigateTurtle()

    time.sleep(2)

    x = float(input("Enter X: "))
    y = float(input("Enter Y: "))

    node.move_to_goal(x, y)

    rclpy.shutdown()

if __name__ == '__main__':
    main()
