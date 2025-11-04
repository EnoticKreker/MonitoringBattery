import React, { useState } from "react";
import { Form, Input, Button } from "antd";
import { login, setToken, me } from "../api/api";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const LoginComponent = () => {
  const navigate = useNavigate();
  const { loginUser } = useAuth();
  const [loading, setLoading] = useState(false);
  const [formError, setFormError] = useState("");

  const onFinish = async (values) => {
    setLoading(true);
    setFormError("");
    try {
      const res = await login(values);
      const token = res.data.access_token;

      setToken(token);
      localStorage.setItem("access_token", token);

      const userRes = await me();
      loginUser(userRes.data, token);

      navigate("/");
    } catch (err) {
      let message = "Authorization failed";
      if (err.response && err.response.data) {
        message = err.response.data.detail || err.response.data.message || message;
      }
      setFormError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Form
      onFinish={onFinish}
      layout="vertical"
    >
      <Form.Item
        name="username"
        label="Email"
        rules={[
          { required: true, message: "Please enter your email" },
          { type: "email", message: "Please enter a valid email" },
        ]}
      >
        <Input placeholder="example@mail.com" />
      </Form.Item>

      <Form.Item
        name="password"
        label="Password"
        rules={[{ required: true, message: "Please enter your password" }]}
      >
        <Input.Password placeholder="********" />
      </Form.Item>

      {formError && (
        <div style={{ color: "red", marginBottom: 16 }}>
          {formError}
        </div>
      )}

      <Form.Item>
        <Button type="primary" htmlType="submit" loading={loading} block>
          Login
        </Button>
      </Form.Item>
    </Form>
  );
};

export default LoginComponent;
