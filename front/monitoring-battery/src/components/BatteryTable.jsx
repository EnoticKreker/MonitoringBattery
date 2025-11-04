import { Table, Button, Modal, Form, Input, Select, Space, Popconfirm, notification } from "antd";
import { useEffect, useState } from "react";
import { listBatteries, createBattery, updateBattery, deleteBattery, listDevices } from "../api/api";

export default function BatteryTable(active) {
  const [batteries, setBatteries] = useState([]);
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);
  const [editingBattery, setEditingBattery] = useState(null);
  const [form] = Form.useForm();
  const [api, contextHolder] = notification.useNotification();

  const fetchDevices = async () => {
    try {
      const res = await listDevices();
      setDevices(res.data);
    } catch (err) {
      console.error(err);
      api.error({ message: "Error", description: "Failed to load devices", placement: "topRight" });
    }
  };

  const fetchBatteries = async () => {
    setLoading(true);
    try {
      const res = await listBatteries();
      const batteriesWithDeviceName = res.data.map(b => ({
        ...b,
        device_name: devices.find(d => d.id === b.device_id)?.name || "",
      }));
      setBatteries(batteriesWithDeviceName);
    } catch (err) {
      console.error(err);
      api.error({ message: "Error", description: "Failed to load batteries", placement: "topRight" });
    }
    setLoading(false);
  };

  
  useEffect(() => {
    if (!active) return;
    fetchDevices().then(fetchBatteries);
  }, [active]);

  useEffect(() => {
    fetchDevices();
  }, []);

  useEffect(() => {
    if (devices.length) fetchBatteries();
  }, [devices]);

  const handleAddOrEditBattery = async (values) => {
    try {
      console.log("values ===", values);
      
      const payload = {
        ...values,
        device_id: values.device_id ?? null,
      };

      if (editingBattery) {
        await updateBattery(editingBattery.id, payload);
        api.success({ message: "Success", description: "Battery updated", placement: "topRight" });
      } else {
        await createBattery(payload);
        api.success({ message: "Success", description: "Battery created", placement: "topRight" });
      }

      setModalOpen(false);
      setEditingBattery(null);
      form.resetFields();
      fetchBatteries();
    } catch (err) {
      console.error(err);
      api.error({ message: "Error", description: "Failed to save battery", placement: "topRight" });
    }
  };


  const handleDeleteBattery = async (id) => {
    try {
      await deleteBattery(id);
      api.success({ message: "Deleted", description: "Battery deleted", placement: "topRight" });
      fetchBatteries();
    } catch (err) {
      console.error(err);
      api.error({ message: "Error", description: "Failed to delete battery", placement: "topRight" });
    }
  };

  const columns = [
    { title: "Name", dataIndex: "name", key: "name" },
    { title: "Voltage", dataIndex: "voltage", key: "voltage" },
    { title: "Residual Capacity", dataIndex: "residual_capacity", key: "residual_capacity" },
    { title: "Lifetime", dataIndex: "lifetime", key: "lifetime" },
    { title: "Assigned Device", dataIndex: "device_name", key: "device" },
    {
      title: "Actions",
      key: "actions",
      render: (_, record) => (
        <Space>
          <Button
            type="link"
            onClick={() => {
              setEditingBattery(record);
              form.setFieldsValue({
                ...record,
                device_id: record.device_id || null,
              });
              setModalOpen(true);
            }}
          >
            Edit
          </Button>
          <Popconfirm title="Are you sure to delete this battery?" onConfirm={() => handleDeleteBattery(record.id)}>
            <Button type="link" danger>Delete</Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <>
      {contextHolder}
      <Button type="primary" style={{ marginBottom: 16 }} onClick={() => setModalOpen(true)}>
        Add Battery
      </Button>

      <Table dataSource={batteries} columns={columns} rowKey="id" loading={loading} />

      <Modal
        title={editingBattery ? "Edit Battery" : "Add Battery"}
        open={modalOpen}
        onCancel={() => {
          setModalOpen(false);
          setEditingBattery(null);
          form.resetFields();
        }}
        onOk={() => form.submit()}
      >
        <Form form={form} layout="vertical" onFinish={handleAddOrEditBattery}>
          <Form.Item name="name" label="Name" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="voltage" label="Voltage" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="residual_capacity" label="Residual Capacity" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="lifetime" label="Lifetime" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="device_id" label="Assign to Device">
            <Select
              placeholder="Select a device"
              allowClear
              onChange={(value) => form.setFieldsValue({ device_id: value ?? null })}
            >
              {devices.map((d) => (
                <Select.Option key={d.id} value={d.id}>
                  {d.name}
                </Select.Option>
              ))}
            </Select>
          </Form.Item>
        </Form>
      </Modal>
    </>
  );
}
