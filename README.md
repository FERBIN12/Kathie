**NINA- ------- Robot**

OS: UBUNTU 22.04

ROS DISTRO: HUMBLE

Gazebo :: Gazebo iginition

Humble installation link::https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html


            
Packages needed:
        
        sudo apt install ros-humble-xacro
        sudo apt install python3-colcon-common-extensions
        sudo apt install ros-humble-joint-state-publisher-gui
        sudo apt install ros-humble-gazebo-ros-pkgs
        sudo apt install ros-humble-slam-toolbox
        
To launch the robot::
        
        ros2 launch nina_description nina_ignition.launch.py

  ![image](https://github.com/user-attachments/assets/74caa712-3e9f-4161-b891-1f72fbe50e7f)

To launch the controller of the AMR:

        ros2 launch nina_controller controller.launch.py
To Teleoperate use:

        ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args --remap /cmd_vel:=/nina_controller/cmd_vel
Use RVIZ for visulization:

        rviz2

![image](https://github.com/user-attachments/assets/d0e5fa11-f5fd-40a8-90c1-33182af71f86)

            
