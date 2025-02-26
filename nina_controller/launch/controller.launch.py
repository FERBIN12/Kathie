from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, GroupAction , OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition

def noisy_controller(context, *args, **kwargs):
    wheel_radius = float(LaunchConfiguration("wheel_radius").perform(context))
    wheel_seperation = float(LaunchConfiguration("wheel_seperation").perform(context))

    wheel_radius_error = float(LaunchConfiguration("wheel_radius_error").perform(context))
    wheel_seperation_error = float(LaunchConfiguration("wheel_seperation_error").perform(context))

    use_python = LaunchConfiguration("use_python").perform(context)

    noisy_controller_py = Node(
        package= "nina_controller",
        executable = "noisy_controller.py",
        parameters = [
            {"wheel_radius": wheel_radius + wheel_radius_error,
             "wheel_seperation": wheel_seperation + wheel_seperation_error}
                    ],
        condition = IfCondition(use_python)
        
                )

    noisy_controller_cpp = Node(
        package= "nina_controller",
        executable = "noisy_controller",
        parameters = [
            {"wheel_radius": wheel_radius + wheel_radius_error,
             "wheel_seperation": wheel_seperation + wheel_seperation_error}
                    ],
        condition = UnlessCondition(use_python)
                )
    
    return [
        noisy_controller_py,
        noisy_controller_cpp
    ]

def generate_launch_description():
    
    use_python_arg = DeclareLaunchArgument(
        "use_python",
        default_value = "false"
    )

    wheel_radius_arg = DeclareLaunchArgument(
        "wheel_radius",
        default_value = "0.033"
    )

    wheel_seperation_arg = DeclareLaunchArgument(
        "wheel_seperation",
        default_value= "0.17"
    )    
    use_simple_controller_arg = DeclareLaunchArgument(
        "use_simple_controller",
        default_value= "True"
    )

    wheel_radius_error_arg = DeclareLaunchArgument(
        "wheel_radius_error",
        default_value= "0.005"
    )

    wheel_seperation_error_arg = DeclareLaunchArgument(
        "wheel_seperation_error",
        default_value= "0.02"
    )

    
    
    

    use_python = LaunchConfiguration("use_python")
    wheel_radius = LaunchConfiguration("wheel_radius")
    wheel_separation = LaunchConfiguration("wheel_seperation")
    use_simple_controller = LaunchConfiguration("use_simple_controller")
    
    joint_state_broadcaster_spawner = Node(
        package = "controller_manager",
        executable= "spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager"
        ]
    )


    nina_controller = Node(
        package= "controller_manager",
        executable = "spawner",
        arguments=[
            "nina_controller",
            "--controller-manager",
            "/controller_manager"
        ],
        condition = UnlessCondition(use_simple_controller)
    
    )

    simple_controller = GroupAction(
        condition = IfCondition(use_simple_controller),
        actions = [

            Node(
                package = "controller_manager",
                executable= "spawner",
                arguments=[
                    "simple_velocity_controller",
                    "--controller-manager",
                    "/controller_manager"
                ]
            ),
            
            Node(
                package = "nina_controller",
                executable = "simple_controller.py",
                parameters = [{"wheel_radius": wheel_radius,
                            "wheel_seperation": wheel_separation}],
                condition = IfCondition(use_python)
            ),

            Node(
                package = "nina_controller",
                executable= "simple_controller",
                parameters = [{"wheel_radius": wheel_radius,
                            "wheel_seperation": wheel_separation}],
                condition = UnlessCondition(use_python)
            )
        ]
    )



    noisy_controller_launch = OpaqueFunction(function = noisy_controller)


    return LaunchDescription([
        use_python_arg,
        wheel_radius_arg,
        use_simple_controller_arg,
        wheel_seperation_arg,
        joint_state_broadcaster_spawner,
        nina_controller,
        simple_controller,
        wheel_radius_error_arg,
        wheel_seperation_error_arg,
        noisy_controller_launch
        
                             ])