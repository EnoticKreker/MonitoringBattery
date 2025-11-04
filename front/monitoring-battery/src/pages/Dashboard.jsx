import { useState, useEffect } from "react";
import { Layout, Menu, Breadcrumb, Button } from "antd";
import { MenuUnfoldOutlined, MenuFoldOutlined } from "@ant-design/icons";
import BatteryTable from "../components/BatteryTable";
import DeviceTable from "../components/DeviceTable";
import { useAuth } from "../context/AuthContext";

const { Header, Sider, Content } = Layout;

export default function Dashboard() {
  const [collapsed, setCollapsed] = useState(false);
  const [selectedKey, setSelectedKey] = useState("1");
  const { user, logout } = useAuth();

  const [deviceLoaded, setDeviceLoaded] = useState(false);
  const [batteryLoaded, setBatteryLoaded] = useState(false);

  useEffect(() => {
    if (selectedKey === "1" && !batteryLoaded) {
      setBatteryLoaded(true);
    }
    if (selectedKey === "2" && !deviceLoaded) {
      setDeviceLoaded(true);
    }
  }, [selectedKey, deviceLoaded, batteryLoaded]);

  const toggle = () => setCollapsed(!collapsed);

  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Sider
        collapsible
        collapsed={collapsed}
        trigger={null}
        style={{ display: "flex", flexDirection: "column" }}
      >
        <div
          style={{
            height: 64,
            margin: 16,
            display: "flex",
            alignItems: "center",
            color: "#fff",
            fontSize: collapsed ? "0px" : "16px",
            overflow: "hidden",
            whiteSpace: "nowrap"
          }}
        >
          Welcome, {user?.email.split("@")[0]}
        </div>

        <Menu
          theme="dark"
          mode="inline"
          selectedKeys={[selectedKey]}
          onClick={(e) => setSelectedKey(e.key)}
          items={[
            { key: "1", label: "Batteries" },
            { key: "2", label: "Devices" },
          ]}
          style={{ flexGrow: 1 }}
        />

        <div style={{ padding: 16 }}>
          <Button type="primary" onClick={logout} block>
            {collapsed ? "←" : "Logout"}
          </Button>
        </div>
      </Sider>

      <Layout>
        <Header style={{ padding: "0 16px", background: "#fff", display: "flex", alignItems: "center" }}>
          {collapsed ? <MenuUnfoldOutlined onClick={toggle} /> : <MenuFoldOutlined onClick={toggle} />}
          <h2 style={{ marginLeft: 16 }}>Monitoring Battery Dashboard</h2>
        </Header>

        <Content style={{ margin: "16px" }}>
          <Breadcrumb style={{ marginBottom: 16 }}>
            <Breadcrumb.Item>Dashboard</Breadcrumb.Item>
            <Breadcrumb.Item>{selectedKey === "1" ? "Batteries" : "Devices"}</Breadcrumb.Item>
          </Breadcrumb>

          {selectedKey === "1" && <BatteryTable active={true} />}
          {selectedKey === "2" && <DeviceTable active={true} />}
        </Content>
      </Layout>
    </Layout>
  );
}
