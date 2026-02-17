#########################################
# without classes, a lot of repeating code
print("----- NO CLASS -----\n")

# robots
r1_name = "Clanker"
r1_battery = 100
r1_position = 0

r2_name = "Robbie"
r2_battery = 80
r2_position = 1

def print_battery_level(name, battery):
    print(f"Battery level of robot {name} is {battery} %")
    
print_battery_level(r1_name, r1_battery)
print_battery_level(r2_name, r2_battery)




#########################################
# basic classes
print("\n----- BASIC CLASS -----\n")

class Robot:
    def __init__(self, name, battery = 100):
        self.name = name
        self.battery = battery
        # in python, we can access all the attributes, edit them etc.
        # there are no private or protected attributes
        # there are class attrs and instance attrs

# already easier than before
def print_battery_level(robot):
    print(f"Battery level of robot {robot.name} is {robot.battery} %")

r1 = Robot("Clanker")
r2 = Robot("Robbie", 80)

print_battery_level(r1)
print_battery_level(r2)



#########################################
# we can also define the method inside the class since it uses only the Robot class instances
print("\n----- ADDING METHODS -----\n")

class Robot:
    def __init__(self, name, battery = 100):
        self.name = name
        self.battery = battery
        
    def print_battery_state(self):
        print(f"Battery level of robot {self.name} is {self.battery} %")

r1 = Robot("Clanker1", 90)
r2 = Robot("Clanker2")

robots = [r1, r2]
for robot in robots:
    robot.print_battery_state()




#########################################
# we can also have more advanced printing method, previous example was too simple
print("\n----- HELPER METHODS -----\n")

class Robot:
    def __init__(self, name, battery_voltage = 4.2):
        self.name = name
        self.battery_voltage = battery_voltage
        self.max_v = 4.2
        self.min_v = 3.2
        
    def print_battery_state(self):
        battery_percentage = (self.battery_voltage - self.min_v) / (self.max_v - self.min_v) * 100
        print(f"Battery level [{self.name}]: {self.battery_voltage} V | {battery_percentage:.1f} %")

r1 = Robot("Clanker", 4.1)
r1.print_battery_state()




#########################################
# lets add another method to show the override of a parent method
print("\n ----- INHERITING FROM PARENT CLASS -----\n")

class Robot:
    def __init__(self, name, battery = 100):
        self.name = name
        self.battery = battery
        
    def print_battery_state(self):
        print(f"Battery level of robot {self.name} is {self.battery} %")
    
    def move(self):
        self.battery -= 10
        print("Moving...")
        
r1 = Robot("Clanker1", 90)
r2 = Robot("Clanker2")

# class Child(Parent):
class Drone(Robot):
    # this overrides the move method from the Parent
    def move(self):
        self.battery -= 15
        print("Flying...")
    
    # we can also add another methods
    def takeoff(self):
        self.battery -= 20
        print("Taking off!!")

d1 = Drone("Ptacek")
d1.print_battery_state()
d1.takeoff()
d1.move()
d1.print_battery_state()




#########################################
# adding more attributes to a child class
print("\n ----- ADDING ATTRIBUTES TO A CHILD CLASS -----\n")

class Drone(Robot):
    # WRONG: overwrites __init__ of parent class!
    # def __init__(self, size=10):
    #     self.size = size
    
    # CORRECT: uses the parent __init__ (key word 'super' as superior) and adds new attrs
    def __init__(self, name, battery=100):
        super().__init__(name, battery)
        self.in_air = False
        
    def move(self):
        self.battery -= 15
        print("Flying...")
    
    def takeoff(self):
        self.battery -= 20
        self.in_air = True
        print("Taking off!!")
        
d2 = Drone("Vrtulnikkk")
d2.print_battery_state()
d2.takeoff()
d2.print_battery_state()
d2.move()
d2.print_battery_state()




#########################################
# we dont want to instantiate a generic Robot class, so we make it abstract, because what even is a generic robot?
print("\n ----- ABSTRACT CLASSES -----\n")

# to use abstract anything, we have to import ABC
from abc import ABC, abstractmethod

# Robot inherits from Abstract Base Class (ABC) and has an abstract method
class Robot(ABC):
    def __init__(self, name, battery = 100):
        self.name = name
        self.battery = battery
        
    def print_battery_state(self):
        print(f"Battery level of robot {self.name} is {self.battery} %")

    @abstractmethod # has to be implemented!
    def move(self):
        pass

class Drone(Robot):
    def __init__(self, name, battery=100, size=10):
        super().__init__(name, battery)
        self.size = size
        
    def move(self):
        print(f">> [{self.name}] flying...")
        
class StationaryRobot(Robot):
    def rotate():
        print("Rotating...")
        
# the abstract class cannot be instantiated
try:
    abstract_class = Robot("npc", 100)
except Exception as e:
    print(f"Error: {e}")

# this class does not implement the abstract method -> cant be instantiated!
try:
    not_implemented = StationaryRobot("npc2")
except Exception as e:
    print(f"Error: {e}")

# this works, the method is implemented
d1 = Drone("Dr. One", 100)
d1.print_battery_state()




#########################################
# another example for an abstract class

class PaymentMethod(ABC):
    @abstractmethod
    def process_payment():
        pass
    
class PayPal(PaymentMethod):
    def process_payment():
        # ... logic for PayPal ...
        pass




#########################################
# lets create more classes from a Robot subclass -> different actions when calling the same method
print("\n ----- MORE ABSTRACT CLASSES -----\n")

class Submarine(Robot):
    def move(self):
        print(f">> [{self.name}] floating...")

class Car(Robot):
    def move(self):
        print(f">> [{self.name}] driving...")

a1 = Drone("droooneee")
a2 = Submarine("subbbmarriinneee")
a3 = Car("Caaarrr")

# so called POLYMORPHISM
list_robots = [a1, a2, a3]
for rob in list_robots:
    rob.move()




#########################################
# in gymnasium, there are no abstract classes, but they act like them
# -> if we dont implement the correct method, it throws an error
print("\n ----- FAKE ABSTRACT CLASSES -----\n")

import gymnasium as gym

class LazyRobot(gym.Env):
    pass

class WorkingRobot(gym.Env):
    def step(self):
        print("STEP...")

# WRONG: step method not implemented
try:
    robb = LazyRobot()
    robb.step()
except Exception as e:
    print(f"Error: {e}")

# CORRECT: implemented
robb = WorkingRobot()
robb.step()




#########################################
# now there are class and instance attributes and also methods
print("\n ----- SHARED DATA -----\n")

class Worker:
    total_workers = 0
    
    def __init__(self, name):
        self.name = name
        Worker.total_workers += 1
        self.say_hello()
        
    def say_hello(self):
        print(f"Hi, my name is {self.name}!")
        
    @classmethod
    def get_total_workers(cls):
        print(f"Total wokrers: {cls.total_workers}")
        
    @staticmethod
    def say_what():
        print("what")

w1 = Worker("Jeff")
w2 = Worker("Metr Pacinka")
Worker.get_total_workers()
w3 = Worker("JD Vance")
Worker.get_total_workers()

Worker.say_what()