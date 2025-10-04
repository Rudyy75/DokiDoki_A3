#Move to (5.5, 8) then call service to move in circle, at the end move to (8, 8)
#Stage 1 - Move to (5.5, 8) and finish circle movement
#Stage 2 - After moving in circle go to (8,8) 

import rclpy
import math
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from example_interfaces.srv import Trigger

class TurtleNigga(Node):
    def __init__(self):
        super().__init__('turtle_nigga')
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.subscriber = self.create_subscription(Pose, '/turtle1/pose', self.wyanig, 10)
        self.timer = self.create_timer(0.1, self.niggamooove)

        self.currentPose = Pose()
        self.LinearError = 0.001
        self.AngularError = 0.001

        self.targetx = 5.5
        self.targety = 8.0
        self.targetO = 0.0

        self.linearKp = 2.0
        self.angularKp = 5.0

        self.reached = False

        self.stage = 1
        self.moveCircle_client = None

    def wyanig(self, pose):
        self.currentPose = pose

    def targetdist(self):
        self.currentx = self.currentPose.x
        self.currenty = self.currentPose.y

        dispx = self.targetx - self.currentx
        dispy = self.targety - self.currenty

        dispf = math.sqrt((dispx ** 2) + (dispy ** 2))

        return dispf
    
    def targetang(self):
        self.currentx = self.currentPose.x
        self.currenty = self.currentPose.y

        dispx = self.targetx - self.currentx
        dispy = self.targety - self.currenty

        fang = math.atan2(dispy, dispx)
        ffang = fang - self.currentPose.theta
        ffang = math.atan2(math.sin(ffang), math.cos(ffang))
        
        return ffang
    
    def niggamooove(self):
        msg = Twist()
        dist = self.targetdist()
        ang = self.targetang()
        orient = self.targetO - self.currentPose.theta
        orient = math.atan2(math.sin(orient), math.cos(orient))

        if self.reached:
            return
        
        if dist > self.LinearError:
            if abs(ang) > self.AngularError:
                msg.linear.x = 0.0
                msg.angular.z = self.angularKp * ang
                self.publisher.publish(msg)
            else:
                msg.linear.x = self.linearKp * dist
                msg.angular.z = self.angularKp * ang
                self.publisher.publish(msg)
        elif abs(orient) > self.AngularError:
            msg.linear.x = 0.0
            msg.angular.z = self.angularKp * orient
            self.publisher.publish(msg)
        else:
            self.reached = True
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.publisher.publish(msg)
            self.get_logger().info("Position Reached")
            self.stageCheck()

    def stageCheck(self):
        if self.stage == 1:
            self.get_logger().info("Nigga will move in circle now")
            self.moveCircle()
        elif self.stage == 2:
            self.get_logger().info("Final Coord Reached")

    def moveCircle(self):
        self.moveCircle_client = self.create_client(Trigger, 'moveInCircle')
        self.get_logger().info("Waiting for Service")
        while not self.moveCircle_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn("Waiting for Service to be Available")

        request = Trigger.Request()
        future = self.moveCircle_client.call_async(request)
        future.add_done_callback(self.pljMoveCircle)

    def pljMoveCircle(self, future):
        try:
            response = future.result()
            if response.success:
                self.get_logger().info("Circle chalu hogaya")
                #idk how to check when the circle finishes so ill just add a timer delay here
                import time
                time.sleep(10) 
                #10 coz time = 2*pi*r/v so nearly 7 or 8, ill give lil extra buffer time
                self.stage = 2
                self.targetx = 8.0
                self.targety = 8.0
                self.targetO = 0.0
                self.reached = False
            else:
                self.get_logger().info("Circle nhi hua")
        except Exception as e:
            self.get_logger().error("Service call failed %r" % (e,))
        
def main(args=None):
    rclpy.init(args=args)
    DokiDoki = TurtleNigga()
    DokiDoki.get_logger().info("Starting DokiDoki Turtle autonav")
    rclpy.spin(DokiDoki)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
    