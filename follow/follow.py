import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import Spawn
import math
import random
import time

class FollowTurtle(Node):
    def __init__(self):
        super().__init__('follow_turtle')

        self.pub1 = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pub2 = self.create_publisher(Twist, '/girl/cmd_vel', 10)

        self.sub1 = self.create_subscription(Pose, '/turtle1/pose', self.pose1_callback, 10)
        self.sub2 = self.create_subscription(Pose, '/girl/pose', self.pose2_callback, 10)

        self.pose1 = None
        self.pose2 = None

        self.spawn_client = self.create_client(Spawn, '/spawn')

        while not self.spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for spawn service...')

        self.spawn_girl()

    def spawn_girl(self):
        req = Spawn.Request()
        req.x = 5.5
        req.y = 5.5
        req.theta = 0.0
        req.name = 'girl'
        self.spawn_client.call_async(req)

    def pose1_callback(self, msg):
        self.pose1 = msg

    def pose2_callback(self, msg):
        self.pose2 = msg

    def move_girl_safe(self):
        msg = Twist()

        if self.pose2 is None:
            return

        if self.pose2.x < 2 or self.pose2.x > 9 or self.pose2.y < 2 or self.pose2.y > 9:
            msg.linear.x = 1.0
            msg.angular.z = 2.5
        else:
            msg.linear.x = 1.5
            msg.angular.z = random.uniform(-1.0, 1.0)

        self.pub2.publish(msg)

    def normalize_angle(self, angle):
        while angle > math.pi:
            angle -= 2*math.pi
        while angle < -math.pi:
            angle += 2*math.pi
        return angle

    def follow(self):
        msg = Twist()

        while self.pose1 is None or self.pose2 is None:
            rclpy.spin_once(self)

        while True:
            self.move_girl_safe()

            dx = self.pose2.x - self.pose1.x
            dy = self.pose2.y - self.pose1.y

            distance = math.sqrt(dx*dx + dy*dy)
            angle_to_goal = math.atan2(dy, dx)

            angle_diff = self.normalize_angle(angle_to_goal - self.pose1.theta)

            msg.linear.x = min(1.5 * distance, 2.0)
            msg.angular.z = 3.0 * angle_diff

            self.pub1.publish(msg)

            rclpy.spin_once(self)
            time.sleep(0.1)

def main():
    rclpy.init()
    node = FollowTurtle()

    time.sleep(2)

    node.follow()

    rclpy.shutdown()

if __name__ == '__main__':
    main()
