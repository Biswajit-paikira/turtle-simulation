import rclpy
from rclpy.node import Node
from std_srvs.srv import Empty
import tkinter as tk

class TurtleGUI(Node):
    def __init__(self):
        super().__init__('turtle_gui')

        self.reset_client = self.create_client(Empty, '/reset')
        self.clear_client = self.create_client(Empty, '/clear')

        while not self.reset_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for reset service...')

        while not self.clear_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for clear service...')

    def call_reset(self):
        req = Empty.Request()
        self.reset_client.call_async(req)

    def call_clear(self):
        req = Empty.Request()
        self.clear_client.call_async(req)

def main():
    rclpy.init()
    node = TurtleGUI()

    root = tk.Tk()
    root.title("Turtle Control")

    btn_reset = tk.Button(root, text="Reset", command=node.call_reset)
    btn_reset.pack(pady=10)

    btn_clear = tk.Button(root, text="Clear", command=node.call_clear)
    btn_clear.pack(pady=10)

    root.mainloop()

    rclpy.shutdown()

if __name__ == '__main__':
    main()
