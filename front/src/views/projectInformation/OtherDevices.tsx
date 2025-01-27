import CustomButton from "components/button";
import SimpleTable from "components/tables/SimpleTable";
import CustomTabs, { TabData } from "components/tabs";
import { MdRemoveRedEye } from "react-icons/md";
import { DeviceObj } from "views/counters";
interface OtherDeviceTableData {
  name: string;
  serial: string;
  lastTime: string;
  lastData: string;
  actions: JSX.Element;
}
interface OtherDevicesProps {
  projectDevices: DeviceObj[];
}
const OtherDevices = (props: OtherDevicesProps) => {
  const { projectDevices } = props;
  const otherDevices = projectDevices.filter(
    (device: DeviceObj) =>
      device.water_meter_type__water_meter_tag__water_meter_tag_id ===
      "4f7205f0-c8a7-4fb1-a450-0c6622d4f364"
  );
  let containedOtherTypes: string[] = [];
  otherDevices.forEach((device: DeviceObj) => {
    if (
      !containedOtherTypes.includes(
        device.water_meter_type__water_meter_type_name
      )
    ) {
      containedOtherTypes.push(device.water_meter_type__water_meter_type_name);
    }
  });
  // //console.log(otherDevices);
  const headers = [
    { title: "نام", headerKey: "name" },
    { title: "شماره سریال", headerKey: "serial" },
    { title: "زمان آخرین فعالیت", headerKey: "lastTime" },
    { title: "آخرین داده", headerKey: "lastData" },
    { title: "جزئیات", headerKey: "actions" },
  ];
  const renderActions = (deviceSerial: string) => {
    return (
      <div className=" flex items-center justify-center">
        <CustomButton
          onClick={null}
          icon={<MdRemoveRedEye />}
          color="blue"
          extra="!p-2"
        />
      </div>
    );
  };
  let tabsData: TabData[] = [];
  const tableData = (type: string) => {
    let otherDeviceTableData: OtherDeviceTableData[] = [];
    otherDevices
      .filter(
        (device: DeviceObj) =>
          device.water_meter_type__water_meter_type_name === type
      )
      .forEach((device: DeviceObj) => {
        otherDeviceTableData.push({
          name: device.water_meter_name,
          serial: device.water_meter_serial,
          lastTime: "__",
          lastData: "__",
          actions: renderActions(device.water_meter_serial),
        });
      });

    return otherDeviceTableData;
  };
  containedOtherTypes.forEach((otherType: string) => {
    tabsData.push({
      label: otherType,
      content: <SimpleTable header={headers} data={tableData(otherType)} />,
    });
  });
  return (
    <>
      {otherDevices.length > 0 ? (
        <CustomTabs tabsData={tabsData} />
      ) : (
        <div className="py-2  text-navy-700  dark:text-white">
          دستگاهی موجود نیست
        </div>
      )}
    </>
  );
};
export default OtherDevices;
