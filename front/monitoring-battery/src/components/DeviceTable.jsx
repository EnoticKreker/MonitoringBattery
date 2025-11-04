import { useEffect, useState } from "react";
import {
  Table,
  Button,
  Modal,
  Form,
  Input,
  Switch,
  Space,
  notification,
  Select,
} from "antd";
import {
  listDevices,
  createDevice,
  updateDevice,
  deleteDevice,
  deleteBatteryByDevice,
  listBatteries,
  addBatteriesToDevice,
} from "../api/api";

export default function DeviceTable(active) {
  const [devices, setDevices] = useState([]);
  const [allBatteries, setAllBatteries] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingDevice, setEditingDevice] = useState(null);
  const [selectedBatteries, setSelectedBatteries] = useState([]);
  const [deviceForm] = Form.useForm();

  const [api, contextHolder] = notification.useNotification();

  const fetchDevices = async () => {
    setLoading(true);
    try {
      const res = await listDevices();
      setDevices(res.data);
    } catch (err) {
      console.error(err);
      api.error({
        message: "Error",
        description: "Failed to load devices",
        placement: "topRight",
      });
    }
    setLoading(false);
  };

  const fetchAllBatteries = async () => {
    try {
      const res = await listBatteries();
      setAllBatteries(res.data);
    } catch (err) {
      console.error(err);
      api.error({
        message: "Error",
        description: "Failed to load batteries",
        placement: "topRight",
      });
    }
  };

  useEffect(() => {
    if (!active) return;
    fetchDevices();
    fetchAllBatteries();
  }, [active]);

  useEffect(() => {
    fetchDevices();
    fetchAllBatteries();
  }, []);

  useEffect(() => {
    if (!isModalOpen) setSelectedBatteries([]);
  }, [isModalOpen]);

  const handleDeviceSubmit = async (values) => {
    if (values.status === undefined) values.status = false;

    try {
      let device;
      if (editingDevice) {
        device = await updateDevice(editingDevice.id, values);

        if (selectedBatteries.length > 0) {
          await addBatteriesToDevice(
            editingDevice.id,
            selectedBatteries.map((id) => ({ id }))
          );
          api.success({
            message: "Batteries Attached",
            description: "Selected batteries have been attached to the device",
            placement: "topRight",
          });
        }

        api.success({
          message: "Device Updated",
          description: "Device updated successfully",
          placement: "topRight",
        });
      } else {
        device = await createDevice(values);

        if (values.batteries && values.batteries.length > 0) {
          await addBatteriesToDevice(
            device.id,
            values.batteries.map((b) => ({
              name: b.name,
              voltage: b.voltage,
              residual_capacity: b.residual_capacity,
              lifetime: b.lifetime,
            }))
          );
        }

        if (selectedBatteries.length > 0) {
          await addBatteriesToDevice(
            device.id,
            selectedBatteries.map((id) => ({ id }))
          );
        }

        api.success({
          message: "Device Created",
          description: "Device created successfully",
          placement: "topRight",
        });
      }

      deviceForm.resetFields();
      setEditingDevice(null);
      setSelectedBatteries([]);
      setIsModalOpen(false);
      fetchDevices();
    } catch (err) {
      console.error(err);
      api.error({
        message: "Error",
        description: err.response?.data?.detail || "Failed to save device",
        placement: "topRight",
      });
    }
  };

  const handleDeleteDevice = async (id) => {
    try {
      await deleteDevice(id);
      api.success({
        message: "Device Deleted",
        description: "Device deleted successfully",
        placement: "topRight",
      });
      fetchDevices();
    } catch (err) {
      console.error(err);
      api.error({
        message: "Error",
        description: "Failed to delete device",
        placement: "topRight",
      });
    }
  };

  const handleDeleteBattery = async (device_id, battery_id) => {
    try {
      await deleteBatteryByDevice(device_id, battery_id);
      api.success({
        message: "Battery Removed",
        description: "The battery was removed successfully",
        placement: "topRight",
      });

      const updatedBatteries = deviceForm
        .getFieldValue("batteries")
        .filter((b) => b.id !== battery_id);
      deviceForm.setFieldValue("batteries", updatedBatteries);

      fetchDevices();
    } catch (err) {
      console.error(err);
      api.error({
        message: "Error",
        description: "Failed to remove battery",
        placement: "topRight",
      });
    }
  };

  const deviceColumns = [
    { title: "Name", dataIndex: "name", key: "name" },
    { title: "Version", dataIndex: "version", key: "version" },
    {
      title: "Status",
      dataIndex: "status",
      key: "status",
      render: (val) => (val ? "Active" : "Inactive"),
    },
    {
      title: "Batteries",
      key: "batteries",
      render: (_, record) => (
        <Space direction="vertical">
          {record.batteries?.map((b) => (
            <div key={b.id}>
              {b.name} ({b.voltage}V)
            </div>
          ))}
        </Space>
      ),
    },
    {
      title: "Actions",
      key: "actions",
      render: (_, record) => (
        <Space>
          <Button
            type="link"
            onClick={() => {
              setEditingDevice(record);
              deviceForm.setFieldsValue(record);
              deviceForm.setFieldValue("batteries", record.batteries || []);
              setIsModalOpen(true);
            }}
          >
            Edit
          </Button>
          <Button type="link" danger onClick={() => handleDeleteDevice(record.id)}>
            Delete
          </Button>
        </Space>
      ),
    },
  ];

  return (
    <>
      {contextHolder}
      <Button
        type="primary"
        style={{ marginBottom: 16 }}
        onClick={() => setIsModalOpen(true)}
      >
        Add Device
      </Button>

      <Table dataSource={devices} columns={deviceColumns} rowKey="id" loading={loading} />

      <Modal
        title={editingDevice ? "Edit Device" : "Add Device"}
        open={isModalOpen}
        onCancel={() => {
          setIsModalOpen(false);
          setEditingDevice(null);
          deviceForm.resetFields();
          setSelectedBatteries([]);
        }}
        onOk={() => deviceForm.submit()}
        width={700}
      >
        <Form form={deviceForm} layout="vertical" onFinish={handleDeviceSubmit}>
          <Form.Item name="name" label="Name" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="version" label="Version" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="status" label="Status" valuePropName="checked">
            <Switch />
          </Form.Item>

          {editingDevice ? (
            <>
              <h4 style={{ marginBottom: 8 }}>Attached Batteries</h4>
              <Space direction="vertical" style={{ width: "100%" }}>
                {deviceForm.getFieldValue("batteries")?.map((b) => (
                  <div
                    key={b.id}
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center",
                      padding: 12,
                      border: "1px solid #d9d9d9",
                      borderRadius: 8,
                      background: "#fafafa",
                      boxShadow: "0 2px 5px rgba(0,0,0,0.05)",
                    }}
                  >
                    <div>
                      <strong>{b.name}</strong> ({b.voltage}V)
                    </div>
                    <Button
                      type="text"
                      danger
                      onClick={() => handleDeleteBattery(editingDevice.id, b.id)}
                    >
                      Remove
                    </Button>
                  </div>
                ))}
              </Space>

              <div style={{ marginTop: 16 }}>
                <h4 style={{ marginBottom: 8 }}>Add Existing Batteries</h4>
                <Form.Item>
                  <Select
                    mode="multiple"
                    placeholder="Select batteries to attach"
                    value={selectedBatteries}
                    onChange={setSelectedBatteries}
                    allowClear
                  >
                    {allBatteries
                      .filter(
                        (b) =>
                          !deviceForm
                            .getFieldValue("batteries")
                            ?.some((db) => db.id === b.id)
                      )
                      .map((b) => (
                        <Select.Option key={b.id} value={b.id}>
                          {b.name} ({b.voltage}V)
                        </Select.Option>
                      ))}
                  </Select>
                </Form.Item>
              </div>
            </>
          ) : (
            <>
              <h4 style={{ marginTop: 16, marginBottom: 8 }}>Add Existing Batteries</h4>
              <Form.Item>
                <Select
                  mode="multiple"
                  placeholder="Select batteries to attach"
                  value={selectedBatteries}
                  onChange={setSelectedBatteries}
                  allowClear
                >
                  {allBatteries.map((b) => (
                    <Select.Option key={b.id} value={b.id}>
                      {b.name} ({b.voltage}V)
                    </Select.Option>
                  ))}
                </Select>
              </Form.Item>

              <h4 style={{ marginTop: 16, marginBottom: 8 }}>Add New Batteries</h4>
              <Form.List name="batteries">
                {(fields, { add, remove }) => (
                  <>
                    {fields.map(({ key, name, ...restField }) => (
                      <div
                        key={key}
                        style={{
                          border: "1px solid #d9d9d9",
                          borderRadius: 8,
                          padding: 12,
                          marginBottom: 12,
                          background: "#fafafa",
                          boxShadow: "0 2px 5px rgba(0,0,0,0.05)",
                        }}
                      >
                        <Space
                          style={{ display: "flex", justifyContent: "space-between" }}
                          align="baseline"
                        >
                          <span style={{ fontWeight: 500 }}>Battery #{key + 1}</span>
                          <Button type="text" danger onClick={() => remove(name)}>
                            Remove
                          </Button>
                        </Space>

                        <Form.Item
                          {...restField}
                          name={[name, "name"]}
                          label="Name"
                          rules={[{ required: true }]}
                        >
                          <Input placeholder="e.g. Li-ion Pack" />
                        </Form.Item>
                        <Form.Item
                          {...restField}
                          name={[name, "voltage"]}
                          label="Voltage (V)"
                          rules={[{ required: true }]}
                        >
                          <Input placeholder="e.g. 12.6" />
                        </Form.Item>
                        <Form.Item
                          {...restField}
                          name={[name, "residual_capacity"]}
                          label="Residual Capacity (mAh)"
                          rules={[{ required: true }]}
                        >
                          <Input placeholder="e.g. 2200" />
                        </Form.Item>
                        <Form.Item
                          {...restField}
                          name={[name, "lifetime"]}
                          label="Lifetime (days)"
                          rules={[{ required: true }]}
                        >
                          <Input placeholder="e.g. 180" />
                        </Form.Item>
                      </div>
                    ))}
                    <Button type="dashed" onClick={() => add()} block>
                      + Add Battery
                    </Button>
                  </>
                )}
              </Form.List>
            </>
          )}
        </Form>
      </Modal>
    </>
  );
}
