import { Card, Form, Input, Button, Typography, notification } from "antd";
import { register } from "../api/api";
import { useNavigate, Link } from "react-router-dom";

const { Text } = Typography;

export default function RegisterPage() {
  const navigate = useNavigate();
  const [api, contextHolder] = notification.useNotification();

  const onFinish = async (values) => {
    try {
      await register(values);

      api.success({
        message: "Registration Successful",
        description: "Your account has been created. You can now log in.",
        placement: "topRight",
      });

      navigate("/login");
    } catch (err) {
      console.error(err);

      let errorDescription = "Registration failed. Please try again.";
      const detail = err.response?.data?.detail;

      if (detail) {
        if (Array.isArray(detail)) {
          errorDescription = detail.map((e) => e.msg || e).join(", ");
        } else {
          errorDescription = detail;
        }
      }

      api.error({
        message: "Registration Failed",
        description: errorDescription,
        placement: "topRight",
      });
    }
  };

  return (
    <div className="auth-container">
      {contextHolder}
      <Card title="Register" style={{ width: 400, margin: "100px auto" }}>
        <Form layout="vertical" onFinish={onFinish}>
          <Form.Item
            name="email"
            label="Email"
            rules={[
              { required: true, message: "Please enter your email" },
              { type: "email", message: "Please enter a valid email" },
            ]}
          >
            <Input placeholder="example@mail.com" />
          </Form.Item>
          <Form.Item name="password" label="Password" rules={[{ required: true }]}>
            <Input.Password />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" block>
              Register
            </Button>
          </Form.Item>
        </Form>

        <div style={{ marginTop: 16, textAlign: "center" }}>
          <Text>
            Already have an account? <Link to="/login">Login here</Link>
          </Text>
        </div>
      </Card>
    </div>
  );
}
