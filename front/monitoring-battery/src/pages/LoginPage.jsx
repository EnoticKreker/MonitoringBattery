import { Card, Typography } from "antd";
import { Link } from "react-router-dom";
import LoginComponent from "../components/LoginComponent.jsx";

const { Text } = Typography;

export default function LoginPage() {
  return (
    <div className="auth-container">
      <Card title="Login" style={{ width: 400, margin: "100px auto" }}>
        <LoginComponent />
        <div style={{ marginTop: 16, textAlign: "center" }}>
          <Text>
            Don't have an account? <Link to="/register">Register here</Link>
          </Text>
        </div>
      </Card>
    </div>
  );
}
