#!/usr/bin/env python3
"""
Custom Roomba Motor Control Script for L298N + 18V Ryobi Battery
Hardware Setup:
- L298N H-Bridge Motor Driver
- 18V Ryobi Battery with 20A fuse
- Two Roomba motors
- 12V jumper REMOVED (for >12V supply)
- Pi 4 GPIO connections as defined below

GPIO Pin Connections:
Motor A (Left): IN1=19, IN2=13, ENA=26
Motor B (Right): IN3=21, IN4=20, ENB=16
GND: Pi GND to L298N pin 5
Power: 18V+ to L298N pin 4, GND to L298N pin 5
"""

import time
import signal
import sys
from RpiMotorLib import rpi_dc_lib

class RoombaMotorController:
    def __init__(self):
        # Motor pin definitions based on L298N documentation
        self.motor_left = rpi_dc_lib.L298NMDc(19, 13, 26, 50, True, "left_motor")
        self.motor_right = rpi_dc_lib.L298NMDc(21, 20, 16, 50, True, "right_motor")
        
        # Set up signal handler for clean shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        
        print("Roomba Motor Controller Initialized")
        print("Hardware: L298N + 18V Ryobi Battery + 20A Fuse")
        print("IMPORTANT: Ensure 12V jumper is REMOVED from L298N module")
        print("Press Ctrl+C to stop safely")
        
    def signal_handler(self, sig, frame):
        """Handle Ctrl+C gracefully"""
        print("\nReceived interrupt signal. Stopping motors...")
        self.stop_all()
        self.cleanup()
        sys.exit(0)
    
    def forward(self, speed=25, duration=None):
        """Move both motors forward"""
        print(f"Moving forward at {speed}% speed")
        self.motor_left.forward(speed)
        self.motor_right.forward(speed)
        if duration:
            time.sleep(duration)
            self.stop_all()
    
    def backward(self, speed=25, duration=None):
        """Move both motors backward"""
        print(f"Moving backward at {speed}% speed")
        self.motor_left.backward(speed)
        self.motor_right.backward(speed)
        if duration:
            time.sleep(duration)
            self.stop_all()
    
    def turn_left(self, speed=25, duration=None):
        """Turn left by reversing left motor"""
        print(f"Turning left at {speed}% speed")
        self.motor_left.backward(speed)
        self.motor_right.forward(speed)
        if duration:
            time.sleep(duration)
            self.stop_all()
    
    def turn_right(self, speed=25, duration=None):
        """Turn right by reversing right motor"""
        print(f"Turning right at {speed}% speed")
        self.motor_left.forward(speed)
        self.motor_right.backward(speed)
        if duration:
            time.sleep(duration)
            self.stop_all()
    
    def stop_all(self):
        """Stop both motors"""
        print("Stopping all motors")
        self.motor_left.stop(0)
        self.motor_right.stop(0)
    
    def brake_all(self):
        """Emergency brake both motors"""
        print("Emergency brake activated")
        self.motor_left.brake(100)
        self.motor_right.brake(100)
    
    def cleanup(self):
        """Clean up GPIO resources"""
        print("Cleaning up GPIO resources")
        self.motor_left.cleanup(False)
        self.motor_right.cleanup(False)
    
    def test_sequence(self):
        """Run a basic test sequence"""
        print("\n=== Starting Motor Test Sequence ===")
        
        try:
            # Test 1: Forward movement
            print("Test 1: Forward movement (3 seconds)")
            self.forward(20, 3)
            time.sleep(1)
            
            # Test 2: Backward movement
            print("Test 2: Backward movement (3 seconds)")
            self.backward(20, 3)
            time.sleep(1)
            
            # Test 3: Turn left
            print("Test 3: Turn left (2 seconds)")
            self.turn_left(25, 2)
            time.sleep(1)
            
            # Test 4: Turn right
            print("Test 4: Turn right (2 seconds)")
            self.turn_right(25, 2)
            time.sleep(1)
            
            # Test 5: Speed ramp test
            print("Test 5: Speed ramp test (15% to 40%)")
            for speed in range(15, 41, 5):
                print(f"  Speed: {speed}%")
                self.forward(speed)
                time.sleep(1)
            self.stop_all()
            
            print("=== Test Sequence Complete ===")
            
        except Exception as e:
            print(f"Error during test: {e}")
            self.brake_all()
            raise
    
    def manual_control(self):
        """Interactive manual control mode"""
        print("\n=== Manual Control Mode ===")
        print("Commands:")
        print("  w - Forward")
        print("  s - Backward") 
        print("  a - Turn Left")
        print("  d - Turn Right")
        print("  x - Stop")
        print("  b - Brake")
        print("  + - Increase Speed")
        print("  - - Decrease Speed")
        print("  q - Quit")
        
        speed = 25
        
        try:
            while True:
                print(f"\nCurrent speed: {speed}%")
                cmd = input("Enter command: ").lower().strip()
                
                if cmd == 'w':
                    self.forward(speed)
                elif cmd == 's':
                    self.backward(speed)
                elif cmd == 'a':
                    self.turn_left(speed)
                elif cmd == 'd':
                    self.turn_right(speed)
                elif cmd == 'x':
                    self.stop_all()
                elif cmd == 'b':
                    self.brake_all()
                elif cmd == '+':
                    speed = min(speed + 5, 100)
                    print(f"Speed increased to {speed}%")
                elif cmd == '-':
                    speed = max(speed - 5, 5)
                    print(f"Speed decreased to {speed}%")
                elif cmd == 'q':
                    break
                else:
                    print("Invalid command")
                    
        except KeyboardInterrupt:
            pass
        finally:
            self.stop_all()

def main():
    """Main function"""
    print("Roomba Motor Controller - L298N + 18V Ryobi Battery")
    print("="*50)
    
    controller = RoombaMotorController()
    
    try:
        # Choose operation mode
        print("\nSelect operation mode:")
        print("1. Auto Test Sequence")
        print("2. Manual Control")
        
        choice = input("Enter choice (1 or 2): ").strip()
        
        if choice == '1':
            controller.test_sequence()
        elif choice == '2':
            controller.manual_control()
        else:
            print("Invalid choice")
            
    except Exception as e:
        print(f"Error: {e}")
        controller.brake_all()
    finally:
        controller.cleanup()
        print("Program terminated safely")

if __name__ == '__main__':
    main()