import asyncio
from datetime import datetime
from core.database import AsyncSessionLocal
from models.device import Device
from models.battery import Battery


async def seed():
    async with AsyncSessionLocal() as session:
        device1 = Device(name="Device 1", version="v1.0", status=True,
                         created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        device2 = Device(name="Device 2", version="v1.0", status=True,
                         created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        session.add_all([device1, device2])
        await session.flush()

        battery_a = Battery(name="Battery A", voltage="3.7V", residual_capacity="90%",
                            lifetime="2 years", device_id=device1.id,
                            created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        battery_b = Battery(name="Battery B", voltage="3.6V", residual_capacity="80%",
                            lifetime="1.5 years", device_id=device1.id,
                            created_at=datetime.utcnow(), updated_at=datetime.utcnow())

        battery_1 = Battery(name="Battery 1", voltage="3.7V", residual_capacity="80%",
                            lifetime="2 years", device_id=None,
                            created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        battery_2 = Battery(name="Battery 2", voltage="4.4V", residual_capacity="50%",
                            lifetime="3 years", device_id=device2.id,
                            created_at=datetime.utcnow(), updated_at=datetime.utcnow())

        session.add_all([battery_a, battery_b, battery_1, battery_2])
        await session.commit()
        print("Initial devices and batteries seeded!")

if __name__ == "__main__":
    asyncio.run(seed())
