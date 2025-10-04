#Service to make that turtle nigga move in a circle

import rclpy
import math
from rclpy.node import Node
from example_interfaces.srv import Trigger
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from functools import partial

class CircleServer(Node):
    def __init__(self):
        super().__init__('move_circle_server')
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.subscriber = self.create_subscription(Pose, '/turtle1/pose', self.wyanig, 10)
        self.service = self.create_service(Trigger, 'moveInCircle', self.moveInCircle)
        self.timer = self.create_timer(0.1, self.niggarotate)

        self.linearErr = 0.01

        self.currentPose = Pose()
        self.start = None
        self.ismoving = False
        self.movedlil = False

        self.radius = 3.0
        self.linearVel = 2.5
        self.angularVel = -(self.linearVel / self.radius)

        self.get_logger().info("Server is Ready to be Called")

    def wyanig(self, pose):
        self.currentPose = pose

        if self.ismoving and self.start is not None:
            delx = self.currentPose.x - self.start.x
            dely = self.currentPose.y - self.start.y
            delf = math.sqrt((delx ** 2) + (dely ** 2))

            if delf > 0.1:
                self.movedlil = True

            if delf < self.linearErr and self.movedlil:
                self.get_logger().info("Circle Done")
                self.stoprotate()
                self.ismoving = False
                self.start = None
                self.movedlil = False


    def niggarotate(self):
        if self.ismoving:
            msg = Twist()
            msg.linear.x = self.linearVel
            msg.angular.z = self.angularVel
            self.publisher.publish(msg)

    def stoprotate(self):
        msg = Twist()
        msg.linear.x = 0.0
        msg.angular.z = 0.0
        self.publisher.publish(msg)

    def moveInCircle(self, request, response):
        self.get_logger().info("Request Received")
        self.ismoving = True
        self.movedlil = False
        self.start = Pose()
        self.start.x = self.currentPose.x
        self.start.y = self.currentPose.y

        response.success = True
        response.message = "Moving in Circle"
        return response

def main(args=None):
    rclpy.init(args=args)
    CircleServer1 = CircleServer()
    rclpy.spin(CircleServer1)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
    