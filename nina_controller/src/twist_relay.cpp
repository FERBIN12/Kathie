#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/twist.hpp>
#include <geometry_msgs/msg/twist_stamped.hpp>

class TwistRelay : public rclcpp::Node
{

public:
    TwistRelay() : Node("twist_relay")
    {
        controller_sub_ = create_subscription<geometry_msgs::msg::Twist>(
            "/nina_controller/cmd_vel_unstamped",
            10,
            std::bind(&TwistRelay::controllerCallback, this, std::placeholders::_1)
        );
    }  


private:
    rclcpp::Subscription<geometry_msgs::msg::TwistStamped>::SharedPtr controller_sub_;
}